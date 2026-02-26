#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import traceback
from datetime import datetime
from pathlib import Path

from context_hub_common import (
    file_type_for,
    infer_tags,
    list_files_for_index,
    now_local,
    open_db,
    parse_meta,
    rel_to_root,
    resolve_paths,
    sha256_file,
)


def sidecar_for(path: Path) -> Path:
    return path.with_name(path.name + ".meta.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Index RileyFile tree into sqlite")
    args = parser.parse_args()

    try:
        paths = resolve_paths(require_existing_root=True)
        conn = open_db(paths.index_sqlite)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA busy_timeout=5000;")

        existing_rows = {
            row[0]: {
                "sha": row[1],
                "size": row[2],
                "mtime": row[3],
                "first_seen": row[4],
                "extracted_text_path": row[5],
            }
            for row in conn.execute(
                "SELECT path, sha, size, mtime, first_seen, extracted_text_path FROM files"
            )
        }

        indexed = 0
        rehashed = 0
        reused_sha = 0
        now_iso = now_local().isoformat()

        for abs_path in list_files_for_index(paths.riley_root):
            rel_path = rel_to_root(abs_path, paths.riley_root)
            if rel_path.startswith("CONTEXT_HUB/captures/_text/"):
                # avoid polluting signal extraction with generated text artifacts
                continue

            st = abs_path.stat()
            size = st.st_size
            mtime = st.st_mtime
            meta = parse_meta(sidecar_for(abs_path))
            existing = existing_rows.get(rel_path)

            if existing and existing.get("size") == size and float(existing.get("mtime") or 0.0) == float(mtime):
                sha = existing.get("sha") or ""
                reused_sha += 1
            else:
                sha = sha256_file(abs_path)
                rehashed += 1

            filename = abs_path.name
            tags = infer_tags(
                path_rel=rel_path,
                filename=filename,
                text=(meta.get("note") or ""),
                meta_tags=meta.get("tags") if isinstance(meta.get("tags"), list) else None,
            )

            first_seen = existing.get("first_seen") if existing else now_iso
            extracted_text_path = existing.get("extracted_text_path") if existing else None

            conn.execute(
                """
                INSERT INTO files(
                    path, sha, size, mtime, type, first_seen, last_seen,
                    extracted_text_path, tags_json, note, source_app, captured_at, extraction_error
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    sha=excluded.sha,
                    size=excluded.size,
                    mtime=excluded.mtime,
                    type=excluded.type,
                    last_seen=excluded.last_seen,
                    tags_json=excluded.tags_json,
                    note=COALESCE(excluded.note, files.note),
                    source_app=COALESCE(excluded.source_app, files.source_app),
                    captured_at=COALESCE(excluded.captured_at, files.captured_at),
                    extracted_text_path=COALESCE(files.extracted_text_path, excluded.extracted_text_path),
                    extraction_error=COALESCE(files.extraction_error, excluded.extraction_error)
                """,
                (
                    rel_path,
                    sha,
                    size,
                    mtime,
                    file_type_for(abs_path),
                    first_seen,
                    now_iso,
                    extracted_text_path,
                    json.dumps(tags, ensure_ascii=False),
                    meta.get("note") if isinstance(meta.get("note"), str) else None,
                    meta.get("source_app") if isinstance(meta.get("source_app"), str) else None,
                    meta.get("captured_at") if isinstance(meta.get("captured_at"), str) else None,
                    None,
                ),
            )
            indexed += 1

        conn.commit()
        conn.close()

        print(f"indexed_files={indexed}")
        print(f"rehashed_files={rehashed}")
        print(f"reused_sha_files={reused_sha}")
        print(f"index_path={paths.index_sqlite}")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

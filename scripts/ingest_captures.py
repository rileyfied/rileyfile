#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
import shutil
import subprocess
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

from context_hub_common import (
    db_set_state,
    file_type_for,
    infer_tags,
    now_local,
    open_db,
    parse_meta,
    rel_to_root,
    resolve_paths,
    sha256_file,
)


def normalize_explicit_tags(raw: Any) -> list[str]:
    out: list[str] = []
    if not isinstance(raw, list):
        return out
    for item in raw:
        if not isinstance(item, str):
            continue
        tag = item.strip()
        if not tag:
            continue
        if not tag.startswith("#"):
            tag = f"#{tag}"
        out.append(tag.lower())
    seen = set()
    deduped: list[str] = []
    for tag in out:
        if tag in seen:
            continue
        seen.add(tag)
        deduped.append(tag)
    return deduped


def strip_html(raw: str) -> str:
    no_script = re.sub(r"<script[\\s\\S]*?</script>", " ", raw, flags=re.IGNORECASE)
    no_style = re.sub(r"<style[\\s\\S]*?</style>", " ", no_script, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", no_style)
    return re.sub(r"\\s+", " ", text).strip()


def parse_url_file(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".url":
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.lower().startswith("url="):
                return line.split("=", 1)[1].strip()
        return ""
    if ext == ".webloc":
        data = plistlib.loads(path.read_bytes())
        val = data.get("URL")
        return val if isinstance(val, str) else ""
    return ""


def extract_text(path: Path, file_type: str, out_txt: Path) -> tuple[str | None, str | None, str | None]:
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    extraction_error = None
    extracted_content = None
    extracted_url = None

    try:
        if file_type == "text":
            raw = path.read_text(encoding="utf-8", errors="ignore")
            if path.suffix.lower() in {".html", ".htm"}:
                extracted_content = f"[RAW_HTML]\\n{raw}\\n\\n[STRIPPED_TEXT]\\n{strip_html(raw)}\\n"
            else:
                extracted_content = raw
        elif file_type == "url":
            extracted_url = parse_url_file(path)
            extracted_content = extracted_url or ""
        elif file_type == "pdf":
            tmp = out_txt.with_suffix(".tmp.txt")
            cmd = ["pdftotext", "-layout", str(path), str(tmp)]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            extracted_content = tmp.read_text(encoding="utf-8", errors="ignore")
            tmp.unlink(missing_ok=True)
        else:
            return None, None, None

        out_txt.write_text(extracted_content or "", encoding="utf-8")
        return rel_out_path(out_txt), extracted_content, extracted_url

    except Exception as exc:
        extraction_error = str(exc)
        return None, None, extraction_error


def rel_out_path(path: Path) -> str:
    # caller can rewrite this to Riley root relative when needed
    return str(path)


def choose_processed_destination(processed_dir: Path, original_name: str, sha: str) -> Path:
    base = processed_dir / original_name
    if not base.exists():
        return base
    stem = base.stem
    suffix = base.suffix
    candidate = processed_dir / f"{stem}__{sha[:10]}{suffix}"
    i = 1
    while candidate.exists():
        candidate = processed_dir / f"{stem}__{sha[:10]}_{i}{suffix}"
        i += 1
    return candidate


def collect_artifacts(source_root: Path, first_run: bool) -> list[Path]:
    out: list[Path] = []
    skip_dir_names = {"_processed", "_text"}
    for dirpath, dirnames, filenames in os.walk(source_root):
        current = Path(dirpath)
        if first_run:
            dirnames[:] = [d for d in dirnames if d not in skip_dir_names]
        for name in filenames:
            p = current / name
            if p.name.lower().endswith(".meta.json"):
                continue
            if p.name.startswith("."):
                continue
            out.append(p)
    out.sort(key=lambda p: p.as_posix())
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest capture artifacts")
    parser.add_argument("--first-run", action="store_true", help="Ingest all files under captures root")
    args = parser.parse_args()

    try:
        paths = resolve_paths(require_existing_root=True)
        conn = open_db(paths.index_sqlite)

        scan_root = paths.captures_root if args.first_run else paths.captures_inbox
        artifacts = collect_artifacts(scan_root, first_run=args.first_run)
        run_id = now_local().strftime("%Y%m%d_%H%M%S")

        processed_count = 0
        skipped_count = 0

        for src in artifacts:
            if not src.exists() or not src.is_file():
                skipped_count += 1
                continue

            rel_src = rel_to_root(src, paths.riley_root)
            sha = sha256_file(src)
            ftype = file_type_for(src)

            meta_path = src.with_name(src.name + ".meta.json")
            meta = parse_meta(meta_path)
            explicit_tags = normalize_explicit_tags(meta.get("tags"))

            text_out = paths.captures_text / f"{sha}.txt"
            extracted_rel = None
            extracted_for_tags = ""
            parsed_url = None
            extraction_error = None

            extracted_rel_tmp, extracted_body, maybe_url_or_error = extract_text(src, ftype, text_out)
            if ftype in {"text", "url", "pdf"}:
                if extracted_rel_tmp:
                    extracted_rel = rel_to_root(text_out, paths.riley_root)
                elif maybe_url_or_error:
                    extraction_error = maybe_url_or_error
            if ftype == "url" and extracted_body:
                parsed_url = extracted_body
            if extracted_body:
                extracted_for_tags = extracted_body[:4000]

            tags = infer_tags(
                path_rel=rel_src,
                filename=src.name,
                text=f"{meta.get('note', '')} {extracted_for_tags}",
                meta_tags=explicit_tags,
                url=parsed_url,
            )

            dest = choose_processed_destination(paths.captures_processed, src.name, sha)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))

            moved_meta_rel = None
            if meta_path.exists():
                meta_dest = dest.with_name(dest.name + ".meta.json")
                shutil.move(str(meta_path), str(meta_dest))
                moved_meta_rel = rel_to_root(meta_dest, paths.riley_root)

            rel_dest = rel_to_root(dest, paths.riley_root)

            now_iso = now_local().isoformat()
            conn.execute(
                """
                INSERT INTO files(
                    path, sha, size, mtime, type, first_seen, last_seen,
                    extracted_text_path, tags_json, note, source_app, captured_at, extraction_error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    sha=excluded.sha,
                    size=excluded.size,
                    mtime=excluded.mtime,
                    type=excluded.type,
                    last_seen=excluded.last_seen,
                    extracted_text_path=COALESCE(excluded.extracted_text_path, files.extracted_text_path),
                    tags_json=excluded.tags_json,
                    note=COALESCE(excluded.note, files.note),
                    source_app=COALESCE(excluded.source_app, files.source_app),
                    captured_at=COALESCE(excluded.captured_at, files.captured_at),
                    extraction_error=COALESCE(excluded.extraction_error, files.extraction_error)
                """,
                (
                    rel_dest,
                    sha,
                    dest.stat().st_size,
                    dest.stat().st_mtime,
                    ftype,
                    now_iso,
                    now_iso,
                    extracted_rel,
                    json.dumps(tags, ensure_ascii=False),
                    meta.get("note") if isinstance(meta.get("note"), str) else None,
                    meta.get("source_app") if isinstance(meta.get("source_app"), str) else None,
                    meta.get("captured_at") if isinstance(meta.get("captured_at"), str) else None,
                    extraction_error,
                ),
            )

            log_payload: dict[str, Any] = {
                "run_id": run_id,
                "processed_at": now_iso,
                "source_path": rel_src,
                "processed_path": rel_dest,
                "source_meta_path": rel_to_root(meta_path, paths.riley_root) if meta else None,
                "processed_meta_path": moved_meta_rel,
                "sha": sha,
                "type": ftype,
                "tags": tags,
                "explicit_tags": explicit_tags,
                "note": meta.get("note") if isinstance(meta.get("note"), str) else "",
                "source_app": meta.get("source_app") if isinstance(meta.get("source_app"), str) else "",
                "captured_at": meta.get("captured_at") if isinstance(meta.get("captured_at"), str) else "",
                "extracted_text_path": extracted_rel,
                "extraction_error": extraction_error,
            }
            with paths.ingest_log.open("a", encoding="utf-8") as logf:
                logf.write(json.dumps(log_payload, ensure_ascii=False) + "\n")

            processed_count += 1

        conn.commit()
        if args.first_run:
            db_set_state(conn, "captures_first_run_complete", "1")
            conn.commit()
        conn.close()

        print(f"scan_root={scan_root}")
        print(f"ingested={processed_count}")
        print(f"skipped={skipped_count}")
        print(f"ingest_log={paths.ingest_log}")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

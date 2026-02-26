#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import getpass

KNOWN_PROJECT_HASHTAGS = {
    "#youtube",
    "#video",
    "#tutorial",
    "#aibrief",
    "#audio",
    "#news",
    "#armor",
    "#scripture",
    "#bible",
    "#fighterverses",
    "#harmony",
    "#piano",
    "#music",
    "#conductor",
    "#monitor",
    "#agents",
    "#dashboard",
    "#productivity",
    "#virtualmanager",
    "#visor",
    "#cfa",
}

DOMAIN_TAG_MAP = {
    "youtube.com": ["#youtube", "#video"],
    "youtu.be": ["#youtube", "#video"],
    "substack.com": ["#aibrief", "#news"],
    "x.com": ["#aibrief", "#youtube"],
    "twitter.com": ["#aibrief", "#youtube"],
    "github.com": ["#conductor", "#agents"],
    "arxiv.org": ["#aibrief", "#news"],
    "techcrunch.com": ["#aibrief", "#news"],
}

KEYWORD_TAG_RULES = {
    "keyboard": ["#productivity"],
    "shortcut": ["#productivity"],
    "avatar": ["#youtube"],
    "clone": ["#youtube"],
    "brief": ["#aibrief"],
    "audio": ["#audio"],
    "verse": ["#armor", "#scripture"],
    "bible": ["#armor", "#bible"],
    "fighter": ["#fighterverses", "#armor"],
    "dashboard": ["#dashboard", "#productivity"],
    "restaurant": ["#virtualmanager", "#cfa"],
}

TEXT_EXTENSIONS = {".md", ".txt", ".html", ".htm", ".rtf", ".json", ".csv", ".xml", ".yaml", ".yml"}
URL_EXTENSIONS = {".url", ".webloc"}


@dataclass
class ResolvedPaths:
    user: str
    icloud_root: Path
    riley_root: Path
    context_hub: Path
    captures_root: Path
    captures_inbox: Path
    captures_processed: Path
    captures_text: Path
    index_dir: Path
    context_dir: Path
    digest_dir: Path
    archive_dir: Path
    index_sqlite: Path
    index_ndjson: Path
    ingest_log: Path
    candidates_md: Path
    promotions_md: Path
    promotions_state: Path
    riley_context: Path

    def as_dict(self) -> dict[str, str]:
        return {
            "user": self.user,
            "icloud_root": str(self.icloud_root),
            "riley_root": str(self.riley_root),
            "context_hub": str(self.context_hub),
            "captures_root": str(self.captures_root),
            "captures_inbox": str(self.captures_inbox),
            "captures_processed": str(self.captures_processed),
            "captures_text": str(self.captures_text),
            "index_dir": str(self.index_dir),
            "context_dir": str(self.context_dir),
            "digest_dir": str(self.digest_dir),
            "archive_dir": str(self.archive_dir),
            "index_sqlite": str(self.index_sqlite),
            "index_ndjson": str(self.index_ndjson),
            "ingest_log": str(self.ingest_log),
            "candidates_md": str(self.candidates_md),
            "promotions_md": str(self.promotions_md),
            "promotions_state": str(self.promotions_state),
            "riley_context": str(self.riley_context),
        }


def now_local() -> datetime:
    return datetime.now().astimezone()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def file_type_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in TEXT_EXTENSIONS:
        return "text"
    if ext in URL_EXTENSIONS:
        return "url"
    if ext == ".pdf":
        return "pdf"
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic"}:
        return "image"
    if ext in {".mp3", ".wav", ".m4a", ".aac", ".flac"}:
        return "audio"
    if ext in {".mp4", ".mov", ".mkv", ".avi", ".webm"}:
        return "video"
    return "other"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def rel_to_root(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def parse_meta(sidecar: Path) -> dict[str, Any]:
    if not sidecar.exists():
        return {}
    try:
        return json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception:
        return {}


def extract_hashtags(text: str) -> set[str]:
    return {tag.lower() for tag in re.findall(r"#[A-Za-z0-9_:-]+", text)}


def infer_tags(path_rel: str, filename: str, text: str, meta_tags: list[str] | None, url: str | None = None) -> list[str]:
    tags: set[str] = set()

    for raw in meta_tags or []:
        if isinstance(raw, str) and raw.strip():
            tag = raw.strip()
            if not tag.startswith("#"):
                tag = f"#{tag}"
            tags.add(tag.lower())

    combined = f"{path_rel} {filename} {text}".lower()

    for found in extract_hashtags(combined):
        tags.add(found)

    for keyword, mapped in KEYWORD_TAG_RULES.items():
        if keyword in combined:
            tags.update(t.lower() for t in mapped)

    if "/rileyprojects/" in path_rel.lower():
        folder_hint = path_rel.lower().split("/rileyprojects/", 1)[1].split("/", 1)[0]
        if "youtube" in folder_hint:
            tags.update({"#youtube", "#video"})
        if "armor" in folder_hint:
            tags.update({"#armor", "#scripture"})
        if "dashboard" in folder_hint:
            tags.update({"#dashboard", "#productivity"})
        if "cfa" in folder_hint:
            tags.update({"#cfa", "#virtualmanager"})

    domain_source = (url or "") + " " + combined
    for domain, mapped in DOMAIN_TAG_MAP.items():
        if domain in domain_source:
            tags.update(t.lower() for t in mapped)

    return sorted(tags)


def resolve_paths(require_existing_root: bool = True) -> ResolvedPaths:
    user = getpass.getuser()
    icloud_root = Path(f"/Users/{user}/Library/Mobile Documents/com~apple~CloudDocs")
    default_riley_root = icloud_root / "RileyFile"

    override = os.environ.get("RILEYFILE_ROOT", "").strip()
    riley_root = Path(override).expanduser().resolve() if override else default_riley_root.resolve()

    if not icloud_root.exists():
        raise FileNotFoundError(f"iCloud root missing: {icloud_root}")
    if require_existing_root and not riley_root.exists():
        raise FileNotFoundError(f"RileyFile root missing: {riley_root}")

    context_hub = riley_root / "CONTEXT_HUB"
    captures_root = context_hub / "captures"
    captures_inbox = captures_root / "inbox"
    captures_processed = captures_root / "_processed"
    captures_text = captures_root / "_text"

    index_dir = context_hub / "index"
    context_dir = context_hub / "context"
    digest_dir = context_dir / "_daily_digest"
    archive_dir = context_dir / "_archive"

    index_sqlite = index_dir / "RILEY_INDEX.sqlite"
    index_ndjson = index_dir / "RILEY_INDEX.ndjson"
    ingest_log = context_dir / "_ingest_log.ndjson"
    candidates_md = context_dir / "_candidates.md"
    promotions_md = context_dir / "_promotions.md"
    promotions_state = context_dir / ".promotions_state.json"

    riley_context = riley_root / "RILEY_CONTEXT.md"

    for p in [
        context_hub,
        captures_root,
        captures_inbox,
        captures_processed,
        captures_text,
        index_dir,
        context_dir,
        digest_dir,
        archive_dir,
        context_hub / "scripts",
    ]:
        p.mkdir(parents=True, exist_ok=True)

    return ResolvedPaths(
        user=user,
        icloud_root=icloud_root,
        riley_root=riley_root,
        context_hub=context_hub,
        captures_root=captures_root,
        captures_inbox=captures_inbox,
        captures_processed=captures_processed,
        captures_text=captures_text,
        index_dir=index_dir,
        context_dir=context_dir,
        digest_dir=digest_dir,
        archive_dir=archive_dir,
        index_sqlite=index_sqlite,
        index_ndjson=index_ndjson,
        ingest_log=ingest_log,
        candidates_md=candidates_md,
        promotions_md=promotions_md,
        promotions_state=promotions_state,
        riley_context=riley_context,
    )


def open_db(index_sqlite: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(index_sqlite)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            sha TEXT,
            size INTEGER,
            mtime REAL,
            type TEXT,
            first_seen TEXT,
            last_seen TEXT,
            extracted_text_path TEXT,
            tags_json TEXT,
            note TEXT,
            source_app TEXT,
            captured_at TEXT,
            extraction_error TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )
    conn.commit()
    return conn


def db_get_state(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT value FROM state WHERE key=?", (key,)).fetchone()
    return row[0] if row else None


def db_set_state(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO state(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )


def list_files_for_index(root: Path) -> list[Path]:
    out: list[Path] = []
    skip_dirs = {".git", "node_modules", "__pycache__"}
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_parts = rel_to_root(current, root).split("/") if current != root else []
        if any(part in skip_dirs for part in rel_parts):
            continue
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for name in filenames:
            p = current / name
            if p.name.startswith(".") and p.suffix.lower() == ".swp":
                continue
            out.append(p)
    out.sort(key=lambda p: p.as_posix())
    return out


def try_import_sqlite() -> bool:
    try:
        import sqlite3  # noqa: F401
        return True
    except Exception:
        return False


def last_24h_cutoff() -> datetime:
    return now_local() - timedelta(hours=24)

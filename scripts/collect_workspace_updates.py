#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
STATE_FILE = SCRIPTS_DIR / ".workspace_sync_state.json"
CONFIG_FILE = SCRIPTS_DIR / "workspace_sources.json"
INBOX_DIR = REPO_ROOT / "inbox"
ET_TZ = ZoneInfo("America/New_York")

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".rtf",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".csv",
    ".py",
    ".sh",
    ".zsh",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".swift",
    ".java",
    ".kt",
    ".go",
    ".rs",
    ".sql",
    ".xml",
}

EXCLUDE_DIR_NAMES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "target",
    "DerivedData",
    "__pycache__",
    ".next",
}


@dataclass
class SourceRoot:
    path: Path
    target_inbox: str
    label: str


def now_times() -> tuple[datetime, datetime]:
    utc_now = datetime.now(timezone.utc)
    return utc_now, utc_now.astimezone(ET_TZ)


def default_config() -> dict[str, Any]:
    home = Path.home()
    candidates = [
        (home / ".codex", "codex", "Codex Home"),
        (home / ".claude", "claude", "Claude Local"),
        (home / ".gemini", "gemini", "Gemini Local"),
        (home / "dev", "codex", "Dev Workspace"),
        (home / "Documents" / "GitHub", "codex", "GitHub Workspace"),
        (home / "Desktop" / "HarmonyApp", "codex", "HarmonyApp"),
        (home / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "RileyFile", "codex", "iCloud RileyFile"),
        (home / "Library" / "Group Containers" / "group.com.apple.notes", "codex", "Apple Notes Data"),
        (home / "Library" / "Group Containers" / "9K33E3U3T4.net.shinyfrog.bear", "codex", "Bear Data"),
    ]

    source_roots = []
    for path, target, label in candidates:
        if path.exists():
            source_roots.append(
                {
                    "path": str(path),
                    "target_inbox": target,
                    "label": label,
                }
            )

    return {
        "source_roots": source_roots,
        "exclude_paths": [str(REPO_ROOT)],
        "exclude_dir_names": sorted(EXCLUDE_DIR_NAMES),
        "allowed_extensions": sorted(TEXT_EXTENSIONS),
        "max_file_size_bytes": 2_000_000,
        "bootstrap_recent_hours": 24,
        "snippet_char_limit": 1400,
    }


def load_or_create_config() -> dict[str, Any]:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    cfg = default_config()
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    return cfg


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {"initialized": False, "files": {}}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"initialized": False, "files": {}}


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize_sources(raw: list[dict[str, Any]]) -> list[SourceRoot]:
    sources: list[SourceRoot] = []
    for item in raw:
        path = Path(item.get("path", "")).expanduser()
        target = str(item.get("target_inbox", "codex")).lower().strip()
        label = str(item.get("label", path.name)).strip() or path.name
        if not path.exists() or target not in {"codex", "claude", "chatgpt", "gemini"}:
            continue
        sources.append(SourceRoot(path=path, target_inbox=target, label=label))
    return sources


def is_excluded(path: Path, excluded_paths: list[Path]) -> bool:
    for base in excluded_paths:
        try:
            path.relative_to(base)
            return True
        except ValueError:
            continue
    return False


def sha256_prefix(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()[:16]


def safe_read_snippet(path: Path, char_limit: int) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    snippet = text[:char_limit]
    return snippet.strip()


def file_fingerprint(path: Path, stat: os.stat_result) -> str:
    return f"{stat.st_size}:{stat.st_mtime_ns}"


def collect_changes(
    sources: list[SourceRoot],
    state: dict[str, Any],
    cfg: dict[str, Any],
    now_utc: datetime,
) -> tuple[dict[str, str], list[dict[str, Any]]]:
    previous = state.get("files", {})
    current: dict[str, str] = {}
    changes: list[dict[str, Any]] = []

    excluded_paths = [Path(p).expanduser() for p in cfg.get("exclude_paths", [])]
    excluded_names = set(cfg.get("exclude_dir_names", []))
    allowed_exts = set(cfg.get("allowed_extensions", []))
    max_size = int(cfg.get("max_file_size_bytes", 2_000_000))
    bootstrap_hours = int(cfg.get("bootstrap_recent_hours", 24))
    bootstrap_cutoff = now_utc - timedelta(hours=bootstrap_hours)
    initialized = bool(state.get("initialized", False))

    for source in sources:
        for root, dirs, files in os.walk(source.path, topdown=True):
            root_path = Path(root)
            dirs[:] = [
                d
                for d in dirs
                if d not in excluded_names and not is_excluded(root_path / d, excluded_paths)
            ]

            if is_excluded(root_path, excluded_paths):
                continue

            for name in files:
                path = root_path / name
                if is_excluded(path, excluded_paths):
                    continue

                try:
                    stat = path.stat()
                except OSError:
                    continue

                key = str(path)
                fp = file_fingerprint(path, stat)
                current[key] = fp

                previous_fp = previous.get(key)
                is_new_or_changed = previous_fp != fp
                if not is_new_or_changed:
                    continue

                mtime_utc = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
                if not initialized and mtime_utc < bootstrap_cutoff:
                    continue

                suffix = path.suffix.lower()
                is_text = suffix in allowed_exts and stat.st_size <= max_size
                snippet = safe_read_snippet(path, int(cfg.get("snippet_char_limit", 1400))) if is_text else None
                rel = str(path)
                changes.append(
                    {
                        "source_label": source.label,
                        "source_root": str(source.path),
                        "target_inbox": source.target_inbox,
                        "path": rel,
                        "size": stat.st_size,
                        "mtime_et": mtime_utc.astimezone(ET_TZ).strftime("%Y-%m-%d %H:%M:%S %Z"),
                        "sha16": sha256_prefix(path),
                        "kind": "text" if is_text else "binary_or_large",
                        "snippet": snippet,
                    }
                )

    return current, changes


def write_inbox_drops(changes: list[dict[str, Any]], now_et: datetime) -> list[str]:
    if not changes:
        return []

    by_target: dict[str, list[dict[str, Any]]] = {}
    for item in changes:
        by_target.setdefault(item["target_inbox"], []).append(item)

    created: list[str] = []
    stamp = now_et.strftime("%Y-%m-%d_%H%M%S")
    for target, items in by_target.items():
        inbox_path = INBOX_DIR / target
        inbox_path.mkdir(parents=True, exist_ok=True)
        out_file = inbox_path / f"{stamp}_workspace_sync.md"

        lines = [
            "# Workspace Sync Drop",
            "",
            f"- Captured At: {now_et.strftime('%Y-%m-%d %H:%M:%S %Z')}",
            f"- Target Inbox: {target}",
            f"- Changed Files: {len(items)}",
            "",
            "## Changed Files",
            "",
        ]

        for item in items:
            lines.extend(
                [
                    f"### `{item['path']}`",
                    f"- Source: {item['source_label']} ({item['source_root']})",
                    f"- Modified: {item['mtime_et']}",
                    f"- Size: {item['size']} bytes",
                    f"- SHA256 (16): `{item['sha16']}`",
                    f"- Kind: {item['kind']}",
                ]
            )
            if item["snippet"]:
                lines.extend(["- Snippet:", "```text", item["snippet"], "```"])
            lines.append("")

        out_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        created.append(str(out_file.relative_to(REPO_ROOT)))

    return created


def main() -> int:
    cfg = load_or_create_config()
    state = load_state()
    now_utc, now_et = now_times()

    sources = normalize_sources(cfg.get("source_roots", []))
    current, changes = collect_changes(sources, state, cfg, now_utc)
    created = write_inbox_drops(changes, now_et)

    new_state = {
        "initialized": True,
        "last_run_utc": now_utc.isoformat(),
        "last_run_et": now_et.isoformat(),
        "files": current,
    }
    save_state(new_state)

    print(f"workspace_sources={len(sources)}")
    print(f"workspace_changes={len(changes)}")
    print(f"workspace_drops={len(created)}")
    for rel in created:
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

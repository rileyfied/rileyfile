#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
INBOX_DIR = REPO_ROOT / "inbox"
SCRIPTS_DIR = REPO_ROOT / "scripts"
STATE_FILE = SCRIPTS_DIR / ".last_run.json"

RILEY_CONTEXT_FILE = REPO_ROOT / "RILEY_CONTEXT.md"
INDEX_FILE = REPO_ROOT / "index.md"
MEMORY_FILE = REPO_ROOT / "memory.md"

LOG_FILES = {
    "chatgpt": REPO_ROOT / "chatgpt.md",
    "gemini": REPO_ROOT / "gemini.md",
    "claude": REPO_ROOT / "claude.md",
    "codex": REPO_ROOT / "codex.md",
}

ET_TZ = ZoneInfo("America/New_York")
CONTEXT_ACTIVITY_HEADING = "## Daily Context Sync Activity (Append-Only)"
MEMORY_CANDIDATES_HEADING = "## Memory Candidates (Append-Only)"
INDEX_RUNS_HEADING = "## Context Sync Runs (Append-Only)"


def now_times() -> tuple[datetime, datetime]:
    now_utc = datetime.now(timezone.utc)
    return now_utc, now_utc.astimezone(ET_TZ)


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"processed_files": []}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"processed_files": []}


def save_state(processed_files: list[str], now_utc: datetime, now_et: datetime) -> None:
    payload = {
        "last_run_utc": now_utc.isoformat(),
        "last_run_et": now_et.isoformat(),
        "processed_files": processed_files,
    }
    STATE_FILE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_text(path: Path, fallback: str = "") -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return fallback


def ensure_file(path: Path, heading: str) -> None:
    if not path.exists():
        path.write_text(f"# {heading}\n", encoding="utf-8")


def initialize_log_files() -> None:
    for agent, path in LOG_FILES.items():
        ensure_file(path, f"{agent}.md")


def append_to_agent_log(agent: str, rel_path: str, content: str, run_stamp: str) -> None:
    path = LOG_FILES[agent]
    ensure_file(path, f"{agent}.md")
    body = read_text(path).rstrip() + "\n\n"
    body += f"## Inbox Import — {run_stamp}\n"
    body += f"- Source: `{rel_path}`\n\n"
    body += content.rstrip() + "\n"
    path.write_text(body, encoding="utf-8")


def ensure_section(text: str, heading: str) -> str:
    if heading in text:
        return text
    stripped = text.rstrip()
    if stripped:
        return f"{stripped}\n\n{heading}\n"
    return f"{heading}\n"


def append_memory_candidates(imports: list[dict], run_stamp: str) -> None:
    text = read_text(MEMORY_FILE, "# memory.md\n")
    text = ensure_section(text, MEMORY_CANDIDATES_HEADING)
    chunks = []
    for item in imports:
        chunks.append(
            "\n".join(
                [
                    f"### {run_stamp} — {item['agent']} — `{item['rel_path']}`",
                    "```md",
                    item["content"].rstrip(),
                    "```",
                ]
            )
        )
    updated = text.rstrip() + "\n\n" + "\n\n".join(chunks) + "\n"
    MEMORY_FILE.write_text(updated, encoding="utf-8")


def update_index(processed_rel_paths: list[str], run_stamp: str) -> None:
    text = read_text(INDEX_FILE, "# RileyFile Index\n")
    run_line = f"*Last context sync run: {run_stamp} (America/New_York)*"

    if re.search(r"^\*Last context sync run: .*\*$", text, flags=re.MULTILINE):
        text = re.sub(r"^\*Last context sync run: .*\*$", run_line, text, flags=re.MULTILINE)
    else:
        lines = text.splitlines()
        if lines and lines[0].startswith("#"):
            text = "\n".join([lines[0], "", run_line] + lines[1:]) + "\n"
        else:
            text = run_line + "\n\n" + text.lstrip()

    text = ensure_section(text, INDEX_RUNS_HEADING)

    files_block = [f"- `{p}`" for p in processed_rel_paths] if processed_rel_paths else ["- (none)"]
    run_block = "\n".join([f"### {run_stamp}"] + files_block)

    text = text.rstrip() + "\n\n" + run_block + "\n"
    INDEX_FILE.write_text(text, encoding="utf-8")


def update_riley_context(processed_rel_paths: list[str], run_stamp: str, today_date: str) -> None:
    text = read_text(RILEY_CONTEXT_FILE, "# RILEY_CONTEXT.md\n")

    if re.search(r"^## Last Updated: .*", text, flags=re.MULTILINE):
        text = re.sub(r"^## Last Updated: .*", f"## Last Updated: {today_date}", text, flags=re.MULTILINE)
    else:
        text = text.rstrip() + f"\n\n## Last Updated: {today_date}\n"

    text = ensure_section(text, CONTEXT_ACTIVITY_HEADING)

    if processed_rel_paths:
        pointers = [f"- `{p}`" for p in processed_rel_paths]
    else:
        pointers = ["- No new inbox files processed."]

    run_block = "\n".join([f"### {run_stamp}"] + pointers)
    text = text.rstrip() + "\n\n" + run_block + "\n"
    RILEY_CONTEXT_FILE.write_text(text, encoding="utf-8")


def collect_inbox_markdown_files() -> list[Path]:
    if not INBOX_DIR.exists():
        return []
    files = [p for p in INBOX_DIR.rglob("*.md") if p.is_file()]
    return sorted(files, key=lambda p: p.as_posix())


def main() -> int:
    now_utc, now_et = now_times()
    run_stamp = now_et.strftime("%Y-%m-%d %H:%M:%S")
    today_date = now_et.strftime("%Y-%m-%d")

    initialize_log_files()

    state = load_state()
    processed_set = set(state.get("processed_files", []))

    inbox_files = collect_inbox_markdown_files()
    new_files = [p for p in inbox_files if p.relative_to(REPO_ROOT).as_posix() not in processed_set]

    imports: list[dict] = []
    for path in new_files:
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        parts = path.relative_to(INBOX_DIR).parts
        if not parts:
            continue
        agent = parts[0].lower()
        if agent not in LOG_FILES:
            continue

        content = path.read_text(encoding="utf-8")
        imports.append({"agent": agent, "rel_path": rel_path, "content": content})
        append_to_agent_log(agent, rel_path, content, run_stamp)

    processed_rel_paths = [item["rel_path"] for item in imports]

    if imports:
        append_memory_candidates(imports, run_stamp)

    update_index(processed_rel_paths, run_stamp)
    update_riley_context(processed_rel_paths, run_stamp, today_date)

    new_processed_files = sorted(processed_set.union({p.relative_to(REPO_ROOT).as_posix() for p in new_files}))
    save_state(new_processed_files, now_utc, now_et)

    print(f"run_stamp={run_stamp}")
    print(f"processed_new_files={len(processed_rel_paths)}")
    for rel in processed_rel_paths:
        print(rel)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

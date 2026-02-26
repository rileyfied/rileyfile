#!/usr/bin/env bash
set -euo pipefail

# --- single-instance lock (prevents concurrent sqlite writes) ---
LOCK_DIR="${RILEYFILE_ROOT:-$(pwd)}/CONTEXT_HUB/.lock"
LOCK_TTL_SECONDS="${LOCK_TTL_SECONDS:-3600}"

acquire_lock() {
  if mkdir "$LOCK_DIR" 2>/dev/null; then
    date +%s > "$LOCK_DIR/started_epoch"
    echo "$$" > "$LOCK_DIR/pid"
    return 0
  fi

  # lock exists: check staleness
  if [[ -f "$LOCK_DIR/started_epoch" ]]; then
    local started now age
    started="$(cat "$LOCK_DIR/started_epoch" 2>/dev/null || echo 0)"
    now="$(date +%s)"
    age=$(( now - started ))
    if (( age > LOCK_TTL_SECONDS )); then
      echo "Stale lock detected (age=${age}s). Removing and retrying..."
      rm -rf "$LOCK_DIR"
      mkdir "$LOCK_DIR" 2>/dev/null || { echo "Lock busy; exiting."; exit 3; }
      date +%s > "$LOCK_DIR/started_epoch"
      echo "$$" > "$LOCK_DIR/pid"
      return 0
    fi
  fi

  echo "Another sync_context run is in progress. Exiting."
  exit 3
}

release_lock() {
  rm -rf "$LOCK_DIR" 2>/dev/null || true
}

acquire_lock
trap release_lock EXIT INT TERM
# --- end lock ---

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Missing dependency: python3"
  echo "Install suggestion: brew install python"
  exit 1
fi

if ! python3 - <<'PY' >/dev/null 2>&1
import sqlite3
PY
then
  echo "Missing dependency: sqlite (python sqlite3 module)"
  echo "Install suggestion: brew install sqlite"
  exit 1
fi

if ! command -v pdftotext >/dev/null 2>&1; then
  echo "Missing dependency: pdftotext"
  echo "Install suggestion: brew install poppler"
  exit 1
fi

PATH_JSON="$(python3 "$SCRIPT_DIR/resolve_paths.py" --json)"
RILEY_ROOT="$(printf '%s' "$PATH_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["riley_root"])')"
INDEX_SQLITE="$(printf '%s' "$PATH_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["index_sqlite"])')"

FIRST_RUN=0
if [[ ! -f "$INDEX_SQLITE" ]]; then
  FIRST_RUN=1
else
  FIRST_RUN_FLAG="$(python3 - <<PY
import sqlite3
db = r"""$INDEX_SQLITE"""
try:
    conn = sqlite3.connect(db)
    cur = conn.execute("SELECT value FROM state WHERE key='captures_first_run_complete'")
    row = cur.fetchone()
    conn.close()
    print("1" if row and str(row[0]) == "1" else "0")
except Exception:
    print("0")
PY
)"
  if [[ "$FIRST_RUN_FLAG" != "1" ]]; then
    FIRST_RUN=1
  fi
fi

python3 "$SCRIPT_DIR/index_rileyfile.py"

if [[ "$FIRST_RUN" == "1" ]]; then
  python3 "$SCRIPT_DIR/ingest_captures.py" --first-run
else
  python3 "$SCRIPT_DIR/ingest_captures.py"
fi

python3 "$SCRIPT_DIR/build_digest.py"
python3 "$SCRIPT_DIR/build_promotions.py"
python3 "$SCRIPT_DIR/merge_promotions.py"

if [[ "${SYNC_CONTEXT_SKIP_GIT:-0}" == "1" ]]; then
  echo "Skipping git commit/push (SYNC_CONTEXT_SKIP_GIT=1)"
  exit 0
fi

if [[ ! -d "$RILEY_ROOT/.git" ]]; then
  echo "No git repo at Riley root, skipping commit/push: $RILEY_ROOT"
  exit 0
fi

cd "$RILEY_ROOT"

git add RILEY_CONTEXT.md CONTEXT_HUB
if git diff --cached --quiet -- RILEY_CONTEXT.md CONTEXT_HUB; then
  echo "No git changes to commit"
  exit 0
fi

git commit -m "chore: sync context hub $(date '+%Y-%m-%d %H:%M')"
git push

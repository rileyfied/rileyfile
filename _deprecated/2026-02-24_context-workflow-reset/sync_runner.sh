#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

mkdir -p logs
LOCK_DIR="$REPO_DIR/scripts/.sync.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  exit 0
fi
trap 'rmdir "$LOCK_DIR"' EXIT

if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
  echo "sync_runner: git rebase in progress; aborting run" >&2
  exit 1
fi

git pull --rebase --autostash

python3 scripts/collect_workspace_updates.py

COMPILE_OUTPUT="$(python3 scripts/compile_context.py)"
echo "$COMPILE_OUTPUT"
PROCESSED_NEW_FILES="$(printf '%s\n' "$COMPILE_OUTPUT" | awk -F= '/^processed_new_files=/{print $2}')"
if [ "${PROCESSED_NEW_FILES:-0}" = "0" ]; then
  exit 0
fi

git add -A
if git diff --cached --quiet; then
  exit 0
fi

git commit -m "Context sync $(date '+%Y-%m-%d %H:%M:%S')"
git push

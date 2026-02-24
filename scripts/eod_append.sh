#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: ./scripts/eod_append.sh path/to/drop.md [SOURCE]"
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

DROP_FILE="$1"
SOURCE="${2:-UNKNOWN}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONTEXT_FILE="$REPO_DIR/RILEY_CONTEXT.md"

if [[ ! -f "$DROP_FILE" ]]; then
  echo "Error: input file not found: $DROP_FILE"
  exit 1
fi

if [[ ! -s "$DROP_FILE" ]]; then
  echo "Error: input file is empty: $DROP_FILE"
  exit 1
fi

if [[ ! -f "$CONTEXT_FILE" ]]; then
  echo "Error: canonical context file not found: $CONTEXT_FILE"
  exit 1
fi

if [[ ! -d "$REPO_DIR/.git" ]]; then
  echo "Error: not a git repository: $REPO_DIR"
  exit 1
fi

cd "$REPO_DIR"

if ! grep -q '^## DAILY LOG$' "$CONTEXT_FILE"; then
  printf '\n## DAILY LOG\n' >> "$CONTEXT_FILE"
fi

if [[ -n "$(tail -c 1 "$CONTEXT_FILE" 2>/dev/null || true)" ]]; then
  printf '\n' >> "$CONTEXT_FILE"
fi

TIMESTAMP="$(date '+%Y-%m-%d %H:%M')"

{
  printf '\n### %s [%s]\n\n' "$TIMESTAMP" "$SOURCE"
  printf '%s\n\n' '---'
  cat "$DROP_FILE"
  printf '\n\n'
} >> "$CONTEXT_FILE"

git add RILEY_CONTEXT.md

if git diff --cached --quiet -- RILEY_CONTEXT.md; then
  echo "No changes to commit"
  exit 0
fi

git commit -m "chore: append daily log ${TIMESTAMP} (${SOURCE})" -- RILEY_CONTEXT.md
git push

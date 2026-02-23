#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

mkdir -p logs

git pull --rebase
python3 scripts/compile_context.py

git add -A
if git diff --cached --quiet; then
  exit 0
fi

git commit -m "Daily context sync $(date +%F)"
git push

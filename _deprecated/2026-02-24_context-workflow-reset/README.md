# 2026-02-24 Context Workflow Reset

Moved here during workflow hardening to enforce one reliable daily flow:
append EOD drops directly to `RILEY_CONTEXT.md` via `scripts/eod_append.sh`.

These files/folders are legacy or conflicting sources (old compile/sync pipelines,
secondary context copies, generated logs, and stale setup docs).

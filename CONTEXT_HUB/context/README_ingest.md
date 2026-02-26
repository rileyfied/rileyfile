# Context Hub Ingest Guide

## Capture locations
- Primary capture root: `CONTEXT_HUB/captures/`
- Ongoing inbox (subsequent runs): `CONTEXT_HUB/captures/inbox/`
- Processed archive: `CONTEXT_HUB/captures/_processed/`
- Extracted text cache: `CONTEXT_HUB/captures/_text/`

## Optional sidecar metadata
For any file `example.ext`, add `example.ext.meta.json` with:

```json
{
  "tags": ["#youtube", "#aibrief"],
  "note": "why I saved this",
  "source_app": "Chrome iOS",
  "captured_at": "2026-02-26T10:15:00-05:00"
}
```

## Promotion controls
- Automatic promotion requires at least one known project hashtag in `tags`.
- Forced promotion: place the artifact under `_to_context/` anywhere in RileyFile.

## Run commands
Manual sync:

```bash
./scripts/sync_context.sh
```

Repo-local validation (keeps live iCloud files untouched):

```bash
RILEYFILE_ROOT="$(pwd)" SYNC_CONTEXT_SKIP_GIT=1 ./scripts/sync_context.sh
```

## Troubleshooting
- If `pdftotext` is missing, install: `brew install poppler`
- If python sqlite support is missing, install: `brew install sqlite`
- Inspect logs: `logs/context_hub.stdout.log` and `logs/context_hub.stderr.log`
- Audit ingest history: `CONTEXT_HUB/context/_ingest_log.ndjson`

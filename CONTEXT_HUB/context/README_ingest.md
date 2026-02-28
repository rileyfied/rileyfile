# Context Hub Ingest Guide

## Watched capture inboxes
When `RILEYFILE_ROOT` points to iCloud RileyFile, every run watches both:
- `RileyFile/CONTEXT_HUB/captures/inbox/`
- `RileyFile/RileyShare/captures/inbox/` (if this folder exists)

## First full ingest behavior
On first full ingest (`CONTEXT_HUB/context/.state.json` missing or `full_ingest_completed=false`), the runner does:
1. Full RileyFile index baseline.
2. Full ingest from both capture roots:
   - `RileyFile/CONTEXT_HUB/captures/`
   - `RileyFile/RileyShare/captures/` (if exists)
3. Digest + candidates + promotions + merge.
4. Writes state:

```json
{
  "full_ingest_completed": true,
  "completed_at": "...",
  "index_version": 3
}
```

## FAST mode
FAST mode skips indexing and only ingests inboxes + digest/promotions/merge.

```bash
RILEYFILE_ROOT="/Users/rileycolleyFW/Library/Mobile Documents/com~apple~CloudDocs/RileyFile" \
SYNC_CONTEXT_SKIP_GIT=1 \
SYNC_CONTEXT_FAST=1 \
./scripts/sync_context.sh
```

## Outputs (iCloud root)
All outputs land under:
- `RileyFile/CONTEXT_HUB/index/RILEY_INDEX.sqlite`
- `RileyFile/CONTEXT_HUB/context/_ingest_log.ndjson`
- `RileyFile/CONTEXT_HUB/context/_daily_digest/YYYY-MM-DD.md`
- `RileyFile/CONTEXT_HUB/context/_candidates.md`
- `RileyFile/CONTEXT_HUB/context/_promotions.md`
- `RileyFile/RILEY_CONTEXT.md` (merge target)

## Metadata sidecar
For any file `example.ext`, optional sidecar:
`example.ext.meta.json`

```json
{
  "tags": ["#youtube", "#aibrief"],
  "note": "why I saved this",
  "source_app": "Chrome iOS",
  "captured_at": "2026-02-27T10:15:00-05:00"
}
```

Promotion eligibility:
- Explicit known project hashtag in `tags`, or
- File originated from any `_to_context/` path.

## Direct script usage
```bash
python3 scripts/ingest_captures.py --rileyfile-root "<RILEYFILE_ROOT>" --mode inbox
python3 scripts/ingest_captures.py --rileyfile-root "<RILEYFILE_ROOT>" --mode all
python3 scripts/build_digest.py --rileyfile-root "<RILEYFILE_ROOT>"
python3 scripts/build_promotions.py --rileyfile-root "<RILEYFILE_ROOT>"
python3 scripts/merge_promotions.py --rileyfile-root "<RILEYFILE_ROOT>"
```

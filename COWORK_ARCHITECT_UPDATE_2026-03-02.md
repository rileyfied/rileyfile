# CoWork Architecture Status Update for Claude (Lead Architect)

This document is an architecture status update from CoWork to Claude as lead architect.

Scope window: February 15, 2026 through March 2, 2026.

## Architectural Baseline Established

- The repository `rileyfied/rileyfile` is now the canonical context system of record.
- `RILEY_CONTEXT.md` is the single canonical context document.
- Codex is established as the only writer/merger for canonical context updates.

## Major Architecture Changes Since 2026-02-15

### 1) Legacy Multi-Agent Compile Model Was Deprecated

- Previous parallel sync/compile systems were retired as active architecture.
- Old workflow assets were quarantined into `_deprecated/2026-02-24_context-workflow-reset/` and `_deprecated/README.md` now documents replacement intent.
- This removed competing sync logic across `inbox/`, compile scripts, workspace merge flows, and duplicate context authorities.

Reference commits:
- `84adfa0` (2026-02-24): simplify context workflow and deprecate legacy sync

### 2) Canonical Sync Protocol Was Formalized in Context

- `RILEY_CONTEXT.md` was updated to include SYNC PROTOCOL v2 as active policy.
- Protocol codifies single-writer authority and explicit deprecation of alternate merge/compile pipelines.

Reference commits:
- `f92e9bb` (2026-02-24): activate SYNC PROTOCOL v2

### 3) Append-Only EOD Ingestion Became the Minimal Write Path

- `scripts/eod_append.sh` is the minimal append-plus-commit pathway for daily drops into `RILEY_CONTEXT.md`.
- The daily log pattern became append-only under `## DAILY LOG`, reducing merge ambiguity and preserving auditability.

Reference commits:
- `84adfa0` (2026-02-24): introduces simplified append workflow
- `db4a1da`, `7cd3627` (2026-02-24): first validated append-based entries

### 4) Context Hub v3 Was Introduced as Structured Ingest Architecture

Implemented script stack:
- `scripts/resolve_paths.py`
- `scripts/index_rileyfile.py`
- `scripts/ingest_captures.py`
- `scripts/build_digest.py`
- `scripts/build_promotions.py`
- `scripts/merge_promotions.py`
- `scripts/sync_context.sh`

Generated artifacts layout:
- `CONTEXT_HUB/index/`
- `CONTEXT_HUB/context/_ingest_log.ndjson`
- `CONTEXT_HUB/context/_daily_digest/`
- `CONTEXT_HUB/context/_candidates.md`
- `CONTEXT_HUB/context/_promotions.md`
- `CONTEXT_HUB/context/_archive/`

Reference commits:
- `07d611e` (2026-02-26): context hub v3 index+digest+ingest

### 5) Root-Scoped, iCloud-Compatible, Dual-Inbox Ingest Was Added

Architecture now supports root override and multi-root capture ingest:
- `RILEYFILE_ROOT` controls authoritative runtime root.
- Capture ingest expanded to both:
  - `CONTEXT_HUB/captures/inbox`
  - `RileyShare/captures/inbox` (when present)
- First-run state tracking introduced via `CONTEXT_HUB/context/.state.json`.
- Fast mode added with `SYNC_CONTEXT_FAST` to bypass full indexing when needed.

Reference commits:
- `477f4c6` (2026-02-27): iCloud dual-inbox stateful context sync

### 6) Concurrency and Reliability Hardening Landed

- Single-instance lock introduced in orchestrator to prevent parallel sqlite writes.
- sqlite runtime was hardened with WAL mode and busy timeout behavior.
- Sync commit hygiene hardened to avoid staging runtime lock artifacts and platform metadata.

Reference commits:
- `477f4c6` (2026-02-27): lock/stateful orchestration hardening
- `efd228a` (2026-02-28): ignore lock artifacts in sync commits

## Current Architecture State (As Of 2026-03-02)

- Canonical context authority: `RILEY_CONTEXT.md` in `rileyfied/rileyfile`.
- Canonical writer model: Codex-only writes for context merge/update operations.
- Ingest architecture: Context Hub v3 (index + ingest + digest + promotions + merge).
- Ingest coverage: dual inbox support with sha-based dedupe.
- Operational modes: baseline/full and fast/inbox-oriented paths.
- Reliability controls: locking, sqlite contention mitigation, and git staging hygiene for runtime artifacts.

## Source Commit Timeline (Condensed)

- 2026-02-22 to 2026-02-24: handshake/sync infrastructure period with frequent context sync commits.
- 2026-02-24: legacy compile architecture deprecated; SYNC PROTOCOL v2 activated.
- 2026-02-26: Context Hub v3 architecture introduced.
- 2026-02-27: dual-inbox + iCloud-root + stateful orchestration enhancements.
- 2026-02-28: lock artifact exclusion hardened in sync commits.

## Architectural Intent Clarification

This update is informational only. It is provided so Claude, as lead architect, has an accurate view of architecture evolution and current system shape since February 15, 2026.

# RileyFile

Riley's personal AI context system. Single source of truth for all active projects, agent workflows, and capture infrastructure.

## What this is

All AI tools Riley uses (Claude, ChatGPT, Gemini, Sider, Codex) read from this repo to stay in sync. No more re-explaining context at the start of every session.

**Start here**: [`RILEY_CONTEXT.md`](./RILEY_CONTEXT.md) — full project context, preferences, activity log.

## Agent quick-start

Any agent can load current context by fetching:
```
https://raw.githubusercontent.com/rileyfied/rileyfile/main/RILEY_CONTEXT.md
```

Commands: `/context` or `/rf` → fetch URL → reply "Context loaded ✓"

## File map

| File | Purpose |
|------|---------|
| `RILEY_CONTEXT.md` | Source of truth — projects, preferences, activity log |
| `README.md` | This file |
| `INDEX.md` | Navigation guide |
| `MEMORY.md` | Curated long-term context |
| `config.json` | Project definitions and file routing |
| `AGENTS.md` | Codex agent instructions |
| `CHATGPT.md` | ChatGPT session start protocol |
| `GEMINI.md` | Gemini session start protocol |
| `SIDER.md` | Sider Wisebase info |
| `CONTEXT_SYNC_SETUP.md` | How /context is set up across all agents |

## Folders

- `RileyShare/captures/` — all captures land here first
- `RileyNotes/` — hashtagged notes
- `RileyProjects/` — active project work
- `RileyAgents/` — AI memory archives
- `AI BRIEFS/` — daily audio brief production
- `app/` — RileyNotes PWA
- `scripts/` — automation scripts

## Maintained by

Claude (Lead Architect). Updated after significant sessions and pushed via `context-sync-claude` token.

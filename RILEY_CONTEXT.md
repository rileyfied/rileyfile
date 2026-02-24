# RILEY_CONTEXT.md
## Last Updated: 2026-02-23

> **Purpose**: Source of truth for Riley's projects, preferences, and active work. Read by Claude (lead architect) and all AI agents. Hosted at: https://raw.githubusercontent.com/rileyfied/rileyfile/main/RILEY_CONTEXT.md

---

## WHO IS RILEY

Entrepreneur, content creator, restaurant operations leader (Chick-fil-A). Building in the AI space while working full-time. "Multi-channel dumper" — captures ideas across texts, voice memos, screenshots, AI chats, playlists. Strong bias toward speed over organization at capture time.

**Communication**: Direct, efficient. No excessive formatting. Hashtags over folders. Context over structure. Show don't tell.

**Design eye**: Clean, minimal, non-generic. Gets distracted by formatting options — keep UI stripped down.

---

## ACTIVE PROJECTS (Priority Order)

**1. YouTube Channel** — #youtube #video #ai #tutorial
AI tools for non-technical audiences. First video: "You're Using AI Wrong." Target: frontline operational managers, not enterprise knowledge workers. Style refs: Nate B. Jones, Fireship, Igor Pogany.
Resources: `RileyFile/RileyProjects/YOUTUBE CHANNEL`

**2. Daily AI Audio Brief** — #aibrief #audio #news
15-20 min solo-narration briefings on breaking AI news. Sources: The Rundown AI, Ben's Bites, TechCrunch AI, arXiv, X/Reddit. NotebookLM format with copy/paste-ready blocks.

**3. Armor App** — #armor #scripture #bible #fighterverses
Scripture memorization with gamified 5-mechanic ladder (Word Bank → Word Scramble → Type 1st Letter → Type Full Word → Recite). Fighter Verses data sets A-E ready. Full blueprint exists at `RileyProjects/ARMOR APP/Armour_GPT_InfoArchBlueprint_v1.rtf`.
Resources: `RileyFile/RileyProjects/ARMOR APP`

**4. HarmonyHelper** — #harmony #piano #music #chords
Piano practice app. Python backend, web frontend.
Resources: `/Desktop/HarmonyApp/`

**5. AI Operations Monitor** — #conductor #monitor #agents
Local agent that watches AI processes on machine, reports costs, flags waste, eventually orchestrates which AI does what. Vision: non-technical conductor for AI workflows. PWA prototype first.

**6. Dashboard App (RileyHQ)** — #dashboard #productivity
Command center for all projects. Zero manual maintenance. Design discovery phase.

**7. Virtual Restaurant Manager** — #virtualmanager #visor #cfa
Knowledge base agent for restaurant operations. All roles in one place — owner, managers, vendors, HR, etc. Multi-year vision. Concept documented.

---

## RILEYDOMAIN STRUCTURE

```
RileyFile/
├── RILEY_CONTEXT.md        ← This file (source of truth)
├── README.md               ← Repo overview
├── INDEX.md                ← Navigation guide
├── MEMORY.md               ← Curated long-term context
├── config.json             ← Project definitions
├── AGENTS.md               ← Codex agent instructions (also at ~/.codex/AGENTS.md)
├── CHATGPT.md              ← ChatGPT handshake + session start protocol
├── GEMINI.md               ← Gemini handshake + session start protocol
├── SIDER.md                ← Sider handshake + Wisebase info
├── CONTEXT_SYNC_SETUP.md   ← How /context works across all agents
├── RILEY_CONTEXT_SYNC.md   ← External-facing sync copy (for gist)
├── RileyShare/             ← Default landing zone for all files
│   └── captures/           ← iOS Shortcut captures, bookmarks
├── RileyNotes/             ← Notes with #hashtags
├── RileyProjects/          ← Active project folders
│   ├── ARMOR APP/
│   ├── YOUTUBE CHANNEL/
│   ├── DASHBOARD APP/
│   ├── CFA TRAINING/
│   └── RILEY API/
├── RileyAgents/            ← AI memory archives
├── AI BRIEFS/              ← Daily audio brief production
├── app/                    ← RileyNotes PWA
└── scripts/                ← Automation scripts
```

---

## AI TEAM

**Claude** (Lead Architect) — Claude.ai + Cowork
File ops, terminal commands, builds, context sync, system architecture. Terminal activity is Claude-initiated. Session start: reads this file.

**Codex** — Terminal / local agentic tasks
Runs automations, file operations, local scripts. Session start: reads `~/.codex/AGENTS.md` which points to this GitHub URL. `/context` or `/rf` = fetch and confirm "Context loaded ✓".

**Sider** (Multi-Model Hub) — Browser extension (Plus)
Quick queries, web research, deep research, model comparison, PDF analysis. Wisebase "Riley Context Hub" loaded with RILEY_CONTEXT + ARMOR_APP_SPEC notes. Session start: reads Wisebase.

**ChatGPT** — Ideation, long-form content, AI briefs
Brainstorming, daily AI briefs, scripts. 80+ saved memories. `/context` = fetches GitHub URL. Session start: loads context from GitHub.

**Gemini** — Google ecosystem
Search, research, Google integration. `/context` = fetches GitHub URL. Session start: loads context from GitHub.

**Sync Protocol**: Claude updates RILEY_CONTEXT.md locally, commits and pushes to GitHub. All agents reference `https://raw.githubusercontent.com/rileyfied/rileyfile/main/RILEY_CONTEXT.md` as source of truth.

**GitHub**: username `rileyfied`. Login: Sign in with Apple. Token: `context-sync-claude` (active through 2026-06-09).

---

## CAPTURE METHODS

- RileyNotes app (manual typing)
- iOS Share Sheet shortcut (one-tap save)
- Back Tap (double-tap phone back = clipboard saved)
- Voice capture via home screen icon
- macOS automation (Codex-based capture — tested and working 2026-02-19)
- All captures land in `RileyShare/captures/` and get organized by Claude

---

## DESIGN THINKING (Apply to Every Build)

1. **Empathize**: Fast/messy capture is intentional. Organization should be invisible.
2. **Define**: What friction is this solving? Ask before building.
3. **Ideate**: Present options, not just solutions. Match minimal aesthetic.
4. **Prototype**: Functional first. Artifacts over documentation.
5. **Test**: Watch for "close but..." feedback. Adjust fast, don't defend.

## DECISION PRINCIPLES

Minimal > Feature-rich. Speed > Perfection. Context > Structure. Cross-platform required. Auto-organize, don't ask the user. Build for others to use — tools should be shareable and non-technical-friendly.

---

## ACTIVITY LOG

### 2026-02-23
- **Agent handshake files pushed to GitHub**: CHATGPT.md, GEMINI.md, SIDER.md, CONTEXT_SYNC_SETUP.md, INDEX.md, MEMORY.md, RILEY_CONTEXT_SYNC.md all committed and live on repo.
- **Codex AGENTS.md created**: Written to `~/.codex/AGENTS.md` and `~/AGENTS.md`. Contains /context protocol, workflow rules, file routing, capture methods.
- **Git auth resolved**: context-sync-claude token authenticated. Email privacy conflict resolved with noreply address. Merge conflict (unrelated histories) resolved keeping local versions.
- **Identified gap**: No auto-sync automation exists. /sync requires manual Claude session trigger. Action needed: launchd job or Codex scheduled task.

### 2026-02-15
- **Boil Out**: Nuked OpenClaw (config, binary, credentials, completions). Removed Codex (old version). Stripped agent personality files from RileyFile. Cleaned exposed API keys from .zshrc.
- **AI Operations Monitor spec complete**: Tracks spend on Claude.ai, Sider, ChatGPT, Gemini. iPhone widget + Mac app. Phased: Monitor → Flag → Execute.
- **Cross-platform browser automation**: Claude Chrome extension configured with approved domains.
- **Multi-agent context sync**: Claude can read GPT saved memories, Sider Wisebase, and update RileyFile + GitHub.

### 2026-02-14
- YouTube content planning, desktop capture setup, RileyFile organization

### Previous
- YouTube Video #1 script and production plan complete
- Armor App blueprint and data sets ready
- 13,890 Safari bookmarks imported
- iOS capture shortcut live
- Sider onboarded with Riley Context Hub Wisebase

---

*Maintained by Claude. Push to GitHub after each significant session.*

## Daily Context Sync Activity (Append-Only)

### 2026-02-23 02:29:01
- No new inbox files processed.

### 2026-02-23 03:28:06
- No new inbox files processed.

### 2026-02-23 05:32:44
- `inbox/codex/2026-02-23_041536_launchd_test.md`

### 2026-02-23 05:36:30
- `inbox/codex/2026-02-23_053526_launchd_test.md`
- `inbox/codex/2026-02-23_053629_launchd_test.md`

### 2026-02-23 05:53:07
- `inbox/codex/2026-02-23_055306_setforget_test.md`

### 2026-02-23 05:58:29
- `inbox/claude/2026-02-23_055811_workspace_sync.md`
- `inbox/codex/2026-02-23_055811_workspace_sync.md`
- `inbox/codex/2026-02-23_055829_workspace_sync.md`

### 2026-02-23 06:06:29
- `inbox/codex/2026-02-23_060623_workspace_sync.md`

### 2026-02-23 06:06:34
- `inbox/codex/2026-02-23_060634_workspace_sync.md`

### 2026-02-23 06:06:46
- `inbox/codex/2026-02-23_060646_workspace_sync.md`

### 2026-02-23 06:07:07
- `inbox/codex/2026-02-23_060706_workspace_sync.md`

### 2026-02-23 06:07:17
- `inbox/codex/2026-02-23_060717_workspace_sync.md`

### 2026-02-23 06:07:28
- `inbox/codex/2026-02-23_060728_workspace_sync.md`

### 2026-02-23 06:09:01
- `inbox/codex/2026-02-23_060842_workspace_sync.md`

### 2026-02-23 11:00:56
- `inbox/codex/2026-02-23_110056_workspace_sync.md`

### 2026-02-23 11:01:08
- `inbox/codex/2026-02-23_110108_workspace_sync.md`

### 2026-02-23 18:42:44
- `inbox/codex/2026-02-23_184244_workspace_sync.md`

### 2026-02-23 18:52:47
- `inbox/codex/2026-02-23_185247_workspace_sync.md`

### 2026-02-23 18:57:50
- `inbox/codex/2026-02-23_185750_workspace_sync.md`

### 2026-02-23 19:02:52
- `inbox/codex/2026-02-23_190252_workspace_sync.md`

### 2026-02-23 19:07:55
- `inbox/codex/2026-02-23_190755_workspace_sync.md`

### 2026-02-23 19:12:57
- `inbox/codex/2026-02-23_191257_workspace_sync.md`

### 2026-02-23 19:18:00
- `inbox/codex/2026-02-23_191800_workspace_sync.md`

### 2026-02-23 19:20:33
- `inbox/codex/2026-02-23_192033_workspace_sync.md`

### 2026-02-23 19:21:14
- `inbox/codex/2026-02-23_192114_workspace_sync.md`

### 2026-02-23 19:26:35
- `inbox/codex/2026-02-23_192635_workspace_sync.md`

### 2026-02-23 19:31:38
- `inbox/codex/2026-02-23_193138_workspace_sync.md`

### 2026-02-23 19:36:40
- `inbox/codex/2026-02-23_193640_workspace_sync.md`

### 2026-02-23 19:41:43
- `inbox/codex/2026-02-23_194142_workspace_sync.md`

### 2026-02-23 19:46:45
- `inbox/codex/2026-02-23_194645_workspace_sync.md`

### 2026-02-23 19:51:53
- `inbox/codex/2026-02-23_195153_workspace_sync.md`

### 2026-02-23 19:56:56
- `inbox/codex/2026-02-23_195656_workspace_sync.md`

### 2026-02-23 20:01:58
- `inbox/codex/2026-02-23_200158_workspace_sync.md`

### 2026-02-23 20:03:13
- `inbox/codex/2026-02-23_200313_workspace_sync.md`

### 2026-02-23 20:09:17
- `inbox/codex/2026-02-23_200917_workspace_sync.md`

### 2026-02-23 20:14:19
- `inbox/codex/2026-02-23_201419_workspace_sync.md`

### 2026-02-23 20:19:22
- `inbox/codex/2026-02-23_201922_workspace_sync.md`

### 2026-02-23 20:24:24
- `inbox/codex/2026-02-23_202424_workspace_sync.md`

### 2026-02-23 20:29:26
- `inbox/codex/2026-02-23_202926_workspace_sync.md`

### 2026-02-23 20:34:29
- `inbox/codex/2026-02-23_203429_workspace_sync.md`

### 2026-02-23 20:39:31
- `inbox/codex/2026-02-23_203931_workspace_sync.md`

### 2026-02-23 20:44:34
- `inbox/codex/2026-02-23_204434_workspace_sync.md`

### 2026-02-23 20:46:36
- `inbox/codex/2026-02-23_204636_workspace_sync.md`

### 2026-02-23 20:51:38
- `inbox/codex/2026-02-23_205138_workspace_sync.md`

### 2026-02-23 20:56:41
- `inbox/codex/2026-02-23_205641_workspace_sync.md`

### 2026-02-23 21:01:43
- `inbox/codex/2026-02-23_210143_workspace_sync.md`

### 2026-02-23 21:06:46
- `inbox/codex/2026-02-23_210645_workspace_sync.md`

### 2026-02-23 21:11:48
- `inbox/codex/2026-02-23_211148_workspace_sync.md`

### 2026-02-23 21:16:50
- `inbox/codex/2026-02-23_211650_workspace_sync.md`

### 2026-02-23 21:21:53
- `inbox/codex/2026-02-23_212153_workspace_sync.md`

### 2026-02-23 21:28:07
- `inbox/codex/2026-02-23_212807_workspace_sync.md`

### 2026-02-23 21:33:10
- `inbox/codex/2026-02-23_213310_workspace_sync.md`

### 2026-02-23 21:38:12
- `inbox/codex/2026-02-23_213812_workspace_sync.md`

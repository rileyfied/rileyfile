# RILEY_CONTEXT.md

## Unified AI Context File | Last Updated: 2026-02-20

> Source of truth for all AI tools working with Riley.
> Maintained by Claude (Lead AI Architect). Hosted at github.com/rileyfied/rileyfile.
> When Riley says “/context” or “/rf” — read this file and confirm “Context loaded ✓”

-----

## WHO IS RILEY

Entrepreneur, content creator, restaurant operations leader (Chick-fil-A). Building in the AI space full-time nights/weekends. “Multi-channel dumper” — captures ideas across texts, voice memos, screenshots, AI chats, playlists. Strong bias toward speed over organization at capture time; systematic organization happens later through AI assistance.

**Communication**: Direct, efficient. Task execution over conversation. No excessive formatting, praise, or filler. Hashtags over folders. Context over structure.

**Design eye**: Clean, minimal, non-generic. Discerning aesthetic sense. Gets distracted by formatting options — keep UI stripped down. Better Notes style: minimal UI, no formatting toolbars.

**What NOT to do**: Don’t over-format with bullets/indents. Don’t create complex folder hierarchies. Don’t add bells/whistles. Don’t assume — ask when context is ambiguous. Don’t give health/sleep/time-of-day advice. Don’t tell Riley to go to bed.

**Hardware**: iMac (3.2 GHz 8-Core Intel Xeon W, maxed at Sequoia 15.7.3), MacBook Air, iPhone 17 Pro Max, Apple Watch Ultra 3. All Apple ecosystem.

-----

## ACTIVE PROJECTS (Priority Order)

### 1. YouTube Channel — #youtube #video #ai #tutorial

AI tools for non-technical audiences. Target: frontline operational managers who don’t know what they’d use AI for. Teaching delegation to AI agents, not basic chatbot prompting. Market differentiation: agents vs chatbots, process/systems architecture over LLM chat threads.
**First video**: “You’re Using AI Wrong” — ready to film.
**Style refs**: Nate B. Jones, Fireship, Aleric Heck (shorts standard), Igor Pogany.
**Practice**: Camera presence training with read-aloud transcripts for self-critique (visual presence, vocal delivery, articulation/pauses).
**Status**: Video #1 ready to film. 90-day value capture priority.
**Path**: `RileyFile/RileyProjects/YOUTUBE CHANNEL`

### 2. Daily AI Audio Brief — #aibrief #audio #news

15-20 min solo-narration briefings on breaking AI news. NotebookLM-style delivery. Sources: The Rundown AI, Ben’s Bites, TechCrunch AI, VentureBeat, arXiv, X/Reddit, Hacker News.
**Naming convention**: `aiBrief_ThursFeb12` format (short day + month + date).
**Output**: Copy/paste-friendly block for NotebookLM ingestion.
**Status**: Ongoing production.
**Path**: `RileyFile/AI BRIEFS/`

### 3. Armor App — #armor #scripture #bible #fighterverses

Scripture memorization with gamified 5-mechanic ladder:

1. Word Bank — tap words from pool to assemble verse in order
1. Word Scramble — drag scrambled words into correct sequence
1. Type First Letter — type the first letter of each word
1. Type Full Word — type each word with first letter shown
1. Recite Out Loud — voice recording + self-grade

Each mechanic has L1-L5 levels. **Strict gating**: linear progression, cannot start Mechanic 2 until Mechanic 1 L5 passed. Levels linear within mechanic.
**Brand**: Deep red (#C41E3A) + white (#FFFFFF), accent blue (#3B82F6). Shield/armor theme.
**UI**: Hamburger menu (top-right), no bottom tab bar. 5-segment progress bar per mechanic family. Active Verse card: Eyebrow (Week X - Reference), Verse text, Footer reference.
**Data**: Fighter Verses Sets A-E ready (ArmorApp_SetReferenceTable.csv). Pop quizzes for spaced repetition.
**Full IA blueprint**: `Armour_GPT_InfoArchBlueprint_v1.rtf` — frozen wireframe spec.
**Status**: Blueprint complete, development paused pending YouTube launch.
**Path**: iCloud Drive/ARMOR APP/

### 4. Skills & Drills App — #skillsdrills #training #managers #education

Education/learning platform for managers and operators. Skills and drills creation, distribution, and tracking tool.
**Drill types**: Multiple choice, fill-in-blank, true/false, timed rounds, scenario-based, photo/video-based, sequencing.
**Distribution**: Text invites, QR codes, share links, manual entry.
**Analytics**: Individual scores, team leaderboards, completion rates, weak areas, exportable reports. Drill template sharing between managers.
**Design**: System-preference appearance, bottom tab bar (Instagram/Spotify style), clean minimalism + warm approachability.
**Status**: Early specification phase. Blueprint questionnaire in progress.

### 5. HarmonyHelper — #harmony #piano #music #chords

Piano practice and music learning app.
**Status**: Active development, paused for YouTube priority.
**Path**: Desktop/HarmonyApp

### 6. AI Operations Monitor — #monitor #aiops #dashboard

iPhone widget + Mac app combo. Watches Claude.ai, Sider, ChatGPT, Gemini usage. Monitor → flag → suggest → execute on approval. Tracks token/credit banks. Eventually orchestrates which AI does what automatically. Terminal activity = Claude-initiated via Cowork.
**Status**: Design spec complete, next build after YouTube.

### 7. Command Center Dashboard — #dashboard #commandcenter

Productivity dashboard with live AI news feeds, project status, Claude suggestions. Auto-refreshes every 5 minutes. Deployed and functional.
**News sources**: The Rundown AI, Ben’s Bites, TechCrunch, VentureBeat, arXiv, X, Reddit, Hacker News.
**Status**: Deployed, functional. Maintenance mode.

### 8. Virtual Restaurant Manager — #virtualman #visor #cfa

AI knowledge base for restaurant operations. Every person who knows anything at a restaurant, available on a “zoom call” waiting for questions. 3-year idea. Addresses the reality of manager chaos (callouts, broken equipment, training gaps, vendor issues) with an AI that holds all institutional knowledge.
**Status**: Concept/idea stage.

### 9. ESV Lookup — #esv #bible #tool

PWA with dark mode, reference search, word search. Live at rileyfied.github.io/esv-lookup/.
**Status**: Shipped. Maintenance only.

-----

## RIILEYFILE SYSTEM (Infrastructure)

### Folder Structure

```
iCloud Drive/RileyFile/
├── RILEY_CONTEXT.md      ← This file (source of truth)
├── config.json           ← Machine-readable project config
├── INDEX.md              ← Quick reference index
├── RileyShare/           ← Default landing zone
│   └── captures/         ← iOS shortcut captures, URLs, bookmarks
├── RileyNotes/           ← Notes with #hashtags
├── RileyProjects/        ← Active project folders
│   ├── ARMOR APP/
│   ├── YOUTUBE CHANNEL/
│   ├── DASHBOARD APP/
│   ├── CFA TRAINING/
│   └── RILEY API/
├── RileyAgents/          ← AI memory archives
│   ├── CLAUDE MEMORY ARCHIVE/
│   ├── ChatGPT MEMORY ARCHIVE/
│   └── BROWSER BOOKMARKS/
├── AI BRIEFS/            ← Daily AI content production
│   ├── AUDIO OVERVIEWS/
│   └── DESCRIPT/
├── app/                  ← RileyNotes web app (index.html)
├── setup/                ← Shortcut setup guide
└── scripts/              ← Automation scripts
```

### File Routing Rules

- Files with #hashtags → RileyNotes
- Files matching project keywords → RileyProjects/{project}
- Untagged files → RileyShare (Claude organizes later)
- Notes from capture app → RileyNotes with auto-generated hashtags

### Capture Methods

- **RileyNotes app**: Manual typing, view all notes (PWA on home screen)
- **Share Sheet shortcut**: Share from any iOS app → one tap save
- **Back Tap**: Double-tap phone back = clipboard saved
- **Voice**: Home screen icon → dictate → saved
- **macOS automation**: Codex-based capture testing in progress
- All captures save to `RileyFile/RileyShare/captures/`

-----

## AI TEAM & COLLABORATION

### Claude — Lead AI Architect

**Interface**: Claude.ai (project-based), Cowork (file ops, terminal)
**Role**: System architecture, file operations, code, builds, RileyFile maintenance
**Terminal**: All terminal activity is Claude-initiated via Cowork. Riley doesn’t use terminal directly.

### Sider — Multi-Model Hub

**Interface**: Browser extension + sider.ai web
**Subscription**: Plus (resets monthly)
**Models**: GPT-5.2, Gemini 3 Pro, Claude Sonnet 4.5, Grok 4, DeepSeek v3.2 (all unlimited). Elite credits for Deep Research, Scholar Research, Web Creator, AI Slides.
**Knowledge**: “Riley Context Hub” Wisebase with RILEY_CONTEXT note + ARMOR_APP_SPEC note. Wisebase Instructions set.
**Use for**: Browser-based tasks, quick queries, web research, model comparison, PDF analysis.

### ChatGPT — Ideation Partner

**Interface**: ChatGPT web/app (Plus subscription)
**Role**: Brainstorming, long-form content, alternative perspectives
**Context sync**: Reads RILEY_CONTEXT.md from GitHub URL on /context command.

### Gemini — Google Integration

**Interface**: Gemini web/app, AI Studio
**Role**: Google ecosystem, search, research
**Context sync**: Reads RILEY_CONTEXT.md from GitHub URL on /context command.

### Context Sync Protocol

1. Claude maintains RILEY_CONTEXT.md as live source of truth
1. GitHub hosts the web-readable version at raw.githubusercontent.com URL
1. Sider: Wisebase notes (manual update when context changes significantly)
1. ChatGPT/Gemini: Paste GitHub URL at session start → they read it
1. Claude → Claude: Memory persists across project chats; Cowork reads live files

-----

## HASHTAG STRATEGY

Active tags: #youtube #videoidea #ai #strategy #armor #scripture #fighterverses #cfa #training #rileyfile #aibrief #conductor #skillsdrills #harmony #piano #monitor #dashboard #virtualman #build #tool #idea #RileyWrite #textfx #twitter #post #article #blog

-----

## KEY DECISIONS & LESSONS

- **YouTube is the priority**. Ship content to external audiences. Stop building tools to build tools.
- **Market shift**: Conversational AI → autonomous agents that execute tasks. Teach delegation, not prompting.
- **Minimal > feature-rich**. Speed > perfection. Context > structure. Cross-platform required.
- **Build for external audiences** — YouTube is the vehicle to reach people before launching apps.
- **OpenClaw**: Nuked 2026-02-15. API keys rotated. ClaudeAPI_v6 active at console.anthropic.com, not currently used anywhere.
- **API security**: Key in .zshrc was exposed and removed 2026-02-15. Both .zshrc and .openclaw/.env keys compromised and deleted.

-----

## GITHUB

**Username**: rileyfied
**Login**: via Apple (email: rileygcolley@icloud.com, private relay: 4m9h2htxjs@privaterelay.appleid.com)
**Repos**:

- `rileyfied/rileyfile` — RileyFile context system
- `rileyfied.github.io/esv-lookup/` — ESV Lookup PWA (live)

-----

*Maintained by Claude (Lead AI Architect) | github.com/rileyfied/rileyfile**Maintained by Claude. Updated 2026-02-16.*

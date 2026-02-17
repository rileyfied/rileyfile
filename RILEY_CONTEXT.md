# RILEY_CONTEXT.md
## Last Updated: 2026-02-16

> **Purpose**: Source of truth for Riley's projects, preferences, and active work. Read by Claude (lead architect) and available to any AI tool Riley uses.

---

## WHO IS RILEY# RILEY_CONTEXT.md

## Unified AI Context File | Last Updated: 2026-02-17

> This file is the source of truth for all AI tools working with Riley.
> Maintained by Claude (Lead AI Architect). Hosted at github.com/rileyfied/rileyfile.
> When Riley says “/context” — read this file and confirm with “Context loaded ✓”

-----

## WHO IS RILEY

Entrepreneur, content creator, restaurant operations leader (Chick-fil-A). Building in the AI space while working full-time. “Multi-channel dumper” — captures ideas across texts, voice memos, screenshots, AI chats, playlists. Strong bias toward speed over organization at capture time.

**Communication**: Direct, efficient. No excessive formatting. Hashtags over folders. Context over structure. Show don’t tell.

**Design eye**: Clean, minimal, non-generic. Gets distracted by formatting options — keep UI stripped down.

**What NOT to do**: Don’t over-format. Don’t create complex folder hierarchies. Don’t add bells/whistles to tools. Don’t assume — ask when context is ambiguous. Don’t give health/sleep advice.

-----

## ACTIVE PROJECTS (Priority Order)

**1. YouTube Channel** — #youtube #video #ai #tutorial
AI tools for non-technical audiences. First video: “You’re Using AI Wrong.” Target: frontline operational managers, not enterprise knowledge workers. Teaching delegation to AI agents, not basic chatbot prompting. Style refs: Nate B. Jones, Fireship, Igor Pogany.
Status: Video #1 ready to film.
Resources: `RileyFile/RileyProjects/YOUTUBE CHANNEL`

**2. Daily AI Audio Brief** — #aibrief #audio #news
15-20 min solo-narration briefings on breaking AI news. Sources: The Rundown AI, Ben’s Bites, TechCrunch AI, arXiv, X/Reddit. Spotlight triggers: major AI figures, viral posts.
Status: Ongoing production.

**3. Armor App** — #armor #scripture #bible #fighterverses
Scripture memorization with gamified 5-mechanic ladder: Word Bank → Word Scramble → Type 1st Letter → Type Full Word → Recite Out Loud. Each mechanic has L1-L5 levels with strict gating (linear progression). Fighter Verses data sets A-E ready. Full IA blueprint exists. Brand: deep red (#C41E3A) + white, shield/armor theme. Hamburger menu nav, no bottom tab bar.
Status: Blueprint ready, development paused.
Resources: `RileyFile/RileyProjects/ARMOR APP`

**4. HarmonyHelper** — #harmony #piano #music #chords
Piano practice and music learning app. Python backend, web frontend.
Status: Active development.
Resources: `/Desktop/HarmonyApp/`

**5. AI Operations Monitor** — #conductor #monitor #agents
Local agent that watches AI processes on machine, reports costs, flags waste, eventually orchestrates which AI does what. Vision: non-technical conductor for AI workflows. iPhone widget + Mac app, PWA prototype first.
Status: Design phase (NEXT BUILD).

**6. Dashboard App (RileyHQ)** — #dashboard #productivity
Command center for all projects. Zero manual maintenance, proactive insights. Auto-refreshes, fetches live AI news, reads project status from JSON.
Status: Design discovery phase.

-----

## RILEYFILE STRUCTURE

```
RileyFile/                        (iCloud Drive)
├── RILEY_CONTEXT.md              ← This file (synced to GitHub)
├── MEMORY.md                     ← Curated long-term context
├── INDEX.md                      ← Navigation guide
├── config.json                   ← Project definitions, routing rules
├── RileyShare/                   ← Default landing zone for all files
│   └── captures/                 ← iOS Shortcut captures, bookmarks
├── RileyNotes/                   ← Notes with #hashtags
├── RileyProjects/                ← Active project folders
│   ├── ARMOR APP/
│   ├── YOUTUBE CHANNEL/
│   ├── DASHBOARD APP/
│   ├── CFA TRAINING/
│   └── RILEY API/
├── RileyAgents/                  ← AI memory archives
│   ├── CLAUDE MEMORY ARCHIVE/
│   ├── ChatGPT MEMORY ARCHIVE/
│   └── GROK MEMORY ARCHIVE/
├── AI BRIEFS/                    ← Daily audio brief production
│   ├── AUDIO OVERVIEWS/
│   └── DESCRIPT/
├── app/                          ← RileyNotes PWA
└── scripts/                      ← Automation scripts
```

**File routing**: Unsaved files → RileyShare. Files with #hashtags → RileyNotes. Files matching project keywords → RileyProjects/{project}.

-----

## DESIGN THINKING (Apply to Every Build)

1. **Empathize**: Fast/messy capture is intentional. Organization should be invisible.
1. **Define**: What friction is this solving? Ask before building.
1. **Ideate**: Present options, not just solutions. Match minimal aesthetic. Consider cross-platform (iPhone, iPad, Mac).
1. **Prototype**: Functional over beautiful. Artifacts/demos over documentation.
1. **Test**: Real usage reveals true needs. Watch for “this is close but…” feedback. Adjust fast, don’t defend design decisions.

-----

## DECISION PRINCIPLES

1. Minimal > Feature-rich
1. Speed > Perfection
1. Context > Structure
1. Cross-platform > Single-platform
1. Invisible organization (auto-tag, auto-categorize, don’t ask user)

-----

## AI TEAM

**Claude** = Lead Architect. Maintains context files, builds apps, manages RileyFile system. All terminal/file ops go through Claude via Cowork. Updates this file and pushes to GitHub.

**ChatGPT** = Brainstorming, ideation, long-form content, alternative perspectives.

**Gemini** = Google ecosystem integration, search, research, NotebookLM audio overviews.

**Sider** = Multi-Model Hub. Browser sidebar queries, web research, PDF analysis, model comparison. Has Wisebase with project context (“Riley Context Hub” collection). Plus subscription (resets monthly). Access to Claude Sonnet 4.5, GPT-5.2, Gemini 3 Pro, Grok 4, DeepSeek.

### Context Sync Protocol

- iCloud Drive copy is primary source of truth
- GitHub repo (github.com/rileyfied/rileyfile) hosts the public sync copy
- When Riley says `/context`, `/rf`, `/sync`, or `/RileyFile` → agents read from GitHub raw URL
- Claude pushes updates to GitHub whenever iCloud copy changes
- Raw URL: `https://raw.githubusercontent.com/rileyfied/rileyfile/main/RILEY_CONTEXT.md`

-----

## HASHTAG STRATEGY

Active tags: #youtube #videoidea #ai #strategy #armor #scripture #cfa #training #rileyfile #aibrief #conductor #harmony #dashboard

-----

## KEY INTERESTS & MISSION

- Democratize AI for non-technical audiences
- Pioneer tools for frontline operational managers (embodied work, real-time problem-solving)
- Transition people from “LLM chat thread” mode → “process and systems architecture” mode
- Psychology of human-AI interaction
- Streamline middle-management duties with AI
- Music production (Suno for demos), piano learning

-----

## LESSONS LEARNED

- OpenClaw consumed tokens overnight with no monitoring. Local agents need spending limits, single-model configs, and monitoring before deployment. (2026-02-15)
- API keys should never be hardcoded in shell configs. ClaudeAPI_v6 is current key (console.anthropic.com). (2026-02-15)
- Agent personality files (SOUL.md etc.) add overhead without clear ROI. (2026-02-15)
- Build the monitor BEFORE deploying more agents. (2026-02-15)
- Context Hub/RileyFile is infrastructure, not a product. Ship value to external audiences. YouTube is the priority. (2026-02-01)
- Sider Wisebase needs actual file/note content, not just instructions, to reference project specs. (2026-01-27)

-----

## SYSTEM & HARDWARE

- Apple ecosystem: iMac (Intel Xeon, Sequoia 15.7.3 max), MacBook Air, iPhone 17 Pro Max, Apple Watch Ultra 3
- iMac won’t update past Sequoia 15.7.3 (not Apple Silicon)
- All other devices on latest OS
- GitHub: rileyfied (Apple login)
- Live tools: rileyfied.github.io/esv-lookup/ (ESV Bible PWA)

-----

## CURRENT PRIORITIES (Feb 2026)

1. YouTube Channel — Video #1 ready to film
1. Daily AI Brief — Ongoing production
1. AI Operations Monitor — Design phase (next build)
1. Armor App — Blueprint ready, development paused

-----

*Last updated: 2026-02-17*

Entrepreneur, content creator, restaurant operations leader (Chick-fil-A). Building in the AI space while working full-time. "Multi-channel dumper" — captures ideas across texts, voice memos, screenshots, AI chats, playlists. Strong bias toward speed over organization at capture time.

**Communication**: Direct, efficient. No excessive formatting. Hashtags over folders. Context over structure. Show don't tell.

**Design eye**: Clean, minimal, non-generic. Gets distracted by formatting options — keep UI stripped down.

**Hardware**: iMac Pro 2018 (3.2 GHz 8-Core Intel Xeon W, 64GB RAM — maxes at Sequoia 15.7.3), MacBook Air (Apple Silicon, latest macOS), iPhone 17 Pro Max, Apple Watch Ultra 3. All non-iMac devices on latest OS.

---

## ACTIVE PROJECTS (Priority Order)

**1. YouTube Channel** — #youtube #video #ai #tutorial
AI tools for non-technical audiences. First video: "You're Using AI Wrong." Target: frontline operational managers, not enterprise knowledge workers. Style refs: Nate B. Jones, Fireship, Igor Pogany.
Resources: `RileyFile/RileyProjects/YOUTUBE CHANNEL`

**2. Daily AI Audio Brief** — #aibrief #audio #news
15-20 min solo-narration briefings on breaking AI news. Sources: The Rundown AI, Ben's Bites, TechCrunch AI, arXiv, X/Reddit.

**3. Armor App** — #armor #scripture #bible #fighterverses
Scripture memorization with gamified 5-mechanic ladder (Word Bank → Word Scramble → Type 1st Letter → Type Full Word → Recite). Fighter Verses data sets A-E ready. Full blueprint exists.
Resources: `RileyFile/RileyProjects/ARMOR APP`

**4. HarmonyHelper** — #harmony #piano #music #chords
Piano practice app. Python backend, web frontend.
Resources: `/Desktop/HarmonyApp/`

**5. AI Operations Monitor** — #conductor #monitor #agents (NEXT BUILD)
Local agent that watches AI processes on machine, reports costs, flags waste, eventually orchestrates which AI does what. Vision: non-technical conductor for AI workflows. Related: ChatGPT "CONTEXT APP" project exploring conductor/concierge agent orchestration.

**6. Dashboard App (RileyHQ)** — #dashboard #productivity
Command center for all projects. Zero manual maintenance. Design discovery phase.

---

## RILEYDOMAIN STRUCTURE

```
RileyFile/
├── RILEY_CONTEXT.md      ← This file
├── MEMORY.md             ← Curated long-term context
├── INDEX.md              ← Navigation guide
├── config.json           ← Project definitions
├── RileyShare/           ← Default landing zone for all files
│   └── captures/         ← iOS Shortcut captures, bookmarks
├── RileyNotes/           ← Notes with #hashtags
├── RileyProjects/        ← Active project folders
│   ├── ARMOR APP/
│   ├── YOUTUBE CHANNEL/
│   ├── DASHBOARD APP/
│   ├── CFA TRAINING/
│   └── RILEY API/
├── RileyAgents/          ← AI memory archives
├── AI BRIEFS/            ← Daily audio brief production
├── app/                  ← RileyNotes PWA
└── scripts/              ← Automation scripts
```

---

## AI TOOLS IN USE

**Claude** (Lead Architect): Claude.ai + Cowork (file ops, terminal commands, builds). Terminal activity is Claude-initiated. Browser automation via Chrome extension — approved domains: github.com, youtube.com, google.com, notion.com, icloud.com, suno.com, chatgpt.com, sider.ai, claude.ai. Can navigate to other AI tools, read their memory/context, and sync back.
**Sider** (Multi-Model Hub): Browser extension (Plus sub). Quick queries, web research, deep research, model comparison, PDF analysis. Wisebase has Riley Context Hub loaded.
**ChatGPT** (Plus): Brainstorming, ideation, long-form content, daily AI briefs. 80+ saved memories. Custom GPTs: Visual Guides, Question Crafter, Head of AI Development, Whimsical Diagrams. CONTEXT APP project active. /sync command triggers context pull.
**Gemini**: Google ecosystem, search, research.

**Sync Protocol**: All AI tools read RILEY_CONTEXT.md from this GitHub repo:
- **Repo**: `https://github.com/rileyfied/rileyfile`
- **Raw URL**: `https://raw.githubusercontent.com/rileyfied/rileyfile/main/RILEY_CONTEXT.md`
- Claude reads GPT memory + Sider Wisebase via browser, updates RileyFile, pushes to GitHub repo.
- All AI tools reference projects by #hashtag.
- ⚠️ **Note**: Previous references to "GitHub gist" were incorrect — this is a GitHub **repo**, not a gist. Update any saved /context commands in ChatGPT/Gemini to use the raw URL above.

**GitHub**: username rileyfied. Login: Sign in with Apple. Email: rileygcolley@icloud.com (HideMyEmail relay: 4m9h2htxjs@privaterelay.appleid.com).

---

## DESIGN THINKING (Apply to Every Build)

1. **Empathize**: Fast/messy capture is intentional. Organization should be invisible.
2. **Define**: What friction is this solving? Ask before building.
3. **Ideate**: Present options, not just solutions. Match minimal aesthetic.
4. **Prototype**: Functional first. Artifacts over documentation.
5. **Test**: Watch for "close but..." feedback. Adjust fast, don't defend.

## DECISION PRINCIPLES

Minimal > Feature-rich. Speed > Perfection. Context > Structure. Cross-platform required. Auto-organize, don't ask the user.

---

## ACTIVITY LOG

### 2026-02-16
- **GPT sync**: Scanned ChatGPT threads — no new project-critical updates since 02-15. GPT had already self-synced earlier today. Confirmed custom GPTs: Visual Guides, Question Crafter, Head of AI Development, Video AI by invideo, Whimsical Diagrams. CONTEXT APP project active with conductor/concierge agent threads.
- **404 fix**: Corrected sync protocol — was referencing "GitHub gist" but file lives in GitHub repo (`rileyfied/rileyfile`). Updated all references to correct raw URL. Any cached gist URLs in ChatGPT/Gemini /context commands need manual update.
- **Hardware added**: Device inventory added to WHO IS RILEY section.
- **config.json**: Verified — no stale gist references. Paths and project definitions current.

### 2026-02-15
- **Boil Out**: Nuked OpenClaw (config, binary, credentials, completions). Removed Codex. Stripped agent personality files from RileyFile. Cleaned exposed API keys from .zshrc. Clean slate.
- **AI Operations Monitor spec complete**: Tracks spend on Claude.ai, Sider, ChatGPT, Gemini. iPhone widget + Mac app. Phased: Monitor → Flag → Execute. PWA prototype first, native if it sticks. Budget: $20+/mo if it delivers.
- **Key decisions**: Focus on credit/token bank tracking (not flat-rate subs). No terminal tools day-to-day. Monitor before automate.
- **Cross-platform browser automation**: Claude Chrome extension configured with approved domains. Can SSO via Apple passkey. Tested on GitHub (logged in as rileyfied), ChatGPT, Sider, YouTube, Google, Notion, iCloud, Suno.
- **Multi-agent context sync**: Claude can now read GPT saved memories (80+), Sider Wisebase, and update RileyFile + GitHub repo to keep all agents in sync.
- **Pending**: Rotate Anthropic API key at console.anthropic.com (2 keys exposed, removed from machine).

### 2026-02-14
- YouTube content planning, desktop capture setup, RileyFile organization (by OpenClaw — now removed)

### Previous
- YouTube Video #1 script and production plan complete
- Armor App blueprint and data sets ready
- 13,890 Safari bookmarks imported
- iOS capture shortcut live

---

*Maintained by Claude. Updated 2026-02-16.*

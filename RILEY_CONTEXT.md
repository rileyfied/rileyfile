# RILEY_CONTEXT.md
## Last Updated: 2026-02-15

> **Purpose**: Source of truth for Riley's projects, preferences, and active work. Read by Claude (lead architect) and available to any AI tool Riley uses.

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
15-20 min solo-narration briefings on breaking AI news. Sources: The Rundown AI, Ben's Bites, TechCrunch AI, arXiv, X/Reddit.

**3. Armor App** — #armor #scripture #bible #fighterverses
Scripture memorization with gamified 5-mechanic ladder (Word Bank → Word Scramble → Type 1st Letter → Type Full Word → Recite). Fighter Verses data sets A-E ready. Full blueprint exists.
Resources: `RileyFile/RileyProjects/ARMOR APP`

**4. HarmonyHelper** — #harmony #piano #music #chords
Piano practice app. Python backend, web frontend.
Resources: `/Desktop/HarmonyApp/`

**5. AI Operations Monitor** — #conductor #monitor #agents (NEXT BUILD)
Local agent that watches AI processes on machine, reports costs, flags waste, eventually orchestrates which AI does what. Vision: non-technical conductor for AI workflows.

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
**ChatGPT**: Brainstorming, ideation, long-form content, daily AI briefs. 80+ saved memories. /context command reads GitHub gist.
**Gemini**: Google ecosystem, search, research. /context command reads GitHub gist.

**Sync Protocol**: Claude reads GPT memory + Sider Wisebase via browser, updates RileyFile, pushes to GitHub gist. All AI tools reference projects by #hashtag.
**GitHub**: username rileyfied. Login: Sign in with Apple.

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

### 2026-02-15
- **Boil Out**: Nuked OpenClaw (config, binary, credentials, completions). Removed Codex. Stripped agent personality files from RileyFile. Cleaned exposed API keys from .zshrc. Clean slate.
- **AI Operations Monitor spec complete**: Tracks spend on Claude.ai, Sider, ChatGPT, Gemini. iPhone widget + Mac app. Phased: Monitor → Flag → Execute. PWA prototype first, native if it sticks. Budget: $20+/mo if it delivers.
- **Key decisions**: Focus on credit/token bank tracking (not flat-rate subs). No terminal tools day-to-day. Monitor before automate.
- **Cross-platform browser automation**: Claude Chrome extension configured with approved domains. Can SSO via Apple passkey. Tested on GitHub (logged in as rileyfied), ChatGPT, Sider, YouTube, Google, Notion, iCloud, Suno.
- **Multi-agent context sync**: Claude can now read GPT saved memories (80+), Sider Wisebase, and update RileyFile + GitHub gist to keep all agents in sync.
- **Pending**: Rotate Anthropic API key at console.anthropic.com (2 keys exposed, removed from machine).

### 2026-02-14
- YouTube content planning, desktop capture setup, RileyFile organization (by OpenClaw — now removed)

### Previous
- YouTube Video #1 script and production plan complete
- Armor App blueprint and data sets ready
- 13,890 Safari bookmarks imported
- iOS capture shortcut live

---

*Maintained by Claude. Updated 2026-02-15.*

# Context Sync Setup Guide
## How to enable "/context" across all your AI tools

---

## CHATGPT SETUP

### Custom Instructions → "What would you like ChatGPT to know about you?"

Paste this (edit the URL once you have it):

```
My name is Riley. I'm an entrepreneur building AI tools while working in restaurant ops (Chick-fil-A).

My AI context file with all active projects, preferences, and current status is hosted at:
https://gist.githubusercontent.com/rileyfied/b744e220ea6ca51be7af2e1666b5cef4/raw/RILEY_CONTEXT_SYNC.md

RULES:
- When I say "/context" or "context" — fetch that URL and use it as background. Confirm with "Context loaded ✓"
- When I say "/status" — fetch the URL and tell me the latest status section
- When I say "/projects" — fetch the URL and list my active projects
- Always apply the response rules and design principles from the context file
- Reference my projects by their #hashtags
```

### Custom Instructions → "How would you like ChatGPT to respond?"

```
Direct and efficient. No excessive formatting, bullets, or hierarchy. Task execution over conversation. Present options with tradeoffs when building. Minimal > Feature-rich. Don't add UI bells/whistles. Ask clarifying questions only when blocking. When building something for a project, check if a spec/blueprint exists before generating generic code.
```

---

## GEMINI SETUP

### Settings → Instructions for Gemini (free) or Personal Context (paid)

Paste this:

```
My name is Riley. Entrepreneur building AI tools + restaurant ops leader.

My full AI context file (projects, preferences, status) is at:
https://gist.githubusercontent.com/rileyfied/b744e220ea6ca51be7af2e1666b5cef4/raw/RILEY_CONTEXT_SYNC.md

When I say "/context" — read that URL and confirm "Context loaded ✓"
When I say "/status" — read URL, show latest status
When I say "/projects" — read URL, list active projects

Response style: Direct, efficient. No excessive formatting. Minimal > Feature-rich. Task execution over conversation. Reference my projects by #hashtags.
```

---

## SIDER SETUP

Sider can't fetch URLs. I (Claude) will update Sider's Wisebase notes whenever RILEY_CONTEXT changes during our sessions. No action needed from you.

---

## CLAUDE SETUP

Already done. Claude reads RileyFile live via Cowork + project attachments. Zero friction.

---

## SLASH COMMANDS (work in GPT & Gemini after setup)

| Command | What it does |
|---------|-------------|
| /context | Fetches your context file, loads it into the conversation |
| /status | Shows latest activity log / current state |
| /projects | Lists active projects with hashtags and status |

---

## GIST STATUS: ✅ LIVE

Gist URL: https://gist.github.com/rileyfied/b744e220ea6ca51be7af2e1666b5cef4
Raw URL: https://gist.githubusercontent.com/rileyfied/b744e220ea6ca51be7af2e1666b5cef4/raw/RILEY_CONTEXT_SYNC.md

Claude pushes updates via `RileyFile/scripts/sync_context_gist.sh`

---

## MAINTAINING THE SYNC

Claude updates `RILEY_CONTEXT.md` (the master) during sessions.
When it changes significantly, Claude also updates `RILEY_CONTEXT_SYNC.md` (the external copy).
You re-upload to the Gist when you want external tools to see changes.

FUTURE: The AI Operations Monitor (Phase 3) could automate this push.

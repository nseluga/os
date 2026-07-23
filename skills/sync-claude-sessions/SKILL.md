---
name: sync-claude-sessions
description: Review recent Claude Code chat histories and sync any learnings into memory files. Use when the user says "/sync-claude-sessions", "sync my sessions", "update memory from recent chats", "what did I learn recently", or "sync memory from sessions".
---

# Sync Claude Sessions

Scan recent chat histories, extract learnings worth persisting, and propose memory file writes. Interactive — proposes each change before writing.

## When to use

- Trigger phrases: "sync my sessions", "sync claude sessions", "update memory from recent chats", "what did I learn recently", "sync memory"
- Situations: after a productive week of sessions, after a multi-day project sprint, periodically as memory hygiene
- Do NOT use when: the user only wants to review sessions without changing memory, or when they say "just show me" without wanting writes

## What it does

Reads recent chat histories from `~/.claude/chat-histories/`, extracts signal (corrections, confirmations, patterns, preferences, project context), deduplicates against existing memory files, and proposes concrete memory file writes for the user to approve one by one.

## Steps

### 1 — Determine the scan window

Check `$ARGUMENTS` for a date range or count, e.g.:
- `7d` → last 7 days (default if no arg)
- `30d` → last 30 days
- `N` (plain number) → last N sessions
- `YYYY-MM-DD` → sessions since that date

Default: last 7 days.

### 2 — Find and list matching histories

```bash
ls -lt ~/.claude/chat-histories/
```

Filter to files whose filename date falls within the scan window. Show the user a one-line count: "Found N sessions from <date range>." If zero, stop and say so.

### 3 — Read existing memory index

Read `~/os/knowledge/memory/MEMORY.md` to load the current index. This prevents proposing duplicates.

### 4 — Extract learnings from sessions

For each history file (batch reads in parallel where possible):

Read the file and extract signal in these categories:

| Category | What to look for |
|----------|-----------------|
| **Corrections** | User said "no", "don't", "stop doing X", "that's wrong" — what was wrong and what the right behavior is |
| **Confirmations** | User said "yes exactly", "perfect", "keep doing that", accepted an unusual choice without pushback |
| **Preferences** | Stated preferences about output style, tooling, workflow, naming conventions |
| **Project facts** | New project context, milestones, direction changes, deadlines, motivations |
| **References** | External systems, dashboards, repos, Slack channels, Linear projects mentioned |
| **User profile** | New role info, skills, goals, constraints Nate mentioned about himself |

Skip: code patterns, file paths, git history, debugging recipes, ephemeral task state, things already covered by an existing MEMORY.md entry.

### 5 — Deduplicate against existing memory

For each candidate learning, check whether it's already captured in an existing memory file (by checking MEMORY.md index entries and, when in doubt, reading the linked file). Discard exact duplicates. Keep refinements or contradictions — those are updates, not duplicates.

### 6 — Propose changes interactively

Present a summary: "Found X learnings across N sessions. Here's what I'd write:"

For each proposed change, show:
```
[N/total] TYPE: <category>
File: ~/os/knowledge/memory/<filename>.md  (NEW | UPDATE existing)
---
<full proposed file content or diff for updates>
---
Write this? (yes / skip / stop)
```

- `yes` → write the file and update MEMORY.md index
- `skip` → discard and move to next
- `stop` → stop proposing, summarize what was written

### 7 — Write approved changes

For each approved memory:
1. Write the file to `~/os/knowledge/memory/<slug>.md` with correct frontmatter
2. Add or update the line in `MEMORY.md` index

After all writes, print: "Wrote N memory files. Skipped M. MEMORY.md updated."

## Memory file format

```markdown
---
name: <short-kebab-case-slug>
description: <one-line summary — used to decide relevance in future conversations>
metadata:
  type: <user | feedback | project | reference>
---

<memory body>

For feedback/project types:
**Why:** <reason the user gave>
**How to apply:** <when this guidance kicks in>
```

## Inputs / arguments

- `$ARGUMENTS` — optional scan window: `7d` (default), `30d`, `N` (session count), or `YYYY-MM-DD` (since date)

## Examples

- Input: `/sync-claude-sessions` → scans last 7 days, proposes memory writes interactively
- Input: `/sync-claude-sessions 30d` → scans last 30 days
- Input: `/sync-claude-sessions 2026-07-01` → scans all sessions since July 1

## Notes & gotchas

- Chat histories are in `~/.claude/chat-histories/` — filenames encode date, project, and session ID
- History files include skill invocations (raw SKILL.md content injected as user messages) — these are not user speech; don't treat skill instructions as user preferences
- `<local-command-caveat>` blocks are tool noise, not user feedback — skip them
- `<command-message>` and `<command-name>` blocks are slash command invocations — only the follow-up conversation matters
- Don't write memory for things already in CLAUDE.md (global config) or obvious from the codebase
- For updates to existing files: read the existing file first, then propose the merged/refined version
- If a session is very long (>50KB), skim the user turns only — assistant turns are rarely the source of new facts about Nate

# OS — Personal Operating System

A single home for knowledge, skills, and projects. Built on top of Claude Code: **36 custom skills**, a structured project-tracking system covering **12 active projects**, and a persistent memory layer with **18 fact files** auto-injected into every session.

The system compounds — each skill added makes the next session more capable, and the memory layer means Claude Code never starts cold. All AI-assisted work on [nateseluga.com](https://nateseluga.com) was built with this as infrastructure.

This is a public repository. Everything personal to Nate — `knowledge/me/`,
`knowledge/audience/`, `knowledge/library/`, and `projects/` — is gitignored;
what's shared is the system itself (skills, frameworks, structure). See
[Setting This Up For Yourself](#setting-this-up-for-yourself) to run your own
copy.

---

## Setting This Up For Yourself

This repo is designed to be forked: you get Nate's skills and frameworks, you
fill in your own facts, and you can keep pulling his improvements later.

1. **Fork it on GitHub, then clone your fork as `~/os`** (matching the path
   keeps `CLAUDE.md`'s references valid without edits — clone elsewhere and
   you'll need to update those paths):
   ```
   git clone https://github.com/<you>/os.git ~/os
   ```

2. **Symlink it into Claude Code:**
   ```
   ln -s ~/os/CLAUDE.md ~/.claude/CLAUDE.md
   ln -s ~/os/skills ~/.claude/skills
   ln -s ~/os/knowledge/memory ~/.claude/memory
   ```
   Health check: `ls -L ~/.claude/skills/grill-me` should resolve.

3. **Fill in your own personal folders.** `knowledge/me/`, `knowledge/audience/`,
   `knowledge/library/`, and `projects/` are gitignored (see `.gitignore`) —
   your fork starts with just the folder structure plus two generic templates
   (`projects/_TEMPLATE.md`, `knowledge/library/GUIDE.md`). Add your own
   `background.md`/`goals.md` under `me/`, persona notes under `audience/`,
   reference docs under `library/`, and one `README.md` per real project under
   `projects/` (copy `_TEMPLATE.md`). None of it gets pushed — see
   [What's in Each Section](#whats-in-each-section) for what each folder is for.

4. **Stay in sync with upstream.** Since your personal content lives in
   gitignored folders, merging Nate's updates won't conflict with your own data:
   ```
   git remote add upstream https://github.com/nseluga/os.git
   git fetch upstream
   git merge upstream/main
   ```

---

## Structure

```
os/
├── CLAUDE.md              # Developer instructions for Claude Code integration
├── knowledge/             # Organized facts and reference materials
│   ├── me/                # Bio, roles, preferences, goals, working style (gitignored)
│   ├── frameworks/        # Mental models, decision methods, reusable thinking
│   ├── audience/          # Notes on target readers / users (gitignored)
│   ├── memory/            # Claude Code's managed memory (auto-updated by Claude)
│   ├── library/           # Reference docs, read on-demand (gitignored)
│   └── raw/               # Inbox for new materials (triaged into above)
├── skills/                # 36 Claude Code skills — reusable workflows and tools
├── projects/              # One index entry per project (gitignored, except _TEMPLATE.md)
│   ├── _TEMPLATE.md       # Copy this per project you want tracked
│   └── <project-name>/    # README.md — repo path, status, next step
└── scripts/               # Utility scripts
```

**Guiding split:**
- **knowledge** = nouns (facts, references, context)
- **skills** = verbs (workflows, tools, automation)
- **projects** = pointers (indexes to actual codebases elsewhere)

---

## What's in Each Section

### `knowledge/me/`
Hand-written facts about who you are and what you want:
- Bio, background, current role/school
- Job targets and career goals
- Active projects (links to real repos)
- Working style and preferences

This is the source of truth for Claude Code about how to work with you.
**Note:** Files here are gitignored — personal, local-only.

### `knowledge/frameworks/`
Reusable mental models and decision-making methods:
- Structured thinking templates
- Frameworks for common tasks (design, refactoring, testing, etc.)
- Decision-making guides pulled in when a task calls for them

### `knowledge/audience/`
Notes on target readers and users for your work:
- Persona notes for portfolio work, talks, writing
- Communication style preferences by audience
- Used when tailoring explanations or designing UX
- **Note:** Files here are gitignored — personal, local-only.

### `knowledge/library/`
Reference materials kept on-disk (read when the task clearly matches):
- Technical documentation
- Style guides and writing references
- Domain-specific knowledge bases
- **Note:** Files here are gitignored; this is a local-only reference store.
  `GUIDE.md` (kept in the repo) explains the folder's conventions.

### `knowledge/memory/`
Claude Code's managed memory system — automatically updated across sessions:
- `MEMORY.md` — index of remembered facts (auto-loaded every session)
- 18 fact files — specific things Claude learned and should remember:
  - `user_*.md` — facts about who you are, your preferences, knowledge
  - `feedback_*.md` — guidance on how to approach work (corrections + confirmations)
  - `project_*.md` — ongoing work, goals, initiatives, deadlines
  - `reference_*.md` — pointers to external resources and systems

Don't hand-edit the format here; Claude Code maintains it. Add your own notes to `knowledge/me/` instead.

### `skills/`
36 Claude Code reusable workflows — custom agents, tools, and automations. Highlights:

| Skill | What it does |
|---|---|
| `dev-team-auto` | Autonomous multi-agent convergence loop — runs overnight unattended, drives items to DONE against rubrics |
| `career-advisor` | Portfolio rubric — evaluates accuracy, clarity, credibility, and recruiter impact |
| `research-partner` / `research-review` | Build-time research teammate (mandated pushback, teach-as-we-build) and skeptical peer review of finished work — both driven by `knowledge/frameworks/research-standards.md` |
| `ai-usage-optimizer` | Reviews AI tool use for real compounding leverage vs. cosmetic use |
| `dt-engineer` / `dt-qa` / `dt-review` | Engineer, QA, and Optimization Reviewer agents in the dev-team loop |
| `grill-me` | Interviews you relentlessly about a plan before you build it |
| `improve-system` | Audits this repo itself — memory, skills, knowledge — biased toward deleting rather than adding |

Each skill lives in `skills/<name>/SKILL.md` with frontmatter (name, description, triggers) and an implementation body. Invoked via `/skill-name` in Claude Code.

### `projects/`
One index entry per project — a pointer to a real repository elsewhere, not the
codebase itself. Each is just metadata: repo path, GitHub link, status, next
step, priority, and a short "where it stands" summary. The point is to
context-switch into a project without re-explaining its state.

The frontmatter is a data contract, so tooling can read it. A project whose work
spans two repos keeps one entry with a second path field (e.g.
`dashboard_repo:`) rather than a second entry.

**Everything under `projects/` is gitignored** except `_TEMPLATE.md` — the
entries are personal. Your fork starts empty here; copy `_TEMPLATE.md` per
project you want tracked.

---

## Browsing as an Obsidian Vault (optional)

The repo is plain markdown and works fine without any of this. But `~/os` opens
directly as an [Obsidian](https://obsidian.md) vault — **Open folder as vault →
`~/os`** — which gives you a graph view, backlinks, and fast search over the
whole system.

**What the graph shows.** Links mean *relationships*, not folder membership. A
`**Related:**` line connects two files that genuinely depend on or explain each
other — a skill to the framework it follows, a client project to the platform it
was built from. Folder structure is shown by **color**, not by edges, so the
graph stays readable instead of collapsing into one star per directory.

**Color the graph by folder.** Obsidian writes `.obsidian/` on every pan and
zoom, so it's gitignored and nothing is shared. Build your own in **Graph view →
settings → Groups**, or paste this into `.obsidian/graph.json` under
`colorGroups`:

```json
"colorGroups": [
  { "query": "path:skills/",               "color": { "a": 1, "rgb": 5431378 } },
  { "query": "path:projects/",             "color": { "a": 1, "rgb": 14701138 } },
  { "query": "path:knowledge/frameworks/", "color": { "a": 1, "rgb": 5395026 } },
  { "query": "path:knowledge/memory/",     "color": { "a": 1, "rgb": 11908533 } },
  { "query": "path:knowledge/me/",         "color": { "a": 1, "rgb": 14513408 } },
  { "query": "path:knowledge/audience/",   "color": { "a": 1, "rgb": 7183337 } }
]
```

Tune the force sliders to your own corpus — copying someone else's settings for
a differently-sized vault gives you a hairball or a scatter.

**Turn on link auto-updating.** **Settings → Files & Links → "Automatically
update internal links"**. Renaming or moving a file is the single most common
way `[[links]]` break, and this fixes them as you go. It's native — no plugins,
no tooling.

**Obsidian maintains links; it never creates them.** Nothing here infers a
relationship from content. New edges get added by hand, following the
`**Related:**` convention documented in `CLAUDE.md` → *Link maintenance*.

**A fresh fork's graph will look empty**, and that's expected: `projects/`,
`knowledge/me/`, `knowledge/audience/`, and `knowledge/library/` are gitignored,
so most of the linked content is content you haven't written yet.

**Checking for broken links.** `python3 scripts/link-check.py` reports any
`[[wikilink]]` that resolves to nothing (or ambiguously to several files), plus
`INDEX.md` entries that have drifted from the folder. It prints nothing when
clean and runs automatically from `scripts/maintenance.sh`.

---

## How This Repo is Used

### Integration with Claude Code
This repo is the **source of truth** for Claude Code's global skills and memory. The symlinks are set up as:
- `~/.claude/skills` → `~/os/skills`
- `~/.claude/memory` → `~/os/knowledge/memory`
- Global `CLAUDE.md` routes sessions back here

Editing a skill or memory file here changes it everywhere immediately.

### Workflow
1. **When starting a new session:** Claude Code reads `CLAUDE.md` and checks `knowledge/me/` and `knowledge/memory/` for context
2. **When working on a project:** Look up the project's README in `projects/` to get the real repo path and status
3. **When doing a task:** Pull in frameworks from `knowledge/frameworks/` or reference materials from `knowledge/library/` as needed
4. **During work:** Claude Code may save learnings to `knowledge/memory/` for use in future conversations

### For GitHub Visitors
What you can see here is the *system* — the skills, frameworks, and structure.
The content that fills it (`knowledge/me/`, `knowledge/audience/`,
`knowledge/library/`, and every entry under `projects/`) is gitignored, so those
folders will look empty from GitHub. That's intentional, not a broken clone.

- **Curious about the skills?** Browse `skills/` — each is a self-contained Claude Code automation, and `skills/INDEX.md` is the map
- **Want to understand the thinking?** Check `knowledge/frameworks/` for mental models and decision methods
- **Interested in the projects themselves?** They live in their own repos — see [github.com/nseluga](https://github.com/nseluga)
- **Want to run it yourself?** [Setting This Up For Yourself](#setting-this-up-for-yourself)

---

## Quick Reference

| What you're looking for | Where to find it |
|---|---|
| Nate's bio, goals, projects | `knowledge/me/INDEX.md` (gitignored — local only) |
| How this repo works | `CLAUDE.md` (developer-focused) or this README |
| A specific project's repo | `projects/<project-name>/README.md` (gitignored — local only) |
| How to use a skill | `skills/<skill-name>/SKILL.md` |
| Mental models for a task | `knowledge/frameworks/INDEX.md` |
| Communication style notes | `knowledge/audience/INDEX.md` (gitignored — local only) |
| Things Claude has learned | `knowledge/memory/MEMORY.md` |

---

## Notes for Developers

- **Don't move or rename `~/os`** without updating the symlinks in `~/.claude`, or skills and memory will silently break
- **Health check:** `ls -L ~/.claude/skills/grill-me` should resolve. If it errors, symlinks are broken
- **Personal content** in `knowledge/me/`, `knowledge/audience/`, `knowledge/library/`, and `projects/` is gitignored and kept local-only (see `.gitignore`)
- **Memory format** is auto-managed by Claude Code; hand-edit `knowledge/me/` instead if you want to add notes
- **Skills are real code** — each `SKILL.md` contains a frontmatter header (name, description, trigger) and implementation body

---

## Author

**Nate Seluga**  
Harvey Mudd College, Class of 2027  
Software engineering · ML/AI · Data science · Baseball analytics

[nateseluga.com](https://nateseluga.com) · [github.com/nseluga](https://github.com/nseluga)

(Bio and working style live in `knowledge/me/`, which is gitignored — local only.)

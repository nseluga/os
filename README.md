# OS — Personal Operating System

A single home for knowledge, skills, and projects. Built on top of Claude Code: **48 custom skills**, a structured project-tracking system covering **8 active projects**, and a persistent memory layer with **10 fact files** auto-injected into every session.

The system compounds — each skill added makes the next session more capable, and the memory layer means Claude Code never starts cold. All AI-assisted work on [nateseluga.com](https://nateseluga.com) was built with this as infrastructure.

This is a public repository. Reference materials in `knowledge/library/` are kept locally only (see `.gitignore`).

---

## Structure

```
os/
├── CLAUDE.md              # Developer instructions for Claude Code integration
├── knowledge/             # Organized facts and reference materials
│   ├── me/                # Bio, roles, preferences, goals, working style
│   ├── frameworks/        # Mental models, decision methods, reusable thinking
│   ├── audience/          # Notes on target readers / users
│   ├── memory/            # Claude Code's managed memory (auto-updated by Claude)
│   ├── library/           # Reference docs (read on-demand; kept local-only)
│   └── raw/               # Inbox for new materials (triaged into above)
├── skills/                # 48 Claude Code skills — reusable workflows and tools
├── projects/              # Index entries for 8 active projects
│   ├── pitcher-injury-risk/
│   ├── batting-average-ability/
│   ├── nba-shot-value/
│   ├── patio/
│   ├── portfolio-website/
│   ├── project-dashboard/
│   ├── os/
│   └── os-evals/
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

### `knowledge/library/`
Reference materials kept on-disk (read when the task clearly matches):
- Technical documentation
- Style guides and writing references
- Domain-specific knowledge bases
- **Note:** Files here are gitignored; this is a local-only reference store

### `knowledge/memory/`
Claude Code's managed memory system — automatically updated across sessions:
- `MEMORY.md` — index of remembered facts (auto-loaded every session)
- 10 fact files — specific things Claude learned and should remember:
  - `user_*.md` — facts about who you are, your preferences, knowledge
  - `feedback_*.md` — guidance on how to approach work (corrections + confirmations)
  - `project_*.md` — ongoing work, goals, initiatives, deadlines
  - `reference_*.md` — pointers to external resources and systems

Don't hand-edit the format here; Claude Code maintains it. Add your own notes to `knowledge/me/` instead.

### `skills/`
48 Claude Code reusable workflows — custom agents, tools, and automations. Highlights:

| Skill | What it does |
|---|---|
| `dev-team-auto` | Autonomous multi-agent convergence loop — runs overnight unattended, drives items to DONE against rubrics |
| `career-advisor` | Portfolio rubric — evaluates accuracy, clarity, credibility, and recruiter impact |
| `baseball-research-advisor` | Skeptical analytics peer reviewer — methodology defensibility, honest ceilings |
| `ai-usage-optimizer` | Reviews AI tool use for real compounding leverage vs. cosmetic use |
| `dt-engineer` / `dt-qa` / `dt-review` | Engineer, QA, and Optimization Reviewer agents in the dev-team loop |
| `grilling` / `grill-me` | Interview preparation and self-assessment |
| `writing-great-skills` | Teaches the skill-writing pattern itself |

Each skill lives in `skills/<name>/SKILL.md` with frontmatter (name, description, triggers) and an implementation body. Invoked via `/skill-name` in Claude Code.

### `projects/`
Index entries for 8 active projects. Each is a pointer to a real repository elsewhere — not the actual codebase, just metadata (repo path, GitHub link, status, next step, priority). Used to context-switch quickly without re-explaining state.

| Project | What it is |
|---|---|
| `pitcher-injury-risk` | Multi-model MLB pitcher injury prediction (Statcast 2015–2024, survival models, IR+ composite) |
| `batting-average-ability` | Same-season skill isolation metric with mixed-effects modeling and ICC |
| `nba-shot-value` | 4-model ML comparison on NBA shot probability and expected value by zone |
| `patio` | Full-stack social betting app (React 19 + Flask + scipy house-odds engine) |
| `portfolio-website` | This portfolio — Astro + Tailwind + MDX, built with this OS as infrastructure |
| `project-dashboard` | Local Astro SSR dashboard that reads these README files to show project status |
| `os` | This repo |
| `os-evals` | Evaluation framework for Claude Code skill and workflow quality |

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
- **Interested in the projects?** Start at `knowledge/me/` — it has links to all active work
- **Curious about the skills?** Browse `skills/` — each is a self-contained Claude Code automation
- **Want to understand the thinking?** Check `knowledge/frameworks/` for mental models and decision methods
- **Just exploring?** Start with this README, then `knowledge/me/README.md`

---

## Quick Reference

| What you're looking for | Where to find it |
|---|---|
| Nate's bio, goals, projects | `knowledge/me/README.md` |
| How this repo works | `CLAUDE.md` (developer-focused) or this README |
| A specific project's repo | `projects/<project-name>/README.md` |
| How to use a skill | `skills/<skill-name>/SKILL.md` |
| Mental models for a task | `knowledge/frameworks/README.md` |
| Communication style notes | `knowledge/audience/README.md` |
| Things Claude has learned | `knowledge/memory/MEMORY.md` |

---

## Notes for Developers

- **Don't move or rename `~/os`** without updating the symlinks in `~/.claude`, or skills and memory will silently break
- **Health check:** `ls -L ~/.claude/skills/grilling` should resolve. If it errors, symlinks are broken
- **Reference materials** in `knowledge/library/` are gitignored and kept local-only (see `.gitignore`)
- **Memory format** is auto-managed by Claude Code; hand-edit `knowledge/me/` instead if you want to add notes
- **Skills are real code** — each `SKILL.md` contains a frontmatter header (name, description, trigger) and implementation body

---

## Author

**Nate Seluga**  
Harvey Mudd College, Class of 2027  
Software engineering · ML/AI · Data science · Baseball analytics

See `knowledge/me/README.md` for full bio and working style.

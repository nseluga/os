# Global Claude Code Config — Nate's OS

`~/os` is Nate's personal operating system and the **source of truth for all
Claude Code sessions** — skills, memory, knowledge, and project indexes all
live here. Skills (`~/.claude/skills`) and memory (`~/.claude/memory`) are
symlinked from it and load automatically.

## Structure

```
os/
├── CLAUDE.md              # this file — loaded globally in every session
├── knowledge/             # what Nate knows
│   ├── me/                # bio, roles, preferences, goals
│   ├── frameworks/        # mental models, methods, reusable thinking
│   ├── audience/          # people/orgs to write or build for
│   ├── library/           # reference docs (local-only/gitignored)
│   ├── raw/               # inbox: unprocessed input to triage
│   └── memory/            # Claude Code managed memory (auto-loaded via autoMemoryDirectory)
├── skills/                # all Claude Code skills
└── projects/              # one folder per project — indexes, not the code
```

## What's in ~/os and when to use it

| Path | What it is | When to read it |
|------|-----------|-----------------|
| `knowledge/me/README.md` | Bio, job targets, projects, working style | When you need background on Nate — role, goals, how he works |
| `knowledge/frameworks/` | Mental models and decision methods | When the task calls for a structured approach or framework |
| `knowledge/audience/` | Notes on target readers/users | When writing, designing UX, or tailoring communication |
| `knowledge/library/` | Reference docs (gitignored) | Only when the task clearly matches a specific doc's topic |
| `projects/<name>/README.md` | Per-project index — real repo path, goals, context | When working on or discussing a named project |
| `knowledge/memory/MEMORY.md` | Index of remembered facts and preferences | Auto-loaded every session (via `autoMemoryDirectory`); relevant fact files are auto-injected as `<system-reminder>`s. Follow links when a fact seems relevant. |

Do not read these files automatically. Pull them on demand when a task makes
the content clearly relevant.

**Exception — always for plan/progress files:** when creating or updating a
`PLAN.md` or `PROGRESS.md` in *any* repo, first read
`~/os/knowledge/frameworks/plan-md.md` /
`~/os/knowledge/frameworks/progress-md.md` and follow that schema.

## Flagging findings for the os repo

When a turn produces something worth persisting — a preference, a repeatable
process, or a pattern to reuse — say so explicitly and offer to save it:

- **Memory** (preferences, facts about Nate, behavioral corrections) → write a
  fact file in `~/os/knowledge/memory/` + a MEMORY.md index line.
- **Reusable process/pattern** → a skill under `~/os/skills/`, or a framework
  note in `knowledge/frameworks/`.

Keep entries pointed and brief. Don't save what the repo, git history, or code
already records. Flag; don't auto-write large changes without a nod.

## Keeping project progress current

When a session lands a significant change in a project's real repo — a feature
shipped, a milestone hit, direction changed, or the obvious next step moved —
offer to update that project's index in `~/os`.

- **Which project:** match the repo against the `repo:` field in each
  `~/os/projects/*/README.md`.
- **What to update:** frontmatter — `last_active` (→ today's date),
  `next_step`, and `status`/`priority` if they changed.
- **What counts as significant:** merged feature, resolved blocker, phase
  boundary, changed plan. Skip routine WIP and small fixes.

Offer; don't auto-write. One line at the end of the turn is enough.

## Integration with Claude Code

- `~/.claude/CLAUDE.md` → `~/os/CLAUDE.md` (this file — symlinked)
- `~/.claude/skills`    → `~/os/skills`
- `~/.agents/skills`    → `~/os/skills`
- `~/.claude/memory`    → `~/os/knowledge/memory`

Don't move or rename `~/os` without re-pointing these symlinks.
Health check: `ls -L ~/.claude/skills/grilling` should resolve.

## Authoring a new skill

```
cp ~/os/skills/skills.md ~/os/skills/<skill-name>/SKILL.md
```

The folder name, the `name:` frontmatter field, and the `/` invocation must
all match. `description:` is the router prompt — lead it with the trigger.

# Global Claude Code Config — Nate's OS

`~/os` is Nate's personal operating system and the **source of truth for all
Claude Code sessions** — skills, memory, knowledge, and project indexes all
live here. Skills (`~/.claude/skills`) and memory (`~/.claude/memory`) are
symlinked from it and load automatically.

## Communication style

Be extremely concise. Sacrifice grammar for the sake of concision. Apply this
both when answering Nate directly and when writing skill instructions/output
templates.

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
| `knowledge/me/` | background.md (resume-grade facts), goals.md (targets/timeline), working style | When you need background on Nate — role, goals, how he works |
| `knowledge/frameworks/` | Mental models and decision methods | When the task calls for a structured approach or framework |
| `knowledge/audience/` | Notes on target readers/users | When writing, designing UX, or tailoring communication |
| `knowledge/library/` | Reference docs (gitignored) | Only when the task clearly matches a specific doc's topic |
| `projects/<name>/README.md` | Per-project index — real repo path, goals, context | When working on or discussing a named project |
| `knowledge/memory/MEMORY.md` | Index of remembered facts and preferences | Auto-loaded every session (via `autoMemoryDirectory`). Individual fact files are NOT auto-loaded — a `UserPromptSubmit` hook (`~/.claude/memory-relevance-hook.py`) keyword-matches each prompt against the index and surfaces candidate files as a system-reminder; still Read them yourself when they look relevant, and don't rely on the hook alone since it's a keyword match, not a relevance judgment. |

Do not read these files automatically. Pull them on demand when a task makes
the content clearly relevant.

**Naming a project loads its repo config.** When Nate names a project ("work
in bcns"), read `projects/<name>/README.md` plus the `CLAUDE.md` and
`.claude/settings.json` at that README's `repo:` path — before doing any work.
Reading settings.json tells you what hooks/permissions the repo expects; it
does not activate them (that needs launching Claude from the repo dir).

**Index maintenance:** indexed folders carry an `INDEX.md` with a
one-line-per-file entry (`knowledge/` and its subfolders, `skills/`,
`projects/`, `agents/`). When you add, remove, or repurpose a file in one,
update that folder's `INDEX.md` line in the same turn — an index that drifts
is worse than none. Exceptions: `knowledge/raw/` contents are transient
(never indexed); `knowledge/memory/`'s file index is `MEMORY.md` (auto-loaded; its `INDEX.md`
explains folder structure only); per-project files stay
`projects/<name>/README.md` (the dashboard's data contract).

**Link maintenance (the other axis):** `INDEX.md` and `[[wikilinks]]` do
different jobs and must not be collapsed into each other.

| | `INDEX.md` | `[[wikilinks]]` |
|---|---|---|
| Axis | **containment** — what lives in this folder | **association** — how this file relates to another |
| Lives | one per folder | inside file bodies |
| Also encoded by | the filesystem, the file explorer, graph color groups | nothing else |

- `INDEX.md` entries stay **backticked filenames**. Do not convert them to
  wikilinks — the folder already encodes containment, and doing so buries the
  real semantic edges inside one giant star per folder.
- `[[wikilinks]]` go in **file bodies**, and their job is **resolution**: when
  something tells you to read "the research standards" or "the hosting
  reference", the link is what turns that name into a path. They do not decide
  *what* to read — they make what was named findable.
- **This matters most where grep fails.** `projects/`, `knowledge/me/`,
  `knowledge/audience/`, and `knowledge/library/` are gitignored, so a
  recursive grep from the repo root silently skips all four. A file in one of
  them that nothing links is effectively unreachable — you have to already know
  its path to find it.
- So the test for a missing link is not "do these two relate?" but **"is this
  file named somewhere it can't be resolved from?"** When you add a file, link
  it from wherever it gets referred to by name, in the same turn you add its
  INDEX line.
- Only link a real reference. An invented link is worse than no link.
- **Imperative paths and links compose — they don't compete.** A skill body
  that says "read `~/os/.../convergence-loop.md` now" states *when*; a
  `**Related:**` link states *where it lives*. Executable paths stay paths —
  an agent handed `[[plan-md]]` instead of a path has nothing to open — so the
  wikilink goes on its own line, never in place of one.
- **Use path-form links whenever the basename isn't unique**
  (`[[projects/patio/audit|audit.md]]`). 28 files here are named `SKILL.md` and
  24 `README.md`; a bare `[[SKILL]]` silently resolves to an arbitrary one.
- `knowledge/memory/MEMORY.md` is exempt: it keeps its
  `- [Title](file.md) — hook` format, which Obsidian resolves anyway.

`scripts/link-check.py` reports drift on both axes (unresolved or ambiguous
wikilinks, and INDEX entries that are stale or missing). It runs from
`scripts/maintenance.sh`.

**Exception — always for plan/progress files:** when creating or updating a
`PLAN.md` or `PROGRESS.md` in *any* repo, first read
`~/os/knowledge/frameworks/plan-md.md` /
`~/os/knowledge/frameworks/progress-md.md` and follow that schema.

**Exception — always before writing a memory file:** read
`~/os/knowledge/frameworks/memory-writing.md` and phrase the new `MEMORY.md`
index line per that guide, so the memory-relevance hook can actually find it.

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
Health check: `ls -L ~/.claude/skills/grill-me` should resolve.

## Authoring a new skill

```
cp ~/os/skills/skills.md ~/os/skills/<skill-name>/SKILL.md
```

The folder name, the `name:` frontmatter field, and the `/` invocation must
all match. `description:` is the router prompt — lead it with the trigger.

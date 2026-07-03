# os — Nate's Internal Operating System

This repo is a personal "operating system": a single home for what I know
(`knowledge/`), what I can do (`skills/`), and what I'm building
(`projects/`). It is also the **real, on-disk source of truth for Claude
Code's global skills and memory** — those live here and are symlinked back
into `~/.claude` (see "Integration with Claude Code" below).

## Structure

```
os/
├── CLAUDE.md              # this file
├── knowledge/             # what I know
│   ├── me/                # bio, roles, preferences, goals (hand-written)
│   ├── frameworks/        # mental models, methods, reusable thinking
│   ├── audience/          # people/orgs I write or build for
│   ├── library/           # reference docs to read on demand (files local-only/gitignored)
│   ├── raw/               # inbox: unprocessed dumps, triage into the above
│   └── memory/            # Claude Code's managed memory (MEMORY.md + facts)
├── skills/                # all Claude Code skills (real bodies) + skills.md template
└── projects/              # one folder per project — index entries, not the code
    ├── portfolio-website/     # -> ~/portfolio
    ├── patio/                 # -> ~/Downloads/Patio
    ├── pitcher-injury-risk/   # -> ~/Pitcher-Injury-Risk
    └── batting-average-ability/  # -> ~/Downloads/Batting Average Ability
```

Guiding split: **knowledge = nouns, skills = verbs, projects = pointers.**
The `projects/` READMEs are *indexes* — the actual codebases live at the
paths listed in each README, not here.

## Start here (context initialization)

When a session starts in this repo, orient yourself in this order:

1. **Read `knowledge/memory/MEMORY.md`** — the index of everything Claude
   already remembers about Nate. Follow links to specific facts as relevant.
2. **Skim `knowledge/me/`** — who Nate is and how he likes to work.
3. **Check `projects/`** — if the task concerns a specific project, open its
   README to get the real repo path, then go work in that repo.
4. **Pull in `knowledge/frameworks/` and `knowledge/audience/`** only when the
   task calls for a method or a target reader. Read documents in
   `knowledge/library/` only when a task points at them (or the topic clearly
   matches) — it's optional reference material, nothing there auto-loads.
5. New unsorted input lands in `knowledge/raw/`; triage it into `me/`,
   `frameworks/`, `audience/`, or a project — don't let it pile up.

## Integration with Claude Code

Skills and memory physically live in this repo and are exposed to Claude Code
via **absolute symlinks**:

- `~/.claude/skills`  → `~/os/skills`
- `~/.agents/skills`  → `~/os/skills`
- `~/.claude/memory`  → `~/os/knowledge/memory`

Implications:
- Editing a skill or memory file here changes it everywhere, immediately.
- Memory (`knowledge/memory/`) is **managed by Claude Code** — it rewrites
  `MEMORY.md` and adds fact files automatically. Don't hand-edit its format;
  put your own notes in `knowledge/me/` instead.
- The links are absolute, so **don't move or rename `~/os`** without re-pointing
  them, or skills and memory will silently stop loading.
- Health check: `ls -L ~/.claude/skills/grilling` should resolve. If it errors,
  the symlink chain is broken.

## Authoring a new skill

Copy the template and fill it in:

```
cp ~/os/skills/skills.md ~/os/skills/<skill-name>/SKILL.md
```

The folder name, the `name:` frontmatter field, and how you invoke it must all
match. `description:` is the router prompt — lead it with the trigger.

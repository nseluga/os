---
name: os
status: active
priority: high
last_active: 2026-07-24
next_step: "Author ~/project-dashboard/PLAN.md (phase 1: os-management pages + configurable data dir) and run dev-team-auto on it."
repo: ~/os
github: https://github.com/nseluga/os
dashboard_repo: ~/project-dashboard
summary: "Personal operating system — knowledge, skills, memory, and project index — plus its dashboard app: the single local UI for all os and project management."
tags: [meta, tooling, frontend]
---

**Related:** [os-evals](../os-evals/README.md) measures which layers of this setup earn their keep via ablation.

## Where it stands

The always-on meta repo — global skills, memory, knowledge, and this project
index live here and load automatically. The canonical shape for every file in
`projects/*/README.md` is defined in [`projects/_TEMPLATE.md`](../_TEMPLATE.md).
Browsable as an Obsidian vault (graph view over the `[[wikilinks]]`).

The **dashboard** (`~/project-dashboard`, Astro SSR + Tailwind v4 + TypeScript,
local-only) is this system's UI — it reads the frontmatter of
`projects/*/README.md` as its data contract. Stages 0–7 shipped 2026-07-09:
project board, `/momentum`, "what to work on next", `/notes`, `/tokens`.
Next phase (per its PLAN.md): os-management pages (memory, knowledge, raw
inbox, skills, plan viewers) with a configurable data dir; then optional graph
view; then voice via the Web Speech API. Multi-user deployment is out of scope.

## Run / verify

    cd ~/project-dashboard && npm run dev   # the os dashboard (Astro SSR)
    npm test                                # unit suites

## Key files

- **projects/_TEMPLATE.md** — project README template / dashboard data contract.
- **knowledge/memory/MEMORY.md** — memory index.
- **skills/** — global skills (symlinked to `~/.claude/skills`).
- **~/project-dashboard/PLAN.md / PROGRESS.md / STANDARDS.md** — dashboard trackers (local, gitignored).

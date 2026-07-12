---
name: Project Dashboard
status: active
priority: low
last_active: 2026-07-09
next_step: "1 test failing (tailwind.config.cjs content glob — tsx not included); fix and push to remote."
repo: ~/project-dashboard
github: https://github.com/nseluga/project-dashboard
summary: "Local dashboard showing state of every active project — sourced from os/projects READMEs. Includes weekly digest, momentum view, what-to-work-on-next recommendation, smart notepad, and auto Claude token tracking pulled from ~/.claude/projects/ JSONL logs."
tags: [tooling, frontend]
---

## Where it stands

All planned stages (0–7) complete and merged to main (2026-07-09); active for incremental additions. Stack: Astro SSR + Tailwind v4 + TypeScript + `@astrojs/node`, local-only. Shipped: project board (collapsible edit controls, per-project field-hide toggles), `/momentum` (git activity bars, stalled/moving badges), "What to work on next" card, `/notes` smart notepad (word-boundary auto-categorization), `/tokens` (auto-pulls Claude Code token usage from `~/.claude/projects/` JSONL, no manual entry), and a full visual design pass. Reads the frontmatter from `~/os/projects/*/README.md` — so the template established there is its data contract.

## Run / verify

    cd ~/project-dashboard && npm run dev      # local dashboard (Astro SSR)
    npm test                                   # unit suites (projects, manual, merge, api, digest)

## Key files

- **PLAN.md / PROGRESS.md** (repo root) — local, gitignored trackers.
- **STANDARDS.md** — conventions.

---
name: Project Dashboard
status: active
priority: low
last_active: 2026-07-09
next_step: "1 test failing (tailwind.config.cjs content glob — tsx not included); push to remote."
repo: ~/project-dashboard
github: https://github.com/nseluga/project-dashboard
summary: "Local dashboard showing state of every active project — sourced from os/projects READMEs. Includes weekly digest, momentum view, what-to-work-on-next recommendation, smart notepad, and auto Claude token tracking pulled from ~/.claude/projects/ JSONL logs."
tags: [tooling, frontend]
---

All planned stages (0–7) complete and merged to main (2026-07-09). Active for incremental additions.

Stack: Astro SSR + Tailwind v4 + TypeScript + `@astrojs/node`, local-only.

Features shipped:
- Project board with collapsible edit controls and per-project field hide toggles
- `/momentum` page — git activity bars, stalled/moving badges
- "What to work on next" recommendation card
- `/notes` smart notepad with word-boundary auto-categorization
- `/tokens` page — auto-pulls Claude Code session token usage from `~/.claude/projects/` JSONL logs per project; shows input/output/cache breakdown with share % and mini-bar; refreshes on every load. No manual entry.
- Full visual design pass — Inter + Plus Jakarta Sans, slate palette, indigo accent, emerald status badges, left-border card accents, WCAG-compliant focus rings

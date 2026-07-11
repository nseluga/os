---
name: Acme Labs
status: active
priority: medium
last_active: 2026-07-09
next_step: "Choose a real business name and run RENAME.md find-replace; then build out the marketing site content"
repo: ~/acme-labs
github: null
summary: "Software studio marketing site + monorepo scaffold for building custom software for local small businesses. Placeholder name 'acme-labs' throughout."
tags: [full-stack, startup, next.js]
---

pnpm + Turborepo monorepo scaffolded 2026-07-09. Build passes lint/typecheck/build.

Stack: Next.js 14 App Router, shared `@acme-labs/ui` component package, shared config package, Tailwind, Vercel-ready.

Business name TBD — `RENAME.md` in the repo root documents all three string forms (`@acme-labs/`, `acme-labs`, `Acme Labs`) to replace once the real name is chosen. Do not rename piecemeal; the file lists a one-liner for repo-wide replacement.

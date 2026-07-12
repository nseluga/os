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

## Where it stands

pnpm + Turborepo monorepo scaffolded 2026-07-09; passes lint/typecheck/build. Next.js 14 App Router, shared `@acme-labs/ui` component package + shared config package, Tailwind, Vercel-ready. Business name is still the `acme-labs` placeholder — nothing renamed yet, and no marketing content written.

## Run / verify

    cd ~/acme-labs && pnpm install && pnpm dev      # dev server
    pnpm lint && pnpm typecheck && pnpm build       # full check

## Key files

- **RENAME.md** (repo root) — documents all three string forms (`@acme-labs/`, `acme-labs`, `Acme Labs`) with a one-liner for repo-wide replacement once the real name is chosen. Do not rename piecemeal.
- Not on GitHub yet (`github: null`).

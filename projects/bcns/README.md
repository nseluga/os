---
name: bcns
status: active
priority: medium
last_active: 2026-07-12
next_step: "Write real marketing content: swap placeholder use-cases for real case studies, add Privacy/Terms pages, confirm domain + support email in site.ts"
repo: ~/bcns
github: null
summary: "bcns — software studio marketing site + monorepo scaffold for building custom software for local small businesses. Marketing content still largely placeholder."
tags: [full-stack, startup, next.js]
---

## Where it stands

pnpm + Turborepo monorepo (Next.js 14 App Router, shared `@bcns/ui` component package + shared config package, Tailwind, Vercel-ready). Passes lint/typecheck/build. Marketing content is still largely placeholder.

## Run / verify

    cd ~/bcns && pnpm install && pnpm dev      # dev server
    pnpm lint && pnpm typecheck && pnpm build  # full check

## Key files

- Real-content gaps are grep-able via `TODO`: `apps/web/lib/site.ts` (domain/email), `apps/web/components/use-cases.tsx` (case studies), `apps/web/components/site-footer.tsx` (Privacy/Terms).
- Not on GitHub yet (`github: null`).

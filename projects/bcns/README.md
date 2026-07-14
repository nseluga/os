---
name: bcns
status: active
priority: high
last_active: 2026-07-13
next_step: "Grill session to produce PLAN.md + PROGRESS.md, then fill real marketing content (use-cases, domain/email, Privacy/Terms pages, contact form backend) before first deploy"
repo: ~/bcns
github: https://github.com/nseluga/bcns
summary: "Software studio monorepo — landing website + scaffold for building custom software for local small businesses."
tags: [full-stack, next.js, startup]
---

## Where it stands

pnpm + Turborepo monorepo (Next.js 14 App Router, shared `@bcns/ui` component library, shared `@bcns/config` package, Tailwind, Vercel-ready). Lint, typecheck, and build all pass. All landing page sections exist (hero, problem/solution, how-it-works, delivery models, use-cases, contact form) but marketing content is largely placeholder. Not yet deployed. PLAN.md and PROGRESS.md don't exist yet — planned for creation via a grill session.

## Run / verify

    cd ~/bcns && pnpm install && pnpm dev        # dev server at localhost:3000
    pnpm lint && pnpm typecheck && pnpm build    # full check

## Key files

- **Detailed trackers (local, gitignored):** `PLAN.md` (what's next) · `PROGRESS.md` (what landed) — not yet created
- **Real-content gaps:** `apps/web/lib/site.ts` (domain/email TODOs) · `apps/web/components/use-cases.tsx` (placeholder case studies) · `apps/web/components/site-footer.tsx` (Privacy/Terms links)
- **Monorepo config:** `turbo.json` · `pnpm-workspace.yaml` · `vercel.json`
- **Shared packages:** `packages/ui/` (@bcns/ui) · `packages/config/` (@bcns/config)

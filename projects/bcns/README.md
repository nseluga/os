---
name: bcns
status: active
priority: high
last_active: 2026-07-14
next_step: "Review + commit PLAN.md v2 on layout-loop/nate-personal-first-draft, then run it (dev-team-auto Section 1 restructure/copy -> layout-loop Section 2 visuals)"
repo: ~/bcns
github: https://github.com/nseluga/bcns
summary: "Software studio (Nate + co-founder Brandon Chung) — landing website + scaffold for building custom software for local small businesses."
tags: [full-stack, next.js, startup]
---

## Where it stands

v1 template build is done: slot architecture (`experimental-overnight-first-draft`) plus a visual first draft (`layout-loop/nate-personal-first-draft`, currently checked out). A 2026-07-14 grilling session locked the v2 direction and wrote a new `PLAN.md` (uncommitted, on the layout-loop branch): multi-page site — thin home (hero + 3 nav cards + contact) with `/services`, `/pricing`, `/about`, `/work` — with all copy drafted in the plan's appendix and unknowns as `[INPUT: …]` slots. Key decisions: warm-visitor audience (outreach/referral), fixed-scope builds at two sizes + AI consulting per day, `/work` live with an honest holding state that auto-flips when real entries land, two-founder About (Nate: engineering; Brandon Chung, NYU: business). Brand file `nate-personal.md` exists, so nothing blocks the run. Deferred: prices/turnaround numbers, founder specifics, domain, inbox, legal text, deploy.

## Run / verify

    cd ~/bcns && pnpm install && pnpm dev        # dev server at localhost:3000
    pnpm lint && pnpm typecheck && pnpm build    # full check

## Key files

- **Detailed trackers:** `PLAN.md` (v2 restructure plan + copy appendix) · `PROGRESS.md` — base branch `layout-loop/nate-personal-first-draft`
- **Real-content gaps:** `[INPUT: …]` slots listed in PLAN.md "Needs-Nate" · `apps/web/lib/site.ts` (domain/email TODOs) · `apps/web/components/site-footer.tsx` legal text
- **Monorepo config:** `turbo.json` · `pnpm-workspace.yaml` · `vercel.json`
- **Shared packages:** `packages/ui/` (@bcns/ui) · `packages/config/` (@bcns/config)

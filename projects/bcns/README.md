---
name: bcns
status: active
priority: high
last_active: 2026-07-21
next_step: "Two branch sets await Nate. (1) Template split (2026-07-21): publish @nseluga/app-core@0.2.0 (agent permission-blocked), merge worktree-template-split (bcns) + skeleton-split-onmain (bcns-app-template), then refresh the template lockfile and smoke-test /new-client-repo with a throwaway slug. (2) Hosting architecture LOCKED same day: per-client systemd isolation, CI artifact deploys, shadow-DB migration gate, contract backup to DO Spaces — code in bcns/infra/ + unified deploy.yml, committed locally but UNPUSHED (gh token needs `gh auth refresh -s workflow` to push workflow files; SSH to GitHub blocked on this network — push via https URL). Next: provision the first real DO droplet with infra/bootstrap.sh and rehearse rebuild-from-scratch before client one goes live. Marketing site follow-ups still deferred: mobile/reduced-motion spot-check, copy gaps (founder photos, testimonials), @nseluga→@bcns org migration."
repo: ~/bcns
github: https://github.com/nseluga/bcns
summary: "Software studio (Nate + Brandon Chung) — platform repo: marketing site plus shared @nseluga/* packages and the hosted-web client template. Client apps live in their own repos."
tags: [full-stack, next.js, startup]
---

## Where it stands

bcns has migrated from build-and-hand-off to **build-and-operate** (setup fee +
recurring monthly, bcns hosts the app), and the platform is now fully on GitHub
under Nate's personal account (`nseluga`, no org). `bcns` is the **platform repo**:
the marketing site (`apps/web`), the shared packages, and the hosted-web template
source — no client apps live here anymore. The shared `@nseluga/*` packages
(`app-core`, `ui`, `config`) are published privately to **GitHub Packages** at
`0.1.0`; client repos consume them by version so a fix propagates with a version
bump. The template `templates/hosted-web/` was extracted to a standalone GitHub
**Template Repository**, `bcns-app-template`, so a new client repo is one click.
**DeLuca's** (the first client, an Electron desktop app) was extracted to its own
repo, `bcns-client-delucas`, with full history — and two long-standing
recurring-rule bugs were fixed there. The template was realigned (July 20, 2026)
to the hosting-reference stack — Supabase (Postgres/auth/storage) + DigitalOcean
droplet + PM2, Clerk/Neon/Stripe and Docker/Coolify removed, BCNS billing decided
as central-never-in-app — and five platform defaults (pg-boss jobs, PM2 deploys,
Twilio SMS, Supabase CLI migrations, template contract) were written into
`~/os/knowledge/library/bcns/hosting-reference.md`. Per-client work is tracked
in its own project entries — **bcns-client-coventry** (first hosted-web client,
in scoping; client-specific overrides layered on the platform defaults) and
**bcns-client-delucas** (maintenance). This entry now covers only the platform:
shared packages, the template, and the marketing site.

The template purpose split landed on branches (2026-07-21): **packages = all
shared logic** (app-core 0.2.0 absorbed the template's health probe, webhook
pipeline, storage interface, and AI opt-in gate — fixes now propagate by version
bump), **template = pure runnable skeleton** with a `TEMPLATE.md` manifest of
customization points, and the new **`/new-client-repo` skill**
(`~/os/skills/new-client-repo/`) creates + stamps + verifies client repos from
it. The stale in-repo `templates/hosted-web/` copy is deleted on that branch —
`bcns-app-template` is canonical.

The marketing site (`apps/web`) got a full **visual/animation pass** (2026-07-20,
"Bold, executed with precision" via `/layout-loop`, merged to `main`): a Fraunces
serif-italic accent word per section headline, springy scroll-in reveals + staggered
entrances, richer card hovers (lift/scale/accent-glow), a scroll-fill node-badge
process flow on `/services`, a FAQ accordion on `/pricing`, a pull-quote on `/about`,
and character for the empty `/work` panels (drifting signature motif + shimmer
skeletons). All presentation-only — no copy/data changed. Shared foundation lives in
`components/reveal.tsx`, the Tailwind preset motion tokens, and `globals.css` hover
utilities; see `LAYOUT_LOOP_REPORT.md` for the per-page breakdown and the two open
review flags (mobile + reduced-motion spot-check).

Two notes for future-me: the `@nseluga/*` package scope is temporary (GitHub
Packages ties scope to the account owner) — migrate to a `bcns` org and rename to
`@bcns/*` when it's no longer solo. And installing the packages needs a **classic
PAT** with `read:packages` (the `gh` CLI token can publish but not download).

## Run / verify

    cd ~/bcns && pnpm install
    pnpm --filter @nseluga/web dev     # marketing site at localhost:3000
    pnpm lint && pnpm typecheck && pnpm build

## Key files

- **Detailed trackers:** `PLAN.md` (platform status + next phase) · `PROGRESS.md` (dated log)
- **Setup / conventions:** `SETUP.md` (repo topology, `bcns-client-<slug>` naming, package publish/install, scope→org migration) · `STANDARDS.md` · `CLAUDE.md`
- **Architecture:** `docs/architecture/hosted-web-model.md` (pricing, hosting stack, one-repo-per-client)
- **Shared packages:** `packages/app-core` (@nseluga/app-core) · `packages/ui` (@nseluga/ui) · `packages/config` (@nseluga/config) — published to GitHub Packages
- **Marketing content registry:** `apps/web/lib/content.ts` — single source of truth; mirror at `apps/web/CONTENT.md`
- **Related repos:** `bcns-app-template` (client starter, Template Repo) · `bcns-client-delucas` (DeLuca's desktop app)

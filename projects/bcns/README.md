---
name: bcns
status: active
priority: high
last_active: 2026-07-20
next_step: "Scope Coventry Hills (first hosted client) in a fresh session, then generate bcns-client-coventry-hills from the bcns-app-template Template Repo and build it. First live deploy (Hetzner/Coolify + Cloudflare + Neon + Clerk + Stripe) happens when it ships. Also: migrate the @nseluga/* package scope to a bcns org once it's no longer solo. Marketing-site copy gaps still open: founder photos, Brandon's NYU details, first past-work entry."
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
recurring-rule bugs were fixed there. Next up is scoping and building **Coventry
Hills**, the first *hosted-web* client, which also triggers the first live deploy.

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

---
name: new-client-repo
description: Create a new bcns client repo from the bcns-app-template Template Repository — interview for slug/name/config decisions, create the private GitHub repo, stamp the customization points from the template's TEMPLATE.md, verify the build, push, and create the os project index entry. Use when the user wants to spin up a new client repo/app, onboard a new bcns client, or says "/new-client-repo".
---

# New client repo

## When to use

- Trigger phrases: "new client repo", "spin up a repo for <client>", "onboard <client>", "/new-client-repo"
- Situations: a new bcns client business needs its hosted-web app repo created from `bcns-app-template`
- Do NOT use for: feature development in an existing client repo, infra provisioning (Supabase/droplet/DNS — that's the template's `DEPLOY.md`), or non-hosted-web clients (e.g. desktop apps like DeLuca's)

## What it does

Produces a **repo-ready** client skeleton: a private `bcns-client-<slug>` GitHub
repo generated from `bcns-app-template`, customized per the template's
`TEMPLATE.md` manifest, with a `CLIENT.md` brief, a green
`pnpm install/build/test`, the stamped commit pushed, and an os project index
entry. No feature code, no cloud infra — it ends at "ready to start development".

## Steps

1. **Interview** (skip anything already given in `$ARGUMENTS`):
   - Client slug (kebab-case business name → repo `bcns-client-<slug>`) and display name.
   - Config decisions — "not decided yet" is a valid answer that keeps the template default:
     - Storage backend (platform default Supabase Storage / client-specific e.g. WebDAV / undecided)
     - AI feature (on/off/undecided — default off)
     - Webhook providers needed (payment processor, SMS, accounting… / undecided — none ship by default)
   - Short client brief: what the business is, what the app is expected to do.
2. **Preflight**: `gh auth status` must pass, and `GITHUB_TOKEN` must be set to a
   **classic PAT with `read:packages`** (the `gh` OAuth token cannot download from
   GitHub Packages). If missing, stop and show the fix from `~/bcns/SETUP.md`
   ("Shared packages" section) before creating anything.
3. **Create**: `gh repo create nseluga/bcns-client-<slug> --template nseluga/bcns-app-template --private --clone` from `~` (clones to `~/bcns-client-<slug>`). Template repo generation is async — if the clone comes up empty, wait a few seconds and `git pull`.
4. **Stamp**: read `TEMPLATE.md` in the new repo and apply every entry in
   "Required at creation". Write `CLIENT.md`: display name, the brief, and each
   config decision — undecided ones recorded as open questions. If a config
   decision WAS made, also note it where `TEMPLATE.md` says it lands.
5. **Verify**: `pnpm install && pnpm build && pnpm test` in the new repo, with no
   env vars beyond `GITHUB_TOKEN`. Only proceed if green — the template's
   keyless-run contract means any failure here is real.
6. **Commit + push**: single commit of the stamps (message: `chore: stamp template for <display name>`), `git push`.
7. **os index**: create `~/os/projects/bcns-client-<slug>/README.md` from
   `~/os/projects/_TEMPLATE.md` — `repo: ~/bcns-client-<slug>`, `status: active`,
   `last_active:` today, `next_step:` scoping/dev kickoff, summary from the brief.
8. **Report**: repo URL, what was stamped, open config questions from `CLIENT.md`,
   and the remaining manual checklist — infra is NOT done by this skill:
   Supabase project, DigitalOcean droplet + PM2 process, Cloudflare DNS,
   UptimeRobot (see the repo's `DEPLOY.md`).

## Inputs / arguments

- `$ARGUMENTS` — optional; anything parseable as slug/display name/decisions is
  used to skip those interview questions (e.g. `/new-client-repo coventry-hills "Coventry Hills"`).

## Examples

- `/new-client-repo` → full interview, then create/stamp/verify/push + os entry.
- `/new-client-repo delucas-cafe "DeLuca's Café"` → interview only the config decisions and brief.

## Notes & gotchas

- The manifest (`TEMPLATE.md`) is the source of truth for what to stamp — do not
  hardcode file lists here; if the template gains a customization point, only
  TEMPLATE.md changes.
- Keep the repo **Private**; naming convention and rationale live in `~/bcns/SETUP.md`.
- `pnpm install` may rewrite `pnpm-lock.yaml` (the template's lockfile can lag
  published package versions) — include the lockfile in the stamp commit.
- Shared-logic changes never happen here: fixes belong in `~/bcns/packages/*`,
  published by version (see `bcns/SETUP.md` "Propagation").

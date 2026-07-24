---
name: reference-bcns-ci-setup
description: Required secrets and known CI gotchas for every bcns client repo deploy pipeline
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9074a9b0-1c9d-43f2-a956-c4fa6cd64ab8
---

## Required secrets per client repo

Set these before the first push to main or CI will fail:

| Secret/Variable | How to set | Value |
|---|---|---|
| `GH_PACKAGES_TOKEN` | `gh secret set GH_PACKAGES_TOKEN --repo nseluga/<repo>` | PAT from `~/.npmrc` (`ghp_*`) |
| `SUPABASE_DB_URL` | `gh secret set SUPABASE_DB_URL --repo nseluga/<repo>` | Pooler URL (see below) |
| `DEPLOY_HOST` | `gh secret set DEPLOY_HOST --repo nseluga/<repo>` | Droplet IP |
| `DEPLOY_SSH_KEY` | `gh secret set DEPLOY_SSH_KEY --repo nseluga/<repo>` | Private key for droplet |
| `CLIENT_SLUG` | `gh variable set CLIENT_SLUG --repo nseluga/<repo>` | e.g. `l2detailz` (variable, not secret) |

## SUPABASE_DB_URL format

Must use the **transaction pooler** URL (not direct) — GitHub Actions runners don't support IPv6 which the direct connection requires.

Format: `postgresql://postgres.<project-ref>:PASSWORD@aws-1-us-west-2.pooler.supabase.com:5432/postgres`

Find project-ref in `supabase/.temp/project-ref`. Password from Supabase dashboard → Project Settings → Database.

## Known CI gotchas (debugged 2026-07-24)

- **pnpm version mismatch**: don't hardcode `version: 9` in pnpm/action-setup — let it read from `packageManager` in package.json. Template fixed.
- **GitHub Packages 401/403**: pnpm 11 doesn't expand env vars in project-level `.npmrc`. Use `pnpm config set "//npm.pkg.github.com/:_authToken" "${{ secrets.GH_PACKAGES_TOKEN }}"` step before install. `GITHUB_TOKEN` (auto) doesn't have cross-repo package read access — needs the PAT.
- **GITHUB_TOKEN name is reserved**: can't store a custom secret named `GITHUB_TOKEN` in repo settings — it's shadowed by the auto-generated token. Use `GH_PACKAGES_TOKEN`.
- **IPv6 on Supabase direct URL**: `db.<ref>.supabase.co` is IPv6-only. GitHub Actions runners are IPv4 only. Always use pooler URL for `supabase db push`.
- **Ship release will fail without droplet**: expected — migrate + build passing is the meaningful signal during local dev.

## PAT management

PAT (`ghp_*`) lives in `~/.npmrc` locally and as `GH_PACKAGES_TOKEN` in each repo secret. GitHub does NOT auto-renew — manual regeneration required on expiry. Expires Aug 19 2026. Update `~/.npmrc` and all repo secrets on renewal.

**Why:** no org-level secret sharing on personal GitHub accounts — each repo needs its own copy.

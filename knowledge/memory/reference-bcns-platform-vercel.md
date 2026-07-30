---
name: reference-bcns-platform-vercel
description: "Where the bcns platform site actually deploys — bcn-services.com Vercel account, bcns team, bcn-services/bcns repo (not the personal account)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: e9cc0f22-a17b-492f-abcb-ce5ad201bab9
  modified: 2026-07-30T01:42:30.691Z
---

The bcns **platform** repo (`~/bcns` — marketing site at `apps/web`) deploys
through infrastructure that is **not** on Nate's personal accounts. Verified
2026-07-29 while debugging a failed production deploy.

| Thing | Value |
|---|---|
| Vercel account | `nseluga@bcn-services.com` (login `nseluga-4864`) — **not** `nseluga@g.hmc.edu` |
| Vercel team | `bcns` (Pro Trial; trial expires ~2026-08-12, no card on file) |
| Vercel project | `bcns-landing` → `https://vercel.com/bcns/bcns-landing` |
| GitHub repo | **`bcn-services/bcns`** — transferred out of `nseluga/bcns` |
| Live URL | `bcns-landing.vercel.app` (no custom domain attached as of 2026-07-29) |
| Chrome profile | **"Work Profile"** — the only browser logged into this account |

Required project settings: **Root Directory = `apps/web`**, "Include files
outside the root directory" **on** (installs the pnpm workspace root so
`@nseluga/ui` / `@nseluga/config` resolve), everything else auto-detected, and
**no `vercel.json`** — see [[reference-vercel-json-precedence]].

**Why this matters:** the personal Vercel scope (`hmcnate-projects`, Hobby) has
no `bcns` team and only the `patio` project, so a session logged in there sees
nothing and `vercel.com/bcns/...` 404s. Local `~/bcns` git remote still points
at `nseluga/bcns`; pushes only work via GitHub's transfer redirect. `gh api
repos/nseluga/bcns/...` silently follows that redirect too, which makes the old
name look correct.

**How to apply:** before touching bcns deploys, confirm which Vercel account
and Chrome profile are in play — connect Claude in Chrome from "Work Profile"
(see [[reference-claude-in-chrome-limits]]), or auth the CLI as
bcn-services.com. Client-repo CI is a separate pipeline:
[[reference-bcns-ci-setup]].

**Related:** [[knowledge/library/bcns/hosting-reference|hosting-reference]] is the standing platform architecture doc (stack, per-client cost model, what to watch for) — this file only covers where the platform site deploys.

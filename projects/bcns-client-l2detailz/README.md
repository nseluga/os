---
name: bcns-client-l2detailz
status: active
priority: high
last_active: 2026-07-24
next_step: "CI pipeline working (migrate + build green). Remaining before deploy: set DEPLOY_HOST, DEPLOY_SSH_KEY, CLIENT_SLUG secrets when droplet ready. Pending: migration 0009 (Supabase SQL editor) + API keys (Maps/Anthropic/Resend) from client."
repo: ~/bcns-client-l2detailz
github: https://github.com/nseluga/bcns-client-l2detailz
summary: "bcns hosted-web client — converting L2 Detailz's static marketing site into a web app with an admin dashboard (booking→calendar, Claude banner maker, Maps routing, lifecycle email)."
tags: [full-stack, next.js, bcns-client]
---

## Where it stands

All 15 pre-marker PLAN.md items DONE (dev-team-auto passes 1 + 2, 2026-07-22);
layout-loop admin visual pass complete (8 routes, 2026-07-23); merged to main
(2026-07-24). CI pipeline green (migrate + build). Full feature set built: public marketing site
(dark/gold/serif), pending-request booking with availability pre-check, admin
inbox (confirm/decline), month/week/day calendar + materials checklists,
Google-Maps optimized "Today's Route", Claude banner maker (freeform + slots +
PNG export + media library), Resend lifecycle email + review-request engine.
**Pending before launch:** Nate tests and signs off PR #2; migration 0009 via
Supabase SQL editor; API keys from client (Maps/Anthropic/Resend); staging
deploy + DNS cutover (item 16, below the stop marker). **Deferred out of
launch:** deposits/payments (Stripe), SMS, public gallery, CRM, weather,
recurring plans.

## Run / verify

    cd ~/bcns-client-l2detailz && export GITHUB_TOKEN=<PAT read:packages> && pnpm install
    pnpm dev            # serves on :3100
    pnpm build && pnpm test

## Key files

- **Trackers:** `PLAN.md` (16 items, one stop marker before the DNS cutover — see [[plan-md]]) · `PROGRESS.md` (see [[progress-md]])
- **Reference:** `reference/current-site-content.md` (captured live-site content for the rebuild)
- **Platform authority:** `~/os/knowledge/library/bcns/hosting-reference.md` · [[projects/bcns/README|bcns]] (parent platform project)

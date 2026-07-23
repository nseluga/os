---
name: bcns-client-l2detailz
status: active
priority: high
last_active: 2026-07-23
next_step: "Nate tests the admin UI (PR #2, branch ui/admin-phase1-phase2 — layout-loop visual pass on 8 routes). Decide: another grilling + full dev pass, or small manual updates → merge → staging deploy + DNS cutover. Pending: migration 0009 (Supabase dashboard SQL editor) + API keys (Maps/Anthropic/Resend)."
repo: ~/bcns-client-l2detailz
github: https://github.com/nseluga/bcns-client-l2detailz
summary: "bcns hosted-web client — converting L2 Detailz's static marketing site into a web app with an admin dashboard (booking→calendar, Claude banner maker, Maps routing, lifecycle email)."
tags: [full-stack, next.js, bcns-client]
---

## Where it stands

All 15 pre-marker PLAN.md items DONE (dev-team-auto passes 1 + 2, 2026-07-22);
layout-loop admin visual pass also complete (8 routes, 2026-07-23). PR #2 open
(`ui/admin-phase1-phase2`). Full feature set built: public marketing site
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

- **Trackers:** `PLAN.md` (16 items, one stop marker before the DNS cutover) · `PROGRESS.md`
- **Reference:** `reference/current-site-content.md` (captured live-site content for the rebuild)
- **Platform authority:** `~/os/knowledge/library/bcns/hosting-reference.md` · parent project entry `bcns`

---
name: bcns-client-l2detailz
status: active
priority: high
last_active: 2026-07-20
next_step: "Get the original l2-detailz.html + logo/brand assets from Nate, then start PLAN.md item 1 (rebuild the public marketing site into the template). Also confirm his current site host and how he takes payment (gates the deferred deposits add-on)."
repo: ~/bcns-client-l2detailz
github: https://github.com/nseluga/bcns-client-l2detailz
summary: "bcns hosted-web client — converting L2 Detailz's static marketing site into a web app with an admin dashboard (booking→calendar, Claude banner maker, Maps routing, lifecycle email)."
tags: [full-stack, next.js, bcns-client]
---

## Where it stands

First hosted-web client scoped from the `bcns-app-template`. Requirements are
locked via a full grilling pass (2026-07-20) and written into the repo's
`PLAN.md` (16 ordered dev-team items) + `PROGRESS.md`. L2 Detailz is a solo
mobile car detailer on Oahu; the job is to rebuild his current static site
(`l2details.com` — dark/gold/serif, three packages) as one integrated Next.js
app on the bcns stack, then add an admin area: pending-request booking with a
daily-capacity availability pre-check, a month/week/day calendar with
per-package materials checklists, a Google-Maps optimized "Today's Route," a
Claude-authored freeform banner maker (publish-to-slot + PNG export + reusable
library, using his uploaded media), and a Resend lifecycle-email engine
(thank-you, re-book reminder, Google-review request). No code written yet.
**Deferred out of launch:** deposits/payments (Stripe), SMS, on-job photo
capture, public gallery, CRM, weather, recurring plans. **Blocked on Nate:**
the original HTML + brand assets (macOS walled off the Messages attachment),
and his current host + payment method.

## Run / verify

    cd ~/bcns-client-l2detailz && export GITHUB_TOKEN=<PAT read:packages> && pnpm install
    pnpm dev            # serves on :3100
    pnpm build && pnpm test

## Key files

- **Trackers:** `PLAN.md` (16 items, one stop marker before the DNS cutover) · `PROGRESS.md`
- **Reference:** `reference/current-site-content.md` (captured live-site content for the rebuild)
- **Platform authority:** `~/os/knowledge/library/bcns/hosting-reference.md` · parent project entry `bcns`

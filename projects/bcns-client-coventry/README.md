---
name: bcns — Coventry
status: in-progress
priority: high
last_active: 2026-07-20
next_step: "Launch /dev-team-auto on the Coventry foundation (13 buildable items above the STOP marker in PLAN.md). Unblock the rest as Tim answers: D-2 (payment system of record), storage A/B, contract-template, EIN for A2P 10DLC."
repo_note: "Generated from the bcns-app-template Template Repo as bcns-client-coventry (Private); cloned to ~/bcns-client-coventry."
github: "nseluga/bcns-client-coventry"
summary: "Coventry Painting & General Contracting — first hosted-web client: all-in-one ops platform (leads → quotes → dispatch → closeout) + sub-facing installable PWA, $100/mo founding-client rate."
tags: [client, full-stack, next.js, hosted-web]
---

## Where it stands

Grilling is **complete** — six design branches settled: job identity (UUID PK +
immutable `COV-####` display ID minted at lead creation), one-record-per-job with
a `status` pipeline (dead lead = `lost`), 10-stage pipeline with the deposit gate
as the one structural piece (blocked on D-2), admin password auth + sub SMS
magic-link login over persistent reusable profiles, seed-import + dated cutover
for migration, and a foundation-first build order. The client repo is generated
and its `PLAN.md` + `PROGRESS.md` are written and pushed (`origin/main` 7787154):
13 buildable foundation items above the `⚠️ AUTONOMOUS RUN — STOP HERE` marker,
7 TBD-gated/deferred items below it (6 `blocked`, each naming its Tim/external
dependency). Next action is to launch `/dev-team-auto`.

Proposal v2 is written (v3 edits specified but not yet produced: PWA not native,
in-house e-signature, QBO draft-invoice handoff, deposit caps as configuration).
Platform defaults come from the hosting-reference;
Coventry-specific **overrides** exist because Tim already runs his own tools:
his self-hosted Nextcloud behind the storage adapter (choice A/B pending, in
writing), QuickBooks Online as money truth with one-directional push, and his
payment processor as deposit truth (D-2, the signature-blocking open item).
Open TBDs for Tim: D-2, storage A/B, attorney-blessed contract template,
EIN/business details for A2P 10DLC SMS registration (1–4 week carrier approval —
start before signature). BCNS-side: one attorney hour on liability language
before countersigning.

## Key files

- **Authority docs:** `~/Downloads/Beacon_Systems_Proposal_Coventry_v2.pdf` (v3 edit checklist lives in the notes) · `~/Downloads/coventry_implementation_notes.md` (client-specific decisions + open items) · `~/os/knowledge/library/bcns/hosting-reference.md` (platform defaults)
- **Repo:** `github.com/nseluga/bcns-client-coventry` (Private) · local `~/bcns-client-coventry` — generated from `bcns-app-template`
- **Trackers:** `~/bcns-client-coventry/PLAN.md` (foundation-first, STOP marker, blocked items) · `~/bcns-client-coventry/PROGRESS.md` (seed ledger, dev-team-auto maintains it)

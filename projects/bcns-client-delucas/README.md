---
name: bcns — DeLuca's
status: active
priority: low
last_active: 2026-07-20
next_step: "No open build items — maintenance mode. Next touch: confirm the two recurring-rule fixes are in the build DeLuca's actually runs, and log any field issues here."
repo: ~/bcns-client-delucas
github: https://github.com/nseluga/bcns-client-delucas
summary: "DeLuca's restaurant management — local-first Electron desktop app; bcns's first client (build-and-hand-off era)."
tags: [client, electron, desktop]
---

## Where it stands

Extracted from the bcns platform repo into its own repo with full history.
Two long-standing recurring-transaction bugs are fixed on main (rule edits now
rewrite current+future materialized transactions, and start_date edits persist
with a shared dashboard refresh). Pre-dates the hosted-web model — this is a
handed-off desktop app, so the hosting-reference stack does not apply; support
is reactive, not a monthly hosting relationship.

## Run / verify

    cd ~/bcns-client-delucas && pnpm install
    pnpm dev            # browser dev via mock bridge
    pnpm test

## Key files

- **Bridge contract:** `src/bridge/BridgeInterface.ts` (renderer ↔ Electron shell)
- **Platform relationship:** consumes `@nseluga/*` packages from GitHub Packages

---
name: bcns
status: active
priority: high
last_active: 2026-07-15
next_step: "End-to-end pipeline test: IMAP + LLM extractor against a test mailbox with real invoice PDFs, then build and smoke-test the Mac installer"
repo: ~/bcns
github: https://github.com/nseluga/bcns
summary: "Software studio (Nate + Brandon Chung) — marketing site plus DeLuca's pizza shop revenue tracker (first client app, Electron desktop)."
tags: [full-stack, next.js, electron, startup]
---

## Where it stands

Overnight run complete and merged to main (2026-07-15). Both products are built. bcns website: multi-page Next.js site with real copy (voice/content pass done, pricing and support model filled, two visual passes complete); remaining gaps are founder photos, Brandon's NYU details, and first real past-work entry. DeLuca's pizza app: Electron desktop tracker fully built through P6 (SQLite P&L, IMAP invoice ingestion, LLM extraction, drag-and-drop fallback, manual entry, backup rotation, Mac DMG + Windows installer); 133 tests green. Not yet tested end-to-end against a real mailbox or real invoice PDFs. Handoff blocked on confirming client's email provider (Gmail fine; Outlook/M365 = IMAP blocked, need drag-and-drop-primary variant).

## Run / verify

    cd ~/bcns && pnpm install
    pnpm --filter web dev           # bcns site at localhost:3000
    pnpm --filter @delucas/app dev  # DeLuca's renderer at localhost:3001
    pnpm lint && pnpm typecheck && pnpm build

## Key files

- **Detailed trackers:** `PLAN.md` · `PROGRESS.md` (repo root, branch: main)
- **bcns content registry:** `apps/web/lib/content.ts` — single source of truth; mirror at `apps/web/CONTENT.md`
- **DeLuca's IPC bridge:** `apps/delucas/src/bridge/` — typed renderer↔shell interface
- **DeLuca's ingestion + LLM:** `apps/delucas/src/shell-electron/ingestion/`
- **Monorepo config:** `turbo.json` · `pnpm-workspace.yaml` · `vercel.json`
- **Shared packages:** `packages/ui/` (@bcns/ui) · `packages/config/` (@bcns/config)

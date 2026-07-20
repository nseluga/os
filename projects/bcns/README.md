---
name: bcns
status: active
priority: high
last_active: 2026-07-17
next_step: "Draft plan for Coventry Hills app (next client project); update bcns website (founder photos, Brandon's NYU details, first past-work entry)"
repo: ~/bcns
github: https://github.com/nseluga/bcns
summary: "Software studio (Nate + Brandon Chung) — marketing site plus DeLuca's pizza shop revenue tracker (first client app, Electron desktop)."
tags: [full-stack, next.js, electron, startup]
---

## Where it stands

Both products are built and E2E validated (2026-07-17).

**bcns website:** Multi-page Next.js site with real copy, two visual passes done. Remaining gaps: founder photos, Brandon's NYU details, first real past-work entry. Running at localhost:3000.

**DeLuca's pizza app:** Electron desktop tracker fully built through P6 + E2E validated against real credentials (Gmail IMAP + Anthropic API). ~15 bugs found and fixed during E2E on branch `delucas-e2e`: model string updated to `claude-haiku-4-5`, Anthropic key now forwarded to SDK, PDF rendering fixed in 4 ways (pdfjs legacy build, Path2D/DOMMatrix globals via @napi-rs/canvas, FilesystemStandardFontDataFactory, process.getBuiltinModule polyfill). 133 tests green.

**Remaining work:** S1 (revenue toggle on drag-drop confirm card), Section 3 packaging (DMG smoke-test — highest risk: pdfjs standard_fonts path inside asar may break), handoff. Handoff blocked on: client laptop OS (IMAP path vs. drag-drop-primary), Slice login (check for @slicelife.com emails), labor-app name. Slice API confirmed to be a fintech partner API — not a merchant sales data API; integration path decided at handoff.

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

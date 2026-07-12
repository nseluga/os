---
name: Patio
status: active
priority: high
last_active: 2026-07-09
next_step: "4.1 — SQLAlchemy + Flask-Migrate (STOP: needs human approval for live DB stamp against Supabase)"
repo: ~/Downloads/Patio
github: https://github.com/nseluga/patio
summary: "Full-stack social betting app for backyard games (Caps, Beerball, Pong, Campus Golf)."
tags: [full-stack, mobile]
mobile_path: ~/Downloads/Patio/mobile/
backend_url: https://patio-backend-y4ft.onrender.com
web_url: https://patio-nu.vercel.app
---

## Where it stands

React Native/Expo conversion complete (M.1–M.3, Expo SDK 54). Backend refactor stages 0–3 complete (2026-07-09): security fixes (0.1–0.8), `@token_required` decorator, app-factory + blueprints, error handlers + rate limiting, input validation, sport-module collapse into `bet_generation.py` with a SportConfig seam. 334 backend tests passing. Backend on Render; the old CRA web frontend on Vercel is reference-only until mobile is fully verified. Next: stage 4.1 SQLAlchemy + Flask-Migrate — the live DB stamp against Supabase needs human sign-off.

## Run / verify

    cd ~/Downloads/Patio/mobile && npx expo start      # mobile app
    cd ~/Downloads/Patio/backend && pytest             # 334 backend tests

## Key files

- **PLAN.md / PROGRESS.md** (repo root) — local, gitignored trackers (execution plan + what's landed).
- **DATABASE.md** — trusted Supabase schema reference (`models.py` is stale/untrusted).
- **STANDARDS.md**, **CLAUDE.md** — conventions; read before writing code.

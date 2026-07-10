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

React Native/Expo conversion complete (M.1–M.3). Mobile: Expo SDK 54. Backend on Render; web frontend on Vercel (reference only until mobile fully verified).

Backend refactor stages 0–3 complete (2026-07-09): security fixes (0.1–0.8), `@token_required` decorator (1.1), app-factory + blueprints (2.1), error handlers + rate limiting (2.2), input validation (2.3), sport module collapse into `bet_generation.py` with SportConfig seam (3.1). 334 backend tests. Next: 4.1 SQLAlchemy migration (live DB stamp requires human sign-off).

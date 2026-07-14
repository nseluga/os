---
name: Portfolio Website
status: in-progress
priority: high
last_active: 2026-07-12
next_step: "Run 1 (single pass): visual polish via Fable + Claude Computer Use + content strip (replace all prose with placeholders for Nate). Then Human Hookup: GitHub → Cloudflare Pages → nateseluga.com."
repo: ~/portfolio
github: https://github.com/nseluga/portfolio
summary: "Personal portfolio site — software engineering, sports analytics, AI tooling, and about."
tags: [frontend, portfolio]
---

## Where it stands

V0–V9 complete. 12 pages, clean build, AI-native layer live (JSON-LD, llms.txt, projects.json). One autonomous run remains: **visual polish** (Fable + Claude Computer Use, elevate typography/spacing/cards to a reference quality bar) combined with a **content strip** (replace all authored prose with labeled placeholders for Nate to fill in — structure and chart wiring stay untouched). After that run, Human Hookup. Blockers needing Nate: resume PDF, Patio live URL + screenshots, LinkedIn URL.

## Run / verify

    cd ~/portfolio && npm run dev      # Astro dev server
    npm run build                      # clean build = 12 pages

## Key files

- **PLAN.md / PROGRESS.md** (repo root) — local, gitignored trackers.
- **STANDARDS.md** — Astro/UI conventions; read before editing pages/components.
- **portfolio-brief.md** — original brief.

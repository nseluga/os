---
name: Portfolio Website
status: in-progress
priority: high
last_active: 2026-07-11
next_step: "V10 — visual polish (Fable + Claude Computer Use), launched from the Claude app. Then Human Hookup: GitHub → Cloudflare Pages → nateseluga.com."
repo: ~/portfolio
github: https://github.com/nseluga/portfolio
summary: "Personal portfolio site — software engineering, sports analytics, AI tooling, and about."
tags: [frontend, portfolio]
---

## Where it stands

V0–V9 complete and merged to `main`. 12 pages, Lighthouse 100s, all project pages written in-voice from real repo data (accurate numbers, no fabrication), AI-native layer live (JSON-LD, llms.txt, projects.json). V8 (voice pass) and V9 (analytics-accuracy + visualization pass, baseball-researcher verified) are done. One build item remains — **V10 visual polish** (Fable + Claude Computer Use), then Human Hookup. Blockers needing Nate: resume PDF, Patio live URL + screenshots, LinkedIn URL, review of framing sections.

## Run / verify

    cd ~/portfolio && npm run dev      # Astro dev server
    npm run build                      # clean build = 12 pages

## Key files

- **PLAN.md / PROGRESS.md** (repo root) — local, gitignored trackers.
- **STANDARDS.md** — Astro/UI conventions; read before editing pages/components.
- **portfolio-brief.md** — original brief.

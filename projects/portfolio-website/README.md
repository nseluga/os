---
name: Portfolio Website
status: in-progress
priority: high
last_active: 2026-07-09
next_step: "Add voice examples to ~/os/knowledge/library/style_reference/, then run /dev-team-auto for V8 (voice pass). After that: launch V9 visual polish from Claude app with Fable."
repo: ~/portfolio
github: https://github.com/nseluga/portfolio
summary: "Personal portfolio site — software engineering, sports analytics, AI tooling, and about."
tags: [frontend, portfolio]
---

V0–V7 complete on `content/v3-voice-loop`, merged to `main`. 12 pages, Lighthouse 100s, all project pages rewritten from real repo data (accurate numbers, no fabrication), rubric-passing. AI-native layer live (JSON-LD, llms.txt, projects.json).

Two autonomous runs remain before Human Hookup:

- **V8 (run 1, dev-team-auto):** Site-wide voice pass — strip AI writing patterns and rewrite phrasing to match Nate's voice. Content, facts, and structure stay identical. Needs voice examples in `~/os/knowledge/library/style_reference/` first (essay for rhythm/structure reference, personal project explanation for voice calibration).
- **V9 (run 2, Fable + Claude Computer Use):** Visual polish — spacing, typography, color personality, visual bug fixes. Launch from Claude app with Fable selected.

Then: Human Hookup (GitHub push → Cloudflare Pages → `nateseluga.com`). Needs Nate for accounts.

---
name: Portfolio Website
status: on-hold
priority: low
last_active: 2026-07-18
next_step: "Go through each project page and update its visualizations, content, and goal; then hook up the domain and publish (GitHub → host → nateseluga.com)."
repo: ~/portfolio
github: https://github.com/nseluga/portfolio
summary: "Personal portfolio site — software engineering, sports analytics, AI tooling, and about."
tags: [frontend, portfolio]
---

## Where it stands

12 pages, clean build, AI-native layer live (JSON-LD, llms.txt, projects.json). **Visual polish done** via a `layout-loop` run (branch `layout-loop/wt-2026-07-17`, not yet merged): the whole site now wears the `nate-personal` dark brand — charcoal-purple field, dual pastel blue/purple accents, Bricolage Grotesque display + IBM Plex Sans body, harmonized chart/thumbnail treatment, centered nav. Review the branch + `LAYOUT-LOOP-REPORT.md`, then merge. Next direction is a **per-project content pass** — go page by page updating each project's visualizations, written content, and stated goal — then the domain hookup + publish. Blockers needing Nate: resume PDF, Patio live URL + screenshots, LinkedIn URL.

## Run / verify

    cd ~/portfolio && npm run dev      # Astro dev server
    npm run build                      # clean build = 12 pages

## Key files

- **PLAN.md / PROGRESS.md** (repo root) — local, gitignored trackers.
- **STANDARDS.md** — Astro/UI conventions; read before editing pages/components.
- **portfolio-brief.md** — original brief.

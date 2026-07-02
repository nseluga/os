# Portfolio Website

**Repo:** `~/portfolio`  
**GitHub:** https://github.com/nseluga/portfolio  
**Status:** active

One-line purpose: Personal portfolio site showcasing technical projects, analytical work, and software engineering capability — target audience: software/ML engineers, sports analytics orgs, data science roles.

## Overview

A curated portfolio designed for credibility and exploration, not as a "hire me" landing page. The site demonstrates **who you are** (through accomplishments), **how you think** (through depth on specific projects), and **why someone should work with you** (through evidence of execution and impact).

**Design philosophy:** Evidence over claims; depth over quantity; show the work, don't describe it.

## Content Structure

Four primary content areas, organized by **interest domain** (not technology):

### 1. Software Engineering
- **Patio** — Full-stack sports betting app; demonstrates complete systems, shipping ability, real product complexity
- [Placeholder for additional backend/systems projects]

### 2. Sports Analytics (anchor section for baseball ops audience)
- **Pitcher Injury Risk** — MLB pitcher health modeling; shows data rigor, domain reasoning, actionable insights for front offices
- **NBA Shot Value** — Cross-sport modeling; shot-value prediction from play-by-play context
- **Batting Average Ability** — Hitter-evaluation metric; separates skill from luck; interpretable player-evaluation tool design
- [Placeholder for additional sabermetrics work]

### 3. Startups & AI
- AI-assisted workflow experiments
- Product concepts and entrepreneurial explorations
- [Placeholder for additional startup/product work]

### 4. About
- Coherent personal narrative connecting Harvey Mudd, software engineering, data science, sports analytics, and building
- Throughline: "I build useful things and I think carefully about problems"

## Tech Stack

- **Frontend:** [React/Next.js — confirm from actual repo]
- **Styling:** [CSS/Tailwind — confirm from actual repo]
- **Deployment:** Vercel (auto-deploy from GitHub)
- **CMS/Content:** [Static generation, Markdown, or headless CMS — confirm from repo]

## Design Goals

### Aesthetic
- Minimal, elegant, typography-led
- High whitespace; restrained palette (near-white background, one accent color)
- Mobile-responsive; fast loading
- Content-first design (text and visuals carry weight, not decoration)

### What to Emulate
- Clean single-column layouts with breathing room
- Quiet typographic hierarchy (dates/labels muted, content near-black, section headers small)
- Inline preview cards for projects (thumbnail + title + context) rather than walls of text
- Subtle interaction (small arrows on links, gentle hover states, no gratuitous animation)

### What to Avoid
- Excessive colors, gradients, decorative shapes/dots/zigzags
- Generic templates and resume-card layouts (sidebar avatar, "Skills / Resume / Testimonials" accordions, skill bars)
- Large unbroken text blocks
- Testimonial carousels, "What I'm Doing" service grids

## Project Page Template

Every project page answers, in order:
1. **The Problem** — what challenge existed
2. **Why It Matters** — why anyone should care
3. **My Approach** — how it was solved (data, methodology, decisions)
4. **Results** — what happened; show visuals (charts, dashboards, screenshots, heatmaps)
5. **Key Takeaways** — what you learned

**Visual priority:** Charts, dashboards, model outputs, screenshots, interactive demos, diagrams. Default move is to show an artifact, not describe it.

## Content Principles

- **Evidence over claims:** Replace adjectives ("passionate," "hard-working") with artifacts
- **Depth over quantity:** A few projects told well beats a long list
- **Show the work:** Visuals carry more weight than prose
- **Assume intelligent reader unfamiliar with the project:** Clear, technical, concise
- **Organize by domain, not technology:** Sections framed by interest (engineering, sports analytics, startups), not languages/frameworks

## Key Files

- Portfolio site source code — [structure varies; confirm from repo]
- Content/project pages — typically in `src/` or content directory
- `portfolio-brief.md` — design brief (referenced in repo, separate from code)
- Deployment config — Vercel settings, auto-deploy from GitHub

## Current Status

Active; ongoing updates as projects mature or new work ships.

## Open Questions

- Which projects ship first vs. which get expanded writeups
- Blogging/writing section strategy (if any)
- Integration of interactive demos or live project previews
- SEO and discoverability strategy (for recruiters searching "Harvey Mudd engineer baseball analytics")

## Target Audiences (in priority order)

1. **Software engineering recruiters** — proof of systems-building, shipping ability, code quality
2. **Sports analytics / baseball operations** — modeling rigor, data handling, domain reasoning
3. **Data science recruiters** — methodology, evaluation, clear results
4. **Startup founders** — initiative, range, ability to build end-to-end
5. **Professors / researchers** — depth, intellectual honesty
6. **Potential collaborators** — how you think, what you care about

## Links

- **GitHub:** https://github.com/nseluga/portfolio
- **Live:** [deployed URL — e.g., nateseluga.com]
- **Design brief:** portfolio-brief.md
- **Deployment:** Vercel (auto-deploy on push to main)

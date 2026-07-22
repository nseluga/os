---
name: layout-loop
description: Improve the visual layout of a website, app, or dashboard so it is uniquely styled to Nate, intuitive, simple, and aesthetically pleasing. Applies a persistent craft layer (Nate's invariant taste) plus a swappable brand profile through a closed visual loop — run app, view in the browser, adjust code, re-view — running autonomously (typically overnight in cowork) on an isolated branch and never merging to main without sign-off. Use when improving/polishing the look of a page, app, or dashboard against Nate's design language.
---

You improve the **visual layout** of a page, app, or dashboard so it is *uniquely styled to Nate, intuitive, simple, and aesthetically pleasing*. You are not a generic UI reviewer (that is `dt-ui`, which enforces correctness). Your job is to **apply Nate's design language** — his invariant craft plus the active brand — and to verify the result by **looking at the rendered pixels**, not by trusting a diff.

You run as a **closed visual loop**, usually **autonomously overnight in cowork** (Claude can see the screen). You work on an **isolated branch, never main**, and **you do not merge** — Nate signs off in the morning and merges himself.

## The two-layer design language

You read two things and merge them every run:

1. **Craft layer** — `~/os/knowledge/library/design-language/craft.md`
   Nate's *invariant* taste: his convictions about hierarchy, whitespace, restraint, density, intuitiveness, and what "aesthetically pleasing" means to him. Principles (prose) + tokens (concrete values). This applies to **every** run regardless of brand. It is the "uniquely Nate" signal.

2. **Brand layer** — `~/os/knowledge/library/design-language/brands/<brand>.md`
   The *swappable* skin for the active context: palette, type, voice, imagery. Hand-authored (from online research + example screenshots/URLs). Portfolio, bcns, or a specific client each get their own file.

**Merge rule:** craft principles steer taste and judgment; brand tokens supply the concrete look. On any conflict, craft governs *craft* concerns (spacing rhythm, hierarchy, restraint) and brand governs *brand* concerns (color, type, voice).

**If `craft.md` does not exist:** stop immediately and tell Nate the craft layer must be extracted first (a dedicated cowork taste-extraction session). Do not guess his taste. The quality of every run is bounded by this file.

## Kickoff — confirm, then detach

You are always launched while Nate is present. Do a short confirm-then-detach exchange, then run autonomously with no further interruption:

1. **Target queue** — the ordered list of pages/routes to improve tonight. Each gets its own full loop. Single page = a queue of one.
2. **Brand** — which brand file to load. Propose the one inferred from the project; Nate confirms/corrects (never guess brand for client work).
3. **Launch** — the dev-server command + URL. Propose defaults discovered from `package.json` (e.g. `pnpm dev` → `localhost:3000`; for the bcns Turborepo, `pnpm --filter <app> dev`). Nate confirms/corrects.

Power-user shortcut: if these are passed as args (`target=`, `brand=`, `launch=`, `url=`), skip the confirmation and go straight to autonomous.

After confirmation: **do not ask anything else until the run ends.** Nate is asleep.

## Isolation and the git gate

- Work in an **isolated branch/worktree**. **Never edit or merge to main.**
- **Commit each iteration** with the change log line as the message, so progression is reviewable.
- **You never merge.** Sign-off is deferred and structural: in the morning Nate reviews the report + diff and merges himself. No sign-off, no merge.

## The loop — one iteration

Per target page, repeat:

1. **Run** the app (start the dev server once per run; reuse it across iterations).
2. **View** — screenshot the current rendered state in the browser.
3. **Diagnose** — before naming the gap, set a spatial thesis: what is the primary reading or task path? What belongs together and what must separate? Which element leads, which supports? What density and spacing rhythm is intended? Then, with that framing, identify the *single biggest* gap versus craft+brand. One gap, not a shotgun.
4. **Adjust** — make one focused change to fix it.
5. **Re-view** — screenshot again; compare to the previous shot.
6. **Log** — record what changed and why (this is the commit message).

One change per pass so every change is attributable.

## The rubric — what "done" means

Measure each page against Nate's four goals, made checkable:

| Goal | Check (must cite visible evidence in the screenshot) |
|---|---|
| **Uniquely styled to Nate** | Uses craft principles + active brand tokens; no colors/spacing outside the defined scales; cohesive with the brand's reference examples |
| **Intuitive** | Primary action is visually dominant; nav/structure legible at a glance; clear affordances; reading and task path remains clear at every supported size |
| **Simple** | Visual noise minimized; every element justified; one accent earning its place. Does **not** use: gradient text, glass/blur as decoration, same-size card grids of icon+heading+text as a page structure, hero-metric templates, tracked uppercase eyebrows on every section, or colored `border-left` costumes on cards. These are AI defaults, not decisions. |
| **Aesthetically pleasing** | Squint test: with detail blurred, the primary element, secondary element, and major groups are still legible in order. Related items are close; distinct groups are separated by generous space, not containers. Tight and generous intervals create deliberate rhythm — not one spacing value repeated throughout. Depth and shadow carry offset and blur; zero-offset colored halos are decoration. |

**Objective gates (hard fails — must pass before "done" is even considered):**
- Text contrast ≥4.5:1 body, ≥3:1 large text (WCAG AA). On colored surfaces, tint secondary text from that hue — never generic gray.
- No overflow, overlap, or clipping at any documented breakpoint.
- Layout holds at mobile **and** desktop breakpoints (resize and re-view).
- Keyboard, touch, and tab order agree with visual order.
- Long text, empty states, and dynamic content do not break the structure.

Do not claim a rubric row is satisfied without pointing to the visual evidence. No self-grading by assertion.

## Stopping conditions — the loop halts on ANY of

1. **Converged** — all objective gates pass AND every rubric row is satisfied.
2. **Diminishing returns** — a pass yields only marginal change, or you cannot name a concrete remaining flaw.
3. **Iteration cap** — 5 passes on this page. Stop and report what remains.

Then move to the next page in the queue.

## Safety rails (unattended = no net)

- **Baseline screenshot** captured before pass 1 of each page, so "better" is measured, not asserted.
- **Change log** per pass prevents **oscillation** — never undo a prior pass's change without stating why.
- **Hard termination is mandatory.** The cap and diminishing-returns check must be airtight; never fiddle past them.
- **Graceful failure** — if the dev server dies or screenshots fail ~2 times, stop cleanly for that page and record it in the report. Never spin on a broken app all night.

## The edit fence — what you may touch

- **Presentation only.** Styling and layout: CSS/Tailwind classes, `className`s, spacing/grid/flex wrappers, component *arrangement*.
- **Never** touch copy, data, props/logic, routing, or API calls.
- Structural markup changes (e.g. extracting a purely-visual wrapper) are allowed **only when purely presentational**, and must be logged as such.
- **Content/data must be provably unchanged** — the rendered text and the values shown are identical before/after. You may restyle a number, never change it. This is the cheap correctness check that proves you stayed in your lane.

## Taste forks when you can't ask

Nate is asleep; you cannot ask. When the craft doc does not clearly resolve a fork:

- **Default — decide-and-log.** Pick the direction best supported by `craft.md`, apply it, and record the alternative in the report ("chose X over Y because craft favors restraint — flag if you disagree").
- **Structural forks only — branch-and-present.** For *layout-architecture* decisions where the whole composition diverges (sidebar vs. top nav, card grid vs. table), produce **both** variants on separate branches/commits for morning comparison. Do not branch on minor forks (a spacing value, an accent placement) — that path is decide-and-log.

## Morning report

Leave one report (per-page sections) for Nate to review before merging:

- **Baseline vs. final** screenshots for each page.
- **Change log** (per iteration, with reasons).
- **Rubric self-assessment** with cited visual evidence, and which stopping condition ended each page.
- **Flagged decisions** — taste forks you resolved (with the alternative) and any structural variants produced.
- **Failures** — any page that hit graceful-failure and why.

## Templates

Authoring `craft.md` or a brand file: see `reference/craft-template.md` and `reference/brand-template.md` in this skill.

---
name: design
description: Use when the user wants to design, style, or visually improve a page, app, dashboard, or site against Nate's design language — picking a visual style, choosing a page composition, building it, or refining an existing surface. Triggers on "/design", "design this page", "pick a style", "restyle X", "make this look right", "improve the layout/look", "try some imagery for this", or any request to apply Nate's craft + style + brand layers. Interactive — Nate makes every taste call. Replaces the retired `layout-loop`.
---

# design

You design a surface against Nate's design language. **Nate is in the room and makes every taste call.** You produce options, cite evidence, and enforce the floor; you never self-grade a taste decision and never converge a loop on your own rubric.

This skill is not `dt-ui` (correctness sweeps) and not `/impeccable` (its own creative-direction engine). It is Nate's stack, with Impeccable used as the technical floor underneath it.

## When to use

- Trigger phrases: "/design", "design this page", "pick a style for X", "restyle", "make this look better", "improve the layout", "try different imagery", "let's do the visual direction".
- Situations: a repo with a UI surface that has no `STYLE.md` yet, or has one and needs the next page / a refinement pass.
- Do NOT use when: the ask is a11y/correctness triage on already-decided visuals (`dt-ui`), a code-quality review (`dt-review`), or content/copy work.

## What it does

Merges five layers into one design contract for the project, then runs the project through four phases — **STYLE → COMPOSITION → BUILD → REFINE**. Phase 1 and 2 hand Nate five real, rendered options and he picks. Phase 3 writes `STYLE.md` at the repo root and builds it. Phase 4 is ongoing refinement, driven from the browser via Impeccable live mode, with imagery generated through Higgsfield.

---

## The layer stack

Merged every run, in this order:

| # | Layer | Path | What it owns |
|---|---|---|---|
| 1 | **Impeccable** | `$IMP/reference/*` + `$IMP/scripts/detector/registry/antipatterns.mjs` | The **technical floor** — what not to do. Objective, computable, machine-enforced. |
| 2 | **craft.md** | `~/os/knowledge/library/design-language/craft.md` | Nate's **invariant judgment** — what survives every mode, style, and brand. |
| 3 | **mode** | `~/os/knowledge/library/design-language/modes/{app,website}.md` | The **dials** — ornamentation budget, density baseline, accent aggression, nav conventions, overview behavior, style fitness. |
| 4 | **style** | `~/os/knowledge/library/design-language/styles/<style>/README.md` | The **genre** — layout logic, type character, palette behavior, texture, ornamentation, imagery. Selected per project in phase 1. |
| 5 | **brand** | `~/os/knowledge/library/design-language/brands/<brand>.md` | The **concrete values** — palette hexes, families, voice. |

### Precedence — read this before resolving any conflict

| Conflict | Winner | Note |
|---|---|---|
| Technical / accessibility math — contrast ratios, touch targets, breakpoints, motion timing, type-scale ratios, measure, spacing systems | **Impeccable** | Always. Cite the Impeccable file; never restate its numbers in project docs. |
| **Taste collision with brand** — the anti-slop registry flags a brand's palette, font, or effect | **Impeccable** | Brand files are **reference, not rules** — so a collision costs a value, not the brand. Drop or move the flagged value and say so; never carve an exemption, and never stop to "re-pick the brand." |
| Judgment Impeccable has no opinion on — what dominates, how much restraint, composition intent, whether a surface has earned character | **craft.md** | Impeccable holds the mechanics, never the direction. |
| Style vs. mode — a genre wants more ornamentation than the mode allows | **mode** | Modes set the budget; styles spend inside it. If the style can't work at that budget, it was the wrong style for the mode — say so and re-pick. |
| Brand vs. style on a value Impeccable does not flag | **brand** | Style says "muted, low-chroma"; brand says which muted hues. Values only — the brand never overrides the style's genre, composition, or imagery logic. |
| Brand file appears to forbid something | **the brand file is wrong** | Brands are reference, not rules. Read a prohibition as strong direction, not a veto — and flag it for rewrite. Nothing in `brands/` may narrow the phase-1 slate or block a build. |

This is the opposite of the usual "brand wins on brand concerns" instinct. It is deliberate.

**The brand layer supplies colour, type character, register, and closest-fit
observations — nothing else.** See `reference/brand-template.md` for the schema and its
authoring rules.

### Resolving Impeccable

Installed as a plugin. **Never hardcode the version** — updates land in a new directory:

```bash
IMP=$(ls -d ~/.claude/plugins/cache/impeccable/impeccable/*/skills/impeccable | sort -V | tail -1)
```

Impeccable's own docs write script paths as `.claude/skills/impeccable/scripts/…` (project-local install). Under the plugin install they are `$IMP/scripts/…`. Run them with **cwd at the project root**, not at `$IMP`. **Verified working 2026-07-25** — the scripts resolve siblings via `import.meta.url` and project state via `resolveProjectRoot(cwd)`, so the plugin path is fully supported. (The only true project-local dependency is `hook-admin.mjs`, which generates Claude Code hook manifests — unrelated to live mode and detect.)

**Adopt** (technical floor only):

| File | Owns |
|---|---|
| `$IMP/reference/craft-floor.md` | The quality floor and absolute bans. Load immediately before editing UI, never for planning-only work. |
| `$IMP/reference/typeset.md` | Measure, scale ratio, tracking floor, weight steps, fallback metrics, loading. |
| `$IMP/reference/colorize.md` | OKLCH ramps, contrast table, semantic color roles, dark-mode composition. |
| `$IMP/reference/layout.md` | Squint test, spatial thesis, spacing scale, structural responsive behavior. |
| `$IMP/reference/animate.md` | The duration/easing table, motion thesis, reduced-motion behavior. |
| `$IMP/reference/adapt.md` | Breakpoints, touch targets, pointer/hover queries, safe areas, responsive images. |
| `$IMP/reference/operate.md` | Depth for app-mode surfaces (component state vocabulary, density, product slop test). |
| `$IMP/reference/audit.md` | The scored technical audit used for a batched verification round. |
| `$IMP/scripts/detector/registry/antipatterns.mjs` | 60 machine-enforced rules — 33 `category: 'slop'`, 27 `category: 'quality'`. |
| `$IMP/reference/live.md` | Live mode contract (phase 4). |

**Do NOT adopt** — these are Impeccable's own taste and creative-direction engine and collide with `craft.md`: `new-work.md`, `visualize.md`, `init.md`, `shape.md`, `critique.md`, `bolder.md`, `quieter.md`, `distill.md`, `delight.md`, `overdrive.md`, `clarify.md`.

### Anti-slop: the registry is the list

Run the detector; do not maintain a parallel prose list of AI tells. Two lists drift.

```bash
node "$IMP/scripts/detect.mjs" --json [--scope layout|type] <files or dirs>
```

`slop`-category findings are AI-default tells (gradient text, glass/blur decoration, side-tab accent borders, hero-metric templates, AI palettes, overused fonts, nested cards, tracked-uppercase eyebrows). `quality`-category findings are craft failures. Verify each finding in context — call out false positives rather than obeying a bad match, but never delete a rule from the mental model because it was inconvenient.

---

## Phases

**Infer the phase from `STYLE.md` state.** Accept `phase=N` to override.

| `STYLE.md` state | Phase |
|---|---|
| Absent, or `style:` empty/missing | **1 — STYLE** |
| `style:` set, `## Composition` empty or absent | **2 — COMPOSITION** |
| Both set, but the real page does not yet reflect them | **3 — BUILD** |
| Contract set and propagated | **4 — REFINE** |

**Preflight, every phase:**

1. Resolve `$IMP`.
2. Read `craft.md`. **If it carries a STALE banner, do not cite its tokens or `Ref:` paths** — use only the principles the banner says survive, and tell Nate the re-extraction is still pending.
3. Read the mode file for the declared mode. Missing or unpopulated → ask Nate for the mode and its dials, or stop.
4. Read the brand file **as reference, not as constraint** — it tells you what the brand is like and what to try to match. Treat its palette, type character, register, and affinities as input to your options; treat any prohibition in it as a defect to flag, not an instruction to obey.
5. Phase artifacts go in `<repo>/.design/` (scratch, gitignored). Only `STYLE.md` is committed.

Nate's **mode** (`app` / `website`) is not Impeccable's **visitor mode** (Persuade / Operate / Read / Experience). Map when loading Impeccable references: `website` → Persuade (or Experience for portfolio/gallery surfaces), `app` → Operate, docs/long-form → Read.

---

### Phase 1 — STYLE

Nate picks the genre. You render it; you do not rank it.

1. Confirm **mode** (`app` | `website`) and **brand** with Nate. Never guess brand for client work.
2. List candidate styles from `~/os/knowledge/library/design-language/styles/`, filtered by the mode file's **style fitness** and each style README's **Mode fitness** line — **and by nothing else**. The brand's "Style affinities" table is advisory: it tells Nate which are closest, it never removes a style from the slate. **If fewer than five styles qualify, stop** — the catalog is not populated enough to sample; tell Nate the extraction session must land first. Do not invent styles to fill slots.
3. Pick a **representative layout** for the project: the real first page's actual content shape, simplified — nav, a hero or entry region, a primary content block, one secondary block, a footer. Same content in all five sections.
4. Produce **one self-contained HTML file** at `<repo>/.design/phase1-styles.html`:
   - **Five full-width stacked sections**, one per style. NOT a tile grid — style is judged on composition and rhythm, and a tile can't show either.
   - Each section renders the **same** representative layout in a **different** style.
   - Each section gets a sticky label: style name + the one-line "what it is" from its README.
   - Single file, inline `<style>`, no build step. Web fonts via a `<link>` to Google Fonts are fine.
   - Format precedent — read these before writing and match the approach: `~/os/knowledge/library/design-language/craft-assets/09-token-sampler.html`, `10-type-direction-sampler.html`, `11-texture-imagery-sampler.html`.
   - Every section already obeys the floor: contrast, spacing, type per `$IMP/reference/craft-floor.md`. Run the detector over the file before showing it.
5. Serve and open it. **`file://` URLs are blocked in the browser tooling** — run `python3 -m http.server` from `<repo>/.design/` and open the `localhost` URL.
6. Nate scrolls and picks one. **Do not recommend a winner unprompted.** If he asks, give one sentence per style on fit to the mode and the project's content, not on which is prettier.
7. Record the pick and go to phase 2.

### Phase 2 — COMPOSITION

Style is locked. Now the structure of the real page.

1. Read the project's **real first page** — its actual routes, copy, data shape, and component inventory. Compositions are built on real content, not lorem.
2. Produce **five structurally different takes** on that page. **Style tokens are identical across all five** — one shared `:root` block. Only structure varies:
   - Shell: sidebar vs. top nav vs. no chrome
   - Entry: split hero vs. centered stack vs. straight-to-content
   - Primary content topology: grid vs. feed vs. table vs. columns
   - Focal hierarchy: which element dominates, which supports, which recedes
3. Same delivery as phase 1 — one self-contained file, `<repo>/.design/phase2-compositions.html`, five full-width stacked sections, labeled, served over `http.server`.
4. **Live mode is the natural engine here.** If the project already has an HMR dev server and live config, generating variants against the real element in the real page beats hand-writing five static sections — see phase 4's live-mode section for the contract. Static file is the fallback when there is no server or no config yet.
5. State the **spatial thesis** for each take in one line (primary path, what groups, what leads) — per `$IMP/reference/layout.md`. That is the label, not a review.
6. Nate picks one. Go to phase 3.

### Phase 3 — BUILD

1. Write `STYLE.md` at the **project repo root**, next to `PLAN.md` / `PROGRESS.md`. Schema below. **Commit it.**
2. Propagate the chosen composition into the real code:
   - Style values land in the project's existing token/theme file. If none exists, create one — do not scatter literals.
   - Build the chosen structure in the real components.
   - Load `$IMP/reference/craft-floor.md` immediately before you start editing UI.
3. Phase 3 may create and restructure presentation markup and tokens. It still **never** changes copy, data, props/logic, routing, or API calls — ask first, always.
4. Verify in **batched rounds, not a loop**: build fully, then one screenshot round covering desktop **and** mobile together, fix everything it shows, confirm with **at most one more round**. Per-tweak screenshot cycles waste money and raise nothing.
5. Run the detector and the objective gates before declaring the build done.

### Phase 4 — REFINE

Ongoing improvement of a surface that already has a contract.

**Before any change: capture a baseline screenshot.** "Better" is measured, not asserted.

#### Live mode — the primary manual-adjustment channel

`/impeccable live` is an in-browser overlay: select an element, pick a design action, get AI-generated HTML/CSS variants hot-swapped through HMR, accept or discard. This is how Nate adjusts quickly in the open web tab.

**Requirements:**
- A running HMR dev server (Vite / Next / Bun / SvelteKit / Astro), **or** a static HTML file open in the browser.
- **Two setup gates, in this order** (verified 2026-07-25 against the plugin install). Neither is a failure — each is a setup prompt:
  1. `{ok:false, error:"context_missing", missing:["PRODUCT.md","DESIGN.md"], nextCommand:"init"}` — fires **first**. Do **not** run `/impeccable init` to satisfy it: `init` is on the do-not-adopt list, and `live.md` states **"DESIGN.md wins on visual decisions"**, which would silently outrank this skill's whole layer stack. Instead hand-write both as **thin shims**: `PRODUCT.md` = what the product is, in a paragraph; `DESIGN.md` = a pointer that says visual authority lives in `STYLE.md` + `~/os/knowledge/library/design-language/`, and that Impeccable governs technical floor only. Keep them minimal — they exist to satisfy the gate, not to hold design decisions.
  2. `{ok:false, error:"config_missing", path}` — fires next. Write `.impeccable/live/config.json` per live.md's **First-time setup** framework table (Astro: `files: ["<root layout .astro>"]`, `insertBefore: "</body>"`, `commentSyntax: "html"`), then rerun.

**Contract** (read `$IMP/reference/live.md` in full before running it; this is the shape, not the whole spec):

```bash
node "$IMP/scripts/live.mjs"                  # cwd = project root; boots the helper, injects live.js
node "$IMP/scripts/live-poll.mjs"             # Claude Code: run as a BACKGROUND task, default long timeout
```

- Open the **app URL** that serves the injected page — never `serverPort` (that is the helper, not the app).
- Never pass a short `--timeout=`. Dispatch on event `type`: `generate` / `steer` / `accept` / `discard` / `manual_edit_apply` / `exit`. Re-poll immediately after every event or `--reply`.
- **Actions:** use `typeset`, `colorize`, `layout`, `adapt`, `animate` — load `$IMP/reference/<action>.md` before generating. For anything else, use the **freeform** action or the **Steer** bar (page-level direction, no element pick) and govern it with `craft.md` + the mode file. Do **not** route through `bolder` / `quieter` / `distill` / `delight` / `overdrive` — those are the taste engine we did not adopt.
- **The overlay preview is the verification channel.** Do not screenshot, re-render, or QA variants between `generate` and `accept` — apply the floor by construction as you write. Full verification (computed contrast, breakpoints, real-copy overflow) runs **once at accept**.
- Interrupted? `live-status.mjs` / `live-resume.mjs` before guessing.
- On exit: `live-server.mjs stop`, then strip leftover `impeccable-variants-start` and `impeccable-carbonize-start` markers.

#### Imagery and animation — Higgsfield

**Two paths exist. Prefer the MCP tools.**

| Path | Surface | Use when |
|---|---|---|
| **MCP tools** (preferred) | `mcp__higgsfield__*` — deferred, load with `ToolSearch` | Default. Typed arguments, structured returns, job polling via `job_status`. No stdout parsing. |
| **Skill pack** | Skill tool → `higgsfield-generate`, `higgsfield-product-photoshoot` | Composed multi-step workflows (product photoshoot modes, marketing studio) where the pack's backend assembles the prompt. |

The skill pack is a Bash wrapper around the `higgsfield` CLI binary. **Verified installed
2026-07-26** at `/usr/local/bin/higgsfield` — no longer a blocker. If `which higgsfield`
ever comes back empty, that path is down and MCP is the fallback, not a hard stop.

Load MCP tools in **one** `ToolSearch` call, not one per tool:

```
ToolSearch "select:mcp__higgsfield__generate_image,mcp__higgsfield__generate_video,mcp__higgsfield__job_status,mcp__higgsfield__models_explore"
```

**Routing, for a design surface:**

| Need | Tool |
|---|---|
| Hero/background imagery, illustration, texture | `generate_image` |
| Unsure which model fits | `models_explore(action:'recommend')` **before** generating |
| Short motion for a landing hero | `generate_video` (image-to-video) |
| Aspect-ratio change on existing video | `reframe` |
| Cutout / transparent background | `remove_background` |
| Expand or uncrop an existing image | `outpaint_image` |
| Resolution bump to 2K/4K | `upscale_image` / `upscale_video` |
| Product shots on a marketing page (product_shot, lifestyle_scene, hero_banner, social_carousel, ad_creative_pack, moodboard_pin, conceptual_product, restyle) | Skill → `higgsfield-product-photoshoot`. Its backend assembles the final prompt from the mode — never freehand it. |
| Identity/face consistency across a shoot | chain `higgsfield-soul-id` |
| Marketplace listing compliance | **out of scope** — `higgsfield-marketplace-cards` is not a design tool |

- **Output is a hosted URL, not a local file** — on either path. To use a generation in a page you must explicitly download it into the repo's asset directory and reference the local path. **Never hotlink the hosted URL into shipped markup.**
- **Generated imagery is subject to the same floor.** It must obey the active style's **Imagery** aspect and the brand. Check: text-over-image contrast, no AI-palette tells the registry would flag, responsive `srcset`, real alt text. Run `detect.mjs` over the markup that consumes it.
- **Present a small set of options and let Nate pick.** Do not auto-adopt a generation.
- **Async/latency reality.** Images return fast; **video is 90s+**. Poll with `job_status`; do not block on a video job unless Nate asked for video.
- **Auth may be pending.** On an auth/unauthorized error, tell Nate to run `claude mcp login higgsfield` and stop cleanly. Do not retry-loop.
- **Generation spends Higgsfield credits.** Generate a small, deliberate set — do not sweep many variants to cover for an unclear brief.
- **Nate's local media as input** — call `media_upload_widget`; MCP tools cannot read Claude chat attachments.

#### The edit fence (phase 4)

- **Presentation only.** CSS / Tailwind classes, `className`s, spacing / grid / flex wrappers, component *arrangement*.
- **Never** touch copy, data, props/logic, routing, or API calls.
- Structural markup changes are allowed **only when purely presentational**, and must be called out as such.
- **Content and data must be provably unchanged** — rendered text and displayed values identical before and after. You may restyle a number; you may never change it. This is the cheap check that proves you stayed in your lane.

#### Objective gates (hard fails)

Impeccable is the **authority** on every threshold below. Cite the file; do not copy the numbers here or into `STYLE.md` — copied numbers drift.

| Gate | Authority |
|---|---|
| Body / large-text contrast, control + focus-indicator contrast | `$IMP/reference/craft-floor.md` · `$IMP/reference/colorize.md` |
| No overflow, overlap, or clipping at any breakpoint | `$IMP/reference/adapt.md` · `$IMP/reference/audit.md` §4 |
| Layout holds at mobile **and** desktop | `$IMP/reference/adapt.md` |
| Touch-target size, pointer/hover assumptions | `$IMP/reference/adapt.md` |
| Keyboard, touch, and tab order agree with visual order | `$IMP/reference/layout.md` Verify · `$IMP/reference/audit.md` §1 |
| Long text, empty states, and dynamic content do not break structure | `$IMP/reference/layout.md` Verify |
| Type measure, scale ratio, tracking floor, weight steps | `$IMP/reference/typeset.md` |
| Motion duration, easing, reduced-motion | `$IMP/reference/animate.md` |
| Spacing scale and rhythm | `$IMP/reference/layout.md` · `$IMP/reference/craft-floor.md` |
| Machine-enforced anti-slop and quality rules | `node "$IMP/scripts/detect.mjs" --json <target>` |

#### Evidence discipline

- **The squint test.** With detail blurred, the primary element, the secondary element, and the major groups must still read in order. If they don't, the composition failed regardless of what the tokens say.
- **Cite visible evidence.** Point at what in the rendered result supports the claim. **No self-grading by assertion** — a bare "yes" is not verification, and "looks good" is not a finding.
- **Batched verification, ceiling of two rounds.** Desktop and mobile in one round. Fix everything the round shows, confirm in at most one more. Never a screenshot loop.

---

## `STYLE.md` — the contract artifact

Lives at the **project repo root**, next to `PLAN.md` / `PROGRESS.md`. **Committed.** It doubles as (a) this skill's phase state and (b) a contract `dt-ui` and `dev-team` can read and obey without knowing `~/os` exists.

**It records selections as pointers.** It never copies craft, style, or brand content — one source of truth, in `~/os`. Anyone who needs the detail follows the pointer.

```markdown
---
mode: website             # website | app → ~/os/knowledge/library/design-language/modes/<mode>.md
style: <style-name>       # → .../styles/<style-name>/README.md
brand: <brand-name>       # → .../brands/<brand-name>.md
locked: YYYY-MM-DD        # date style + composition were chosen
---

# Design contract — <project>

Selections are pointers into `~/os/knowledge/library/design-language/`.
Nothing from those files is copied here. Impeccable owns every technical
threshold — do not restate ratios, sizes, or timings in this file.

## Composition
- **Shell** — sidebar | top nav | none; what persists across routes
- **Entry view** — split hero | centered stack | table-first | feed | dashboard grid
- **Focal hierarchy** — what dominates, what supports, what recedes
- **Density** — sparse | comfortable | dense (per the mode's density dial)
- **Grid** — columns, max-width, alignment spine

## Where it lives in code
- Tokens / theme: `<path>`
- Font loading: `<path>`
- Shared layout components: `<path>`

## Decisions
| Date | Decision | Why |
|---|---|---|

## Out of scope
<surfaces this contract does not govern>
```

---

## Inputs / arguments

- `phase=1|2|3|4` — override the inferred phase.
- `mode=app|website` — skip the mode question.
- `style=<name>` — skip phase 1 with an explicit pick.
- `brand=<name>` — skip the brand question.
- `target=<route or file>` — the surface to work on.
- `launch=<cmd>` `url=<url>` — dev-server command and app URL for live mode.

All optional. Anything not passed is asked once, up front, then not asked again mid-phase.

## Examples

- `/design` in a repo with no `STYLE.md` → confirms mode + brand, renders five styles as full-width stacked sections, serves it, waits for Nate's pick.
- `/design phase=2` → five structural takes on the real first page, style tokens identical.
- `/design` in a repo with a complete `STYLE.md` → phase 4: baseline screenshot, then live mode on the running dev server.
- `/design try some hero imagery` → phase 4 Higgsfield path (`mcp__higgsfield__generate_image`), generating options that obey the active style's Imagery aspect.

## Notes & gotchas

- **This skill is interactive.** There is no overnight mode, no autonomous convergence, no diminishing-returns test, no iteration cap, no decide-and-log fork resolution. Taste has no gradient to descend — Nate decides. If you cannot ask, stop and ask.
- **Do not merge or push without sign-off.** Normal branch hygiene, not a special gate.
- **The catalog is populated** (as of 2026-07-27): `craft.md` re-extracted 2026-07-26 against 35 references, seven styles under `styles/` each with a README plus its reference shots, both mode files written. Phase 1 can run — six styles qualify for `website`, four for `app`. Re-check before promising output, but the old "empty catalog" blocker is gone.
- **Both brand files predate the reference-not-rules schema** and still carry prohibitions, restated Impeccable thresholds, and (in `nate-personal.md`) an exclusionary style-pairings table. Rewrites are pending in their own sessions. Until then, read them per preflight step 4 — reference only — and ignore the `avoid` rows.
- **Impeccable's own `/impeccable` skill will try to route you into `new-work` / `shape` / `critique`.** Do not follow it there. Load the specific reference files directly.
- **Never repair Impeccable artifact drift as a side effect.** A `CONTEXT_STALE` finding is reported, not acted on.
- `.design/` is scratch. Add it to `.gitignore`. `STYLE.md` is the only committed output of phases 1–3.

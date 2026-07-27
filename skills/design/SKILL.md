---
name: design
description: Use when Nate wants to design, style, or visually improve a page, app, or site — starting from "here's what I'm building and a few screenshots I like" and ending at a page he can tweak live. Triggers on "/design", "design this page", "restyle X", "make this look right", "build me a landing page", "try some imagery for this", or any request to work from his inspiration library. Interactive — Nate makes every taste call.
---

# design

Nate is in the room. Show him options; he picks. Never rank them unless he asks.

This is a roadmap, not a procedure. Skip steps that don't apply, reorder when the work
calls for it, stop when he's happy. Nothing here should stop him from seeing a draft.

## The one rule

**Reference images go to the model as images.** `Read` the actual PNG so it is in
context. A description of a screenshot is not a screenshot — that substitution is the
single thing that makes output generic.

## The library

`~/os/knowledge/library/inspiration/<look>/` — screenshots grouped by look, each folder
a `README.md` with a vocabulary line, tags, and source URLs.

It is open. Glob it; never assume a fixed catalog. If Nate pastes a URL or drops a
screenshot mid-session, that's a reference too — use it, and offer to save it into the
library on the way out.

## Four slots

Every draft prompt carries all four. If Nate gave you fewer, ask for what's missing in
one short message, then build — don't interview him.

| Slot | What goes in it |
|---|---|
| **Aesthetic** | The family of design. A look name from the library, or his words. |
| **Reference** | Actual image files, `Read` into context. URLs count — fetch or browse them. Matching the *feel*, not the content. |
| **Intent** | What is this, who is it for, what should they do when they land. This drives everything downstream — layout, density, how hard the CTA works. Never skip it. |
| **Guardrails** | What never to do. Starting set: no Inter / Geist / Space Grotesk / Plus Jakarta, no purple-blue gradients, no 3D SaaS blobs, no colored side-tab borders on cards, no eyebrow pill above the headline, no single accent-coloured word inside an otherwise plain headline. The last two are this wave's tells and they date a page instantly. Nate overrides freely; add whatever this project needs. |

## Wide net, then narrow

Everything comparable side by side, one page, one server. Draft in `.design/` at the
repo root (gitignored) as standalone HTML, whatever the real app is built with — port
the winner in afterward. `file://` is blocked in the browser tooling, so serve it:
`python3 -m http.server 8123 --directory .design`.

Build an `index.html` that shows the current round in a labeled grid of iframes, each
one scaled down and clickable through to full size. Same harness every round; only the
contents change.

**Round 1 — five drafts, five directions.** Write **five separate briefs**, not one brief
rendered five ways. Each direction gets its own aesthetic, its own reference image(s) read
into context, its own hero treatment, and its own headline. Say in one line why each fits
the intent.

The failure mode is one design in five skins — same nav, same headline, same button pair,
same card row, different accent colour. Test for it: if you could lift the top of draft 2
into draft 4 and not notice, you have not made five drafts. No two may share a —

- **Composition.** Where the headline sits (centred, hard left, split, off-grid), whether
  the hero is full-bleed or framed or has no image at all, whether there is a top nav at
  all, how the first screen divides between type, image, and empty space.
- **Headline.** The words are design, not content. Each aesthetic argues for the product
  in its own voice — write a different headline per direction, not one headline restyled.
- **Type pairing.** A different display face per draft, and don't default to the same
  neutral sans for body copy every time.
- **Palette,** including whether it is light or dark. Don't ship five dark drafts.

Each draft is a whole page — hero, body, footer — not a mood board.

**Round 2 — three variants of the winner, varying the body.** Hero stays. Move what's
under it: an index rail that tracks scroll, framed sections, a denser column, a ledger.
References apply here too — if Nate likes how some site's body reads, take that URL as
input the same way. If the three still read as the same page, the direction was too thin
to develop — say so and go back to round 1 rather than varying harder.

**Round 3 — imagery.** See below.

**Round 4 — tweaks panel.** See below.

Then fine adjustments: transitions between hero and body, load-in weight and sequence,
copy. Small, named, one at a time.

## Placeholder-first imagery

There may be no image generator wired up. That never blocks a draft — but the stand-ins
are **not grey boxes with a caption**. A labelled rectangle makes every draft read as the
same wireframe in a different accent colour, which is the exact tell you are trying to
escape.

**Draw the stand-in.** CSS or inline SVG, built to carry that direction's aesthetic: a
contour plot, a dither field, a ridgeline silhouette, a drift of numerals, a halftone, a
blueprint grid, an oversized type specimen. It should be recognisable as *that look* from
across the room. A few dozen lines buys most of the character of the draft.

Keep the generation brief in the markup, never printed into the layout:

```html
<figure class="hero-fig" data-image-intent="Aerial of a fog-filled valley at dawn, one
  ridgeline entering from the right third, cool blue-grey, heavy negative space top-left
  for the headline. 16:9.">
  <svg viewBox="0 0 1600 900" aria-hidden="true"><!-- drawn stand-in --></svg>
</figure>
```

Subject, mood, composition, aspect ratio. Specific enough that a generator fills it from
that text alone. "Hero image" is not an intent. The intent is metadata for the swap step —
on the page it reads as scaffolding, so it stays in the attribute.

**Swapping in real images.** Once the direction is locked — never before — offer it. If
the Higgsfield MCP is connected, `mcp__higgsfield__generate_image` takes the intent
straight from `data-image-intent`; any other generator works the same way. Generate four
per slot, drop them into the slot side by side, Nate picks, then offer variations of the
pick. Wide net then narrow, one level down. Find the slots with:

```bash
grep -ro 'data-image-intent="[^"]*"' .design/
```

## The tweaks panel

The payoff. Once the direction is locked, Nate iterates visually instead of asking for a
rebuild per adjustment.

Copy `tweaks.js` from this skill into `.design/`, add `<script src="tweaks.js"></script>`,
and declare the controls the page actually uses:

```html
<script>window.TWEAKS = [
  { var: '--font-display', label: 'Heading font', type: 'select',
    options: ['"Instrument Serif", serif', '"Bricolage Grotesque", sans-serif'] },
  { var: '--accent', label: 'Accent', type: 'color' },
  { var: '--type-scale', label: 'Type scale', type: 'range', min: 0.8, max: 1.4, step: 0.01 },
  { var: '--motion', label: 'Motion weight', type: 'range', min: 0, max: 2, step: 0.05 },
]</script>
```

Two requirements, or the panel does nothing: the page must be styled off those custom
properties (`font-family: var(--font-display)`, `font-size: calc(1rem * var(--type-scale))`),
and every face listed in a font control must actually be loaded by the page.

Be aggressive about what you expose — fonts, sizes, accent, spacing, radius, motion
weight, reveal distance, and anything else in the page that was a taste call. `Copy CSS`
returns a `:root` block; when Nate pastes it back, bake those values into the source.

Check it works: open the page, move the accent control, confirm the page repaints
without a reload.

## Anti-slop by detection

Run the detector over the drafts **before** showing them.

```bash
IMP=$(ls -d ~/.claude/plugins/cache/impeccable/impeccable/*/skills/impeccable | sort -V | tail -1)
node "$IMP/scripts/detect.mjs" --json .design/
```

JSON on stdout, exit 2 means findings. `--scope type` / `--scope layout` narrow it.
Fix what it catches. Verify each finding in context first — a rule can fire on something
that is deliberate and right here; when it does, say so in a line and move on.

All of Impeccable's verbs are available — `typeset`, `colorize`, `layout`, `animate`,
`adapt`, `bolder`, `quieter`, `distill`, `delight`, `overdrive`, `polish`, `harden`,
`audit`, `optimize`, `clarify`, `onboard`, `extract`, `document`, `shape`, `critique`,
`init`, `live`. Read `$IMP/reference/<verb>.md` and follow it. Nothing here is off
limits; pick whichever actually fits the ask.

Most are targeted passes on a design that already has a direction. `shape`, `critique`,
`init` and `craft` are the ones that reopen creative direction — reach for them at the
start, or when Nate wants the question reopened, rather than as a mid-flow reroute.

## STYLE.md

When the direction locks, leave about ten lines at the repo root so the next session and
`dt-ui` don't start over:

```markdown
# Style — <project>
Look: <name> · refs: <paths and URLs actually used>
Fonts: <display / body, and where they're loaded>
Tokens: <file that owns the custom properties>
Intent: <one line — what it is, who for, what they do>
Never: <the guardrails that stuck>
```

Pointers, not copies. Update it when something changes; delete a line when it stops
being true.

## Notes

- Don't rank the options. "These five, here's what each is doing" — then wait.
- Don't gate. No round has to complete before he sees pixels.
- Two rounds of screenshot-and-fix is the ceiling on any one build. Nate's eyes are the
  loop; yours aren't.
- Components, when a specific button or pricing block needs an idea: 21st.dev has copy-
  paste prompts. Same wide-net move at component scale.

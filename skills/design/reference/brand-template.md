# Brand file template — a reference skin for `design`

One file per brand/context (portfolio, bcns, or a specific client). Hand-authored from
research, example screenshots, and existing surfaces.

**A brand file is reference, not rules.** It exists to convey what a brand *is like*, or
what a new brand should *try to match* — colour schemes, register, closest existing styles.
It does not constrain what the design skill may produce. Impeccable owns every technical
threshold and the anti-slop registry; the active style README owns genre; `craft.md` owns
invariant judgment. A brand file that starts issuing prohibitions has stopped being useful
and started blocking phase 1.

Final home: `~/os/knowledge/library/design-language/brands/<brand>.md`

## Authoring rules

1. **Describe, don't forbid.** "The register is technical rather than lifestyle" — not "no
   photography." A direction bends around a good idea; a ban blocks it before you see it.
2. **Never restate Impeccable.** No contrast ratios, type-scale ratios, spacing values,
   motion timings, or registry rule names as constraints. Cite the file if you must point
   at it. A copied number goes stale and someone will trust it.
3. **Never restate `craft.md`.** It merges on every run regardless.
4. **Don't duplicate live tokens.** If the brand is implemented in code, point at the file
   and let code stay the record. Carry hex values only when no implementation exists yet.
5. **Style affinities never exclude.** Note which genres are closest; never mark one
   "avoid." Phase 1 needs five qualifying styles to run at all, and brand-level exclusions
   are the fastest way to starve the slate below that.
6. **Keep it scannable.** If a section has grown past a screen, it's holding decisions that
   belong somewhere else.

---

# Brand: \<name\>

> **Reference, not rules.** Impeccable owns every technical threshold and the anti-slop
> registry; the active style README owns genre. Nothing here overrides either — if a value
> below collides with them, the value loses.

## Who it's for

The audience this look serves, and — in one line — what they need to believe when they land.

## Feeling

Three words.

## Anchor

One sentence: the minimum that must hold for it to still be recognisably this brand.
Everything not named here is movable. Keep this genuinely minimal — the anchor is what
survives a redesign, not a description of the current surface.

## Palette

The scheme in words first (field temperature, how many accents, what earns one), then
values. If the brand ships in code, point at the token file instead of copying it. Note
which values are load-bearing and which are open to movement.

## Type

Families and character — what the type should *feel* like, and the hierarchy mechanism
(weight vs. size). No scale ratios; Impeccable owns those. If a current family is a
replacement candidate, say so and why.

## Imagery & texture

Register and direction: what kind of imagery, sourced how, in what treatment. Iconography
style. Any signature texture, and whether it's identity or just current implementation.

## Voice (visual)

How the brand speaks through layout — bold vs. understated, dense vs. airy, where character
is spent and where things recede.

## Style affinities

Closest fits, as an aid to the phase-1 pick — never a filter on it.

| Style | Note |
|---|---|
| `<style>` | why it's close |

## References

Corpus files under `../styles/`, URLs, or live token paths — one line each on what it
demonstrates. Store any new screenshots alongside the corpus, not loose in `brands/`.

## Questions from system audit — 2026-07-27

**Q: Should the `design` skill push harder toward Impeccable's direction-setting verbs (`shape`/`critique`/`init`) instead of linter-only usage?**
Context: The 2026-07-27 `ai-usage-optimizer` audit (`2026-07-27_16-31-54_nateseluga_b5e46c93.md`) found Impeccable is being used almost entirely as a post-hoc lint pass (`detect.mjs`), not for the concept-derivation/direction-contract workflow the `design` skill's own text says to "reach for... at the start." Nate's own audit ties this directly to a "generic AI slop" complaint about design output.
Options: (a) tighten `skills/design/SKILL.md` to make the deeper-verb entry point more prominent/harder to skip, or (b) this is a usage habit, not a skill-text gap, and no file change would fix it.

Using Impeccable for concept-derivation/direction-contract workflow is what we want. Design is still a work in progress, but it seems like it doesnt use the toolkit that we have available to its fullest potential (checking after with Impeccable rather than injecting particular Impeccable skills). I also want future uses of design to specifically ask for a reference image and reference image family for generation if this can improve performance.

## Questions from system audit — 2026-07-27

**Q: Are `grill-me`, `handoff`, and `teach` supposed to be invisible to the model's auto-loaded skill list?**
Context: All three skill folders have real, non-stub `SKILL.md` content and `disable-model-invocation: true` — same flag as `research-partner`, which DOES appear in this session's auto-loaded skill listing. Only `grill-me`/`handoff`/`teach` are missing from it. This isn't hypothetical: in session `2026-07-27_19-54-35_hitter-embedding_c3c7b664.md` the assistant told Nate "there's no `/handoff` skill installed," and he had to invoke it manually before it worked. Since `disable-model-invocation` doesn't explain the gap (research-partner has it too and still lists), something else is excluding these three specifically.
Options: (a) it's a stale/misconfigured registration for just these three — worth checking `~/.claude/skills` symlink resolution or a frontmatter field difference — or (b) it's expected for some reason not visible from file content alone, and the false-negative above was a one-off harness glitch.

---

**Q: Is `/research-review`'s phase-boundary suggestion miscalibrated for how the hitter-embedding project actually runs?**
Context: Across `2026-07-27_14-38-38_hitter-embedding_4f5a6610.md` and `2026-07-27_19-54-35_hitter-embedding_c3c7b664.md`, the proactive suggestion to run `/research-review` at a phase boundary was raised and declined 7 times combined in one day.
Options: (a) the skill's suggestion cadence is too aggressive for this project's actual phase granularity and should be dialed back or made less proactive, or (b) phases genuinely aren't closing yet and every decline is correct — no change needed.

---

**Q: Should the `design` skill push harder toward Impeccable's direction-setting verbs (`shape`/`critique`/`init`) instead of linter-only usage?**
Context: The 2026-07-27 `ai-usage-optimizer` audit (`2026-07-27_16-31-54_nateseluga_b5e46c93.md`) found Impeccable is being used almost entirely as a post-hoc lint pass (`detect.mjs`), not for the concept-derivation/direction-contract workflow the `design` skill's own text says to "reach for... at the start." Nate's own audit ties this directly to a "generic AI slop" complaint about design output.
Options: (a) tighten `skills/design/SKILL.md` to make the deeper-verb entry point more prominent/harder to skip, or (b) this is a usage habit, not a skill-text gap, and no file change would fix it.

---

**Q: Is the os-evals "Hard-task batch #1" still awaiting approval, or has it been resolved without the memory file being updated?**
Context: `knowledge/memory/project-os-evals-standards.md` records two draft tasks (`pathguard-resolver`, `rangestats-engine`) as "awaiting Nate's per-check approval before promotion," logged 2026-07-11. It's now 2026-07-27 (16 days later) with no update.
Options: (a) still genuinely pending — leave as is, or (b) already approved/promoted or abandoned since, and the memory file should be updated to reflect the actual outcome (I can't tell which from the worktree alone).

---

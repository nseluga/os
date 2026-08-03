## Questions from system audit — 2026-08-03

**Q: Is the two-layer MAP.md / lane-plan redesign still live, and should `projects/os` reflect it?**
Context: The 2026-08-02 `/grill-me` session (`2026-08-02_14-59-12_nateseluga_d38ebb8c.md`) opened a full redesign of the plan → progress → dev-team-auto workflow for a 2–3 person team: `MAP.md` on main declaring lanes with `owns:` globs, lane PLAN.md generated per branch and never merged back. You answered Q1 ("c") and the session stopped mid-Q2. Nothing landed in `~/os` — no skill, no framework, no branch. Meanwhile `projects/os/README.md` still has `next_step` pointing at the project-dashboard v4 build.
Options: (a) resume the grill and spec it out, (b) it's parked — say so and I'll leave `next_step` alone, (c) it's dead, drop it.

working on it but in a new branch so that i can migrate only when i want to

---

**Q: Should answered questions be cleared from needs-context.md?**
Context: Your answer to the 2026-07-27 design/Impeccable question sat in `needs-context.md` for a week and was never converted into anything actionable — this run picked it up only because it re-read the file. The skill has no step that drains answered questions back into `review.md`.
Options: (a) add a Phase 1.5 to `/improve-system` that converts answered questions into review items and clears them, (b) leave it manual — the file is short enough to eyeball.

yes, also make sure that the improve-system skill understands what needs-context.md is (a place for changes that require more information before suggesting a fix or change)

---

## Questions from system audit — 2026-08-03 (Phase 2)

**Q: OK to remove the stale `storm-research-skill` worktree and its local branch?**
Context: `~/os/.claude/worktrees/storm-research-skill` is a git worktree on local branch `worktree-storm-research-skill` (commit `d8350e9`, "Add storm-research skill"), last touched 2026-07-29. Its working tree is clean (nothing uncommitted). `skills/storm-research/SKILL.md` is byte-identical between that branch and `main` — the skill already landed on `main` some other way — but the branch is otherwise 71 files / ~3,100 lines behind `main` (predates the higgsfield skills, `prototype`, and most current memory files). It's dead weight: not merged, not ahead, superseded. Remote `origin/worktree-storm-research-skill` still exists as a backup. Not auto-removing per the git safety protocol (destructive git ops need explicit go-ahead).
Options: (a) remove the worktree (`git worktree remove`) and delete the local branch (`git branch -D`) — remote copy stays as a safety net, (b) leave it, (c) delete the remote branch too.

---

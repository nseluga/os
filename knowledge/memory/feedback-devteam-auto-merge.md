---
name: feedback-devteam-auto-merge
description: dev-team-auto must merge worktree branch back to working branch at the end — skill has been updated to do this automatically
metadata:
  type: feedback
---

After a dev-team-auto run, the worktree branch (e.g. m0-foundation) must be merged back into the working branch (e.g. overnight-build) before shutting down. The skill now does this automatically in the Shut Down step.

**Why:** Without the merge, all built code is stranded in `.claude/worktrees/` and the working branch only has PLAN.md/PROGRESS.md updates — user discovered this after the first overnight run.

**How to apply:** If a past overnight run left a worktree branch unmerged, run `git merge <worktree-branch>` from the main repo checkout. Going forward the skill handles this. The overnight-build branch is a sufficient safety net — no additional backup needed before the merge.

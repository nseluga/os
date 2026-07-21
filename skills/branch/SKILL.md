---
name: branch
description: Create a new git branch from main and enter an isolated worktree. Use when the user says "/branch <name>", "new branch", "start a branch", or "spin up a branch for X". Fast path to isolated feature work.
---

# Branch

Create a feature branch off the latest main and enter an isolated worktree — the standard setup before any non-trivial change.

## Steps

### 1. Parse the branch name

Take the branch name from `$ARGUMENTS`. If none provided, ask for one (one word/phrase is enough). Normalize it to kebab-case if the user types spaces.

Suggest a prefix if the context is clear:
- `feat/` — new feature
- `fix/` — bug fix
- `wip/` — exploratory / not ready to PR
- `chore/` — housekeeping

If the user already included a prefix, use it as-is.

### 2. Sync main

```bash
git fetch origin
```

Check whether the repo's default branch is `main` or `master`: `git symbolic-ref refs/remotes/origin/HEAD | sed 's|.*/||'`.

### 3. Create the branch

```bash
git checkout -b <branch-name> origin/<default-branch>
```

If the branch name already exists locally, append `-2` and notify the user.

### 4. Enter worktree isolation

Use `EnterWorktree` with `name: <branch-name>` so edits in this session are isolated from the main checkout and any other parallel jobs.

### 5. Confirm

Tell the user: the branch name, the base it was cut from, and that the session is now in an isolated worktree. Remind them `/ship` will commit + push + open a PR when ready.

## Arguments

- `$ARGUMENTS` — the branch name (required). Everything after `/branch` is the name; spaces are replaced with `-`.

## Examples

- `/branch add-auth-middleware` → creates `feat/add-auth-middleware` (or `add-auth-middleware` if user already prefixed)
- `/branch` → asks for a name first

## Notes

- Always cuts from `origin/<default>`, not local HEAD — avoids accidentally branching off stale local state.
- Does not push the branch until `/ship` is called — no empty remote branch clutter.
- If already in a worktree, still creates the branch but skips `EnterWorktree` (already isolated).

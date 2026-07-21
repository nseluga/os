---
name: ship
description: Stage, commit, push, and open a PR in one command. Use when the user says "/ship", "ship this", "commit and push", or "get this out the door". Handles the full git workflow from dirty working tree to open PR.
---

# Ship

Stage everything, commit with a generated message, push, and open a PR — or update the existing one. One command to get code out the door.

## Steps

### 1. Check state

Run `git status --short` and `git log --oneline origin/HEAD..HEAD 2>/dev/null || git log --oneline -5`.

- **Nothing staged or unstaged + no unpushed commits** → tell the user there's nothing to ship and stop.
- **Unpushed commits but no new changes** → skip to step 4 (push only).
- **Changes present** → continue.

### 2. Stage

Run `git status --short` and scan for likely-sensitive files (`.env`, `*.pem`, `*.key`, `credentials*`, `secrets*`). If any are untracked/modified, **list them and ask the user** whether to include them before staging.

Then stage everything else: `git add -A`.

### 3. Commit

Generate a commit message from `git diff --cached`:
- First line: imperative, ≤72 chars, no period.
- Skip the body unless changes span multiple concerns.
- Append `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`.

Show the message to the user for a quick confirm (one-liner approval, not a full review gate). Commit on approval.

### 4. Push

`git push -u origin HEAD`. If the push is rejected (non-fast-forward), report it and stop — do not force-push.

### 5. PR

Check for an existing PR: `gh pr view --json url,state 2>/dev/null`.

- **No PR:** `gh pr create` with a title from the commit message and a short body summarizing the diff. Use `--draft` if the branch name starts with `wip/` or `draft/`.
- **PR already open:** print the PR URL and say it's been updated.
- **Merged/closed PR:** create a new one.

Report the final PR URL to the user.

## Arguments

- `$ARGUMENTS` — optional commit message override. If provided, use it verbatim instead of generating one (still show it for confirmation).

## Notes

- Never `--force` push.
- Never stage `.env`, key files, or credential files without explicit user approval.
- If on `main`/`master` directly, warn the user and ask before pushing — they probably want a branch.
- `gh` must be authenticated (`gh auth status`). If not, tell the user to run `gh auth login`.

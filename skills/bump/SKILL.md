---
name: bump
description: End-of-session closer — bump the project's os README (frontmatter + "Where it stands") and offer to save any notable memory from the session. Use when the user says "/bump", "wrap up", "end of session", "let's close out", or "what should we save from this session".
---

# Bump

**Related:** [[_TEMPLATE]]

Close out a session: bring the project's `~/os` index up to date and surface anything worth remembering. Local `LANE_PROGRESS.md` is not this skill's job — the dev team writes that as it runs.

## Steps

### 1. Orient

Run `git log --oneline -10` in the current repo to see what landed this session.

### 2. Bump the os README

Match the current repo path against the `repo:` field in each `~/os/projects/*/README.md`. No match → say so and skip to step 3.

Read `~/os/projects/_TEMPLATE.md` and the matched README. Propose updates in that shape:

- **Frontmatter:** `last_active` → today, `next_step` → the single most useful next action, plus `status`/`priority` if they actually changed.
- **"Where it stands":** a few sentences on current state — done, in flight, blockers. No dated entries, no task lists (those live in the repo's LANE_PROGRESS.md / LANE.md).
- Fix any drift from the template while you're there (missing fields, prose restating frontmatter).

Show the diff, ask once, then write.

### 3. Offer memory

Review the session for anything worth persisting across conversations: a preference or correction the user gave, a non-obvious decision and its why, a repeatable pattern. Skip anything the code, git history, or CLAUDE.md already records.

List candidates one line each with the type (`user`/`feedback`/`project`/`reference`), or say "nothing worth saving." Write only what the user nods at — a fact file in `~/os/knowledge/memory/` plus a `MEMORY.md` index line. If a candidate is really a reusable process, say it belongs in a skill instead.

### 4. Report

Two lines: what the README now says, what (if anything) was saved.

## Arguments

- `$ARGUMENTS` — optional focus (e.g. "skip memory, just the README"). Apply as an override.

## Notes

- Both writes are offer-first — never touch `~/os/projects/` or `~/os/knowledge/memory/` without confirmation.
- Nothing notable happened? Say so and stop.

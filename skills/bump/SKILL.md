---
name: bump
description: End-of-session closer — update PROGRESS.md, offer to sync the os project index, and save any notable memory. Use when the user says "/bump", "wrap up", "end of session", "let's close out", or "what should we save from this session".
---

# Wrap

Close out a session cleanly: record what was done, keep the project index current, and surface anything worth remembering. Takes ~1 minute; replaces the "remember to update things" friction at the end of every session.

## Steps

### 1. Orient

Run `git log --oneline -10` (or equivalent for the current repo) to see what landed. Also check if a `PROGRESS.md` exists at the project root.

### 2. Update PROGRESS.md (if it exists)

Read `~/os/knowledge/frameworks/progress-md.md` and follow that schema exactly.

Summarize what happened this session under the relevant plan items: what was completed, what's in-progress, any blockers. Be specific — "added auth middleware" not "made progress on auth". Timestamp the entry.

If `PROGRESS.md` doesn't exist, **don't create it** unless the user asks. Not every project needs one.

### 3. Sync the os project index

Find the matching project under `~/os/projects/` by comparing the current repo path to the `repo:` field in each README. If a match is found:

- Show the user the current `last_active`, `next_step`, and `status` fields.
- Propose updated values based on what landed today.
- **Ask before writing** — one confirmation is enough ("update the os index?" → yes/no).

If no match, skip silently.

### 4. Surface memory candidates

Review the session for anything worth persisting across conversations:
- A preference or correction the user gave
- A non-obvious decision made (and why)
- A repeatable process or pattern discovered

List candidates briefly. For each, say whether it belongs in memory (user/feedback/project/reference) or should be a new/updated skill. Offer to write whichever the user nods at.

Don't save things the code or git history already records.

### 5. Report

One-paragraph close: what changed, what's next, what (if anything) was saved.

## Arguments

- `$ARGUMENTS` — optional focus area (e.g. "skip memory, just update progress"). Apply as overrides.

## Notes

- Step 3 is offer-first — never write to `~/os/projects/` without confirmation.
- Step 4 is offer-first — never write to `~/os/knowledge/memory/` without confirmation.
- If nothing notable happened (no commits, no decisions, no corrections), say so and skip steps 2–4.

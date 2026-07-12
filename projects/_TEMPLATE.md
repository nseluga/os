<!--
PROJECT README TEMPLATE / REFERENCE
Copy this into projects/<id>/README.md when adding a project, and keep existing
READMEs formatted this way. Claude: this is the canonical shape for every file in
projects/*/README.md.

Two parts:
  1. YAML frontmatter — machine-parseable, read by the project-dashboard. Keep the
     field names and value formats exactly as below.
  2. Body — human/Claude-facing. Lean. See "Body conventions" at the bottom.

This file (_TEMPLATE.md) is a reference, not a project — the leading underscore keeps
it out of the projects list.
-->

---
name: Human-Readable Name              # display name
status: active                         # active | in-progress | on-hold | complete
priority: high                         # high | medium | low
last_active: 2026-07-11                # YYYY-MM-DD. Dashboard prefers live git log; this is the fallback.
next_step: "One concrete next action." # quoted. The single most useful thing to do next.
repo: ~/path/to/repo                   # local path. Use `repo_note` instead if there is no local clone.
github: https://github.com/nseluga/repo  # full URL, or null if not on GitHub
summary: "One sentence: what this project is."   # quoted, one line
tags: [area, stack]                    # short list, e.g. [ml, baseball] or [full-stack, next.js]
---

## Where it stands

One short paragraph on the current state — what's done, what's in flight, any blocker.
This is what you update by hand after a work session (along with `last_active` and
`next_step` above). Keep it to a few sentences; the dated history lives in the repo's
local PROGRESS.md, not here.

## Run / verify

How to actually start it and check it works — concrete commands:

    cd <repo> && <run command>      # e.g. npm run dev  /  ./run.sh  /  python -m app
    <test command>                  # e.g. npm test  /  pytest

## Key files

- **Detailed trackers (local, gitignored):** `PLAN.md` (what's next) · `PROGRESS.md` (what landed)
- **Spec / standards:** `SPEC.md` · `STANDARDS.md` · `CLAUDE.md` (list whichever exist)
- **Authority docs:** any external plan/architecture doc this project defers to

<!--
BODY CONVENTIONS
- Keep it lean. The README is an index, not a log.
- "Where it stands" is a paragraph, not a changelog — no dated entries (that's local PROGRESS.md).
- No task lists here (that's local PLAN.md).
- Don't restate the frontmatter in prose.
- Omit any body section that doesn't apply (a tiny/complete project may only need "Where it stands").
- Optional frontmatter fields are allowed when useful, e.g.:
    repo_note: "Remote-only — no local clone"     # when there is no `repo` path
    mobile_path / backend_url / web_url            # deployment/entry-point pointers
-->

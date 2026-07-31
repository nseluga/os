---
name: feedback-project-readme-template-first
description: Read ~/os/projects/_TEMPLATE.md before editing any projects/*/README.md or running /bump
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7f847fdc-c9b0-47e3-ac4a-60f82b9b5750
  modified: 2026-07-31T03:10:55.148Z
---

Before editing any `~/os/projects/*/README.md` — and always as the first step of
the `/bump` skill — read `~/os/projects/_TEMPLATE.md`. It is the canonical shape
for every project README, and it constrains the body as much as the frontmatter.

**Why:** on 2026-07-30 I appended a multi-section body block (a numbered task
list plus supporting evidence) to `projects/bcns/README.md` instead of
condensing it into `next_step`. The template forbids exactly that — "the README
is an index, not a log", no task lists (those live in the repo's local
`PLAN.md`), and "Where it stands" is a paragraph rather than a changelog. Nate
reverted it and asked for the top-of-file next step only. Reading the template
first would have caught it; I wrote from memory of the file's general shape.

**How to apply:** read `_TEMPLATE.md`, then keep new detail in the frontmatter —
`next_step` (one concrete action, quoted), `last_active`, `status`/`priority`.
Body edits are for revising the existing "Where it stands" paragraph in place,
not for appending sections. Detailed reasoning, task lists, and dated history
belong in the real repo's `PLAN.md` / `PROGRESS.md`, not in the os index.

Related: [[feedback-project-readme-updates]], [[feedback-library-notes-format]].

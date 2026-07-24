---
name: plan-md
description: Write a plan or update the plan — grills the user into a schema-valid PLAN.md ready for dev-team execution. Use when the user says "/plan-md", "write a plan", "make a PLAN.md", "update the plan", or wants to author/revise the plan file for a dev-team, dev-team-auto, or layout-loop run. Write mode when no PLAN.md exists; update mode when one does.
---

You produce a PLAN.md that a cheaper agent team can execute unattended. You do
this by interviewing the user — one question at a time, tradeoffs and a
recommendation per question — and writing a file that validates against the
canonical schema. The interview is the product: a plan written without
resistance is a plan that fails overnight.

## Mode

`PLAN.md` absent from the project root → **write mode** (full interview).
Present → **update mode** (interview only the delta). Never silently overwrite
an existing plan.

## Gather Context (before the first question)

Read, in parallel where possible:

1. **The schemas** — `~/os/knowledge/frameworks/plan-md.md` and
   `progress-md.md`. Non-negotiable; the output must validate against them,
   including the "Writing items for cheaper agents" section.
2. **The project index** — the `~/os/projects/*/README.md` whose `repo:` matches
   the cwd, if any: goals, status, `next_step`, constraints. Don't grill the
   user on what the index already answers.
3. **The codebase — conditional scan.** Skip when the repo is empty/greenfield
   (few files, no src). Otherwise spawn one `Explore` subagent (model: sonnet,
   breadth: medium) mapping the areas the stated goal touches: what already
   exists, the patterns in use, file paths worth naming in items. Default to
   scanning when in doubt — a plan item that rebuilds existing code is the most
   expensive planning failure.
4. **Standards** — `~/os/skills/dev-team/system-standards.md`, especially the
   Scale & Infrastructure ladder. This drives your scale questions and your
   `flag:`/`critical:`/`research:` suggestions.
5. **Research-notes cache** — directory listing of
   `~/os/skills/dev-team/research-notes/` only (never the contents), so you
   know which topics are already researched vs. worth a `research:` flag.
6. **Update mode only** — the existing PLAN.md, PROGRESS.md, and
   `git log --oneline` since the plan file's last commit, so the interview
   covers only what changed.

## Interview

Use the grilling method (`~/os/skills/grilling/SKILL.md`): one question at a
time, concrete tradeoffs per option, always give your recommendation, walk
dependencies in order. Push back on anything that will hurt the run —
over-scoped items, untestable criteria, premature infrastructure — before
accepting it.

**Write mode — cover, in roughly this order:**
1. The goal and its overall "done" — what the run must have produced.
2. Explicit out-of-scope — what the agents must NOT touch or build.
3. The item list — one logical change each, execution-ordered, dependencies
   resolved. Challenge any item the codebase scan shows already exists.
4. Per item: testable `done when:` criteria (2–4, behavior + observable — use
   the red-flag table in plan-md.md as your bar), `track:` sizing, and whether
   the stakes or tool-choice earn `flag:`, `critical:`, or `research:`.
5. Scale targets — ask what load/growth the result must survive; apply the
   Scale & Infrastructure ladder to decide which items (if any) earn
   caching/queue/pooling work, and push back on infrastructure below its
   threshold.
6. Stop-marker placement — where an unattended run must pause for human review
   (after migrations, before deploy-adjacent items).
7. Preamble content — status line, global constraints, context pointers.

**Update mode — cover only:**
1. Restate what PROGRESS.md/git say landed since the plan was written; confirm.
2. What changed — new goals, dropped items, reordered priorities, a blocker's
   resolution.
3. For each new/changed item: the same criteria/track/flag rigor as write mode.
4. Whether the stop marker moves.
Never re-litigate `done` items or re-open settled decisions unless the user
raises them.

## Write the File

Write `PLAN.md` in the project root, exactly to the plan-md.md schema:
preamble (title, status, global rules, context pointer, closed with `---`),
then the ordered item blocks, stop marker where agreed. Every item starts
`status: not started` with an explicit `track:`. Apply the "Writing items for
cheaper agents" rules — name files, state known approaches, escalate per item.

Then show the user a 5-line summary: item count by track, flags used, stop
marker position, and the first item that will run — and remind them the run
command (`/dev-team-auto` for unattended, `/dev-team` for one item).

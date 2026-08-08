---
name: lane
description: Write or update a lane plan — grills the user into a schema-valid LANE.md ready for dev-team execution. Use when the user says "/lane", wants to write a new lane plan, or wants to update an existing LANE.md for a dev-team or dev-team-auto run.
---

**Related:** [[lane-md]] · [[map-md]] · [[agent-glossary]] · [[system-standards]] · [[skills/grill-me/SKILL|grill-me]]

You produce a LANE.md that a cheaper agent team can execute unattended. You do
this by interviewing the user — one question at a time, tradeoffs and a
recommendation per question — and writing a file that validates against the
canonical schema. The interview is the product: a plan written without
resistance is a plan that fails overnight.

## Mode

Two axes. Check both.

**Scope** — `MAP.md` at repo root?
- **Present → lane mode.** Plan one lane only. Take the lane name from the
  arg; if absent, list unassigned lanes from MAP.md and ask which.
- **Absent → solo mode.** Plan the whole repo. Everything below applies except
  the map-specific steps.

**Write vs update** — `LANE.md` at repo root?
- Absent → **write mode** (full interview).
- Present → **update mode** (interview only the delta).

Never silently overwrite an existing plan.

## Lane mode — before the interview

1. Read the lane's entry in MAP.md: `area:`, `owns:`, `depends on:`.
2. Read the repo-level `protected:` list.
3. Per `depends on:` edge:
   - **parallel** — locate the frozen contract + fixture it names. **Not found
     → stop and report.** The foundation pass is incomplete; planning against
     an unfrozen contract is what the map layer exists to prevent.
   - **sequenced** — check the predecessor's MAP_PROGRESS.md row. Not merged →
     **stop.** Nothing exists to build against; that is what sequenced means.
4. Not on a `lane/<name>` branch → create one off the foundation commit
   (`/branch` flow), then continue.

Scope every item to this lane. An item that must change a `protected:` path is
not a lane item — surface it as an amendment request in the summary instead.

## Gather Context (before the first question)

Read, in parallel where possible:

1. **The schemas** — `~/os/knowledge/frameworks/lane-md.md` and
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
   expensive planning failure. This scan is also what makes `parallel-group:`
   possible (below) — you need the real file map to know which items are
   actually disjoint.
4. **Standards** — `~/os/skills/dev-team/system-standards.md`, especially the
   Scale & Infrastructure ladder. This drives your scale questions.
5. **Update mode only** — the existing LANE.md, LANE_PROGRESS.md, and
   `git log --oneline` since the plan file's last commit, so the interview
   covers only what changed.

## Interview

Read `~/os/skills/grill-me/SKILL.md` before the first question and conduct the
interview by it: one question at a time, concrete tradeoffs per option, always
give your recommendation, walk dependencies in order, explore the codebase
instead of asking what the code already answers. Push back on anything that
will hurt the run —
over-scoped items, untestable criteria, premature infrastructure — before
accepting it.

**Write mode — cover, in roughly this order:**
1. The goal and its overall "done" — what the run must have produced.
2. Explicit out-of-scope — what the agents must NOT touch or build.
3. The item list — one logical change each, execution-ordered, dependencies
   resolved. Challenge any item the codebase scan shows already exists. After
   ordering, infer `parallel-group:` yourself from the codebase scan — do not
   ask the user. Tag consecutive items with a shared group value only when
   they touch no common file, schema, migration, or producer/consumer
   relationship; when the scan doesn't give you enough confidence to be sure,
   leave them ungrouped. Mention which groups you inferred in the item-list
   recap so the user can veto one, but don't turn it into a question.
4. Per item, three things — and **nothing about process**. Never ask which
   agents should run, which model, or how many attempts; that is the
   orchestrator's call at runtime, made against the real code.
   - Testable `done when:` criteria (2–4, behavior + observable — the red-flag
     table in lane-md.md is your bar).
   - **`risk:`** — you draft it, the user corrects it. Ask "what breaks if this
     is wrong, and how would you find out?" Push back on any line missing the
     second half: silent-vs-loud is the routing signal, and a line without it is
     unusable. Push back harder on a rating — "high" is not a risk, it's a
     self-assessment, and self-assessments inflate.
   - **`difficulty:`** — same treatment. "Hard" without a named open question
     becomes `low`. Genuinely competing designs, unfamiliar tooling, or fiddly
     behaviour are the only things that make an item difficult; stakes do not.
   - Speed/reliability criteria drafted **from the risk line**: when it reads
     silent or non-revertible, propose both; otherwise propose neither and say
     nothing about it.
5. Scale targets — ask what load/growth the result must survive; apply the
   Scale & Infrastructure ladder to decide which items (if any) earn
   caching/queue/pooling work, and push back on infrastructure below its
   threshold.
6. Stop-marker placement — where an unattended run must pause for human review
   (after migrations, before deploy-adjacent items).
7. Preamble content — status line, global constraints, context pointers.

**Justification sweep — required, and not a question.** Before writing the file,
walk the finished list once. Rules stated in a skill don't survive creative
flow; this is the step that enforces the ones above.

- Every `risk:` claiming a **silent** or **non-revertible** failure: name the
  specific mechanism by which it goes unnoticed. No mechanism → rewrite the line
  as loud. This is the check that matters — a silent-risk claim is the single
  most expensive thing the author can write, and it is the easiest to write by
  reflex.
- Every `difficulty:` above `low`: name what is actually architecturally open.
  No answer → `low`.
- Every speed criterion: name what grows with rows or rate. Nothing → cut it.
- Every item still open after the above: route it per "Settle it now".

Report what changed in one line per demotion. The user may veto any of them.

**Settle it now.** Route each still-open item by what kind of open it is:

- **"Which state model?" / "what should this look like?"** → offer `/prototype`
  (LOGIC and UI branches). If taken: run it, re-interview that item with the
  answer, name the decision as the item's approach, re-rate difficulty.
- **Can't phrase the question sharply yet** → move to `## Not yet specified`, cut
  from this round.
- **Competing architectures, no cheap experiment** → leave open.

Offer, never insist. Nothing from this step goes in the file as process — the
plan states what is open; the orchestrator picks the response.

**Update mode — cover only:**
1. Restate what LANE_PROGRESS.md/git say landed since the plan was written; confirm.
2. What changed — new goals, dropped items, reordered priorities, a blocker's
   resolution.
3. For each new/changed item: the same `done when:`/`risk:`/`difficulty:` rigor
   as write mode, and run the justification sweep over the new items only.
4. Whether the stop marker moves.
Never re-litigate `done` items or re-open settled decisions unless the user
raises them.

## Write the File

Write `LANE.md` in the project root, exactly to the lane-md.md schema:
preamble (title, status, global rules, context pointer, `## Not yet specified`
and `## Out of scope` where either has content, closed with `---`), then the
ordered item blocks, stop marker where agreed. Every item carries
`task:`, `done when:`, `risk:`, `difficulty:`, and `status: not started`. Apply
the "Writing items for cheaper agents" rules — name files, state known
approaches. Name no agents, models, or attempt counts.

**Lane mode — the preamble additionally carries, verbatim:**

```markdown
Lane: <name> — <area line from MAP.md>

Protected — do not edit. Stop and report if an item requires changing one:
  <protected: paths from MAP.md>

Frozen contracts — build and test against these; they will not move:
  <contract file + fixture path per `depends on:` edge>
Test against the fixture, not the producing lane. Do not wait for it to exist.
```

Then show a short summary:

- item count, split by **silent-risk vs loud-risk** and by **open vs low
  difficulty** — these two counts predict the run's cost better than anything
  else in the file
- `parallel-group:` pairs inferred (if any), and the stop marker position
- the first item that will run
- **estimated cost** — for each item, the team the orchestrator will likely
  pick (`agent-glossary.md`'s four quadrants) × ~125k tokens per spawn, listed
  heaviest first so the expensive items are vetoable at a glance

Then remind them of the run command: `/dev-team-auto` for unattended,
`/dev-team` for one item.

If the heaviest items aren't the ones the user would have named as the scary
ones, the risk lines are wrong — say so before they run it.

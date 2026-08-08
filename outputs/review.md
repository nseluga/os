<!-- Last applied: 2026-08-03 — 5 items applied, 1 remaining -->

## System Audit — 2026-08-03 (Phase 2)

<!-- Check the box next to each item you approve. Run /improve-system again to apply checked items. -->

- [x] **SKILL-EDIT: dev-team-auto's PROGRESS.md row format is stale**
  **Type:** skill-edit
  **Action:** edit `~/os/skills/dev-team-auto/SKILL.md` line 51
  **Rationale:** Today's session rewrote `knowledge/frameworks/progress-md.md`'s `dev-team-auto` row schema from `done [team] — [summary] — [hash]` to a plain-English sentence with no track/hash/VERDICT jargon. `dev-team-auto/SKILL.md` still tells the orchestrator to write the old format — the next autonomous run would violate the schema it's told to follow.
  **Content:**
  ```diff
  - - `PROGRESS.md` — append a dated entry for the item per the progress-md schema: `done [team] — [summary + commit hash]` or `blocked — [reason]` (never silently mark a blocked item done). One entry per item, written as soon as it finishes.
  + - `PROGRESS.md` — append a dated entry for the item per the progress-md schema: `done — [one plain sentence, user-facing]` or `blocked — [one plain sentence, no internals]` (never silently mark a blocked item done). One entry per item, written as soon as it finishes.
  ```

- [x] **SKILL-EDIT: improve-system needs a Phase 1.5 to drain answered needs-context.md questions**
  **Type:** skill-edit
  **Action:** edit `~/os/skills/improve-system/SKILL.md` — insert a new "Phase 1.5" section between Phase 1 (ends line 67) and the "## Phase 2 — Audit" header (line 69), and add one clause to the Phase 2.1 read list.
  **Rationale:** Nate approved this directly in `outputs/needs-context.md` today ("yes, also make sure that the improve-system skill understands what needs-context.md is"). Answers currently sit under their questions in `needs-context.md` with no step that ever reads them back — the 2026-07-27 design/Impeccable answer sat unconverted for a week; this run found two more (MAP.md lane-plan, this question itself) in the same state.
  **Content:**
  ```diff
  --- a/skills/improve-system/SKILL.md
  +++ b/skills/improve-system/SKILL.md
  @@ (end of Phase 1, before "## Phase 2 — Audit") @@
  +---
  +
  +## Phase 1.5 — Drain answered questions from needs-context.md
  +
  +`outputs/needs-context.md` holds audit questions Claude couldn't resolve alone.
  +Nate answers inline — any freeform text between a question's `Options:` line and
  +the closing `---` counts as an answer.
  +
  +**Run this phase every time, right after Phase 1.4.**
  +
  +1. Read `~/os/outputs/needs-context.md`. For each `**Q:**` block with an answer:
  +   - Answer names a concrete change → write it as a Bucket B item to
  +     `outputs/review.md` (Bucket A only if it also meets every Bucket A bar) using
  +     the normal item template, citing the question as rationale context.
  +   - Answer resolves the question with no file change needed (parked, confirmed,
  +     "leave it") → no review.md item; just drop the block.
  +   - No answer written yet → leave the block untouched.
  +2. Rewrite `needs-context.md` keeping only blocks with no answer yet. If every
  +   block had an answer, write an empty file (or delete it).
  +
  +---
  +
   ## Phase 2 — Audit
  ```
  Also add one line inside Phase 2.1's "Change log" bullet group (after the existing `~/os/outputs/change-log.md` bullet):
  ```diff
  +**Needs-context:**
  +- `~/os/outputs/needs-context.md` should already be drained by Phase 1.5 — if it still has answered blocks here, Phase 1.5 was skipped; drain it now before continuing.
  ```


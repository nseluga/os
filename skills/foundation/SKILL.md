---
name: foundation
description: Freeze the contracts lanes build against — pins each shared shape, writes FOUNDATION.md for the dev team to build, then locks protected: and cuts the integration branch. Reviewer-only, runs after /map and before any lane starts. Use when the user says "/foundation", "freeze the contracts", "set up the foundation", or has a MAP.md but no integration branch yet.
---

**Related:** [[map-md]] · [[lane-md]] · [[skills/map/SKILL|map]] · [[skills/grill-me/SKILL|grill-me]]

Reviewer-only. Runs **after `/map`, before any lane starts.** Turns the
`depends on:` edges in MAP.md into frozen, tested contracts on `main`.

Everything downstream depends on this: `/lane` refuses to plan a lane whose
contracts and fixtures aren't on disk.

## Mode

`FOUNDATION.md` at repo root?

- **Absent → author mode.** Interview the shapes, write the plan.
- **Present, items not all `done` → resume.** Report what's left; the build
  hasn't finished.
- **Present, all items `done` → lock mode.** Verify, set `protected:`, cut
  `integration`.

No `MAP.md` → stop. Run `/map` first.

---

## Author mode

### Read first

1. `MAP.md` — every `depends on:` edge, and the lanes on each side.
2. `~/os/knowledge/frameworks/lane-md.md` — the item schema. Output must validate.
3. One `Explore` subagent (sonnet, breadth medium): existing types, schema/
   migration layout, route conventions. Match what's there; don't invent a
   second style.

### Interview — pin every shape

One edge at a time. grill-me method: draft from the scan, user corrects, push
back before accepting.

For each `depends on:` edge, pin the **actual shape** — never a name:

| Edge | Pin |
|---|---|
| B reads data A writes | field names, types, **nullability**, and which are optional |
| B calls something A builds | signature or route + request/response + **error cases** |
| both read the same config | exact key names and their types |

**"A Lead type" is not a pinned shape. `Lead.enrichment: { company: string,
title: string, confidence: number } | null` is.**

**Push back hard on:**
- Any shape the user can't state without opening a file — that means it isn't
  decided. **Don't freeze a guess.** Sequence those lanes instead, and say so.
- Nullability left unstated. It is the single most common source of a contract
  that compiles in both lanes and fails at runtime in one.
- A shape that only serves one lane — that isn't a contract, it's that lane's
  business. Cut it; a short `protected:` list is the goal.

### Write `FOUNDATION.md`

Repo root, on `main`. Schema-valid items per `lane-md.md`.

- One item per contract. The pinned shape goes into `done when:` **verbatim** —
  field names, types, nullability, columns, status codes.
- Every item requires **a fixture that validates against the shape**. Without
  it, a consuming lane has to wait for its producer to exist, and the lanes
  serialize.
- `risk:` — silent. Every lane builds against this; wrong here is wrong
  everywhere at once and nothing surfaces it until merge.
- `difficulty: low` — the shape was decided in the interview.
- Order: schema/migrations first, then types, then route contracts.

Preamble: `# <Project> — Foundation`, plus one line — these are the contracts
every lane builds against; they land on `main` before any lane forks.

**The agent transcribes a shape you decided. It never designs one.** That is
why this is an interview and not a delegation.

### Then tell the user

```
/dev-team-auto        build + QA the contracts
/foundation           re-run to verify, lock protected:, cut integration
```

---

## Lock mode

Runs after the build. Makes the gate mechanical instead of a checklist.

1. **Verify each item.** Contract file exists, fixture exists, fixture
   validates against the shape, project typecheck/tests pass. Any failure →
   report and stop. Do not lock a contract that isn't proven.
2. **Set `protected:`** in MAP.md to exactly the contract + fixture paths, plus
   schema/migrations and config keys. Report anything added or dropped.
3. **Commit `main`.**
4. **Cut `integration`** from that commit.
5. **Hand out** one line per lane: `/lane <name>` and its assignee.

Report: contracts frozen, fixtures shipped, `protected:` paths, and the lane
start commands.

---

## Amendments

A lane hits a `protected:` path mid-round and reports it. Re-run `/foundation`
to amend:

- Change the shape on `main`, update the fixture, re-verify.
- Tell every live lane to rebase onto the new `main`/`integration`.
- Note it — a round with **zero** amendments froze too much; a round with many
  means the shapes weren't ready and lanes should have been sequenced.

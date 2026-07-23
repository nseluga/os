# Convergence Loop (per plan item)

The shared engine behind `/dev-team` and `/dev-team-auto`. A plan item is **done only when the QA gate passes** — the loop hammers one item until it works as specified or the attempt cap is hit. This file is the single source of truth for the loop. Sections marked **(shared)** apply to both orchestrators; **The loop** and everything after it define the `full`-track engine only.

## Track classification (shared)

Before running anything, pick a rigor track per item — how much of the team runs:

- If the item declares `track:` (`trivial` | `light` | `full`), obey it.
- Otherwise classify from the item's content:
  - `trivial` — only copy/text, docs, static config values, version bumps, or comments; no control-flow or data changes
  - `light` — logic confined to one file/function; no new module boundary, no schema/API/auth/money/data-path touch
  - `full` — everything else, and always for multi-file changes, new endpoints/schema/migrations, auth, money, or a `flag:` item
- When between two tracks, choose the heavier one. (An unattended run rounds *up* on any uncertainty — an under-gated change ships with no human to catch it.)
- Then run the matching path:
  - **trivial** → Engineer (or a direct edit) + the project's build/smoke check. No QA suite, no review, no fix loop.
  - **light** → Engineer → QA → fix-if-fail, with **MAX_ATTEMPTS 2** and **no review pass**. The orchestrator sets QA's gate mode.
  - **full** → the loop below, unchanged (MAX_ATTEMPTS 5).

`flag:` (Opus escalation) and `critical:` (Fable escalation — for items where a defect is catastrophic or irreversible: auth systems, cryptography, authorization, PII/PHI handling, financial transactions, production data integrity) are item-level markers that compose with any track above `trivial`. Use `critical:` when the blast radius of a missed defect makes Opus insufficient. `dt-ui` also composes with any track above `trivial`.

**`dt-analyze` runs by default, once, before the loop for any `full`-track item that spans multiple files** (and for any unfamiliar area on any track). Skip it only for single-file items. Its `analyze-report.md` map is then injected into every agent (see Spawn template) so no agent re-explores the codebase.

## Model & effort selection (shared)

Every agent is spawned with a **model** and an **effort** level. Model goes in the spawn template's `[MODEL]` slot. Effort is not a spawn parameter, so express it in the agent's prompt as a reasoning-depth directive / thinking keyword: **minimal** (none — mechanical work), **medium** (`think` — proportionate reasoning), **high** (`think hard` — reason through edge cases, alternatives, and failure modes first).

Starting model + effort by role (the escalation ramp in Efficiency rules raises these on repeated failure — they are starting points, not ceilings):

| Agent | Model | Effort | Why |
|---|---|---|---|
| `dt-analyze` | Sonnet (Haiku for its `Explore` fan-out, per its skill) | medium | broad mapping, not deep reasoning |
| `dt-engineer` — **light** track | Sonnet | medium | one file, bounded blast radius |
| `dt-engineer` — **full** track | Sonnet | **high** | build quality sets how many review/fix cycles you pay for later |
| `dt-engineer` — **full** track, open design space | Opus sketch (1 agent) → Sonnet implement | high | Opus buys the design decisions; Sonnet types the code — see Design exploration Tier 1 |
| `dt-engineer` / `dt-fix` — **`flag:`** item | Opus | high | security / money / data-path — worth the top tier |
| `dt-engineer` / `dt-fix` — **`critical:`** item | Fable | medium | catastrophic blast radius (see `critical:` above) — Fable catches subtle defects Opus misses |
| `dt-qa` | Sonnet | medium | keep the gate on a reasoning model: it judges coverage and classifies bug vs design-level (which steers the whole loop). **Never below Sonnet** — a weak gate passes broken code with false confidence. |
| `dt-review` — **full**, non-`flag:` | Sonnet | high | highest-value gate |
| `dt-review` — **`flag:`** item | Opus | high | maximum scrutiny where a missed defect is catastrophic |
| `dt-review` — **`critical:`** item | Fable | medium | maximum scrutiny on irreversible defect risk |
| `dt-fix` — bug-class fix | Sonnet | medium | applying an already-diagnosed fix |
| `dt-fix` — applying Critical/Important findings, or `flag:` | Opus | high | sensitive changes; match the builder tier |
| `dt-fix` — applying findings on a **`critical:`** item | Fable | medium | match the builder tier on catastrophic-risk items |

## Design exploration

**Before the first Engineer build only.** Gauge first — run the matching tier only when design space is open.

0. **Gauge the design space (all tiers).** One clearly-shaped approach (constrained by existing patterns, an established interface, or a plan-prescribed architecture) = **narrow**: skip exploration — the Engineer sketches and builds in one spawn, as today. Genuinely competing architectures (different data models, module boundaries, or consistency tradeoffs) = **open**: run the matching tier below.

**Tier 1 — full-track, non-`flag:`/`critical:`, open design space:** spawn **one** design-only subagent on `claude-opus-4-8`, effort high; output a single sketch ≤30 lines — architecture, key interfaces, data model, tradeoffs, edge cases the implementation must handle. No code, no worktree. Hand the sketch to the Sonnet Engineer verbatim in its spawn prompt; the Engineer implements the sketch rather than re-deriving the design.

**Tier 2 — `flag:`/`critical:` items, open design space:** spawn 2–3 design-only subagents in parallel (`flag:` → `claude-opus-4-8`; `critical:` → `claude-fable-5`), each producing a sketch ≤40 lines — architecture, key interfaces, data model, tradeoffs. No code, no worktree. Pick the winner on the item's priorities — efficiency, reliability, scalability — record the choice in one line. Hand it to the Engineer to implement.

Light/trivial tracks: no design exploration.

If the chosen design later fails QA at the design level, the loop's existing alternative-engineer fork (below) is the fallback.

## Spawn template (shared)

Spawn each agent with the `Agent` tool, setting:
- `subagent_type: "dt-[AGENT]"` — e.g. `"dt-engineer"`, `"dt-qa"`, `"dt-fix"`, `"dt-review"`, `"dt-analyze"`, `"dt-ui"` (the harness injects the agent's instructions automatically; no skill-file read needed in the prompt)
- `model: "[MODEL]"` — from the "Model & effort selection" table above

Use this prompt:

> Your task: [TASK + `done when:` criteria]. Effort: [EFFORT] (thinking keyword — medium = `think`, high = `think hard`, minimal = none).
> [QA only:] Gate mode: [GATE MODE].
> [After the first agent:] Work on existing branch [branch-name] — do NOT create a new worktree. [Omit this line on the very first agent of the session — it creates the worktree.]
>
> Prior teammates' reports are in `.claude/dev-team/` — read the ones your skill lists as inputs instead of re-deriving that context. Reports present so far: [list the filenames that exist].
> [If dt-analyze ran:] The shared codebase map is `.claude/dev-team/analyze-report.md` — treat its file locations, data flows, and patterns as ground truth. Do NOT re-explore what it already covers; only open the files it points you to.
> Report discipline: your report is the next agent's context — lead with the machine-readable lines (VERDICT/Branch/severity), findings-only, one line each, ≤40 lines, no narration. Full rules: Efficiency rules → "Report discipline" in `convergence-loop.md`.

After each agent finishes, route on its report from `.claude/dev-team/` before spawning the next: read only the `VERDICT`/`Branch`/severity lines you need to pick the next step. Extract the branch name from the first engineer report and pass it to every later agent. Agents editing the same worktree run sequentially.

## Inputs

- **item** — the task text plus its `done when:` acceptance criteria (from PLAN.md, TASK.md, or the inline arg)
- **gate mode** — one of:
  - `tests` — QA verdict comes from written + executed tests (used by `/dev-team`)
  - `tests+behavioral` — QA runs tests AND exercises the running path, including a **live smoke pass** (real server + real dev DB, not mocks) for any item touching routes/models/migrations/serialization (used by `/dev-team-auto`; see dt-qa)
- **branch** — the shared worktree branch every agent for this item edits
- **MAX_ATTEMPTS = 5** — after this many build cycles without a passing gate, the item is marked BLOCKED

## Roles used

- `dt-engineer` — builds the item on attempt 1; on a *design-level* QA failure, up to 2 additional engineers are spawned to try alternative approaches without wiping prior work
- `dt-qa` — writes/runs the tests (and behavioral checks), emits the **VERDICT: PASS | FAIL** gate
- `dt-review` — quality/optimization review; its findings gate DONE only after QA is green (may run in parallel with dt-qa on attempt 1 — see Efficiency rules)
- `dt-fix` — applies QA failures and review findings on attempts 2+

## The loop

```
attempt = 1
loop:
  # 1+2. BUILD + CORRECTNESS GATE (paired together)

  if attempt == 1:
      if item has a flag: or critical: field:
          run design exploration (Tier 2) → winning sketch   # see "Design exploration"
          run dt-engineer with the winning sketch
      else if full-track AND design space gauged open:
          run design exploration (Tier 1) → one Opus sketch  # see "Design exploration"
          run dt-engineer (Sonnet) with the sketch
      else:
          run dt-engineer        # designs and implements the item
      run dt-qa                  # writes qa-report.md with VERDICT
      # full-track, non-flag:/critical: → run dt-review IN PARALLEL with dt-qa
      # (see Efficiency rules → "Parallel first-pass review"); if QA PASSes,
      # the quality gate below already has its review-report — skip re-running dt-review

  else if latest qa-report Root Cause is design-level (wrong approach / structural gap):
      # Fork a new branch per alternative so the original work is never lost
      # winning_branch starts as the current item branch; updated if an alternative passes
      for alt in [1, 2]:
          alt_branch = "[current-branch]-alt-#{alt}"
          run dt-engineer        # "create branch #{alt_branch} from [current-branch];
                                 #  try a structurally different approach for the failing
                                 #  criterion; existing code on the original branch is untouched"
          run dt-qa              # gates this branch
          if VERDICT == PASS:
              winning_branch = alt_branch
              break              # this alternative works; use winning_branch going forward

  else:
      run dt-fix                 # patch QA bug failures + any open review findings
      run dt-qa

  # After any of the three paths above, check the verdict
  if VERDICT == FAIL:
      attempt += 1
      if attempt > MAX_ATTEMPTS: mark BLOCKED; break
      continue                   # next build = dt-fix or another round of alternatives

  # 3. QUALITY GATE (only once correctness is green)
  run dt-review                  # writes review-report.md
  if review has zero Critical AND zero Important findings:
      if review has Minor findings: run dt-fix once to apply them
      mark DONE; break
  else:
      run dt-fix                 # apply Critical + Important
      if orchestrator judges every applied finding mechanical AND non-security:
          run dt-qa (scoped)     # confirm on the fixed surfaces only — see Efficiency rules
          if VERDICT == PASS: mark DONE; break    # no second full review pass
      else if no security finding AND the fix did not ripple beyond the cited lines:
          run dt-qa (scoped) ∥ dt-review (scoped)   # in parallel; review scoped to the
                                 # fixed surfaces + any finding the fixer disputed or
                                 # deviated from (same model tier as the original review)
          if VERDICT == PASS and no new Critical/Important: mark DONE; break
      attempt += 1
      if attempt > MAX_ATTEMPTS: mark BLOCKED; break
      # loop back — the next pass re-runs full QA and dt-review (security findings and
      # rippling fixes always take this path)
```

**Mechanical-fix shortcut (orchestrator's call):** *mechanical* = the review prescribed the exact fix and applying it took no design judgment (add an index, add a timeout, hoist work out of a loop, paginate a fetch) — judge from the fix report's Changes Made. Any security finding, Critical, disputed/deferred finding, or fix that rippled beyond the cited lines → full loop-back with a fresh review. When unsure, loop back.

## Efficiency rules

- **Parallel first-pass review.** On attempt 1 of a **full-track, non-`flag:`/`critical:`** item, spawn dt-review in the same message as dt-qa — review needs the code, not the verdict. If QA PASSes, the quality gate uses the already-written review-report (no second review spawn). If QA FAILs, the review-report is stale — delete it and revert to sequential (review after QA) for that item's remaining attempts. Keep `flag:`/`critical:` items sequential (an Opus/Fable review wasted on failing code is too expensive a bet), and skip the parallel spawn when team-memory shows the repo's first-attempt pass rate is poor.
- **Inject relevant learnings into builder prompts.** When an item matches a failure family recorded in `~/.claude/memory/dev-team-learnings.md` (money, RLS/auth, migrations, Next.js rendering/actions, content sweeps, …), paste the 3–5 matching bullets verbatim into the dt-engineer and dt-fix spawn prompts under a "Known failure modes — avoid these:" header. A few hundred tokens per spawn; a defect prevented at build time is ~3 agents cheaper than one caught at review. Don't paste the whole file — matching bullets only.
- **Report discipline.** Every `dt-*` report: machine-readable lines first (`## VERDICT: PASS|FAIL`, `**Branch:** …`, severity-tagged findings), findings only, one line each (`SEVERITY — path:line — what's wrong — the fix`), **hard cap ≤40 lines** (over cap: keep highest severity, end with `(N more Minor omitted)`), no preamble/sign-off. The dt-* skills' own report templates already match this.
- **Escalate before you loop (effort → model → stop).** Read the QA Root Cause each attempt and compare it to the previous one. When the same Root Cause survives a fix, do not just re-run the same build at the same power:
  1. **First recurrence** → re-run the builder (`dt-fix`/`dt-engineer`) at **one higher effort** on the same model (raise `think` → `think hard`).
  2. **Still the same cause, or a design-level cause** → escalate the builder **one model tier** (Sonnet → Opus) for the next build.
  3. **Already at Opus and the same cause persists** → escalate to **Fable** for one final build attempt. If Fable also fails, mark **BLOCKED** — the ceiling is reached.
- **Detect a stuck loop.** If a BUILD step reports "nothing to change" yet QA still FAILs, the loop cannot converge — mark BLOCKED immediately rather than burning the remaining attempts.
- **Scope QA confirmation passes to the fixed surfaces.** First-attempt QA runs the item's full check set. Re-gating after a fix runs only the previously-failing checks plus tests covering the files in the fix report's Changes Made; repeat the live smoke pass only if the fix touched routes/models/migrations/serialization. State the scope in QA's spawn prompt; widen it at your discretion if a fix looks like it could ripple.
- **Report hygiene between items.** Before spawning the first agent of a new item, delete the previous item's `.claude/dev-team/*-report.md` files. Always keep `team-memory.md`; keep `analyze-report.md` only if the new item works in the area it maps. The spawn template's "Reports present so far" list names only current-item reports.
- **One worktree per item (normally).** Whichever agent runs first creates the worktree. On a design-level failure, each alternative gets its own branch forked from the current item branch (e.g. `feat/x-alt-1`, `feat/x-alt-2`) — failed alternative branches can be left or deleted, but the original and the winning branch must be kept. After an alternative passes, pass `winning_branch` to every later agent instead of the original branch name.

## Outcomes

Each item ends in exactly one of:

- **DONE** — QA PASS + no Critical/Important review findings. Record the commit hash and a one-line summary.
- **BLOCKED** — attempt cap hit, or a non-convergent loop detected. Record: the last QA `VERDICT`, which `done when:` criteria are still unmet, and the last Root Cause hint so a human (or the next session) can pick it up.

## Run memory log (read at start, append the moment each item resolves)

The team keeps a persistent, cross-run memory at **`.claude/dev-team/team-memory.md`** in the working repo. Unlike the per-run `*-report.md` files (overwritten each item), this file **accumulates** — it is how the next run learns from this one.

- **At the start of a run**, both orchestrators read this file if it exists and factor its `Remember next run:` notes into track/agent choices (e.g. a flaky test suite, a build command that needs a flag, an approach that failed before). If it does not exist, create it with a `# Dev-team memory log` header on first write.
- **The moment an item resolves** — DONE or BLOCKED, *every* item, *every* track — append one entry **in the same step that records the item's outcome** (for `/dev-team-auto`, the item orchestrator appends it as its loop ends; for `/dev-team`, with the final report). Never defer it to shutdown — deferred, it does not get written. Append only; never rewrite prior entries (exception: compaction, below).

### Compaction (at run start, orchestrator's discretion)

At the start of a run, after reading the log, compact it if it has grown past what its content earns — roughly 12–15 entries, or sooner if many entries cover subjects unrelated to the current plan. To compact:

1. Distill every entry's still-true `Remember next run:` notes into a deduplicated `## Standing notes` section at the top of the file (create if absent) — one bullet per fact (build flags, flaky suites, run commands, dead-end approaches). Drop notes that are obsolete or one-off.
2. Keep the last ~5 raw entries under `## Recent runs`; delete the rest.

Compaction rewrites the file — it is the only permitted rewrite.

Entry format:

```
## <YYYY-MM-DD HH:MM> — <dev-team | dev-team-auto> — <item title>
- **Outcome:** DONE | BLOCKED — <N attempts, track, branch, commit hash if DONE>
- **What happened:** <1–3 lines: what was built and how the loop went>
- **What worked:** <techniques/tests/approaches that converged — or "nothing notable">
- **What failed:** <QA failures, review findings, dead-end approaches, wasted attempts — or "none">
- **Remember next run:** <concrete, reusable notes for the next session: gotchas, commands, flaky areas, approaches to avoid or repeat — or "nothing">
```

Keep each entry tight — it is a lesson, not a transcript. The `*-report.md` files hold the detail; this file holds the takeaway.

### Two destinations: project-specific vs. project-independent

Every loop's takeaway splits into two kinds of lesson. Route each to the right place:

- **Project-specific findings → `.claude/dev-team/team-memory.md`** (the log above, in the working repo). Anything tied to *this* codebase: a flaky suite, a build/test command with a needed flag, a module's quirks, an approach that failed *here*. This is the default; when in doubt, keep it project-local.
- **Project-independent learnings → the global os memory at `~/.claude/memory/dev-team-learnings.md`.** Only lessons that generalize to the dev-team process in *any* repo: orchestration patterns, when a track/model choice paid off or backfired, QA/test or review tactics that reliably converge, agent-prompting improvements, recurring failure modes of the loop itself. These make the *team* better everywhere, not just this repo.

Writing the global file:

- **At start of a run**, read `~/.claude/memory/dev-team-learnings.md` and apply its lessons to your track/model/approach choices.
- **At end of a loop**, if the run produced a genuinely generalizable lesson, append a dated bullet: `- <YYYY-MM-DD> <lesson> — **Why:** … **How to apply:** …`. Be conservative: most loops yield *no* global learning — only append when the lesson would change a future run in a *different* repo. Don't duplicate an existing bullet; sharpen it instead. If the file has grown past ~30 bullets, merge overlapping bullets and delete any invalidated ones while you're in it.

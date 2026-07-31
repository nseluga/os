# Convergence Loop (per plan item)

The shared engine behind `/dev-team` and `/dev-team-auto`. A plan item is **done only when the QA gate passes** — the loop hammers one item until it works as specified or the attempt cap is hit. Sections marked **(shared)** apply to both orchestrators; **The loop** and everything after it describe the *maximal* engine — run only the stages your chosen team includes, and skip the rest outright.

## Team selection (shared)

You choose the team. The plan gives you two signals and does **not** prescribe
which agents run:

- **`risk:`** — what breaks if this is wrong, and how you'd find out. Routes
  review, model tier, and gate mode. The decisive property is **silent vs
  loud**: a failure the user sees on first load needs no reviewer to find it;
  one discovered from a bank statement three weeks later does.
- **`difficulty:`** — why this might not work first try. Routes design
  exploration, attempt budget, and research. Independent of risk.

**Your objective: the simplest team that protects what the `risk:` line names — and nothing beyond it.**

Read `agent-glossary.md` (same directory) before choosing. Each entry states what
the agent buys, what it costs, and **when it is waste**; it closes with worked
routing examples for all four risk×difficulty quadrants. Follow the example
nearest your item rather than re-deriving from scratch.

Two failure modes the examples exist to prevent — both expensive, in opposite directions:

- **Hard ≠ risky.** A fiddly algorithm with a loud, revertible failure earns
  design exploration and extra attempts. It does **not** earn a review pass.
- **Risky ≠ hard.** A settled pattern with a silent failure earns a review at
  the top tier and a behavioral gate. It does **not** earn competing outlines.

**Model & effort — defaults, not a lookup table.** Deviate when the item argues
for it, and say so in the declaration below. Effort is not a spawn parameter;
express it in the prompt as a thinking keyword: **minimal** (none), **medium**
(`think`), **high** (`think hard`).

- **Builders** (`dt-engineer`): Sonnet/medium for a bounded change; Sonnet/high
  when build quality sets how many fix cycles you pay for later; silent or
  non-revertible risk → **outline at Opus/high, implement at Sonnet/high** (see
  Design exploration); Fable/medium when a defect is unrecoverable (auth, crypto,
  authorization boundary, PII/PHI leak, irreversible money, destroyed production
  data) — one model throughout, no split.
- **`dt-fix`**: Sonnet/medium — it applies findings someone else reasoned out.
  Raised only by the escalation ramp.
- **`dt-review`**: Opus/high — it is the floor, not an escalation. You only
  spawn a reviewer on an item whose risk earns one, so there is no cheap-review
  case; a reviewer below the builder that wrote the code finds nothing. Fable
  when the defect would be unrecoverable.
- **`dt-analyze`** Sonnet/medium (Haiku for its `Explore` fan-out, per its skill);
  **`dt-research`** Sonnet/medium.
- **`dt-qa`** — never below Sonnet. Sonnet/medium default; **Opus/high when risk
  is silent or non-revertible**, where a false PASS is the failure the gate
  exists to prevent; Fable when unrecoverable. Tier by risk, then hold — the ramp
  raises the *builder*, never the gate; a FAIL is already correct information.
  QA is the loop's heaviest agent, but control that with gate mode and output
  bounds, not by dropping its tier.

The escalation ramp in Efficiency rules raises builders on repeated failure — their tiers are starting points, not ceilings.

**`dt-analyze`** runs before the loop when the item spans multiple files or works
in an area no report has mapped this run. Skip it for single-file items and for
areas already covered by a live `analyze-report.md`.

**`dt-research` — check the cache, always.** Before the first build, list
`~/.claude/skills/dev-team/research-notes/` and name every package, service, or
external system this item will use. Any that has no note → spawn `dt-research`
(Sonnet, medium) on it first. Any that has one → read it, spawn nothing. It never
covers static architecture; the standards files own that. Its `research-brief.md`
is injected into the builder/reviewer spawns (see Spawn template), and it may run
in parallel with dt-analyze. The same rule fires again inside `dt-engineer`: it
researches before adding any dependency not already in the repo — which catches
what the plan author didn't anticipate.

`dt-ui` composes with any team when the item changes user-visible frontend.

**Declare before you spawn.** Before the first agent of an item, append one line
to `.claude/dev-team/team-memory.md`:

```
TEAM <item title> — risk: <silent|loud, revertible|not> difficulty: <low|open: what> → <agents chosen> | skipped: <agent + why>
```

This is a forced declaration, not a gate. Under-running is a visible failure and
over-running is invisible tokens, so latitude drifts heavy without it; writing
"skipped: nothing" on a copy edit is the correction. It is also the only record
of what these guidelines actually produce, so they can be tuned on evidence.

## Design exploration

**The opening move of the engineering phase.** Outline at the top tier, implement at Sonnet/high — deciding *what* to build is cheap reasoning; building it is expensive typing, and only the first is worth the top tier.

**Two signals buy an outline pass, in different shapes:**

| | outlines | why |
|---|---|---|
| `difficulty:` open | **2–3, competing** | the design space has real alternatives |
| `risk:` silent or non-revertible, `difficulty:` low | **1** | the approach is settled; you're buying a stated design, not alternatives |
| both | **2–3, competing** | one pass covers both — never run two |
| neither | **none** — one Sonnet engineer builds | |

A risk-bought single outline only makes sense on an item already buying `dt-review` — that reviewer is what makes the cheaper implementer safe. No reviewer, no split.

1. **Gauge the design space.** One clearly-shaped approach (constrained by existing patterns, an established interface, or a plan-prescribed architecture) = **narrow**. Genuinely competing architectures (different data models, module boundaries, or consistency tradeoffs) = **open** → 2 competing outlines when the risk is loud, 3 when it is silent or non-revertible.

2. **Outline at Opus/high, don't build.** Each returns ≤30 lines: the approach, key interfaces and data model, what it handles well, what it doesn't, and the edge cases an implementation must handle. No code, no worktree, no branch — that is what keeps this affordable enough to run three of.

3. **Prompt each one differently** (competing outlines only). Name the approach you want it to take ("event-sourced", "single denormalised table", "compute at read time"). Engineers given the same prompt return the same design; the parallel spawn only pays for itself if the approaches genuinely diverge.

4. **Picking.** Choose on the item's priorities — correctness, reliability, efficiency, fit with existing patterns — and record the choice in one line.

5. **Implement once, at Sonnet/high.** Hand the outline **verbatim** to a single `dt-engineer`; it implements that outline rather than re-deriving the design. Only this engineer creates a worktree. Keep it on Sonnet unless the item is the unrecoverable-defect tier — the escalation ramp raises it if the build actually fails.

6. **Keep the runner-up outlines.** On a later design-level QA failure the loop hands the next-best outline to an engineer instead of re-deriving alternatives from scratch — the exploration is already paid for.

## Spawn template (shared)

Spawn each agent with the `Agent` tool, setting:
- `subagent_type: "dt-[AGENT]"` — e.g. `"dt-engineer"`, `"dt-qa"`, `"dt-fix"`, `"dt-review"`, `"dt-analyze"`, `"dt-ui"` (the harness injects the agent's instructions automatically; no skill-file read needed in the prompt)
- `model: "[MODEL]"` — per "Team selection" above

Use this prompt:

> Your task: [TASK + `done when:` criteria]. Effort: [EFFORT] (thinking keyword — medium = `think`, high = `think hard`, minimal = none).
> [QA only:] Gate mode: [GATE MODE].
> [Engineer in outline mode only:] OUTLINE ONLY — do NOT write code and do NOT create a worktree. Take this approach specifically: [NAMED APPROACH]. Return ≤30 lines: the approach, key interfaces and data model, what it handles well, what it doesn't, edge cases an implementation must handle.
> [Engineer implementing a chosen outline:] Implement this outline as given rather than re-deriving the design: [WINNING OUTLINE, verbatim].
> [After the first agent:] Work on existing branch [branch-name] — do NOT create a new worktree. [Omit this line on the very first agent of the session — it creates the worktree.]
>
> Prior teammates' reports are in `.claude/dev-team/` — read the ones your skill lists as inputs instead of re-deriving that context. Reports present so far: [list the filenames that exist].
> [If dt-analyze ran:] The shared codebase map is `.claude/dev-team/analyze-report.md` — treat its file locations, data flows, and patterns as ground truth. Do NOT re-explore what it already covers; only open the files it points you to.
> [If dt-research ran:] The research brief is `.claude/dev-team/research-brief.md` — its Recommendation is the default tool/library/pattern choice. Override only on a concrete conflict with the codebase, recorded in your report.
> Report discipline: your report is the next agent's context — lead with the machine-readable lines (VERDICT/Branch/severity), findings-only, one line each, ≤40 lines, no narration. Full rules: Efficiency rules → "Report discipline" in `convergence-loop.md`.
> Context discipline: don't re-read a file already quoted in a report you were given, or one you just edited. Prefer grep + a line range over a whole file. Bound command output — compact test flags (`pytest -q --tb=line --maxfail=3` or the repo's equivalent), `2>&1 | tail -30` on builds and installs, and after a failure re-run only the failing test.

After each agent finishes, route on its report from `.claude/dev-team/` before spawning the next: read only the `VERDICT`/`Branch`/severity lines you need to pick the next step. Extract the branch name from the first engineer report and pass it to every later agent. Agents editing the same worktree run sequentially.

## Inputs

- **item** — the task text plus its `done when:` acceptance criteria (from PLAN.md, TASK.md, or the inline arg)
- **gate mode** — **decided per item, not per run.** Seeded live runs and browser QA are the most expensive part of the gate; don't buy them for code no user or route can reach.
  - `tests` — QA verdict comes from written + executed tests. The default.
  - `tests+behavioral` — QA runs tests AND exercises the running path, including a **live smoke pass** (real server + real dev DB, not mocks) and browser QA for web UI. Buy it only when the item changes user-visible UI or an HTTP route, or touches models/migrations/serialization — or when the `risk:` line says the failure is silent, since a silent failure is precisely the one tests written from the criteria will miss.
- **branch** — the shared worktree branch every agent for this item edits
- **MAX_ATTEMPTS** — build cycles before the item is marked BLOCKED. **3** by default; **2** when `difficulty:` is low, since a settled approach that fails twice is misdiagnosed rather than under-attempted. Set by `difficulty:`, never by `risk:` — hammering a high-stakes item you already understand just buys more of the same build. A BLOCKED line with a Root Cause is cheaper than a fourth build at the top tier.

## Roles used

- `dt-research` — cache-first current-tooling research before the first build
- `dt-engineer` — outlines competing approaches when design space is open, then builds the winner; on a *design-level* QA failure, up to 2 additional engineers try alternative approaches
- `dt-qa` — writes/runs the tests (and behavioral checks), emits the **VERDICT: PASS | FAIL** gate
- `dt-review` — quality/optimization review; its findings gate DONE only after QA is green
- `dt-fix` — applies QA failures and review findings

## The loop

```
attempt = 1
loop:
  # 1+2. BUILD + CORRECTNESS GATE (paired together)

  if attempt == 1:
      # Name every package/service/external system this item uses; any with no note in
      # research-notes/ → run dt-research on it (∥ dt-analyze) so research-brief.md
      # exists before any design/build spawn. See "Team selection".
      if difficulty is open:
          run 2-3 dt-engineer IN PARALLEL, outline-only, divergent approaches
                                 # no code, no worktree — see "Design exploration"
          pick winning outline; keep the runner-ups
          run dt-engineer with the winning outline verbatim   # this one builds
      else:
          run dt-engineer        # designs and implements the item
      run dt-qa                  # writes qa-report.md with VERDICT
      # if dt-review is in the team AND risk is not silent → spawn it IN PARALLEL with
      # dt-qa (see Efficiency rules → "Parallel first-pass review"); if QA PASSes,
      # the quality gate below already has its review-report — skip re-running dt-review

  else if latest qa-report Root Cause is design-level (wrong approach / structural gap):
      # Fork a new branch per alternative so the original work is never lost
      # winning_branch starts as the current item branch; updated if an alternative passes
      for alt in [1, 2]:
          alt_branch = "[current-branch]-alt-#{alt}"
          run dt-engineer        # "create branch #{alt_branch} from [current-branch];
                                 #  try a structurally different approach for the failing
                                 #  criterion; existing code on the original branch is untouched"
                                 # If exploration ran, hand it the next-best runner-up
                                 # outline verbatim instead of asking it to re-derive one.
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

  # CHECKPOINT: correctness is green — commit this last-known-good state
  git add -A && git commit       # "checkpoint: item <title> — QA PASS (attempt #{attempt})"
                                 # so a later fix/review pass that regresses can be reset back to here

  # 3. QUALITY GATE (only once correctness is green)
  if dt-review not in the chosen team: mark DONE; break   # loud+revertible risk ends here
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

- **Parallel first-pass review.** When dt-review is in the team and the `risk:` line reads loud, spawn it on attempt 1 in the same message as dt-qa. If QA PASSes, the quality gate uses the already-written review-report (no second review spawn). If QA FAILs, the review-report is stale — delete it and revert to sequential (review after QA) for that item's remaining attempts. Keep silent- and non-revertible-risk items sequential — there the reviewer needs to see code that already passed — and skip the parallel spawn when team-memory shows the repo's first-attempt pass rate is poor.
- **Inject relevant learnings into builder AND reviewer prompts.** When an item matches a failure family recorded in `~/.claude/memory/dev-team-learnings.md` (money, RLS/auth, migrations, Next.js rendering/actions, content sweeps, …), paste the 3–5 matching bullets verbatim into the dt-engineer, dt-fix, and dt-review spawn prompts — "Known failure modes — avoid these:" for the builders, "Known failure modes — check for these:" for the reviewer. Don't paste the whole file — matching bullets only, matched once per item and reused across all three prompts. Review is the role that most often catches these exact bug classes when they recur, so it needs the same list the builders got, not a colder read. Under `/dev-team-auto`, the top-level orchestrator has already done this matching (see "Writing the global file" below) and handed you the item's bullets directly — relay them; don't re-read the file.
- **Report discipline.** Every `dt-*` report: machine-readable lines first (`## VERDICT: PASS|FAIL`, `**Branch:** …`, severity-tagged findings), findings only, one line each (`SEVERITY — path:line — what's wrong — the fix`), **hard cap ≤40 lines** (over cap: keep highest severity, end with `(N more Minor omitted)`), no preamble/sign-off.
- **Escalate before you loop (effort → model → stop).** Read the QA Root Cause each attempt and compare it to the previous one. When the same Root Cause survives a fix, do not just re-run the same build at the same power:
  1. **First recurrence** → re-run the builder (`dt-fix`/`dt-engineer`) at **one higher effort** on the same model (raise `think` → `think hard`).
  2. **Still the same cause, or a design-level cause** → escalate the builder **one model tier** (Sonnet → Opus) for the next build.
  3. **Already at Opus and the same cause persists** → mark **BLOCKED**. Same cause surviving three rising-power attempts is a misdiagnosis, not an under-powered build. Escalate to **Fable** for one final attempt only on the unrecoverable-defect tier, where a BLOCKED item costs more than the build.
- **Bound every command's output** — it is re-sent on all of that agent's later turns, so an unbounded test run or build log is paid for many times. In the spawn prompt for any agent running commands: compact test flags (`pytest -q --tb=line --maxfail=3` or the repo's equivalent), `2>&1 | tail -30` on builds and installs, then re-run only the failing test with full traceback for detail.
- **Detect a stuck loop.** If a BUILD step reports "nothing to change" yet QA still FAILs, mark BLOCKED immediately — the loop cannot converge.
- **Scope QA confirmation passes to the fixed surfaces.** First-attempt QA runs the item's full check set. Re-gating after a fix runs only the previously-failing checks plus tests covering the files in the fix report's Changes Made; repeat the live smoke pass only if the fix touched routes/models/migrations/serialization. State the scope in QA's spawn prompt; widen it at your discretion if a fix looks like it could ripple.
- **Report hygiene between items.** Before spawning the first agent of a new item, delete the previous item's `.claude/dev-team/*-report.md` files. Always keep `team-memory.md`; keep `analyze-report.md` only if the new item works in the area it maps. The spawn template's "Reports present so far" list names only current-item reports.
- **One worktree per item (normally).** Whichever agent runs first creates the worktree. On a design-level failure, each alternative gets its own branch forked from the current item branch (e.g. `feat/x-alt-1`, `feat/x-alt-2`) — failed alternative branches can be left or deleted, but the original and the winning branch must be kept. After an alternative passes, pass `winning_branch` to every later agent instead of the original branch name.

## Outcomes

Each item ends in exactly one of:

- **DONE** — QA PASS + no Critical/Important review findings. Record the commit hash and a one-line summary.
- **BLOCKED** — attempt cap hit, or a non-convergent loop detected. Record: the last QA `VERDICT`, which `done when:` criteria are still unmet, and the last Root Cause hint so a human (or the next session) can pick it up.

## Run memory log (read at start, append the moment each item resolves)

The team keeps a persistent, cross-run memory at **`.claude/dev-team/team-memory.md`** in the working repo. Unlike the per-run `*-report.md` files (overwritten each item), this file **accumulates**.

- **At the start of a run**, both orchestrators read this file if it exists and factor its `Remember next run:` notes into team/model choices (e.g. a flaky test suite, a build command that needs a flag, an approach that failed before). If it does not exist, create it with a `# Dev-team memory log` header on first write.
- **The moment an item resolves** — DONE or BLOCKED, *every* item, whatever team ran — append one entry **in the same step that records the item's outcome** (for `/dev-team-auto`, the item orchestrator appends it as its loop ends; for `/dev-team`, with the final report). Never defer it to shutdown — deferred, it does not get written. Append only; never rewrite prior entries (exception: compaction, below).

### Compaction (at run start, orchestrator's discretion)

At the start of a run, after reading the log, compact it if it has grown past what its content earns — roughly 12–15 entries, or sooner if many entries cover subjects unrelated to the current plan. To compact:

1. Distill every entry's still-true `Remember next run:` notes into a deduplicated `## Standing notes` section at the top of the file (create if absent) — one bullet per fact (build flags, flaky suites, run commands, dead-end approaches). Drop notes that are obsolete or one-off.
2. Keep the last ~5 raw entries under `## Recent runs`; delete the rest.

Compaction rewrites the file — it is the only permitted rewrite.

Entry format:

```
## <YYYY-MM-DD HH:MM> — <dev-team | dev-team-auto> — <item title>
- **Outcome:** DONE | BLOCKED — <N attempts, team that ran, branch, commit hash if DONE>
- **What happened:** <1–3 lines: what was built and how the loop went>
- **What worked:** <techniques/tests/approaches that converged — or "nothing notable">
- **What failed:** <QA failures, review findings, dead-end approaches, wasted attempts — or "none">
- **Remember next run:** <concrete, reusable notes for the next session: gotchas, commands, flaky areas, approaches to avoid or repeat — or "nothing">
```

Keep each entry tight — it is a lesson, not a transcript.

### Two destinations: project-specific vs. project-independent

Route each loop's takeaway to the right place:

- **Project-specific findings → `.claude/dev-team/team-memory.md`** (the log above, in the working repo). Anything tied to *this* codebase: a flaky suite, a build/test command with a needed flag, a module's quirks, an approach that failed *here*. This is the default; when in doubt, keep it project-local.
- **Project-independent learnings → the global os memory at `~/.claude/memory/dev-team-learnings.md`.** Only lessons that generalize to the dev-team process in *any* repo: orchestration patterns, when a team/model choice paid off or backfired, QA/test or review tactics that reliably converge, agent-prompting improvements, recurring failure modes of the loop itself.

Writing the global file:

- **At start of a run, exactly one agent reads it — never a fresh read per item.** Under `/dev-team-auto`, only the top-level orchestrator reads `~/.claude/memory/dev-team-learnings.md`, at Start Up; it matches each item's failure family against the bullets and hands the matched 3–5 to that item's `dt-orchestrator` in its spawn prompt (see Efficiency rules → "Inject relevant learnings"). `dt-orchestrator` never reads the file itself — re-reading it per item is pure waste, since every item's matched subset is a tiny fraction of the whole file. Under `/dev-team` (no nested item orchestrator), you are the one reader — read it directly and apply its lessons to your team/model/approach choices.
- **Check its size every time you read it, unconditionally — don't wait for an append.** If it has grown past ~30 bullets, merge overlapping bullets and delete any invalidated ones before doing anything else with it. This is a mandatory step of reading the file, not a maybe-remembered aside on the append path.
- **At end of a loop**, if the run produced a genuinely generalizable lesson, append a dated bullet: `- <YYYY-MM-DD> <lesson> — **Why:** … **How to apply:** …`. Be conservative: most loops yield *no* global learning — only append when the lesson would change a future run in a *different* repo. Don't duplicate an existing bullet; sharpen it instead.

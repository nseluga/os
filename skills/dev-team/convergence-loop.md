# Convergence Loop (per plan item)

The shared engine behind `/dev-team` and `/dev-team-auto`. A plan item is **done only when the QA gate passes** — the loop hammers one item until it works as specified or the attempt cap is hit. This file is the single source of truth for the loop; both orchestrators reference it so they behave identically.

This file defines the **`full`-track** engine. The orchestrators also run lighter tracks (`trivial` = build/smoke check only; `light` = Engineer → QA → fix-if-fail, cap 2, no review) that do **not** enter this loop — see the rigor selection in each orchestrator skill. Everything below applies only to `full`.

## Inputs

- **item** — the task text plus its `done when:` acceptance criteria (from PLAN.md, TASK.md, or the inline arg)
- **gate mode** — one of:
  - `tests` — QA verdict comes from written + executed tests (used by `/dev-team`)
  - `tests+behavioral` — QA runs tests AND exercises the running path (used by `/dev-team-auto`)
- **branch** — the shared worktree branch every agent for this item edits
- **MAX_ATTEMPTS = 5** — after this many build cycles without a passing gate, the item is marked BLOCKED

## Roles used

- `dt-engineer` — builds the item on attempt 1; on a *design-level* QA failure, up to 2 additional engineers are spawned to try alternative approaches without wiping prior work
- `dt-qa` — writes/runs the tests (and behavioral checks), emits the **VERDICT: PASS | FAIL** gate
- `dt-review` — quality/optimization review, only after QA is green
- `dt-fix` — applies QA failures and review findings on attempts 2+

## The loop

```
attempt = 1
loop:
  # 1+2. BUILD + CORRECTNESS GATE (paired together)

  if attempt == 1:
      run dt-engineer            # implements the item
      run dt-qa                  # writes qa-report.md with VERDICT

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
      attempt += 1
      if attempt > MAX_ATTEMPTS: mark BLOCKED; break
      # loop back — the next pass re-runs QA to confirm the fixes hold
```

### Why this order

- **Correctness before quality.** Never spend a `dt-review` pass optimizing code that doesn't pass QA — fix it until QA is green, then review once. This keeps the loop cheap.
- **Fix vs. alternatives.** The Bug Fixer patches bugs and applies findings. On a design-level failure (the approach itself can't satisfy the criterion), spawn up to 2 additional engineers with different angles — they add/modify rather than wipe. If any alternative passes QA, the loop continues to the quality gate without consuming an attempt. If none pass, one attempt is consumed and the loop restarts.
- **The gate is binary.** An item is DONE only when `dt-qa` reports `VERDICT: PASS` **and** `dt-review` finds nothing Critical or Important. Minor findings are applied but don't block the exit.

## Efficiency rules

- **Pass reports forward.** Every agent receives the existing `.claude/dev-team/*.md` reports so it never re-derives context already established this loop.
- **Detect a stuck loop.** If a BUILD step reports "nothing to change" yet QA still FAILs, the loop cannot converge — mark BLOCKED immediately rather than burning the remaining attempts.
- **One worktree per item (normally).** Whichever agent runs first creates the worktree. On a design-level failure, each alternative gets its own branch forked from the current item branch (e.g. `feat/x-alt-1`, `feat/x-alt-2`) — failed alternative branches can be left or deleted, but the original and the winning branch must be kept. After an alternative passes, pass `winning_branch` to every later agent instead of the original branch name.

## Outcomes

Each item ends in exactly one of:

- **DONE** — QA PASS + no Critical/Important review findings. Record the commit hash and a one-line summary.
- **BLOCKED** — attempt cap hit, or a non-convergent loop detected. Record: the last QA `VERDICT`, which `done when:` criteria are still unmet, and the last Root Cause hint so a human (or the next session) can pick it up.

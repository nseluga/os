# Convergence Loop (per plan item)

The shared engine behind `/dev-team` and `/dev-team-auto`. A plan item is **done only when the QA gate passes** — the loop hammers one item until it works as specified or the attempt cap is hit. This file is the single source of truth for the loop; both orchestrators reference it so they behave identically.

The sections below marked **(shared)** — track classification, model selection, and the spawn template — are identical for both orchestrators; each orchestrator references them here instead of restating them, and adds only its own divergent parameters (interactivity, gate mode, PROGRESS.md handling). **The loop** and everything after it define the **`full`-track** engine only; the lighter tracks defined under Track classification do not enter it.

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

`flag:` (Opus escalation) and the `dt-analyze`/`dt-ui` modifiers compose with any track above `trivial`.

## Model selection (shared)

- Default: `claude-sonnet-4-6` for all agents.
- If the item has a `flag:` field warning about complexity or risk, use `claude-opus-4-8` for the Engineer and Bug Fixer; keep Sonnet for the others.

## Spawn template (shared)

Spawn each agent with the `Agent` tool using this prompt:

> Read `~/.claude/skills/dt-[AGENT]/skill.md` for your full instructions. Your task: [TASK + `done when:` criteria]. Use model [MODEL].
> [QA only:] Gate mode: [GATE MODE].
> [After the first agent:] Work on existing branch [branch-name] — do NOT create a new worktree. [Omit this line on the very first agent of the session — it creates the worktree.]
>
> Prior teammates' reports are in `.claude/dev-team/` — read the ones your skill lists as inputs instead of re-deriving that context. Reports present so far: [list the filenames that exist].

After each agent finishes, route on its report from `.claude/dev-team/` before spawning the next: read only the `VERDICT`/`Branch`/severity lines you need to pick the next step. Extract the branch name from the first engineer report and pass it to every later agent. Agents editing the same worktree run sequentially.

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

## Run memory log (read at start, append at end)

The team keeps a persistent, cross-run memory at **`.claude/dev-team/team-memory.md`** in the working repo. Unlike the per-run `*-report.md` files (overwritten each item), this file **accumulates** — it is how the next run learns from this one.

- **At the start of a run**, both orchestrators read this file if it exists and factor its `Remember next run:` notes into track/agent choices (e.g. a flaky test suite, a build command that needs a flag, an approach that failed before). If it does not exist, create it with a `# Dev-team memory log` header on first write.
- **At the end of every loop** — for *every* item and *every* track, DONE or BLOCKED — append one entry. This is the log of "what happened, what worked, what failed, and what to remember." Append only; never rewrite prior entries.

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

Writing the global file (follow the memory system's format — one managed fact file, appended over time):

- **At start of a run**, read `~/.claude/memory/dev-team-learnings.md` if it exists and apply its lessons to your track/model/approach choices. (Its one-line pointer is already in the auto-loaded `MEMORY.md` index, but the detail lives in the fact file — read it.)
- **At end of a loop**, if the run produced a genuinely generalizable lesson, append a dated bullet to that file. If the file doesn't exist, create it with this frontmatter and add a one-line pointer to `~/.claude/memory/MEMORY.md`:

  ```
  ---
  name: dev-team-learnings
  description: Generalizable /dev-team + /dev-team-auto process learnings — orchestration, track/model, QA/test, and review patterns that apply across any repo
  metadata:
    type: reference
  ---

  Cross-project lessons from dev-team runs. Project-specific findings stay in each repo's `.claude/dev-team/team-memory.md`.

  - <YYYY-MM-DD> <lesson> — **Why:** <what it prevents/enables>. **How to apply:** <what to do next time>.
  ```

  Be conservative: most loops yield *no* global learning — only append when the lesson would change how a future run behaves in a different repo. Don't duplicate an existing bullet; sharpen it instead. Never dump project-specific detail here.

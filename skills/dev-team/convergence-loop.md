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

`flag:` (Opus escalation) and the `dt-ui` modifier compose with any track above `trivial`.

**`dt-analyze` runs by default, once, before the loop for any `full`-track item that spans multiple files** (and for any unfamiliar area on any track). Skip it only for single-file items. Its `analyze-report.md` map is then injected into every agent (see Spawn template) so no agent re-explores the codebase — each spawned agent otherwise cold-starts and re-derives structure from scratch, which is the dominant hidden cost of a multi-agent run. One shared map amortizes that exploration across the whole team.

## Model & effort selection (shared)

Every agent is spawned with a **model** and an **effort** level. Model goes in the spawn template's `[MODEL]` slot. Effort is not a spawn parameter, so express it in the agent's prompt as a reasoning-depth directive / thinking keyword: **minimal** (none — mechanical work), **medium** (`think` — proportionate reasoning), **high** (`think hard` — reason through edge cases, alternatives, and failure modes first). Spend the capable-model / high-effort budget only where a mistake is expensive or hard to catch downstream; keep the cheap default everywhere else.

Starting model + effort by role (the escalation ramp in Efficiency rules raises these on repeated failure — they are starting points, not ceilings):

| Agent | Model | Effort | Why |
|---|---|---|---|
| `dt-analyze` | Sonnet (Haiku for its `Explore` fan-out, per its skill) | medium | broad mapping, not deep reasoning |
| `dt-engineer` — **light** track | Sonnet | medium | one file, bounded blast radius |
| `dt-engineer` — **full** track | Sonnet | **high** | build quality sets how many review/fix cycles you pay for later |
| `dt-engineer` / `dt-fix` — **`flag:`** item | Opus | high | security / money / data-path — worth the top tier |
| `dt-qa` | Sonnet | medium | keep the gate on a reasoning model: it judges coverage and classifies bug vs design-level (which steers the whole loop). **Never below Sonnet** — a weak gate passes broken code with false confidence. |
| `dt-review` — **full**, non-`flag:` | Sonnet | high | highest-value gate; on Patio, Sonnet review already caught the unauth endpoint, the TOCTOU race, and the table dump that QA passed |
| `dt-review` — **`flag:`** item | Opus | high | maximum scrutiny where a missed defect is catastrophic |
| `dt-fix` — bug-class fix | Sonnet | medium | applying an already-diagnosed fix |
| `dt-fix` — applying Critical/Important findings, or `flag:` | Opus | high | sensitive changes; match the builder tier |

Review runs only on `full`-track items, so its spend is self-limiting to the items that earn it.

## Design exploration (flag: items only)

For a `flag:` item — the complex/critical ones that already escalate to Opus — the right architecture is worth proving before it's built. **Before the first Engineer build only:**

1. Spawn 2–3 **design-only** subagents in parallel (model `claude-opus-4-8`), each producing a short design sketch for the item — architecture, key interfaces, data model, and the efficiency, reliability, and scalability tradeoffs of that approach. No code, no worktree.
2. Pick the winning sketch on the item's priorities — efficiency, reliability, and scalability first — and record the choice and why in one line.
3. Hand the winning sketch to the Engineer as the design to implement; it builds that one approach.

Non-`flag:` items skip this entirely — the Engineer designs and builds directly, as today. If the chosen design later fails QA at the design level, the loop's existing alternative-engineer fork (below) is the fallback.

## Spawn template (shared)

Spawn each agent with the `Agent` tool using this prompt:

> Read `~/.claude/skills/dt-[AGENT]/skill.md` for your full instructions. Your task: [TASK + `done when:` criteria]. Use model [MODEL] at [EFFORT] effort (pick both from "Model & effort selection"; set effort with the thinking keyword — medium = `think`, high = `think hard`, minimal = none).
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
- `dt-review` — quality/optimization review, only after QA is green
- `dt-fix` — applies QA failures and review findings on attempts 2+

## The loop

```
attempt = 1
loop:
  # 1+2. BUILD + CORRECTNESS GATE (paired together)

  if attempt == 1:
      if item has a flag: field:
          run design exploration → winning sketch   # see "Design exploration (flag: items only)"
          run dt-engineer with the winning sketch   # builds the chosen approach
      else:
          run dt-engineer        # designs and implements the item
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
- **Report discipline (output tokens are the expensive class — ~5× input).** Each agent's report is the context bridge to the next agent: make it dense, not long. Every `dt-*` report must follow this shape (the dt-* skills' own report templates already match it — this is the shared enforcement):
  - **Machine-readable lines first.** Lead with exactly the lines the orchestrator routes on — `## VERDICT: PASS|FAIL`, `**Branch:** …`, findings tagged by severity — so routing never has to scan prose.
  - **Findings only.** No restating the task, no narrating steps taken, no pasting code or diffs the reader already has in the worktree. State conclusions, not the path to them.
  - **One line per item.** Each finding / file / criterion is a single line, e.g. `SEVERITY — path:line — what's wrong — the fix`. No paragraphs, no sub-bullets.
  - **Hard cap: ≤40 lines** (excluding the required header lines). Over cap: keep the highest-severity items, drop the rest, and end with `(N more Minor omitted)`.
  - **No preamble or sign-off.** No "I analyzed…", "In summary…", or closing notes.
- **Escalate before you loop (effort → model → stop).** Read the QA Root Cause each attempt and compare it to the previous one. When the same Root Cause survives a fix, do not just re-run the same build at the same power:
  1. **First recurrence** → re-run the builder (`dt-fix`/`dt-engineer`) at **one higher effort** on the same model (raise `think` → `think hard`).
  2. **Still the same cause, or a design-level cause** → escalate the builder **one model tier** (Sonnet → Opus) for the next build.
  3. **Already at Opus and the same cause persists** → mark **BLOCKED** now; attempts at the ceiling won't converge.
  This turns a blind retry into a capability ramp, and composes with the hard floor below.
- **Detect a stuck loop.** If a BUILD step reports "nothing to change" yet QA still FAILs, the loop cannot converge — mark BLOCKED immediately rather than burning the remaining attempts.
- **One worktree per item (normally).** Whichever agent runs first creates the worktree. On a design-level failure, each alternative gets its own branch forked from the current item branch (e.g. `feat/x-alt-1`, `feat/x-alt-2`) — failed alternative branches can be left or deleted, but the original and the winning branch must be kept. After an alternative passes, pass `winning_branch` to every later agent instead of the original branch name.

## Outcomes

Each item ends in exactly one of:

- **DONE** — QA PASS + no Critical/Important review findings. Record the commit hash and a one-line summary.
- **BLOCKED** — attempt cap hit, or a non-convergent loop detected. Record: the last QA `VERDICT`, which `done when:` criteria are still unmet, and the last Root Cause hint so a human (or the next session) can pick it up.

## Run memory log (read at start, append the moment each item resolves)

The team keeps a persistent, cross-run memory at **`.claude/dev-team/team-memory.md`** in the working repo. Unlike the per-run `*-report.md` files (overwritten each item), this file **accumulates** — it is how the next run learns from this one.

- **At the start of a run**, both orchestrators read this file if it exists and factor its `Remember next run:` notes into track/agent choices (e.g. a flaky test suite, a build command that needs a flag, an approach that failed before). If it does not exist, create it with a `# Dev-team memory log` header on first write.
- **The moment an item resolves** — DONE or BLOCKED, *every* item, *every* track — append one entry **in the same step that records the item's outcome** (the PROGRESS.md write for `/dev-team-auto`; the final report for `/dev-team`). Ride it on the outcome-recording action that already fires reliably every item — do **not** defer it to shutdown. Deferred, it does not get written: by end of run the orchestrator is hundreds of lines past this instruction, which is why past runs left no `team-memory.md` at all. Append only; never rewrite prior entries.

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

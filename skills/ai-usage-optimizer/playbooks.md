# Systems Leverage Playbooks

One playbook per leverage gap. Each opens with the **leading word** that anchors
the fix. The theme throughout: *Nate built these systems — the goal is to make
reaching for them reflexive, and to keep the systems themselves healthy.*

---

## Skill Leverage — "reach"

**Gap:** Doing work by hand that a purpose-built skill already covers. The skill
exists, is loaded, and never gets invoked.

**Rule:** Before starting a chunk of work, ask *"is there a skill for this?"* The
answer is usually yes — the catalog is large. Reach for the system instead of
free-handing it.

**Work → skill map (Nate's actual toolkit):**
| When the work is… | Reach for |
|-------------------|-----------|
| Multi-file feature / build with tests + review | `/dev-team` (or `/dev-team-auto` unattended) |
| A single dev-team role (build, QA, review, fix, UI, analyze) | `/dt-engineer`, `/dt-qa`, `/dt-review`, `/dt-fix`, `/dt-ui`, `/dt-analyze` |
| Stress-testing a plan before building | `/grilling` |
| Designing a module interface or API | `/codebase-design`, `/design-an-interface` |
| A hard bug or perf regression | `/diagnosing-bugs` |
| Building a feature test-first | `/tdd` |
| Portfolio / writing / project pages | `/career-advisor`, `/writing-*`, `/edit-article` |
| Baseball analytics methodology review | `/baseball-research-advisor` |
| Reviewing a branch or diff | `/review`, `/code-review` |
| Filing bugs conversationally | `/qa` |
| Planning a refactor into safe commits | `/request-refactor-plan` |

**Anti-pattern:** A 700-turn portfolio session with zero skill invocations. That's
a whole toolkit sitting idle. Even one `/career-advisor` or `/review` pass would
have paid off.

**Diagnosis tip:** Cross `project_turns` (where effort went) against `skills_used`
(what fired). Big effort + empty skills = the highest-value gap in the report.

---

## Dev-Team Leverage — "delegate the build"

**Gap:** Hand-implementing multi-file features in the main session when the
dev-team convergence loop (Engineer → QA → Review → Fix) would build it more
robustly and in isolation.

**Rule:** If a task is more than a one-file edit and has a definition of "done,"
route it through the dev-team rather than doing it inline.

**Decision:**
```
Is it a single small edit?            → do it inline
Multi-file, has acceptance criteria?  → /dev-team (interactive) 
Whole PLAN.md to grind overnight?     → /dev-team-auto (unattended, experimental branch)
Just need one role right now?         → /dt-<role> standalone
```

**Why it matters:** The loop gives you tests (QA gate) and an optimization review
for free, on an isolated worktree — strictly more than a raw inline build. Skipping
it means you also skip the safety net you built.

**Anti-pattern:** Build-heavy Patio/portfolio sessions that never once invoked
`dev-team` or any `dt-*` role.

---

## Subagent Leverage — "fan out"

**Gap:** Broad investigation or parallel research done serially in the main
context when subagents could isolate the noise and run in parallel.

**Rule:** Delegate to a subagent when (a) the task spans >3 exploratory queries,
(b) you want an independent judgment, or (c) raw output would bloat main context.
Spawn independent legs in one message so they run in parallel.

**Which agent:**
- Broad file/symbol search where the target isn't known → `Explore`
- Multi-step research or refactor leg → `general-purpose`
- A dev-team role → the matching `dt-*` subagent
- Questions about Claude Code / SDK / API itself → `claude-code-guide`

**Anti-pattern:** Spawning a subagent for a one-file read (cold-start overhead not
worth it) — *or* the reverse, trawling 20 files inline when one Explore agent would
have returned just the conclusion.

---

## Memory System — "surface"

**Gap:** The managed memory system exists, but sessions end without persisting
what was learned — so the same context gets re-explained next time.

**Rule:** At the end of any session where something non-obvious surfaced, write it
to `~/.claude/memory` (→ `~/os/knowledge/memory`). Specifically:
- Preferences corrected mid-session ("no, don't do it that way") → `feedback`
- Confirmed non-obvious approaches ("yes, exactly") → `feedback`
- Project decisions not in the code (why, deadlines, constraints) → `project`
- Background/role revealed → `user`

**Write triggers:**
| Signal | Type | Capture |
|--------|------|---------|
| "no", "don't", "stop" | feedback | the rule + why + when it applies |
| "yes exactly", "perfect" | feedback | the validated approach |
| deadline / stakeholder mentioned | project | the fact + why it matters |
| background/role revealed | user | expertise level, how to pitch explanations |

**Anti-pattern (write side):** Memories about what *code* does — that's derivable.
Write only what's *not* in the code.

**Anti-pattern (health side):** High write rate but the same correction keeps
recurring → memory is being written but not retrieved. Check that `MEMORY.md` has
a pointer line and the `description:` is a real retrieval hook.

---

## Project Structure — "route through os"

**Gap:** The `~/os` structure (knowledge / skills / projects) is the source of
truth, but work happens without consulting or feeding it.

**Rule:** Let the structure do its job:
- Starting work on a named project → open its `projects/<name>/README.md` for the
  real repo path and context before diving in.
- New unsorted input (dumps, notes) → drop in `knowledge/raw/`, then triage into
  `me/`, `frameworks/`, `audience/`, or a project. Don't let raw pile up.
- Reusable know-how learned in a session → it belongs in `knowledge/`, not lost.
- A new repeatable workflow → consider authoring a skill (`cp skills/skills.md …`)
  rather than re-deriving it each time.

**Health signal:** If `project_turns` shows heavy work in a repo that has no
`projects/<name>/` index entry, the structure has a gap — add the pointer.

---

## System Health — "prune and sharpen"

**Gap:** The catalog grows but isn't maintained. Skills go stale, overlap, or
never fire because their trigger is weak.

**Checks (run only when the usage data points at them):**
- **Dead + overlapping:** a `skills_never_used` entry that duplicates one you do
  use → merge or delete. Two skills competing for the same trigger help neither.
- **Weak trigger:** a skill that *fits* recent work but never auto-invoked → its
  `description:` router line is the problem. Rewrite it to lead with the trigger
  phrase (the first sentence is what the router reads).
- **Orphaned system:** a whole subsystem (e.g. all `dt-*`) unused for many sessions
  → decide if it's genuinely not needed or just not top-of-mind, and fix whichever.

**Rule:** Health findings must be backed by the usage data — don't audit skills in
the abstract. Unused + overlapping + fits-the-work-but-never-fired are the signals.

---

## Model Selection — "match"

**Gap:** Using a heavy model for lightweight tasks (unnecessary cost/latency) or a
light model for complex tasks (poor output requiring extra correction rounds).

**The core models available in Claude Code:**

| Model | ID | Best for |
|-------|----|----------|
| Haiku 4.5 | `claude-haiku-4-5-20251001` | Simple, mechanical, high-volume tasks |
| Sonnet 4.6 | `claude-sonnet-4-6` | Default workhorse — most coding tasks |
| Opus 4.8 | `claude-opus-4-8` | Hard reasoning, architecture, deep debugging |
| Fable 5 | `claude-fable-5` | Most capable — reserve for the hardest tasks |

**Switch with:** `/model` in Claude Code to open the picker.
**Fast mode:** `/fast` toggles Opus 4.8 with speed optimization — good when Sonnet feels slow on complex tasks.

**Task → model mapping:**

| Task type | Model | Signals |
|-----------|-------|---------|
| Quick lookup ("what does this function do?") | Haiku | Short question, single file, no ambiguity |
| Rename / small rewrite / format fix | Haiku | Mechanical, known transformation |
| Add boilerplate ("add endpoint like X") | Haiku or Sonnet | Template-like, low reasoning needed |
| Standard feature implementation | Sonnet (default) | Multi-file, moderate complexity |
| Bug fix with known cause | Sonnet | The path is clear, just execute |
| Code review of a diff | Sonnet | Pattern matching, not deep reasoning |
| Hard debugging ("why is this failing?") | Opus | Unknown root cause, causal chain |
| Architecture / schema design | Opus | Multi-constraint reasoning, tradeoffs |
| Security audit | Opus | Needs careful, thorough analysis |
| Planning a large refactor | Opus | Upfront cost saves downstream rounds |
| Running `/grilling` or `/diagnosing-bugs` | Opus | Heavy analysis skills need the power |
| Subagent for research/exploration | Haiku or Sonnet | Don't burn Opus on a subagent that just greps |

**Model-switching habit:** Never run an entire session on one model by default.
Size each task before starting. If a simple session grows complicated — unexpected
bug, design gets hairy — switch up before continuing, not after five mediocre turns.

**Anti-pattern:**
```
Entire session on Sonnet including:
  - "Why does the JWT fail silently?"         ← needs Opus
  - "Design the new player ranking system"    ← needs Opus
  - "Rename this variable"                    ← Haiku is fine

→ Switch model per task, not per session
```

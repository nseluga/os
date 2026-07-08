---
name: ai-usage-optimizer
description: Audit how well Nate is actually using the AI systems he built (skills, the dev-team, subagents, memory, the os/projects structure) and prescribe better leverage. Also recommends the right model when invoked before a task. Use when the user wants a usage audit of his own systems, wants to know which skills/subsystems he's under-using, wants memory or system-health checked, or asks "which model should I use for X".
---

# AI Usage Optimizer

This audits **the systems Nate built in `~/os` and how well he personally uses
them** — not Claude's low-level execution mechanics. The question is: *you built
dozens of skills, a dev-team, a memory system, and an os structure — are you
actually getting leverage out of them, or are they sitting on the shelf?*

Two modes depending on how it's invoked:

- **Preemptive** — user described a task they're about to do → skip to Model Recommendation branch
- **Audit** — no task described → run the full systems-usage audit (adoption-led, with a system-health pass and model coaching)

---

## Phase 0 — Detect Mode

Check whether a task description was provided as part of the invocation (e.g. `/ai-usage-optimizer I'm about to redesign the auth flow`).

- Task description present → go to **Model Recommendation branch** immediately. Do not run the audit.
- No task description → go to **Phase 1** (full audit).

---

## [PREEMPTIVE] Model Recommendation Branch

Analyze the task description to recommend the right model before the user starts.

**Step 1 — Classify the task** using these signals:

| Signal | Weight |
|--------|--------|
| Keywords: "why", "debug", "architect", "design", "plan", "refactor", "security", "audit", "investigate", "performance", "optimize", "migrate", "figure out", "best approach" | +2 complexity |
| Message length > 300 chars | +1 complexity |
| Multi-step task ("design AND implement", "plan then build") | +1 complexity |
| Keywords: "what is", "where is", "show me", "rename", "add a", "quick", "list all" | +1 simplicity |
| Message length < 80 chars | +1 simplicity |
| Boilerplate ("add endpoint like this other one") | +1 simplicity |

**Step 2 — Map to model** using the table in [`playbooks.md`](playbooks.md) under "Model Selection."

**Step 3 — If a built skill fits the task, name it.** Before recommending only a
model, check whether one of Nate's own skills is the right entry point (e.g.
build work → `/dev-team`; stress-testing a plan → `/grilling`; a hard bug →
`/diagnosing-bugs`). Recommending the system beats recommending the raw model.

**Step 4 — Output** in this format:

```
## Model Recommendation

**Task classified as:** [Simple / Standard / Complex]

**Recommended model:** [Model name]
**Switch with:** `/model` in Claude Code, then select [model name]

**Fitting system (if any):** [/skill-name — why it fits, or "none — drive it directly"]

**Why:** [One sentence on why this model fits the task complexity]

**Rule of thumb for this task type:** [One sentence generalizable tip]
```

If the task is already a good fit for Sonnet with no matching skill, say so — don't recommend switching or a skill just to recommend something.

---

## [AUDIT] Phase 1 — Collect Metrics

Run the analyzer:

```bash
python3 ~/.claude/skills/ai-usage-optimizer/analyze.py 25
```

Capture the full JSON. If it errors, diagnose and fix before proceeding — never estimate metrics. The report measures *system usage*: skill adoption, dev-team activity, subagent leverage, memory writes, which projects the work happened in, real-world token spend, and model fit.

## Phase 2 — Score Each Dimension

Assign **Strong** / **Needs Work** / **Critical** to each. These dimensions are
about *leveraging the systems*, not tool mechanics.

| Dimension | Metric | Thresholds |
|-----------|--------|------------|
| Skill leverage | `sessions_with_skills` ÷ `sessions_analyzed` | ≥0.50 Strong · 0.20–0.49 Needs Work · <0.20 Critical |
| Skill breadth | `skills_used_count` (distinct built skills invoked) | ≥6 Strong · 2–5 Needs Work · <2 Critical |
| Dev-team leverage | `sessions_with_dev_team` vs. build-heavy sessions | used on most multi-file build work Strong · used occasionally Needs Work · never on build work Critical |
| Subagent leverage | `agent_usage_rate` | ≥0.30 Strong · 0.10–0.29 Needs Work · <0.10 Critical |
| Memory system | `memory_write_rate` | ≥1.0 Strong · 0.4–0.9 Needs Work · <0.4 Critical |
| Model fit | `total_model_mismatches` + `ever_switched_model` | 0 mismatches + switched Strong · 1–4 mismatches Needs Work · 5+ or never switched Critical |

Judgment note: `adoption_rate` over the whole catalog will look brutal (many
skills are niche or third-party). Don't score on raw adoption_rate — score on
whether the *work that actually happened* used the skills that fit it. Use
`skills_used`, `skills_never_used`, and `project_turns` together to make that call.

## Phase 3 — Adoption Deep-Dive (the core)

This is the heart of the audit. Cross-reference **what work happened** against
**which built systems were used**.

1. Look at `project_turns` — where did the effort go? (e.g. portfolio, Patio, os).
2. Look at `skills_used` — what did that effort actually invoke?
3. For each high-effort project/session, name the built skills that *should have*
   been in play but weren't, from `skills_never_used`. Be specific and honest:
   - Heavy build/feature work that never touched `dev-team` / `dt-*`
   - Planning or design work that never ran `grilling`, `codebase-design`, or `design-an-interface`
   - Bug work that never ran `diagnosing-bugs` or `tdd`
   - Writing/portfolio work that never used `career-advisor`, `writing-*`, or `edit-article`
   - Review work that never ran `review` or `code-review`
4. Call out the **top 3 highest-value unused skills** for Nate's actual workload —
   the ones that would have paid off in the sessions just analyzed. Name the
   session/project where each would have helped.

Frame this as leverage left on the table, not a scolding. He built these; the
goal is to make them reflexive.

## Phase 4 — System Health Pass (secondary)

A lighter look at the systems themselves, surfaced only where usage reveals a
design problem:

- **Dead skills:** anything in `skills_never_used` that has been unused for a long
  time *and* overlaps a skill he does use → candidate to merge, delete, or fix its
  `description:` trigger so it actually fires.
- **Trigger gaps:** a skill that fits the work but never auto-invoked may have a
  weak `description:` router line. Flag it as a description problem, not a usage
  problem.
- **Memory drift:** if `memory_write_rate` is high but the same corrections keep
  recurring, memory is being written but not retrieved — flag for review.

Keep this section short. Only raise health issues that the usage data actually points at.

## Phase 5 — Cost Attribution (observational)

This answers the cost-side question that complements adoption: *"where did my
tokens actually go, and was the system I reached for worth it?"* — using real
spend from the logs.

**Boundary — read this before reporting cost.** This is **observational**, not a
controlled benchmark. The tasks across sessions differ, so you **cannot** conclude
"system X is more token-efficient than Y" from these numbers — that's the job of
the benchmarking system Nate is building, which holds the task fixed. Here you may
only say *where* tokens went and *which sessions were outliers*. Never rank systems
on efficiency from this data.

Also note `cost_units` is a **weighted proxy** (input×1, cache-write×1.25,
cache-read×0.1, output×5), not dollars. Use it for relative comparison; report raw
tokens alongside it for grounding.

Read from the report:
1. `project_cost` — which project consumed the most spend.
2. `cost_outliers` — the 5 most expensive sessions, each with its project, turns,
   cost-per-turn, and which skills (if any) it used. **A high-cost outlier with
   `skills: null` is the headline finding** — expensive work done with zero system
   leverage, tying cost directly back to the adoption gap.
3. `skilled_avg_cost_per_session` vs `unskilled_avg_cost_per_session` — a descriptive
   contrast only. Do **not** frame it as "skills save/cost tokens" (confounded);
   frame it as "here's what your skilled vs. unskilled sessions cost on average."
4. `skill_cost_profile` — for context, what sessions using each skill cost. Useful
   for spotting a system that reliably rides along with very expensive sessions.

## Phase 6 — Model Coaching

Inspect `model_distribution`, `underpowered_tasks`, and `overpowered_tasks`.

- **Underpowered** (complex task, Sonnet/Haiku used): list up to 3 example tasks, name which model they warranted.
- **Overpowered** (simple task, Opus/Fable used): list up to 3 examples, note the unnecessary cost.
- **Never switched model:** flag as a habit to break — switching is free.

Use the model selection table in [`playbooks.md`](playbooks.md) to justify recommendations.

## Phase 7 — Prescribe Per Dimension

For each **Needs Work** or **Critical** dimension, give one prescription from [`playbooks.md`](playbooks.md) with one concrete example drawn from *this* report (name the real project/session). Skip Strong dimensions.

## Phase 8 — Report Format

```
## AI Systems Usage Report
**Sessions analyzed:** N  **Date:** YYYY-MM-DD
**Skills built:** X  ·  **Skills used:** Y  ·  **Effort by project:** [top 3]

### Leverage Scores
[Full dimension table with tiers]

### Adoption Deep-Dive
[Top 3 highest-value unused skills for the actual workload, each tied to a real session/project where it would have paid off]

### System Health
[Only issues the usage data points at — dead skills, weak triggers, memory drift]

### Cost Attribution
[Observational, not a benchmark. Spend by project; the top cost-outlier sessions with
their leverage (flag high-cost + zero-skill sessions); skilled vs. unskilled avg as a
descriptive contrast. State the weighted-proxy caveat once. Never rank systems on efficiency.]

### Model Coaching
[Mismatch summary + examples + switch instructions]

### Findings & Prescriptions
[Only Needs Work / Critical dimensions, each: finding → prescription → concrete example]

### Next-Session Cheat Sheet
[≤8 rules covering Nate's actual task types — which skill to reach for when, plus model switching]
```

Completion criterion: every dimension scored, the top-3 unused-skill deep-dive
delivered with real examples, cost attribution reported with the observational
caveat, model mismatches listed, every Needs Work / Critical dimension prescribed.
Do not end until all are covered.

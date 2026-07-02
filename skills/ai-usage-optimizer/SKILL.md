---
name: ai-usage-optimizer
description: Audit recent Claude Code sessions and prescribe efficiency improvements. Also recommends the right model when invoked before a task. Use when the user wants to reduce token spend, speed up tasks, optimize agent/subagent orchestration, improve memory hygiene, get a usage efficiency report, or asks "which model should I use for X".
---

# AI Usage Optimizer

Two modes depending on how it's invoked:

- **Preemptive** — user described a task they're about to do → skip to Model Recommendation branch
- **Audit** — no task described → run full session audit including model coaching

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

**Step 3 — Output** in this format:

```
## Model Recommendation

**Task classified as:** [Simple / Standard / Complex]

**Recommended model:** [Model name]
**Switch with:** `/model` in Claude Code, then select [model name]

**Why:** [One sentence on why this model fits the task complexity]

**Rule of thumb for this task type:** [One sentence generalizable tip]
```

If the task is already a good fit for Sonnet (standard complexity), say so — don't recommend switching just to recommend something.

---

## [AUDIT] Phase 1 — Collect Metrics

Run the analyzer:

```bash
python3 ~/.claude/skills/ai-usage-optimizer/analyze.py 25
```

Capture the full JSON. If it errors, diagnose and fix before proceeding — never estimate metrics.

## Phase 2 — Score Each Dimension

Assign **Strong** / **Needs Work** / **Critical** to each:

| Dimension | Metric | Thresholds |
|-----------|--------|------------|
| Parallelism | `overall_parallelism_rate` | ≥0.40 Strong · 0.15–0.39 Needs Work · <0.15 Critical |
| Missed parallel ops | `missed_parallel_opportunities` | <5 Strong · 5–20 Needs Work · >20 Critical |
| Agent leverage | `agent_usage_rate` | ≥0.30 Strong · 0.10–0.29 Needs Work · <0.10 Critical |
| Memory hygiene | `total_memory_writes` ÷ sessions | ≥1.5 Strong · 0.5–1.4 Needs Work · <0.5 Critical |
| Tool discipline | `bash_read_substitutions` | <3 Strong · 3–10 Needs Work · >10 Critical |
| Reread waste | `excessive_rereads` entry count | 0 Strong · 1–3 Needs Work · 4+ Critical |
| Context load | `avg_assistant_msg_len` | <600 Strong · 600–1200 Needs Work · >1200 Critical |
| Model fit | `total_model_mismatches` + `ever_switched_model` | 0 mismatches + switched Strong · 1–4 mismatches Needs Work · 5+ or never switched Critical |

## Phase 3 — Model Coaching

Inspect `model_distribution`, `underpowered_tasks`, and `overpowered_tasks` from the report.

For each mismatch type present, call it out:

**Underpowered** (complex task, Sonnet/Haiku used): List up to 3 example tasks from `underpowered_tasks`. Name the tasks and say which model they warranted.

**Overpowered** (simple task, Opus/Fable used): List up to 3 examples. Note the unnecessary cost.

**Never switched model** (all turns on same model): Flag this as a habit to break — model-switching is free and should be routine.

Use the model selection table in [`playbooks.md`](playbooks.md) to justify recommendations.

## Phase 4 — Prescribe Per Dimension

For each **Needs Work** or **Critical** dimension, one prescription from [`playbooks.md`](playbooks.md) with one concrete example. Skip Strong dimensions.

## Phase 5 — Report Format

```
## Claude Usage Efficiency Report
**Sessions analyzed:** N  **Date:** YYYY-MM-DD

### Efficiency Scores
[Full dimension table with tiers]

### Model Coaching
[Mismatch summary + examples + switch instructions]

### Findings & Prescriptions
[Only Needs Work / Critical, each: finding → prescription → example]

### Next-Session Cheat Sheet
[8 or fewer rules covering this user's actual task types, including model switching]
```

Completion criterion: every dimension scored, model mismatches listed with examples, every Needs Work / Critical dimension has a prescription. Do not end until all are covered.

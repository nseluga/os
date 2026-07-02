---
name: dev-team
description: Orchestrates the full professional dev team pipeline: Analyzer → Engineer → Reviewer → Bug Fixer. Use --stage to run a subset. Use --opus for complex tasks. Task from inline arg or TASK.md.
---

You are the dev-team orchestrator. You sequence the right agents for the job, pass reports between them, and gate between stages.

## Parse Arguments

From the arguments passed to this skill:

**Task:** any text that is not a flag is the task description. If no task text is given, read `TASK.md` from the project root. If neither exists, ask the user before proceeding.

**Stage flag** (default: `all`):
- `--stage analyze` — run Analyzer only
- `--stage engineer` — run Engineer only
- `--stage review` — run Reviewer only
- `--stage fix` — run Bug Fixer only
- `--stage all` — run full pipeline (Engineer → Reviewer → Bug Fixer)
- `--stage analyze+engineer` — run Analyzer then Engineer
- Analyzer is never included in `--stage all` automatically — it must be explicitly requested

**Model flag** (default: Sonnet):
- `--opus` — use `claude-opus-4-8` for Engineer and Bug Fixer agents
- default — use `claude-sonnet-4-6` for all agents

## Run the Pipeline

Run only the stages requested. For each stage, spawn an Agent using the instructions below. Wait for each agent to complete before spawning the next — stages are sequential.

After each stage completes, read the report it wrote before spawning the next agent. Pass the report content directly in the next agent's prompt.

---

### Stage: Analyzer

Spawn an Agent with this prompt (fill in [TASK]):

> Read `~/.claude/skills/dt-analyze/skill.md` for your full instructions. Your task: [TASK]

After it completes, read `.claude/dev-team/analyze-report.md`.

---

### Stage: Engineer

Spawn an Agent with this prompt (fill in [TASK], [MODEL], and [ANALYZE_REPORT] if available):

> Read `~/.claude/skills/dt-engineer/skill.md` for your full instructions. Your task: [TASK]. Use model [MODEL].
>
> [If analyze report exists:] The Analyzer has already mapped the codebase. Here is the analysis report — use it instead of re-exploring:
> [ANALYZE_REPORT content]

After it completes, read `.claude/dev-team/engineer-report.md`.

---

### Stage: Reviewer

Spawn an Agent with this prompt (fill in [ENGINEER_REPORT]):

> Read `~/.claude/skills/dt-review/skill.md` for your full instructions.
>
> The Engineer has completed their work. Here is the engineer report:
> [ENGINEER_REPORT content]

After it completes, read `.claude/dev-team/review-report.md`.

---

### Stage: Bug Fixer

Spawn an Agent with this prompt (fill in [MODEL], [ENGINEER_REPORT], [REVIEW_REPORT]):

> Read `~/.claude/skills/dt-fix/skill.md` for your full instructions. Use model [MODEL].
>
> Engineer report:
> [ENGINEER_REPORT content]
>
> Review report:
> [REVIEW_REPORT content]

After it completes, read `.claude/dev-team/fix-report.md`.

---

## After the Pipeline

When all requested stages are complete, summarize for the user:
- Which stages ran
- Branch name (from engineer report)
- Count of review findings and how many were fixed (from fix report, if applicable)
- Any disputed or deferred findings the user should know about
- Next step: `git merge [branch]` to bring the work into main when satisfied

Do not merge automatically. The user reviews and merges.

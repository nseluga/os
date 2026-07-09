#!/usr/bin/env python3
"""
Analyzes recent Claude Code sessions to surface how well Nate is USING the
AI systems he built (~/os): skills, the dev-team, subagents, memory, and the
project structure. Adoption-led, with a light system-health signal, plus
model-fit detection. Outputs a structured JSON report consumed by the
ai-usage-optimizer skill.
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
SKILLS_DIR = CLAUDE_DIR / "skills"   # symlink → ~/os/skills

AGENT_TOOL = "Agent"
SKILL_TOOL = "Skill"

# A skill launch surfaces in the transcript three ways, two of which the old
# leading-"/" check missed — undercounting dev-team-auto and any prompt-box
# invocation, which then showed up as "skills: null" cost outliers:
#   1. the assistant's `Skill` tool call            (already handled below)
#   2. a slash command typed in the prompt box, recorded inside <command-name>
#      tags — NOT as a leading "/"
#   3. the injected skill body, which always begins
#      "Base directory for this skill: .../skills/<name>"
# These patterns recover (2) and (3).
COMMAND_NAME_RE = re.compile(r"<command-name>\s*/?([\w.-]+(?::[\w.-]+)?)\s*</command-name>")
SKILL_BODY_RE = re.compile(r"Base directory for this skill:\s*\S*/skills/([\w.-]+)")

# Weighted cost proxy. These are the standard Anthropic price ratios relative to
# base input tokens (cache reads ~0.1x, cache writes ~1.25x, output ~5x) and are
# model-independent AS RATIOS — so "cost units" is comparable across sessions and
# systems without pinning a per-model dollar price. It is a proxy, not a bill.
COST_WEIGHTS = {
    "input_tokens": 1.0,
    "cache_creation_input_tokens": 1.25,
    "cache_read_input_tokens": 0.1,
    "output_tokens": 5.0,
}


def usage_cost(usage):
    """Return (raw_total_tokens, weighted_cost_units) for one message's usage."""
    if not isinstance(usage, dict):
        return 0, 0.0
    raw = 0
    cost = 0.0
    for field, weight in COST_WEIGHTS.items():
        v = usage.get(field, 0) or 0
        raw += v
        cost += v * weight
    return raw, cost

# Skill families that make up the "systems Nate built". Used to group the
# adoption report so a whole subsystem's usage is visible at a glance.
DEV_TEAM_SKILLS = {
    "dev-team", "dev-team-auto",
    "dt-analyze", "dt-engineer", "dt-qa", "dt-review", "dt-fix", "dt-ui",
}


def model_tier(model_id):
    m = model_id.lower()
    if "fable" in m:   return "fable"
    if "opus" in m:    return "opus"
    if "sonnet" in m:  return "sonnet"
    if "haiku" in m:   return "haiku"
    return "unknown"


def classify_complexity(text):
    """Return 'complex', 'standard', or 'simple' based on task description signals."""
    t = text.lower()
    complex_hits = sum(1 for s in [
        "why ", "why is", "why does", "debug", "architect", "design ", "plan ",
        "refactor", "migrate", "security", "audit", "analyze", "deep dive",
        "not working", "broken", "failing", "figure out", "understand why",
        "how should", "best approach", "tradeoff", "strategy", "investigate",
        "performance", "optimize", "restructure", "overhaul",
    ] if s in t)
    simple_hits = sum(1 for s in [
        "what is", "where is", "show me", "rename", "add a ", "what does",
        "how do i", "quick", "list all", "find the", "what are",
    ] if s in t)

    if len(text) > 500:
        complex_hits += 2
    elif len(text) < 80:
        simple_hits += 1

    if complex_hits > simple_hits:
        return "complex"
    if simple_hits > complex_hits:
        return "simple"
    return "standard"


def load_skill_catalog():
    """Every skill folder under ~/os/skills — the full menu of systems built."""
    catalog = []
    try:
        for entry in sorted(SKILLS_DIR.iterdir()):
            if entry.is_dir() and (entry / "SKILL.md").exists():
                catalog.append(entry.name)
    except Exception:
        pass
    return catalog


# Catalog as a set for O(1) membership — used to reject built-in slash commands
# (/model, /compact, /clear) that appear in <command-name> tags but aren't skills.
SKILL_CATALOG = set(load_skill_catalog())


def friendly_project(dir_name):
    """Decode an encoded cwd dir name into a readable project label."""
    name = dir_name
    prefix = "-Users-nateseluga-"
    if name.startswith(prefix):
        name = name[len(prefix):]
    if not name:
        name = "home"
    if "--claude-worktrees-" in name:
        base, _, wt = name.partition("--claude-worktrees-")
        name = f"{base or 'home'} (worktree: {wt})"
    return name or dir_name


def parse_sessions(max_sessions=20):
    sessions = []
    if not PROJECTS_DIR.exists():
        return sessions
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        for f in sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                session = parse_jsonl(f, project_dir.name)
                if session:
                    sessions.append(session)
            except Exception:
                pass
    sessions.sort(key=lambda s: s["mtime"], reverse=True)
    return sessions[:max_sessions]


def parse_jsonl(path, project):
    events = []
    try:
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
    except Exception:
        return None

    if not events:
        return None

    mtime = path.stat().st_mtime
    turns = 0
    agent_spawns = 0
    memory_writes = 0
    raw_tokens = 0
    cost_units = 0.0
    skill_invocations = Counter()
    subagent_types = Counter()
    models_seen = Counter()
    model_task_pairs = []   # (model, complexity, task_preview)
    last_user_text = ""

    session_skills = set()

    def mark_skill(raw, trusted=True):
        # One logical invocation can surface through several transcript signals
        # (tool call + <command-name> tag + injected body). Count each distinct
        # skill once per session so adoption/presence and per-session cost
        # attribution stay correct instead of double-counting the same run.
        # `trusted` signals (Skill tool, injected body) are always real skills;
        # untrusted ones (a bare slash command / <command-name> tag) must match
        # the catalog, else built-in CLI commands (/model, /compact) leak in.
        name = str(raw).split(":")[-1].strip()
        if not name or name in session_skills:
            return
        if not trusted and name not in SKILL_CATALOG:
            return
        session_skills.add(name)
        skill_invocations[name] += 1

    for event in events:
        etype = event.get("type")

        if etype == "user":
            content = event.get("message", {}).get("content", "")
            if isinstance(content, str):
                last_user_text = content
            elif isinstance(content, list):
                texts = [b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text"]
                last_user_text = " ".join(texts)

            # Detect skill launches through every signal (see regexes above):
            # injected body, <command-name> tag, and a leading "/skill-name".
            for m in SKILL_BODY_RE.finditer(last_user_text):
                mark_skill(m.group(1))
            for m in COMMAND_NAME_RE.finditer(last_user_text):
                mark_skill(m.group(1), trusted=False)
            stripped = last_user_text.strip()
            if stripped.startswith("/") and len(stripped) > 1:
                mark_skill(stripped[1:].split()[0], trusted=False)

        elif etype == "assistant":
            content = event.get("message", {}).get("content", [])
            model = event.get("message", {}).get("model", "unknown")
            if not isinstance(content, list):
                continue

            models_seen[model] += 1
            r, c = usage_cost(event.get("message", {}).get("usage"))
            raw_tokens += r
            cost_units += c
            turn_has_tool = False

            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") != "tool_use":
                    continue
                turn_has_tool = True
                name = block.get("name", "")
                inp = block.get("input", {}) if isinstance(block.get("input"), dict) else {}

                if name == AGENT_TOOL:
                    agent_spawns += 1
                    st = inp.get("subagent_type")
                    if st:
                        subagent_types[st] += 1
                elif name == SKILL_TOOL:
                    sk = inp.get("skill")
                    if sk:
                        mark_skill(sk)
                elif name == "Write" and "memory" in str(inp.get("file_path", "")):
                    memory_writes += 1

            if turn_has_tool:
                turns += 1
                if last_user_text:
                    complexity = classify_complexity(last_user_text)
                    tier = model_tier(model)
                    model_task_pairs.append({
                        "model": model,
                        "tier": tier,
                        "complexity": complexity,
                        "task": last_user_text[:120],
                    })
                last_user_text = ""

    if turns == 0 and not skill_invocations:
        return None

    # Model mismatch detection
    mismatches = []
    for pair in model_task_pairs:
        tier, complexity = pair["tier"], pair["complexity"]
        if complexity == "complex" and tier in ("haiku", "sonnet"):
            mismatches.append({"type": "underpowered", **pair})
        elif complexity == "simple" and tier in ("fable", "opus"):
            mismatches.append({"type": "overpowered", **pair})

    dev_team_calls = sum(c for s, c in skill_invocations.items() if s in DEV_TEAM_SKILLS)

    return {
        "project": friendly_project(project),
        "session_id": path.stem,
        "mtime": mtime,
        "total_turns": turns,
        "raw_tokens": raw_tokens,
        "cost_units": round(cost_units),
        "cost_per_turn": round(cost_units / turns) if turns else 0,
        "skill_invocations": dict(skill_invocations),
        "dev_team_calls": dev_team_calls,
        "agent_spawns": agent_spawns,
        "subagent_types": dict(subagent_types),
        "memory_writes": memory_writes,
        "model_distribution": dict(models_seen),
        "model_diversity": len(models_seen) > 1,
        "model_mismatches": mismatches,
    }


def aggregate(sessions):
    catalog = load_skill_catalog()
    if not sessions:
        return {"sessions_analyzed": 0, "skill_catalog_size": len(catalog),
                "skills_never_used": catalog}

    total_turns = sum(s["total_turns"] for s in sessions)
    total_agent_spawns = sum(s["agent_spawns"] for s in sessions)
    total_memory_writes = sum(s["memory_writes"] for s in sessions)
    total_dev_team_calls = sum(s["dev_team_calls"] for s in sessions)

    skill_usage = Counter()
    subagent_usage = Counter()
    combined_models = Counter()
    all_mismatches = []
    project_sessions = Counter()
    project_turns = Counter()

    # --- Cost attribution accumulators ---
    total_cost = 0
    total_raw_tokens = 0
    project_cost = Counter()
    # For each skill: total cost of sessions it appeared in, and how many sessions.
    skill_session_cost = defaultdict(int)
    skill_session_count = defaultdict(int)
    dev_team_session_cost = 0
    dev_team_session_n = 0
    skilled_session_cost = 0
    skilled_session_n = 0
    unskilled_session_cost = 0
    unskilled_session_n = 0

    for s in sessions:
        skill_usage.update(s["skill_invocations"])
        subagent_usage.update(s["subagent_types"])
        combined_models.update(s["model_distribution"])
        all_mismatches.extend(s["model_mismatches"])
        project_sessions[s["project"]] += 1
        project_turns[s["project"]] += s["total_turns"]

        c = s["cost_units"]
        total_cost += c
        total_raw_tokens += s["raw_tokens"]
        project_cost[s["project"]] += c
        for sk in s["skill_invocations"]:
            skill_session_cost[sk] += c
            skill_session_count[sk] += 1
        if s["dev_team_calls"] > 0:
            dev_team_session_cost += c
            dev_team_session_n += 1
        if s["skill_invocations"]:
            skilled_session_cost += c
            skilled_session_n += 1
        else:
            unskilled_session_cost += c
            unskilled_session_n += 1

    # Average cost of sessions each skill co-occurs with (attribution, not split).
    skill_cost_profile = {
        sk: {
            "sessions": skill_session_count[sk],
            "total_cost": skill_session_cost[sk],
            "avg_cost_per_session": round(skill_session_cost[sk] / skill_session_count[sk]),
        }
        for sk in sorted(skill_session_cost, key=lambda k: -skill_session_cost[k])
    }

    # Outlier sessions: the most expensive, with what (if anything) they leveraged.
    cost_outliers = [
        {
            "project": s["project"],
            "cost_units": s["cost_units"],
            "raw_tokens": s["raw_tokens"],
            "turns": s["total_turns"],
            "cost_per_turn": s["cost_per_turn"],
            "skills": list(s["skill_invocations"].keys()) or None,
        }
        for s in sorted(sessions, key=lambda x: -x["cost_units"])[:5]
    ]

    # Adoption: which built skills are used vs. never touched.
    used_from_catalog = [sk for sk in catalog if sk in skill_usage]
    never_used = [sk for sk in catalog if sk not in skill_usage]
    # Invocations that hit a catalog skill vs. one-off/typo/unknown.
    catalog_invocations = sum(c for sk, c in skill_usage.items() if sk in catalog)
    total_invocations = sum(skill_usage.values())

    sessions_with_skills = sum(1 for s in sessions if s["skill_invocations"])
    sessions_with_agents = sum(1 for s in sessions if s["agent_spawns"] > 0)
    sessions_with_memory = sum(1 for s in sessions if s["memory_writes"] > 0)
    sessions_with_dev_team = sum(1 for s in sessions if s["dev_team_calls"] > 0)

    ever_switched_model = any(s["model_diversity"] for s in sessions)
    underpowered = [m for m in all_mismatches if m["type"] == "underpowered"]
    overpowered  = [m for m in all_mismatches if m["type"] == "overpowered"]

    n = len(sessions)
    return {
        "sessions_analyzed": n,
        "total_turns": total_turns,

        # --- Skill adoption (primary) ---
        "skill_catalog_size": len(catalog),
        "skills_used": dict(skill_usage.most_common()),
        "skills_used_count": len(used_from_catalog),
        "skills_never_used": never_used,
        "adoption_rate": round(len(used_from_catalog) / len(catalog), 2) if catalog else 0,
        "skill_invocation_rate": round(total_invocations / n, 2),
        "sessions_with_skills": sessions_with_skills,
        "catalog_invocation_share": round(catalog_invocations / total_invocations, 2) if total_invocations else 0,

        # --- Dev-team subsystem ---
        "dev_team_calls": total_dev_team_calls,
        "sessions_with_dev_team": sessions_with_dev_team,

        # --- Subagent leverage ---
        "total_agent_spawns": total_agent_spawns,
        "agent_usage_rate": round(sessions_with_agents / n, 2),
        "subagent_types": dict(subagent_usage.most_common()),

        # --- Memory system ---
        "total_memory_writes": total_memory_writes,
        "memory_write_rate": round(total_memory_writes / n, 2),
        "sessions_with_memory": sessions_with_memory,

        # --- Project structure ---
        "project_sessions": dict(project_sessions.most_common()),
        "project_turns": dict(project_turns.most_common()),

        # --- Cost attribution (observational token spend) ---
        # NOTE: "cost_units" is a weighted proxy (see COST_WEIGHTS), not dollars.
        # This is real-world spend from the logs, NOT a controlled benchmark —
        # tasks differ across sessions, so use it to spot where tokens went and
        # flag outliers, not to compare systems apples-to-apples.
        "total_cost_units": total_cost,
        "total_raw_tokens": total_raw_tokens,
        "avg_cost_per_session": round(total_cost / n),
        "project_cost": dict(project_cost.most_common()),
        "skill_cost_profile": skill_cost_profile,
        "dev_team_avg_cost_per_session": round(dev_team_session_cost / dev_team_session_n) if dev_team_session_n else 0,
        "skilled_avg_cost_per_session": round(skilled_session_cost / skilled_session_n) if skilled_session_n else 0,
        "unskilled_avg_cost_per_session": round(unskilled_session_cost / unskilled_session_n) if unskilled_session_n else 0,
        "cost_outliers": cost_outliers,

        # --- Model fit (kept) ---
        "model_distribution": dict(combined_models.most_common()),
        "ever_switched_model": ever_switched_model,
        "underpowered_tasks": underpowered[:10],
        "overpowered_tasks": overpowered[:10],
        "total_model_mismatches": len(all_mismatches),

        "per_session": sessions,
    }


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    sessions = parse_sessions(n)
    report = aggregate(sessions)
    print(json.dumps(report, indent=2))

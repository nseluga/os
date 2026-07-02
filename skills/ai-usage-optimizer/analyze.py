#!/usr/bin/env python3
"""
Analyzes recent Claude Code sessions to surface efficiency patterns.
Outputs a structured JSON report consumed by the ai-usage-optimizer skill.
"""

import json
import sys
from collections import defaultdict, Counter
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"

READ_TOOLS = {"Read", "Glob", "Grep"}
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit"}
BASH_TOOL = "Bash"
AGENT_TOOL = "Agent"
SEARCH_TOOL = "ToolSearch"


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


def parse_sessions(max_sessions=20):
    sessions = []
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
    turns = []
    user_msg_lengths = []
    assistant_msg_lengths = []
    agent_spawns = 0
    memory_writes = 0
    tool_search_calls = 0
    bash_read_subs = 0
    re_reads = defaultdict(int)
    models_seen = Counter()
    model_task_pairs = []   # (model, complexity, task_preview)
    last_user_text = ""

    for event in events:
        etype = event.get("type")

        if etype == "user":
            content = event.get("message", {}).get("content", "")
            if isinstance(content, str):
                last_user_text = content
                user_msg_lengths.append(len(content))
            elif isinstance(content, list):
                texts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        texts.append(block.get("text", ""))
                        user_msg_lengths.append(len(block.get("text", "")))
                last_user_text = " ".join(texts)

        elif etype == "assistant":
            content = event.get("message", {}).get("content", [])
            model = event.get("message", {}).get("model", "unknown")
            if not isinstance(content, list):
                continue

            models_seen[model] += 1

            turn_tools = []
            turn_text_len = 0

            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")

                if btype == "text":
                    turn_text_len += len(block.get("text", ""))

                elif btype == "tool_use":
                    name = block.get("name", "")
                    inp = block.get("input", {})
                    turn_tools.append(name)

                    if name == AGENT_TOOL:
                        agent_spawns += 1
                    if name == SEARCH_TOOL:
                        tool_search_calls += 1
                    if name == "Write" and "memory" in str(inp.get("file_path", "")):
                        memory_writes += 1
                    if name == "Read":
                        re_reads[inp.get("file_path", "")] += 1
                    if name == BASH_TOOL:
                        cmd = str(inp.get("command", ""))
                        if any(kw in cmd for kw in ["cat ", "head ", "tail ", "echo "]):
                            bash_read_subs += 1

            if turn_tools:
                turns.append(turn_tools)
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

            if turn_text_len:
                assistant_msg_lengths.append(turn_text_len)

    if not turns:
        return None

    parallel_turns = sum(1 for t in turns if len(t) > 1)
    single_tool_turns = sum(1 for t in turns if len(t) == 1)
    total_turns = len(turns)
    parallelism_rate = parallel_turns / total_turns if total_turns else 0

    all_tools = [t for turn in turns for t in turn]
    tool_freq = dict(Counter(all_tools).most_common(15))
    excessive_rereads = {fp: cnt for fp, cnt in re_reads.items() if cnt >= 3}

    missed_parallel = 0
    for i in range(len(turns) - 1):
        a, b = turns[i], turns[i + 1]
        if (len(a) == 1 and len(b) == 1
                and a[0] in READ_TOOLS | {BASH_TOOL}
                and b[0] in READ_TOOLS | {BASH_TOOL}):
            missed_parallel += 1

    # Model mismatch detection
    mismatches = []
    for pair in model_task_pairs:
        tier, complexity = pair["tier"], pair["complexity"]
        if complexity == "complex" and tier in ("haiku", "sonnet"):
            mismatches.append({"type": "underpowered", **pair})
        elif complexity == "simple" and tier in ("fable", "opus"):
            mismatches.append({"type": "overpowered", **pair})

    return {
        "project": project,
        "session_id": path.stem,
        "mtime": mtime,
        "total_turns": total_turns,
        "parallel_turns": parallel_turns,
        "single_tool_turns": single_tool_turns,
        "parallelism_rate": round(parallelism_rate, 2),
        "missed_parallel_opportunities": missed_parallel,
        "agent_spawns": agent_spawns,
        "memory_writes": memory_writes,
        "tool_search_calls": tool_search_calls,
        "bash_read_substitutions": bash_read_subs,
        "excessive_rereads": excessive_rereads,
        "tool_frequency": tool_freq,
        "model_distribution": dict(models_seen),
        "model_diversity": len(models_seen) > 1,
        "model_task_pairs": model_task_pairs,
        "model_mismatches": mismatches,
        "avg_user_msg_len": int(sum(user_msg_lengths) / len(user_msg_lengths)) if user_msg_lengths else 0,
        "avg_assistant_msg_len": int(sum(assistant_msg_lengths) / len(assistant_msg_lengths)) if assistant_msg_lengths else 0,
    }


def aggregate(sessions):
    if not sessions:
        return {}

    total_turns = sum(s["total_turns"] for s in sessions)
    total_parallel = sum(s["parallel_turns"] for s in sessions)
    total_missed = sum(s["missed_parallel_opportunities"] for s in sessions)
    total_agent_spawns = sum(s["agent_spawns"] for s in sessions)
    total_memory_writes = sum(s["memory_writes"] for s in sessions)
    total_bash_subs = sum(s["bash_read_substitutions"] for s in sessions)

    all_rereads = {}
    for s in sessions:
        for fp, cnt in s["excessive_rereads"].items():
            all_rereads[fp] = all_rereads.get(fp, 0) + cnt

    combined_tools = Counter()
    combined_models = Counter()
    all_mismatches = []
    for s in sessions:
        combined_tools.update(s["tool_frequency"])
        combined_models.update(s["model_distribution"])
        all_mismatches.extend(s["model_mismatches"])

    overall_parallelism = round(total_parallel / total_turns, 2) if total_turns else 0
    sessions_with_agents = sum(1 for s in sessions if s["agent_spawns"] > 0)
    agent_usage_rate = round(sessions_with_agents / len(sessions), 2)
    avg_u = int(sum(s["avg_user_msg_len"] for s in sessions) / len(sessions))
    avg_a = int(sum(s["avg_assistant_msg_len"] for s in sessions) / len(sessions))

    ever_switched_model = any(s["model_diversity"] for s in sessions)
    underpowered = [m for m in all_mismatches if m["type"] == "underpowered"]
    overpowered  = [m for m in all_mismatches if m["type"] == "overpowered"]

    return {
        "sessions_analyzed": len(sessions),
        "total_turns": total_turns,
        "overall_parallelism_rate": overall_parallelism,
        "missed_parallel_opportunities": total_missed,
        "total_agent_spawns": total_agent_spawns,
        "agent_usage_rate": agent_usage_rate,
        "total_memory_writes": total_memory_writes,
        "bash_read_substitutions": total_bash_subs,
        "excessive_rereads": dict(sorted(all_rereads.items(), key=lambda x: -x[1])[:10]),
        "top_tools": dict(combined_tools.most_common(15)),
        "model_distribution": dict(combined_models.most_common()),
        "ever_switched_model": ever_switched_model,
        "underpowered_tasks": underpowered[:10],
        "overpowered_tasks": overpowered[:10],
        "total_model_mismatches": len(all_mismatches),
        "avg_user_msg_len": avg_u,
        "avg_assistant_msg_len": avg_a,
        "per_session": sessions,
    }


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    sessions = parse_sessions(n)
    report = aggregate(sessions)
    print(json.dumps(report, indent=2))

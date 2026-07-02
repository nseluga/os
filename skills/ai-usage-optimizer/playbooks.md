# Efficiency Playbooks

One playbook per waste vector. Each opens with the **leading word** that anchors the fix.

---

## Parallelism — "batch"

**Waste vector:** Single-tool turns executing serially when calls are independent.

**Rule:** Every time you issue a tool call, ask: what else can I start *right now* that doesn't depend on this result? Issue all independent calls in the same message block.

**High-yield batching patterns:**
- Exploration: `Read` + `Bash(grep)` + `Bash(find)` — all together, never serial
- Pre-flight: `git status` + `git diff` + `git log` — always parallel
- Multi-file reads: any time 2+ files are needed for the same decision, read them together
- Agent fan-out: spawn multiple `Agent` calls in one message for independent research legs

**Anti-pattern to break:**
```
Turn 1: Read file_a.py           ← wrong
Turn 2: Read file_b.py           ← wrong
Turn 3: Bash("grep pattern .")   ← wrong

→ Replace with one turn: [Read file_a.py] [Read file_b.py] [Bash grep]
```

**When NOT to batch:** When output of call A determines the *path* of call B. Sequential is correct there — don't force a batch.

---

## Agent Leverage — "delegate"

**Waste vector:** Doing broad investigation in the main context when a subagent could isolate the noise.

**Rule:** Delegate when (a) the task spans >3 grepping queries, (b) you need an independent judgment, or (c) the output would bloat main context with raw results.

**Delegation decision tree:**
```
Is the target file/symbol already known?
  Yes → use Read/grep directly (subagent overhead not worth it)
  No, and it requires >3 exploratory queries → spawn Explore subagent

Is a second opinion needed (security review, architecture check)?
  Yes → spawn claude or code-reviewer subagent

Will the result be large raw output (log trawl, big grep sweep)?
  Yes → spawn general-purpose subagent, ask for a summary back
```

**Parallel subagent teams:** For multi-leg research, spawn all agents in one message. Each gets a self-contained prompt (no references to "what we discussed" — the agent hasn't seen the conversation).

```
Agent(description="Find auth endpoints", prompt="List all Flask routes in backend/app.py that check JWT. Return route + line number only.")
Agent(description="Find DB queries", prompt="List raw SQL queries in backend/app.py. Return query text + line number.")
← both in same message, run in parallel
```

**Anti-pattern:** Spawning a subagent to do a one-file read or a task that takes <30 seconds inline. Subagent cold-start costs ~1000 tokens of overhead.

---

## Memory Hygiene — "surface"

**Waste vector:** Repeatedly explaining the same context to Claude across sessions because nothing was persisted.

**Rule:** At the end of any session where you learned something non-obvious, write it. Specifically surface:
- User preferences corrected mid-session ("no, don't do it that way")
- Confirmed non-obvious approaches ("yes, that was right")  
- Project decisions that aren't in the code (why something was done, deadlines, constraints)
- New tools/patterns the user introduced

**Memory write triggers:**
| Signal | Memory type | What to capture |
|--------|-------------|-----------------|
| User says "no", "don't", "stop" | feedback | The rule + why + when to apply |
| User says "yes exactly", "perfect" | feedback | The validated approach |
| User mentions a deadline or stakeholder | project | The fact + why it matters |
| User reveals their background/role | user | Their expertise level, how to pitch explanations |

**Anti-pattern:** Writing memories about what *code* does — that's derivable. Write only what's *not* in the code.

**Memory file format:**
```markdown
---
name: slug-kebab-case
description: One-line hook for retrieval
metadata:
  type: feedback | user | project | reference
---
Rule/fact here. **Why:** reason. **How to apply:** when this kicks in.
```

---

## Tool Discipline — "native"

**Waste vector:** Using `Bash(cat)`, `Bash(head)`, `Bash(echo)` when dedicated tools exist that give better UX and are more token-efficient.

**Substitution table:**
| What you're tempted to do | Use instead |
|---------------------------|-------------|
| `Bash("cat file.py")` | `Read(file_path)` |
| `Bash("head -50 file.py")` | `Read(file_path, limit=50)` |
| `Bash("tail -20 file.py")` | `Read(file_path, offset=N, limit=20)` |
| `Bash("echo 'content' > file")` | `Write(file_path, content)` |
| `Bash("sed -i 's/old/new/g' file")` | `Edit(file_path, old_string, new_string)` |
| `Bash("grep -n pattern file")` | `Bash` is fine here — Grep tool if available |

**When Bash IS correct:**
- Running build/test commands
- Git operations
- Multi-step shell pipelines
- Anything requiring shell state or environment

---

## Reread Waste — "cache in mind"

**Waste vector:** Reading the same file 3+ times across a session, paying tokens each time.

**Rule:** After the first read of a large file, reason from what you've already seen rather than re-reading. If you need a specific section you didn't read, use `offset`+`limit` to fetch only that section.

**Patterns that cause rereads:**
- Editing a file, then re-reading to "verify" — unnecessary, Edit would have failed if it missed
- Checking a file early in session, then re-reading late when the file hasn't changed
- Subagents re-reading files the main agent already read (each subagent is stateless — this is unavoidable, but minimize by passing excerpts in the subagent prompt)

**When reread is correct:**
- The file was edited by another tool since the last read
- You need a different section not previously loaded

---

## Context Load — "trim"

**Waste vector:** Long assistant responses that narrate reasoning rather than deliver results; or loading large files entirely when only a section is needed.

**Rules:**
1. **Trim prose:** Don't narrate internal deliberation. State results and decisions. One sentence per status update.
2. **Partial reads:** Use `offset`+`limit` when you know which part of a file you need. Reading a 500-line file for one function wastes ~400 lines of context.
3. **Summarize into context:** When using subagents to explore, ask them to return a concise summary (not raw tool output). The summary enters main context; the raw output stays in the subagent's now-discarded window.
4. **Compression awareness:** Sessions compress after ~40k tokens. Work that's early in a long session may get summarized — if a detail is critical, write it to memory or a file so it survives compression.
5. **Skill descriptions load every turn:** Model-invoked skills cost tokens on every turn. Prefer `disable-model-invocation: true` for skills you always call manually.

---

## Subagent Team Patterns — "formation"

Named formations for common multi-agent tasks:

**Fan-out / gather** — Multiple agents explore in parallel, main synthesizes:
```
[Agent A: find X] [Agent B: find Y] [Agent C: find Z]  ← one message
Synthesize all three results inline
```

**Sequential pipeline** — Agent A's output feeds Agent B (can't parallelize):
```
Agent A: research → returns structured summary
Agent B: implement (given summary in prompt)
```

**Independent review** — Two agents give separate opinions on the same artifact:
```
[Agent A: security review of diff] [Agent B: correctness review of diff]
← use when you want two genuinely independent reads
← both see the same diff excerpt embedded in their prompts
```

**Self-contained prompt rule:** Every subagent prompt must be independently executable. Include: the goal, the specific files/paths to look at, any prior decisions that constrain the work, and the expected output format. Never write "based on what we discussed" — the subagent hasn't seen the conversation.

---

## Prompt Efficiency — "precise"

**Waste vector:** Vague or over-broad prompts that require follow-up clarification rounds.

**Rules:**
1. **State the constraint, not just the goal.** "Fix the login bug" → "The login endpoint at `backend/auth.py:45` throws a 500 when `username` contains an apostrophe — fix the SQL injection without changing the response schema."
2. **Name the file and line.** Saves one round of exploration.
3. **Specify the output format.** "Return only the modified function, no prose" halves the response.
4. **Scope the task.** "Don't touch anything outside `backend/auth.py`" prevents scope creep that wastes turns on unwanted changes.
5. **Pre-load context in the prompt.** If you know the architecture, say it. Don't make Claude re-derive what you already know.

---

## Model Selection — "match"

**Waste vector:** Using a heavy model for lightweight tasks (unnecessary cost/latency) or a light model for complex tasks (poor output requiring extra correction rounds).

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
| Subagent for research/exploration | Haiku or Sonnet | Don't burn Opus on a subagent that just grepping |

**Model-switching habit:**
Never run an entire session on one model by default. Size each task before starting it. If you open a session for a simple lookup, stay on Sonnet. If the task grows — you hit an unexpected bug, the design gets complicated — switch up before continuing, not after you've spent 5 turns getting mediocre output from an underpowered model.

**Anti-pattern:**
```
Entire session on Sonnet including:
  - "Why does the JWT fail silently?"         ← needs Opus
  - "Design the new player ranking system"    ← needs Opus
  - "Rename this variable"                    ← Haiku is fine

→ Switch model per task, not per session
```

---
name: feedback-hook-schema-verify-against-docs
description: "When writing a Claude Code hook that reads stdin JSON, verify field names against the official hooks reference, not by guessing then writing a self-consistent test"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4f7a1375-3888-4f15-97b1-8209ee2e519f
  modified: 2026-08-04T12:26:06.152Z
---

A hook script must read the exact JSON keys Claude Code sends on stdin — verify
these against https://code.claude.com/docs/en/hooks.md (or the docs-guide
agent) before writing the parsing code, not by assumption.

**Why:** `~/.claude/memory-relevance-hook.py` (the active-memory-recall system
documented in [[memory-writing]]) read `hook_input.get("user_prompt")`
instead of the real key `"prompt"`. It silently no-op'd on every real
`UserPromptSubmit` event for two full days (Aug 2-3, 96 real prompts, 0 fires)
while its own unit + stress test suites reported 58/58 passing — because both
test files fed the same wrong key (`"user_prompt"`) the hook expected, so the
mismatch was invisible to self-testing. Manual smoke-tests of the hook via
`echo '{...}' | python3 hook.py` had the same blind spot for the same reason.

**How to apply:** for any new stdin-consuming hook (UserPromptSubmit, Stop,
PreToolUse, etc.), pull the field list from official docs first. When
validating a hook actually fires in production, don't just re-run its own
test suite — grep real session transcripts
(`~/.claude/projects/*/*.jsonl`, field `message.content[].text` containing
the hook's known output string) for evidence it fired on genuine prompts,
since a hook and its tests sharing one wrong assumption will pass cleanly
while doing nothing live.

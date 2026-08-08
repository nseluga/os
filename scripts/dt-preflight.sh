#!/usr/bin/env bash
# Preflight for /dev-team-auto. Run from the repo root before the first item.
# Gathers the run's baseline; never blocks. The orchestrator reads and interprets.
# Exits 0 always — a failing suite IS the baseline, not an error.

set -uo pipefail
cd "${1:-.}" || exit 0

echo "=== dt-preflight: $(pwd) ==="

# 1. Declared test command vs. what's actually on disk (obs 5).
declared=$(node -p "require('./package.json').scripts?.test ?? ''" 2>/dev/null)
echo "declared test command: ${declared:-<none>}"
# Prune by NAME, not path — nested node_modules (monorepos, worktrees) are the
# common case and a top-level `-path ./node_modules` prune silently misses them.
files=$(find . \( -name node_modules -o -name .git -o -name .venv -o -name dist \
  -o -name .next -o -name .claude \) -prune -o \
  \( -name '*.test.*' -o -name '*.spec.*' -o -name 'test_*.py' -o -name '*_test.go' \) \
  -print 2>/dev/null | wc -l | tr -d ' ')
echo "test files on disk: $files"
echo "  ^ if the suite below reports far fewer tests than $files files' worth, the"
echo "    declared command is stale (migration leftover) — find the real runner."

# 2. Stale listeners on common dev/test ports (obs 1).
echo "--- ports ---"
for p in 3000 3001 4000 5173 5432 8000 8080; do
  pid=$(lsof -ti tcp:"$p" -sTCP:LISTEN 2>/dev/null | head -1)
  [ -n "$pid" ] && echo "PORT $p BUSY — pid $pid ($(ps -p "$pid" -o comm= 2>/dev/null))"
done
echo "  ^ any listener you did not start is a stale server from a prior run."
echo "    Kill it before item 1 or live-smoke tests poll the wrong server/DB."

# 3. The baseline itself (obs 3, 4).
echo "--- baseline suite ---"
if [ -z "$declared" ]; then
  echo "no test script declared — find the real command before gating on tests"
else
  npm test 2>&1 | tail -40
fi
echo "=== end preflight ==="
echo "Record: pass/fail counts + the NAME of every failure. Those failures are"
echo "not regressions and must not be 'fixed' by editing assertions."

#!/bin/bash
# Guard against recursive invocation — nested claude sessions would re-trigger this
LOCK="/tmp/os-maintenance-$USER.lock"
if ! mkdir "$LOCK" 2>/dev/null; then exit 0; fi
trap "rm -rf $LOCK" EXIT

OS_DIR="$HOME/os"
LOG="$HOME/.claude/os-maintenance.log"

triage_raw() {
  local raw_dir="$OS_DIR/knowledge/raw"
  local count
  count=$(find "$raw_dir" -maxdepth 1 -type f ! -name "README.md" | wc -l | tr -d ' ')

  [ "$count" -eq 0 ] && return 0

  echo "[$(date)] Triaging $count file(s) from knowledge/raw/" >> "$LOG"
  claude -p "You are maintaining Nate's personal OS repo at ~/os.

Triage all files in knowledge/raw/ (except README.md) into their proper homes:
- Personal info, preferences, goals, working style → knowledge/me/
- Mental models, methods, reusable frameworks → knowledge/frameworks/
- Info about people or orgs Nate writes/builds for → knowledge/audience/
- Project-specific info → projects/<name>/ (match by name)

After placing each file, delete it from knowledge/raw/. Then run:
  git -C ~/os add -A && git -C ~/os commit -m 'auto: triage knowledge/raw/'

Be concise. If a file's category is ambiguous, default to knowledge/me/." \
    --cwd "$OS_DIR" >> "$LOG" 2>&1

  echo "[$(date)] Triage complete" >> "$LOG"
}

triage_raw

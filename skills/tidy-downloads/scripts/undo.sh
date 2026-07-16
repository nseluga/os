#!/usr/bin/env bash
# undo.sh — reverse a tidy run. Moves every file back to where it came from.
#
# Usage: undo.sh [LOG.tsv]
#   With no arg, undoes the most recent run in ~/Downloads/.tidy-undo/.
#   Log lines are: <current_path><TAB><original_path>
#
# Collision-safe on the way back too: never overwrites.
set -euo pipefail

BASE="${TIDY_BASE:-$HOME/Downloads}"
UNDO_DIR="$BASE/.tidy-undo"

LOG="${1:-}"
if [ -z "$LOG" ]; then
  LOG=$(ls -t "$UNDO_DIR"/*.tsv 2>/dev/null | head -1 || true)
  [ -z "$LOG" ] && { echo "no undo logs found in $UNDO_DIR" >&2; exit 1; }
fi
echo "undoing: $LOG"

restored=0
# Reverse order so nested moves unwind cleanly
tail -r "$LOG" | while IFS=$'\t' read -r cur orig || [ -n "$cur" ]; do
  [ -z "${cur:-}" ] && continue
  if [ ! -e "$cur" ]; then echo "skip (gone): $cur" >&2; continue; fi
  mkdir -p "$(dirname "$orig")"
  target="$orig"
  if [ -e "$target" ]; then
    name="${orig%.*}"; ext="${orig##*.}"
    [ "$ext" = "$orig" ] && ext=""
    n=2
    while :; do
      if [ -n "$ext" ]; then cand="$name (restored $n).$ext"; else cand="$name (restored $n)"; fi
      [ -e "$cand" ] || { target="$cand"; break; }
      n=$((n+1))
    done
  fi
  mv "$cur" "$target"
  echo "restored: $(basename "$cur")"
  restored=$((restored+1))
done
echo "done. moved back from $LOG"

#!/usr/bin/env bash
# safe_move.sh — execute a tidy plan safely, with an undo log.
#
# Usage: safe_move.sh PLAN.tsv [BASE_DIR]
#   PLAN.tsv lines: <source_name><TAB><dest_subfolder>
#     source_name   = a top-level entry in BASE_DIR (name only, no path)
#     dest_subfolder = folder under BASE_DIR to move it into (created if needed)
#   BASE_DIR defaults to ~/Downloads.
#
# Guarantees:
#   - Never deletes. Never overwrites: name collisions get " (2)", " (3)"... suffixes.
#   - Records every move to ~/Downloads/.tidy-undo/<timestamp>.tsv for undo.sh.
#   - Skips sources that don't exist, are the undo/output dirs, or in-progress downloads.
set -euo pipefail

PLAN="${1:?usage: safe_move.sh PLAN.tsv [BASE_DIR]}"
BASE="${2:-$HOME/Downloads}"
UNDO_DIR="$BASE/.tidy-undo"
mkdir -p "$UNDO_DIR"
LOG="$UNDO_DIR/$(date +%Y%m%d-%H%M%S).tsv"

moved=0 skipped=0
while IFS=$'\t' read -r src dest || [ -n "$src" ]; do
  [ -z "${src:-}" ] && continue
  case "$src" in \#*) continue ;; esac            # comment lines

  srcpath="$BASE/$src"
  if [ ! -e "$srcpath" ]; then
    echo "skip (missing): $src" >&2; skipped=$((skipped+1)); continue
  fi
  case "$src" in
    _sorted|.tidy-undo|*.crdownload|*.part|*.download )
      echo "skip (protected): $src" >&2; skipped=$((skipped+1)); continue ;;
  esac
  if [ -z "${dest:-}" ]; then
    echo "skip (no dest): $src" >&2; skipped=$((skipped+1)); continue
  fi

  destdir="$BASE/$dest"
  mkdir -p "$destdir"

  # Collision-safe target name
  base="$src"; target="$destdir/$base"
  if [ -e "$target" ]; then
    name="${base%.*}"; ext="${base##*.}"
    [ "$ext" = "$base" ] && ext=""                # no extension
    n=2
    while :; do
      if [ -n "$ext" ]; then cand="$destdir/$name ($n).$ext"; else cand="$destdir/$name ($n)"; fi
      [ -e "$cand" ] || { target="$cand"; break; }
      n=$((n+1))
    done
  fi

  mv "$srcpath" "$target"
  printf '%s\t%s\n' "$target" "$srcpath" >> "$LOG"   # dest<TAB>original, for undo
  echo "moved: $src -> $dest/$(basename "$target")"
  moved=$((moved+1))
done < "$PLAN"

echo "---"
echo "moved $moved, skipped $skipped"
echo "undo log: $LOG"

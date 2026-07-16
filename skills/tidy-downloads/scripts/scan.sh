#!/usr/bin/env bash
# scan.sh — emit a TSV inventory of the top level of a directory for classification.
# Columns: name<TAB>type<TAB>ext<TAB>size_bytes<TAB>mtime_iso
# Skips in-progress downloads, dotfiles, and the tidy working dir. Does NOT recurse.
set -euo pipefail

DIR="${1:-$HOME/Downloads}"
cd "$DIR"

for entry in *; do
  [ -e "$entry" ] || continue                      # empty dir guard
  case "$entry" in
    .* ) continue ;;                                # dotfiles
    _sorted|.tidy-undo ) continue ;;                # our own working output
    *.crdownload|*.part|*.download|*.tmp ) continue ;;  # in-progress downloads
  esac

  if [ -d "$entry" ]; then
    case "$entry" in
      *.app|*.rtfd|*.bundle|*.framework ) type="bundle" ;;
      * ) type="dir" ;;
    esac
    ext=""
  else
    type="file"
    ext="${entry##*.}"
    [ "$ext" = "$entry" ] && ext=""                 # no extension
  fi

  size=$(stat -f%z "$entry" 2>/dev/null || echo 0)
  mtime=$(stat -f "%Sm" -t "%Y-%m-%dT%H:%M" "$entry" 2>/dev/null || echo "")
  printf '%s\t%s\t%s\t%s\t%s\n' "$entry" "$type" "$ext" "$size" "$mtime"
done

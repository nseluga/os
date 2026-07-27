#!/usr/bin/env bash
# Smoke test for the `design` skill stack. Read-only — creates and modifies nothing.
# Usage: bash ~/os/skills/design/reference/smoke-test.sh [project-dir]
# Exit: 0 = ready to run, 1 = a hard component is broken, 2 = wired but corpus not extracted yet.
PROJ="${1:-$HOME/portfolio}"
DL="$HOME/os/knowledge/library/design-language"
pass=0; fail=0; pend=0
ok(){ printf '  \033[32mPASS\033[0m  %s\n' "$1"; pass=$((pass+1)); }
no(){ printf '  \033[31mFAIL\033[0m  %s\n' "$1"; fail=$((fail+1)); }
wait_(){ printf '  \033[33mPEND\033[0m  %s\n' "$1"; pend=$((pend+1)); }

echo "== 1. Impeccable (technical floor) =="
IMP=$(ls -d "$HOME"/.claude/plugins/cache/impeccable/impeccable/*/skills/impeccable 2>/dev/null | sort -V | tail -1)
[ -n "$IMP" ] && ok "resolves: ${IMP#$HOME/}" || { no "plugin not found — run: claude plugin install impeccable@impeccable"; exit 1; }
for f in craft-floor typeset colorize layout animate adapt operate audit live; do
  [ -f "$IMP/reference/$f.md" ] || no "missing reference/$f.md"
done
[ -f "$IMP/scripts/detector/registry/antipatterns.mjs" ] && ok "anti-slop registry present" || no "antipatterns.mjs missing"
if out=$(cd "$PROJ" 2>/dev/null && node "$IMP/scripts/detect.mjs" --json --help 2>&1); then ok "detect.mjs executes"; else no "detect.mjs failed: $out"; fi

echo "== 2. Impeccable live mode (in $PROJ) =="
if [ -d "$PROJ" ]; then
  lv=$(cd "$PROJ" && node "$IMP/scripts/live.mjs" 2>&1 | head -c 400)
  case "$lv" in
    *context_missing*) wait_ "live gate 1: needs PRODUCT.md + DESIGN.md shims (expected)";;
    *config_missing*)  wait_ "live gate 2: needs .impeccable/live/config.json (expected)";;
    *'"ok": true'*|*'"ok":true'*) ok "live mode fully configured";;
    *) no "live.mjs unexpected output: $lv";;
  esac
else no "project dir not found: $PROJ"; fi

echo "== 3. The design skill =="
S="$HOME/os/skills/design/SKILL.md"
[ -f "$S" ] && ok "SKILL.md present ($(wc -l < "$S" | tr -d ' ') lines)" || no "SKILL.md missing"
[ "$(grep -m1 '^name:' "$S" | awk '{print $2}')" = "design" ] && ok "frontmatter name matches folder" || no "name/folder mismatch"
[ -e "$HOME/.claude/skills/design/SKILL.md" ] && ok "symlink resolves (skill is live)" || no "not visible via ~/.claude/skills"
[ -d "$HOME/os/skills/layout-loop" ] && no "layout-loop still present — should be deleted" || ok "layout-loop retired"

echo "== 4. Design language layers =="
[ -f "$DL/craft.md" ] && { grep -q "STALE" "$DL/craft.md" && wait_ "craft.md present but STALE (re-extraction pending)" || ok "craft.md extracted"; } || no "craft.md missing"
for d in modes styles brands; do [ -d "$DL/$d" ] && ok "$d/ exists" || no "$d/ missing"; done
nm=$(ls "$DL"/modes/*.md 2>/dev/null | grep -vc README)
[ "$nm" -ge 2 ] && ok "mode files written ($nm)" || wait_ "modes/ holds only README — app.md + website.md not written"
ns=$(find "$DL/styles" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
[ "$ns" -ge 5 ] && ok "style catalog has $ns styles (phase 1 can run)" || wait_ "style catalog has $ns styles — phase 1 HARD-STOPS below 5"
grep -q "RETIRED" "$DL/brands/nate-personal.md" 2>/dev/null && wait_ "nate-personal brand RETIRED — needs re-authoring" || ok "nate-personal brand usable"

echo "== 5. Reference corpus =="
# Before an extraction session the corpus sits in raw/; after one it lives in styles/.
# Count both, so this check stays meaningful on either side of the session.
n=$(ls "$HOME"/os/knowledge/raw/*.png "$HOME"/os/knowledge/raw/*.jpg 2>/dev/null | wc -l | tr -d ' ')
f=$(find "$DL/styles" -mindepth 2 -type f \( -name '*.png' -o -name '*.jpg' \) 2>/dev/null | wc -l | tr -d ' ')
tot=$((n+f))
[ "$tot" -ge 30 ] && ok "$tot references in corpus ($f filed by style, $n awaiting clustering)" || wait_ "only $tot references (want 30-50)"
[ -f "$HOME/os/knowledge/raw/sources.md" ] && ok "sources.md present" || no "sources.md missing — URLs unrecoverable"
t=$(cd "$HOME/os" && git ls-files knowledge/raw/ knowledge/library/ | grep -cE '\.(png|jpg|jpeg)$')
[ "$t" -eq 0 ] && ok "images gitignored (public repo safe)" || no "$t images TRACKED — third-party work would be published"

echo "== 6. Higgsfield =="
# Two paths: MCP tools (preferred, loaded via ToolSearch at runtime — not testable
# from a shell) and the skill pack, which shells out to a separate CLI binary.
if command -v higgsfield >/dev/null 2>&1; then
  ok "higgsfield CLI on PATH ($(higgsfield --version 2>/dev/null | head -1))"
else
  wait_ "higgsfield CLI not on PATH — skill-pack path is down; MCP tools are the fallback"
  echo "        install: curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh"
fi
[ -f "$HOME/.claude/skills/higgsfield-generate/SKILL.md" ] && ok "higgsfield-generate skill pack present (gitignored — reinstall from marketplace)" || wait_ "higgsfield-generate skill pack missing"

echo
echo "  $pass passed · $fail failed · $pend pending"
[ "$fail" -gt 0 ] && { echo "  => BROKEN: fix failures above."; exit 1; }
[ "$pend" -gt 0 ] && { echo "  => WIRED, NOT READY: plumbing is sound; pending items are the extraction session."; exit 2; }
echo "  => READY: /design can run end to end."; exit 0

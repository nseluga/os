#!/usr/bin/env python3
"""Link-drift check for the ~/os vault.

Reports two kinds of drift:
  1. [[wikilinks]] that resolve to no file (or ambiguously to several)
  2. INDEX.md entries that name something absent, or omit something present

Prints one line per finding, nothing when clean. Exit 1 if anything is found.
"""
import os
import re
import subprocess
import sys
import pathlib

ROOT = pathlib.Path(os.environ.get("OS_DIR", pathlib.Path.home() / "os"))
SKIP_DIRS = {".git", ".claude", ".obsidian", "node_modules"}

# INDEX.md files that deliberately describe structure rather than list contents,
# and folders that are deliberately unindexed (see CLAUDE.md "Index maintenance").
INDEX_EXEMPT = {"knowledge/memory/INDEX.md", "knowledge/raw/INDEX.md"}

WIKILINK = re.compile(r"\[\[([^\]|#^]+)")
INDEX_BULLET = re.compile(r"^\s*[-*]\s+`([^`\n]+)`", re.M)  # a list entry's subject
FENCED = re.compile(r"^```.*?^```", re.M | re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def prose(text):
    """Drop fenced blocks and inline code — Obsidian renders no links there."""
    return INLINE_CODE.sub("", FENCED.sub("", text))


def ignored(paths):
    """Basenames of the given paths that git is configured to ignore."""
    paths = [str(p) for p in paths]
    if not paths:
        return set()
    try:
        r = subprocess.run(
            ["git", "-C", str(ROOT), "check-ignore", "--stdin"],
            input="\n".join(paths), capture_output=True, text=True,
        )
    except OSError:
        return set()  # no git available — report everything rather than nothing
    return {pathlib.Path(line).name for line in r.stdout.splitlines() if line.strip()}


def md_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".md"):
                yield pathlib.Path(dirpath) / fn


def check_links(files):
    by_name = {}
    by_path = set()
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        by_path.add(rel[:-3])  # drop .md
        by_name.setdefault(f.stem, []).append(rel)

    findings = []
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        for raw in WIKILINK.findall(prose(f.read_text(errors="ignore"))):
            # `\|` is the escaped alias separator used inside markdown tables
            target = raw.rstrip("\\").strip()
            if not target:
                continue
            if target.endswith(".md"):
                target = target[:-3]
            if target in by_path:
                continue
            hits = by_name.get(target.rsplit("/", 1)[-1], [])
            if len(hits) == 1 and "/" not in target:
                continue
            if not hits:
                findings.append(f"unresolved link  {rel}: [[{raw}]]")
            else:
                findings.append(
                    f"ambiguous link   {rel}: [[{raw}]] -> {', '.join(sorted(hits))}"
                )
    return findings


def check_indexes(files):
    findings = []
    for f in files:
        if f.name != "INDEX.md":
            continue
        rel = f.relative_to(ROOT).as_posix()
        if rel in INDEX_EXEMPT:
            continue
        d = f.parent
        text = f.read_text(errors="ignore")
        # Only bullet entries are claims about what the folder holds, so only
        # those can be stale. But a file named anywhere in the INDEX — including
        # in prose — counts as covered, so it isn't reported as omitted.
        claimed = {e.strip().rstrip("/") for e in INDEX_BULLET.findall(text)}
        present = set()
        for child in d.iterdir():
            name = child.name
            if name.startswith(".") or name in ("INDEX.md", "README.md"):
                continue
            if child.is_dir() or name.endswith(".md"):
                present.add(name)
        # An entry may name a file ("plan-md.md"), a folder ("dev-team"), or a
        # folder's stem — accept any spelling that points at something present.
        stems = {p.rsplit(".md", 1)[0] for p in present}
        for entry in sorted(claimed):
            if entry not in present and entry not in stems:
                findings.append(f"index lists missing  {rel}: `{entry}`")

        # Listing gitignored content is fine (projects/INDEX.md does it by
        # design); failing to list it is not drift, since it does not ship.
        for item in sorted(present - ignored(d / n for n in present)):
            stem = item.rsplit(".md", 1)[0]
            # Documented anywhere counts — several INDEXes describe their
            # contents in an ASCII tree rather than a backticked bullet list.
            if item not in text and stem not in text:
                findings.append(f"index omits present  {rel}: `{item}`")
    return findings


def main():
    files = sorted(md_files())
    findings = check_links(files) + check_indexes(files)
    for line in findings:
        print(line)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

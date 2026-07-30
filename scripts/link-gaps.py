#!/usr/bin/env python3
"""Locator-gap finder: where one file NAMES another but nothing resolves it.

Advisory, NOT a gate — it emits candidates for review and is deliberately not
wired into maintenance.sh. Run it when you want to audit link coverage.

It detects *references* ("this file names that file"), never *relationships*
("these files seem similar"). Semantic similarity produces a hairball and was
rejected by design; see CLAUDE.md -> Link maintenance.

Precision rules, each of which killed a whole class of false positives:
  - multi-word aliases only (a stem like `review` matches everything)
  - bare filenames only when that basename is unique (24 files are README.md)
  - same-folder pairs skipped: containment already resolves them
  - an INDEX.md naming its own subtree is containment, which stays backticked
  - STOPLIST for names that are also ordinary prose here ("engineer report")

Known limit: it cannot tell "the engineer report" (an artifact the dev-team
loop produces) from a reference to dt-engineer's skill file. Role nouns that
double as prose are irreducible without semantics — expect some noise.
"""
# Names that read as ordinary prose in this repo, not as file references.
STOPLIST = {
    "dev team", "engineer report", "qa report", "fix report", "review report",
    "research brief", "analyze report", "research partner", "career advisor",
    "task observer", "ingest data", "improve system", "new client repo",
}
import os, re, sys, pathlib
ROOT=pathlib.Path.home()/'os'; SKIP={'.git','.claude','.obsidian','node_modules'}
files=[]
for dp,dn,fn in os.walk(ROOT):
    dn[:]=[d for d in dn if d not in SKIP]
    files+=[pathlib.Path(dp)/f for f in fn if f.endswith('.md')]
files=[f for f in files if not f.is_symlink()]
rel={f:f.relative_to(ROOT).as_posix() for f in files}
text={f:f.read_text(errors='ignore') for f in files}

H1=re.compile(r'^#\s+(.+)$',re.M); NAME=re.compile(r'^name:\s*(.+)$',re.M)
W=re.compile(r'\[\[([^\]|#^]+)'); MD=re.compile(r'\[[^\]]*\]\(([^)]+\.md)[^)]*\)')

def aliases(f):
    a=set()
    stem=f.stem.replace('-',' ').replace('_',' ').strip()
    if len(stem.split())>=2: a.add(stem.lower())
    m=H1.search(text[f])
    if m:
        t=re.sub(r'[^\w\s-]',' ',m.group(1)).strip().lower()
        if len(t.split())>=2: a.add(t)
    m=NAME.search(text[f])
    if m:
        n=m.group(1).strip().strip('"').replace('-',' ').lower()
        if len(n.split())>=2: a.add(n)
    return a

# which targets does file f already link to?
byname={}
for f,r in rel.items(): byname.setdefault(f.stem,[]).append(f)
paths={r.removesuffix('.md'):f for f,r in rel.items()}
def linked(f):
    out=set()
    for raw in W.findall(text[f]):
        t=raw.rstrip('\\').strip().removesuffix('.md')
        if t in paths: out.add(paths[t])
        else:
            h=byname.get(t.rsplit('/',1)[-1],[])
            if len(h)==1: out.add(h[0])
    for m in MD.findall(text[f]):
        p=(f.parent/m).resolve()
        if p in rel: out.add(p)
    return out

EXEMPT={'MEMORY.md','CLAUDE.md','README.md','INDEX.md'}
uniq={k for k,v in byname.items() if len(v)==1}
rows=[]
for tgt in files:
    if tgt.name in EXEMPT: continue
    al=aliases(tgt)
    # a bare filename only locates anything if that basename is unique
    fname=tgt.name if tgt.stem in uniq else None
    for src in files:
        if src is tgt: continue
        t=text[src]; L=None; hit=None
        for a in al:
            if a in STOPLIST: continue
            for m in re.finditer(r'(?<![\w/-])'+re.escape(a)+r'(?![\w-])', t, re.I):
                hit=a; break
            if hit: break
        if not hit and fname:
            for m in re.finditer(r'(?<![\w/-])'+re.escape(fname)+r'(?![\w])', t):
                hit=fname; break
        if not hit: continue
        if src.parent==tgt.parent: continue   # same folder: containment resolves it
        # an INDEX naming its own subtree is containment, which stays backticked by design
        if src.name=='INDEX.md' and str(tgt).startswith(str(src.parent)+os.sep): continue
        if L is None: L=linked(src)
        if tgt in L: continue
        rows.append((rel[src],hit,rel[tgt]))

print(f"{len(rows)} candidate locator gaps -- review, do not treat as drift\n")
for s,h,t in sorted(rows):
    print(f'  {s}\n      says "{h}"  ->  {t}')

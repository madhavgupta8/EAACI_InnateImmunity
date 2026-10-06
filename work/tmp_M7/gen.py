#!/usr/bin/env python3
"""Fill citation markers from the ledger.
[[ID,ID]] -> <span class="src" title="ID,ID">Abbas p.12, 13</span>   (M7 style)
{{ID,ID}} -> <span class="src" title="ID,ID">A12,13</span>           (pearls short style)
"""
import csv, glob, os, re, sys
ROOT = "/Users/madhavgupta/Projects/Papa_EAACIexam"
L = {}
for f in glob.glob(ROOT + "/work/ledger/M*.csv"):
    for r in csv.DictReader(open(f, encoding="utf-8")):
        L[r["fact_id"].strip()] = r
SHORT = {"Abbas": "A", "Janeway": "J", "HAE-GL": "GL"}
bad = []

def label(ids, short):
    groups = {}
    for i in ids:
        r = L.get(i)
        if not r:
            bad.append(i); continue
        pg = r["page"].strip().replace("p.", "")
        groups.setdefault(r["source"], [])
        if pg not in groups[r["source"]]:
            groups[r["source"]].append(pg)
    if short:
        return " ".join(SHORT[s] + ",".join(p) for s, p in groups.items())
    return "; ".join(f"{s} p.{', '.join(p)}" for s, p in groups.items())

def sub(m, short):
    ids = [x.strip() for x in m.group(1).split(",") if x.strip()]
    vol = any(L.get(i, {}).get("volatile") == "Y" for i in ids)
    return f'<span class="src{" volatile" if vol else ""}" title="{",".join(ids)}">{label(ids, short)}</span>'

for tpl, out in [("M7.tpl.html", "pack/modules/M7-summary.html"), ("pearls.tpl.html", "pack/pearls.html")]:
    p = os.path.join(ROOT, "work/tmp_M7", tpl)
    if not os.path.exists(p): continue
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"\[\[([^\]]+)\]\]", lambda m: sub(m, False), t)
    t = re.sub(r"\{\{([^}]+)\}\}", lambda m: sub(m, True), t)
    open(os.path.join(ROOT, out), "w", encoding="utf-8").write(t)
    print("wrote", out)
if bad:
    print("UNKNOWN IDS:", sorted(set(bad))); sys.exit(1)

#!/usr/bin/env python3
"""Build script for the innate immunity pack.

1. Merge work/ledger/M*.csv -> pack/ledger/facts.csv (+ facts.html review sheet)
2. Validate ledger and MCQs; check every fact ID cited in HTML exists
3. Merge work/mcq/*.json -> pack/quiz/questions.js
4. Build pack/quiz/answer-key.html -> answer-key.pdf, pack/pearls.html -> pearls.pdf
"""
import csv, glob, html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, "work")
P = os.path.join(ROOT, "pack")
CHROME = os.path.expanduser(
    "~/Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-arm64/chrome-headless-shell")
FIELDS = ["fact_id", "module", "fact", "source", "page", "quote", "volatile", "verified_by"]
problems = []


def warn(msg):
    problems.append(msg)


# ---------- 1. ledger ----------
facts = []
for f in sorted(glob.glob(os.path.join(W, "ledger", "M*.csv"))):
    with open(f, newline="", encoding="utf-8") as fh:
        r = csv.DictReader(fh)
        if r.fieldnames != FIELDS:
            warn(f"{os.path.basename(f)}: header {r.fieldnames} != {FIELDS}")
        for row in r:
            facts.append({k: (row.get(k) or "").strip() for k in FIELDS})
ids = {}
for row in facts:
    if row["fact_id"] in ids:
        warn(f"duplicate fact_id {row['fact_id']}")
    ids[row["fact_id"]] = row
    if row["source"] not in ("Abbas", "Janeway", "HAE-GL"):
        warn(f"{row['fact_id']}: unknown source {row['source']!r}")
    if not row["quote"]:
        warn(f"{row['fact_id']}: empty quote")
    if row["volatile"] not in ("Y", "N"):
        warn(f"{row['fact_id']}: volatile={row['volatile']!r}")

os.makedirs(os.path.join(P, "ledger"), exist_ok=True)
with open(os.path.join(P, "ledger", "facts.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, FIELDS)
    w.writeheader()
    w.writerows(facts)

SRC_FULL = {"Abbas": "Abbas 11e", "Janeway": "Janeway 8e", "HAE-GL": "WAO/EAACI HAE GL 2017"}
rows = "\n".join(
    f"<tr class='{'vol' if r['volatile']=='Y' else ''}'><td>{html.escape(r['fact_id'])}</td><td>{html.escape(r['fact'])}</td>"
    f"<td>{SRC_FULL.get(r['source'], r['source'])} p.{html.escape(r['page'].replace('p.', ''))}</td>"
    f"<td class='q'>“{html.escape(r['quote'])}”</td><td>{'⚠' if r['volatile']=='Y' else ''}</td><td class='chk'></td></tr>"
    for r in facts)
with open(os.path.join(P, "ledger", "facts.html"), "w", encoding="utf-8") as fh:
    fh.write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Fact ledger — expert review</title>
<link rel="stylesheet" href="../assets/style.css"><style>
main{{max-width:1200px}} td{{font-size:.82rem}} td.q{{color:#5b6475;font-style:italic}} tr.vol td{{background:#fdf6ea!important}}
td.chk{{width:4.5rem}} @media print{{@page{{size:A4 landscape}} thead{{display:table-header-group}}}}
</style></head><body><main>
<h1>Fact ledger — expert review sheet</h1>
<p class="subtitle">{len(facts)} facts · single source of truth for notes, MCQs and video scripts.
Tick the last column (✓ / ✗ + note). ⚠ = volatile fact (drug, guideline, number) — check against current guidance.</p>
<table><thead><tr><th>ID</th><th>Fact</th><th>Source</th><th>Supporting quote</th><th>Vol.</th><th>Verified</th></tr></thead>
<tbody>{rows}</tbody></table></main></body></html>""")

# ---------- 2. HTML citation check ----------
for f in sorted(glob.glob(os.path.join(P, "modules", "*.html"))) + [os.path.join(P, "pearls.html")]:
    if not os.path.exists(f):
        continue
    txt = open(f, encoding="utf-8").read()
    for m in re.finditer(r'class="src[^"]*"\s+title="([^"]+)"|title="([^"]+)"\s+class="src', txt):
        for fid in re.split(r"[,\s]+", (m.group(1) or m.group(2)).strip()):
            if fid and fid not in ids:
                warn(f"{os.path.basename(f)} cites unknown fact {fid}")
    for d in re.findall(r'<figure class="diagram" id="(D\d+)"', txt):
        pass

# ---------- 3. MCQs ----------
qs = []
for f in sorted(glob.glob(os.path.join(W, "mcq", "*.json"))):
    try:
        qs += json.load(open(f, encoding="utf-8"))
    except Exception as e:
        warn(f"{os.path.basename(f)}: JSON error {e}")
seen = set()
for q in qs:
    qid = q.get("id")
    if qid in seen:
        warn(f"duplicate question {qid}")
    seen.add(qid)
    t = q.get("type")
    if t == "A":
        if len(q["options"]) != 5 or sum(o["correct"] for o in q["options"]) != 1:
            warn(f"{qid}: Type A needs 5 options / 1 correct")
    elif t == "KPRIM":
        if len(q["options"]) != 4:
            warn(f"{qid}: KPrim needs 4 options")
    elif t == "SCT":
        for it in q["items"]:
            if set(it["credits"]) != {"-2", "-1", "0", "+1", "+2"}:
                warn(f"{qid}: SCT credits keys")
    else:
        warn(f"{qid}: unknown type {t}")
    for o in q.get("options", []):
        if re.search(r"\b(all|none) of the above\b", o["text"], re.I):
            warn(f"{qid}: 'all/none of the above'")
        if not o.get("explanation") or not o.get("source"):
            warn(f"{qid}{o['key']}: missing explanation/source")
    for fid in q.get("fact_ids", []):
        if fid not in ids:
            warn(f"{qid}: unknown fact {fid}")


def order(q):
    m = re.match(r"(M\d|SCT)-?([AKS])?(\d+)", q["id"])
    return (q["module"], {"A": 0, "KPRIM": 1, "SCT": 2}[q["type"]], int(re.findall(r"\d+$", q["id"])[0]))


qs.sort(key=order)
with open(os.path.join(P, "quiz", "questions.js"), "w", encoding="utf-8") as fh:
    fh.write("// Generated by work/build.py from work/mcq/*.json — do not edit by hand.\n")
    fh.write("window.QUESTIONS = " + json.dumps(qs, ensure_ascii=False, indent=1) + ";\n")

# ---------- 4. answer key ----------
e = html.escape
parts = []
for q in qs:
    if q["type"] in ("A", "KPRIM"):
        key = (next(o["key"] for o in q["options"] if o["correct"]) if q["type"] == "A"
               else " / ".join("+" if o["correct"] else "−" for o in q["options"]))
        opts = "".join(
            f"<li><b>{o['key']}{' ✔' if (o['correct'] and q['type']=='A') else ''}{(' (+)' if o['correct'] else ' (−)') if q['type']=='KPRIM' else ''}</b> {e(o['text'])}"
            f"<br><span class='ex'>{e(o['explanation'])} <span class='src'>{e(o['source'])}</span></span></li>"
            for o in q["options"])
        parts.append(f"<div class='q'><h3>{q['id']} <span class='tag'>{'Type A' if q['type']=='A' else 'KPrim'}</span> "
                     f"<span class='key'>Key: {key}</span></h3><p>{e(q['stem'])}</p><ol class='opts'>{opts}</ol></div>")
    else:
        lines = "".join(
            f"<li><b>Hypothesis:</b> {e(it['hypothesis'])} · <b>New info:</b> {e(it['new_info'])}<br>"
            f"Credits: {', '.join(f'{k}: {v}' for k, v in it['credits'].items())}<br><span class='ex'>{e(it['rationale'])} <span class='src'>{e(it['source'])}</span></span></li>"
            for it in q["items"])
        parts.append(f"<div class='q'><h3>{q['id']} <span class='tag'>SCT</span></h3><p>{e(q['stem'])}</p><ol class='opts'>{lines}</ol></div>")
with open(os.path.join(P, "quiz", "answer-key.html"), "w", encoding="utf-8") as fh:
    fh.write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Answer key — Innate immunity quiz</title>
<link rel="stylesheet" href="../assets/style.css"><style>
.q{{border-top:1px solid #d9dee7;padding:.4rem 0;break-inside:avoid}} .q h3{{margin:.3rem 0;font-size:1rem}}
.q p{{margin:.2rem 0 .3rem}} .opts{{list-style:none;padding-left:.5rem;margin:.2rem 0;font-size:.88rem}} .opts li{{margin:.2rem 0}}
.ex{{color:#5b6475}} .key{{float:right;color:#2e7d5b}} .tag{{font-size:.72rem;background:#eef1f5;border-radius:4px;padding:0 .35rem;color:#5b6475;font-weight:400}}
@media print{{html{{font-size:9.5pt}}}}
</style></head><body><main><h1>Answer key — innate immunity quiz</h1>
<p class="subtitle">{sum(q['type']=='A' for q in qs)} Type A · {sum(q['type']=='KPRIM' for q in qs)} KPrim · {sum(q['type']=='SCT' for q in qs)} SCT.
KPrim: 4/4 = 1 pt, 3/4 = 0.5 pt, ≤2/4 = 0. Sources: Abbas 11e, Janeway 8e, WAO/EAACI HAE guideline 2017.</p>
{''.join(parts)}</main></body></html>""")


def pdf(src, dst):
    if not os.path.exists(CHROME):
        warn("headless chrome not found; PDFs skipped")
        return
    subprocess.run([CHROME, "--headless", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={dst}", "file://" + src], capture_output=True)


pdf(os.path.join(P, "quiz", "answer-key.html"), os.path.join(P, "quiz", "answer-key.pdf"))
if os.path.exists(os.path.join(P, "pearls.html")):
    pdf(os.path.join(P, "pearls.html"), os.path.join(P, "pearls.pdf"))
if "--all-pdf" in sys.argv:
    os.makedirs(os.path.join(P, "pdf"), exist_ok=True)
    for f in sorted(glob.glob(os.path.join(P, "modules", "*.html"))):
        pdf(f, os.path.join(P, "pdf", os.path.basename(f).replace(".html", ".pdf")))
    pdf(os.path.join(P, "ledger", "facts.html"), os.path.join(P, "pdf", "fact-ledger.pdf"))

print(f"facts: {len(facts)}  questions: {len(qs)} "
      f"(A {sum(q['type']=='A' for q in qs)}, KPrim {sum(q['type']=='KPRIM' for q in qs)}, SCT {sum(q['type']=='SCT' for q in qs)})")
print(f"problems: {len(problems)}")
for p in problems:
    print("  -", p)

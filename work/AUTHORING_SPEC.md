# Authoring spec — Innate Immunity lecture pack (EAACI/UEMS exam, 19 Oct 2026)

Read this whole file before you write anything. The master plan is `../innate-immunity-lecture-plan.md`.

## 1. Source lock (most important rule)

- Write ONLY facts that you find in the page-tagged source files in `work/sources_text/`.
  Each page starts with a marker such as `##### [Abbas 11e p.65] (PDF page 79) #####`.
  Cite the **book page** from that marker (not the PDF page).
- Allowed sources and citation short forms:
  | File | Cite as |
  |---|---|
  | `abbas_ch*.txt` | `Abbas p.65` (Abbas, Cellular and Molecular Immunology, 11th ed.) |
  | `janeway_ch*.txt` (OCR text, may have small OCR errors) | `Janeway p.52` (Janeway's Immunobiology, 8th ed.) |
  | `hae_guideline_2017.txt` | `HAE-GL p.4` (WAO/EAACI HAE guideline, 2017 revision, Allergy 2018) |
- Do NOT use your own background knowledge for facts, numbers, drug names or gene names that are not in these files. If a topic in the plan is not covered by the sources, write a short note `Not covered in provided sources — needs expert input.` and add it to your report. Do not fill the gap from memory.
- Volatile facts (drug approvals, doses, prevalence numbers, guideline recommendations) → mark them volatile (see below). The HAE guideline file is the 2017 revision; a newer 2021 revision exists but is not in the sources. Add a caution box in any HAE-treatment section that says recommendations follow the 2017 revision and must be checked against the current guideline.
- Janeway 8th ed. and Abbas 11th ed. can disagree with newer nomenclature. Prefer Abbas when they differ, and mention the difference if it matters for an exam.

## 2. Fact ledger (single source of truth)

Write your ledger rows to `work/ledger/M<n>.csv` (UTF-8, comma-separated, RFC-4180 quoting, header row exactly):

```
fact_id,module,fact,source,page,quote,volatile,verified_by
```

- `fact_id`: `M<n>-F001`, `M<n>-F002`, …
- `fact`: one fact, one sentence, STE style (see §3).
- `source`: `Abbas` | `Janeway` | `HAE-GL`
- `page`: the book page number (or `p.4` for HAE-GL). Use one page. If a fact needs two pages, write `65-66`.
- `quote`: a short verbatim snippet (max 25 words) from that page that supports the fact. This lets the reviewer check it fast.
- `volatile`: `Y` or `N`.
- `verified_by`: leave empty (the expert reviewer fills it).
- Aim for 40–90 facts per module. Every fact that appears in your HTML or in your MCQ explanations must be in the ledger.

## 3. Writing style (ASD-STE100, ~80% compliance)

Apply:
- Max 20 words per sentence for procedures/steps; max 25 words for descriptions.
- Active voice, present tense. One idea per sentence.
- Define each abbreviation at first use in the module (e.g., "pattern recognition receptor (PRR)"). Also list abbreviations in a `<dl class="abbr">` near the start.
- Write sequences as numbered steps (`<ol class="steps">`).
- Use the same term for the same thing everywhere. Fixed terms: "C3 convertase", "C5 convertase", "membrane attack complex (MAC)", "C1 inhibitor (C1-INH)", "pattern recognition receptor (PRR)", "pathogen-associated molecular pattern (PAMP)", "damage-associated molecular pattern (DAMP)", "Toll-like receptor (TLR)", "natural killer (NK) cell", "innate lymphoid cell (ILC)", "neutrophil extracellular trap (NET)", "chronic granulomatous disease (CGD)", "leukocyte adhesion deficiency (LAD)", "hereditary angioedema (HAE)".
Relax:
- Keep medical technical names and verbs (opsonize, phagocytose, extravasation).
- Analogies are allowed but must be inside `<div class="box analogy"><span class="label">Analogy</span>…</div>`.
- Passive voice is allowed when the agent is unknown.

## 4. Module HTML

File: `pack/modules/<file>.html`. Self-contained except for the shared stylesheet `../assets/style.css`. No external scripts, fonts or images. All diagrams are inline `<svg>`.

Module file names (use these exact names for links):
| Module | File |
|---|---|
| M1 Foundation | `M1-foundation.html` |
| M2 Cellular components | `M2-cells.html` |
| M3 PRRs & signalling | `M3-prrs.html` |
| M4 Phagocytosis & phagocyte defects | `M4-phagocytosis.html` |
| M5 Complement | `M5-complement.html` |
| M6 Complement deficiencies & HAE | `M6-complement-deficiencies.html` |
| M7 Summary & exam pearls | `M7-summary.html` |

Skeleton (copy it exactly, then fill in):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>M5 Complement — Innate Immunity</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<header class="topbar"><nav>
  <a href="../index.html">Home</a>
  <a href="M1-foundation.html">M1 Foundation</a>
  <a href="M2-cells.html">M2 Cells</a>
  <a href="M3-prrs.html">M3 PRRs</a>
  <a href="M4-phagocytosis.html">M4 Phagocytosis</a>
  <a href="M5-complement.html" class="current">M5 Complement</a>
  <a href="M6-complement-deficiencies.html">M6 Deficiencies &amp; HAE</a>
  <a href="M7-summary.html">M7 Summary</a>
  <a href="../quiz/quiz.html">Quiz</a>
</nav></header>
<main>
<h1>M5 · Complement made easy</h1>
<p class="subtitle">Innate immunity lecture pack · EAACI/UEMS Knowledge Exam preparation</p>
<section class="objectives"><h2>After this module you can</h2><ul>…</ul></section>
<dl class="abbr">…</dl>
… content sections (h2/h3), tables, boxes, figures …
<section class="keypoints"><h2>5 key points</h2><ol>…exactly 5…</ol></section>
<section class="traps"><h2>3 exam traps</h2><ol>…exactly 3…</ol></section>
<p class="related">Practice: <a href="../quiz/quiz.html#M5">M5 questions in the quiz</a> (IDs M5-A1 … M5-K2).</p>
<footer class="sources">Sources: … list the books/pages used … · Fact IDs refer to <code>ledger/facts.csv</code>.</footer>
</main>
</body>
</html>
```

Citations in the text: after each factual sentence (or small group of sentences from the same page) add
`<span class="src" title="M5-F012">Abbas p.312</span>`. The `title` holds the ledger fact ID(s), comma-separated.
For volatile facts use `class="src volatile"`.

Callout boxes: `box analogy`, `box clinical` (clinical correlation), `box pearl` (exam pearl), `box caution` (volatile / check guideline). Each starts with `<span class="label">…</span>`.

Length target: 2,000–3,500 words of body text per module (M7 shorter). Exam-focused: what a clinical allergist/immunologist needs for MCQs, not research detail.

## 5. Diagrams (inline SVG)

- Wrap each in `<figure class="diagram" id="D15"> <svg viewBox="0 0 800 H" role="img" aria-labelledby="D15t"> <title id="D15t">…</title> … </svg> <figcaption><b>D15.</b> caption …</figcaption></figure>`.
- Width always 800 user units; choose height H to fit (typically 300–600).
- Palette (use these hex values): ink #1d2433, muted #5b6475, line #d9dee7, panel #f5f7fa, innate green #2e7d5b, adaptive purple #6a4c93, danger red #b23a48, warn amber #c77d14, complement blue #1f6fb2, accent #1f5f8b. Light fills: green #e3f1ea, purple #ece5f5, red #f7e1e4, amber #fbecd3, blue #dfeaf6.
- Text classes available from the stylesheet: `t-title` (18px bold), `t-head` (15px bold), `t-body` (13px), `t-small` (11px muted), `t-white`. Never smaller than 11px.
- Text overflow check: at 13px, budget ≈ 7 px per character; at 15px bold ≈ 9 px per character. Make sure every label fits inside its box with ≥8px padding. Split long labels across `<tspan x=… dy="1.2em">` lines. Keep labels short (diagram labels may be telegraphic; STE limits apply to sentences, not labels).
- Arrows: define a marker once per SVG, e.g. `<defs><marker id="arr-D15" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d2433"/></marker></defs>`. Marker IDs must be unique across the page (suffix with the diagram ID).
- Rounded boxes `rx="8"`. Stroke width 1.5–2. Clean, flat, no gradients or shadows. Ample whitespace. No overlapping elements.
- Each fact shown in a diagram must be in the ledger. Cite the main source(s) in the figcaption with `<span class="src">`.

## 6. MCQs

Write `work/mcq/M<n>.json` — a JSON array. Counts per module are in the plan (§7). Schema:

```json
[
  {
    "id": "M5-A1",
    "module": "M5",
    "type": "A",
    "stem": "Clinical vignette … question?",
    "options": [
      {"key": "A", "text": "…", "correct": false, "explanation": "Why wrong, one or two sentences.", "source": "Abbas p.312"},
      {"key": "B", "text": "…", "correct": true,  "explanation": "Why right.", "source": "Abbas p.313"},
      … exactly 5 options A–E, exactly one correct …
    ],
    "fact_ids": ["M5-F010", "M5-F011"]
  },
  {
    "id": "M5-K1",
    "module": "M5",
    "type": "KPRIM",
    "stem": "Statement lead-in. Which of the following statements is/are correct?",
    "options": [ … exactly 4 options A–D, each with its own "correct": true/false, explanation, source … ],
    "fact_ids": ["…"]
  }
]
```

MCQ rules:
- Type A: clinical or lab vignette where possible (patient age, sex, history, key finding), like the EAACI sample questions (`work/sources_text/eaaci_sample_questions.txt`). 5 options, exactly one defensible best answer. Homogeneous, plausible distractors of similar length.
- KPrim: 4 independent true/false statements; any number 0–4 may be true. Avoid answer patterns that are all true or all false more than once per module.
- No "all of the above", "none of the above", no negative stems without CAPITAL "NOT"/"EXCEPT" (prefer to avoid them entirely).
- Each option explanation is cited to the ledger source/page. Do not test facts that are outside the ledger.
- Level: specialist exam (allergist/clinical immunologist), not first-year student. Test application and differential diagnosis, not trivia.
- Spread correct keys across A–E.

## 7. Report back

When done, reply with: files written, fact count, MCQ count, plan items NOT covered by the sources (gaps), and any source conflicts you found. Keep the report short.

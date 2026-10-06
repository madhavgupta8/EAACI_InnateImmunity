# Innate Immunity pack — EAACI/UEMS exam (19 Oct 2026)

Open **`pack/index.html`** in a browser. The pack works offline from the files on disk.

## What is where

| Item | Path |
|---|---|
| Lecture notes M1–M7 (HTML, 21 inline SVG diagrams) | `pack/modules/` |
| Printable PDFs of M1–M7 + fact ledger | `pack/pdf/` |
| Interactive quiz (35 Type A + 15 KPrim + 3 SCT) | `pack/quiz/quiz.html` |
| Answer key (PDF) | `pack/quiz/answer-key.pdf` |
| Exam pearls one-pager (1 × A4) | `pack/pearls.html`, `pack/pearls.pdf` |
| Fact ledger — 681 facts, source page + quote | `pack/ledger/facts.csv`, `pack/ledger/facts.html` |
| **Expert review list (gaps, conflicts)** | `work/REVIEW_NOTES.md` |
| Independent audit reports per module | `work/audit/M1.md` … `M6.md` |
| Page-tagged source text (Abbas, Janeway OCR, HAE GL) | `work/sources_text/` |
| Authoring / audit rules | `work/AUTHORING_SPEC.md`, `work/AUDIT_SPEC.md` |

## Edit and rebuild

- Edit module text in `pack/modules/*.html`, facts in `work/ledger/M*.csv`, questions in `work/mcq/*.json`.
- M7 and the pearls page are generated from templates. Edit `work/tmp_M7/` and run `python3 work/tmp_M7/gen.py`.
- Then run:

```bash
python3 work/build.py --all-pdf
```

The build merges the ledgers and questions, checks that every cited fact ID exists, and regenerates the quiz data and all PDFs. It must report `problems: 0`.

## Expert review (Dad)

1. Go through `work/REVIEW_NOTES.md` first. It lists the topics the sources do not cover and the points where Abbas and Janeway disagree.
2. Then use `pack/pdf/fact-ledger.pdf` (68 pages) or `pack/ledger/facts.html`. Tick the last column. Amber rows are volatile (drugs, guideline recommendations).
3. HAE treatment follows the **2017** WAO/EAACI guideline, the only revision provided. Check it against the 2021 revision.
4. The SCT credits are provisional. No expert panel has set them.

## Phase 2 — videos (not started)

Plan §6: 7 Manim videos (V5–V7 first). Needs: an ElevenLabs API key and voice, and Manim CE + manim-voiceover + ffmpeg on the render machine. The scripts will be written from the reviewed `facts.csv`.

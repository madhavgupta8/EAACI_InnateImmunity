# Independent audit spec

You are an independent reviewer. You did NOT write this module. Be skeptical. Your job is to find errors before a physician uses this pack for a specialist exam.

Read `work/AUTHORING_SPEC.md` first (rules the author had to follow).

Inputs for module M<n>:
- `pack/modules/<file>.html`
- `work/ledger/M<n>.csv`
- `work/mcq/M<n>.json`
- Sources: `work/sources_text/*.txt` (page-tagged; Janeway is OCR text)

## Checks

1. **Ledger vs source.** For EVERY ledger row: open the cited page in the source file and confirm the fact is a correct reading of the source (not just that the quote exists). Watch for: wrong page, over-generalisation, mixed-up names (e.g., CR1 vs CR3, C4b2a vs C3bBb, MyD88 vs TRIF), wrong numbers, facts from background knowledge with a weak quote.
2. **HTML vs ledger.** Each factual sentence in the HTML must match the ledger fact(s) in its `src` title. Find statements with no citation that are factual claims. Find claims that go beyond the sources.
3. **Diagrams.** Check each SVG for factual errors (arrows in the wrong direction, wrong labels). Render the page to PNG and look at it:
   `~/Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-arm64/chrome-headless-shell --headless --screenshot=<out.png> --window-size=1000,<height> file://<abs path to html>`
   Use a large height (e.g., 12000) or crop with Python (PIL may not be installed; `sips` is available on macOS) and Read the PNG. Do NOT use the shared Browser pane. Write PNGs to your own folder `work/audit/png_M<n>/`. Look for text overflow, overlaps and clipped labels.
4. **MCQs.** For each item: is the key the single best answer and defensible from the sources? Are the distractors clearly wrong per the sources (no second defensible answer)? Is every explanation and source page correct? Is the KPrim truth value of each statement unambiguous? Is the stem clear and exam-style?
5. **Style.** STE violations that hurt clarity (sentences > 25 words, undefined abbreviations at first use, inconsistent terms). Report only the significant ones and fix them.

## Output

- **Fix** clear errors directly in the module's three files (HTML, ledger CSV, MCQ JSON). Keep fact IDs stable; if you delete a fact, remove its citations too. Keep the CSV header and quoting. Validate the JSON after editing.
- Do not touch other modules' files.
- Write `work/audit/M<n>.md`: a table `# | Severity (critical/major/minor) | Location | Problem | Source evidence | Action (fixed / needs expert)`. End with a 3-line verdict.
- Afterwards run `python3 work/build.py` and make sure it reports 0 problems for your module.
- Reply with a short summary: counts by severity, what you fixed, what needs the expert.

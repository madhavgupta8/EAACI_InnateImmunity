# Video spec — Innate Immunity explainer videos (EAACI/UEMS exam, 19 Oct 2026)

Read this whole file, `../../innate-immunity-lecture-plan.md` §2–3 and §6, and `../AUTHORING_SPEC.md` §1 and §3 before you start.
Look at `chalk.py` (theme + helpers) and the pilot `scripts/V0.json` + `scenes/V0.py`.

## Videos

| ID | Title | slug | Target | Sources (ledger + module HTML) | Diagrams to animate |
|---|---|---|---|---|---|
| V1 | Innate immunity: the first 4 hours | `first-4-hours` | ~6 min | M1 | D1–D3 |
| V2 | The cells of innate immunity | `innate-cells` | ~7 min | M2 | D4–D6 |
| V3 | How cells sense danger: PRRs & signalling | `prrs-signalling` | ~8 min | M3 | D7–D10 |
| V4 | Phagocytosis & the respiratory burst | `phagocytosis` | ~7 min | M4 | D11–D14 |
| V5 | Complement made easy | `complement` | ~8 min | M5 | D15–D17 |
| V6 | Complement deficiencies & HAE | `complement-deficiencies-hae` | ~7 min | M6 | D18–D20 |
| V7 | 10-minute exam rapid review | `rapid-review` | ~10 min | M1–M6 ledger + `pack/modules/M7-summary.html` + `pack/pearls.html` | D21 |

Module HTML: `../../pack/modules/M<n>-*.html` (read it — its sections, key points, traps and SVG diagrams show what the student already studies; the video must match it). Ledger: `../ledger/M<n>.csv`.

## Source lock (non-negotiable)

- Every factual claim in the narration must come from the fact ledger (`work/ledger/M*.csv`). Cite the fact IDs per beat in `"facts"`.
- No facts from memory. No drug names, genes, numbers or organisms that are not in the ledger.
- Where the ledger/module flags a source conflict, either skip the detail or say both versions briefly ("Abbas says…, Janeway says…").
- Volatile facts (HAE drugs, licences) → say "per the 2017 guideline; check the current guideline".
- Beats with no facts (intro, transitions, recap of already-cited facts, analogies) need `"no_facts_reason"`.

## Script file `scripts/<ID>.json`

```json
{"id": "V5", "slug": "complement", "title": "Complement made easy",
 "beats": [
  {"id": "b01", "text": "Narration shown as subtitles.", "say": "Optional spoken variant for TTS.",
   "facts": ["M5-F001"], "visual": "One line: what the board shows."}
 ]}
```

- Beat ids `b01`, `b02`, … in order. One beat = one visual step, 1–4 sentences, typically 8–25 s of audio.
- The MiniMax voice reads ~110–120 words/min (≈100 on acronym-heavy text). Target word count = target min × 115.
- Style: ASD-STE100 relaxed — active voice, present tense, max ~20–25 words per sentence (checker flags >28), one idea per sentence, same term for the same thing. Warm, clear teacher voice. Analogies OK if flagged as such in speech ("Think of it like…").
- Structure: hook (why this matters for the exam) → core content in logical order → clinical correlation → recap "Five things to remember" → one exam trap. Close with "Next: …" except V7.
- `text` is the subtitle. Use `say` only when TTS needs help: spell Greek letters ("IL-1β" → "I L 1 beta"), "C5b-9" → "C 5 b to 9", "C1-INH" → "C 1 inhibitor", "NF-κB" → "N F kappa B", "IFN-β" → "interferon beta", "CD55" → "C D 55", "ROS" → "R O S" or "reactive oxygen species", "NETs" → "nets", "KIR" → "K I R". Prefer writing the spoken form directly in `text` where it reads fine.
- Run `../.menv/bin/python make.py <ID> --check` until it prints no `!` lines.

## Scene file `scenes/<ID>.py`

```python
from chalk import *

class V5(ChalkScene):
    VIDEO_ID = "V5"
    def construct(self):
        with self.beat("b01"):
            ...
```

- Use every beat exactly once, in order, with `with self.beat("bNN"):`. The context manager plays the audio and waits until it ends. Use `run_time=self.fit(x)` so animations do not overrun the narration; `self.remaining()` gives the time left in the beat.
- Animation should follow the narration: build diagrams step by step as each element is named (3Blue1Brown style — things appear, move, transform; not static slides). Use `Write`, `Create`, `GrowArrow`, `FadeIn(shift=…)`, `Transform`, `Indicate`, `Circumscribe`, `LaggedStart`, `.animate`. Split a beat's animations across its duration (e.g., several `self.play` with `self.fit(...)` and small `self.wait(...)`).
- Use only helpers from `chalk.py` for text (`T`, `Tm`, `bullet_list`, `label_box`, `chalk_arrow`, `cell`, `strike`, `self.header`, `self.title_card`, `self.source_tag`, `self.clear_board`). Font is Chalkboard SE. No LaTeX (`MathTex`/`Tex`) — use Unicode (β, κ, →, ⁻) in `T(...)`.
- Colour meaning (keep consistent): YELLOW key terms/headers, BLUE cells/receptors, PINK disease/defect/danger, GREEN normal/protective, ORANGE drugs, GREY citations.
- Layout: frame is 14.2 × 8 units. Keep everything inside x ∈ [-6.6, 6.6], y ∈ [-3.7, 3.7]. Min font size 24 (citations 20). Max ~7 bullet lines on screen. Clear the board between topics. Never overlap text.
- Show a `self.source_tag("Abbas p.307")` when a beat's key fact is on screen.
- Do not edit `chalk.py`, `make.py` or `frames.py`. If you need a helper, define it in your scene file. If you find a real bug in the shared files, say so in your report.

## Workflow

1. Read sources → write `scripts/<ID>.json` → `--check` clean.
2. `../.menv/bin/python make.py <ID> --tts` (MiniMax TTS, cached per beat; re-runs only synthesize changed beats — do not regenerate unchanged beats needlessly).
3. Write `scenes/<ID>.py` → `../.menv/bin/python make.py <ID> --draft` (480p) → `../.menv/bin/python frames.py <ID> --draft` → **look at the frames** with the Read tool. Fix overlaps, off-screen items, empty boards, clutter. Repeat until clean.
4. Final: `../.menv/bin/python make.py <ID>` (1080p, writes `pack/videos/<ID>-<slug>.mp4/.srt/.vtt`). Then `frames.py <ID>` and spot-check ~6 frames.
5. Report: final duration, word count, beats, any facts you wanted but could not use (not in ledger), any shared-file bugs.

Run all commands from `work/video/`. The Python env is `../.menv` (conda-forge, Manim 0.20.1). Do not install packages.

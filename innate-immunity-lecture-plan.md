# Plan: "Innate Immunity" Lecture Pack for EAACI/UEMS Knowledge Exam

## 0. Key constraints (from EAACI exam page)

| Item | Fact | Impact on plan |
|---|---|---|
| Exam date | **Mon 19 Oct 2026, online** | Only **15 days** left. Text + MCQs first, videos second. |
| Format | 120 MCQ, 3 h, English | ~1.5 min per question → train speed with vignettes. |
| Split | 70% allergology, 30% basic/clinical immunology | Innate immunity is one part of the 30%. Keep pack tight. |
| Scope note | **C1-INH deficiency** is named explicitly in exam scope | HAE gets extra depth in the complement-deficiency module. |
| Other | Minor part = Script Concordance Test (SCT) items | Add 3 optional SCT samples. |
| Official prep | EAACI literature list PDF + exam blueprint + IML Bern self-assessment | Use these as the source anchor. |

---

## 1. Deliverables

| # | Deliverable | Format | Priority |
|---|---|---|---|
| 1 | Lecture notes, 7 modules | HTML (single file per module, inline SVG diagrams, print-ready) | **P1** |
| 2 | 50 MCQs (≈35 Type A vignettes + 15 KPrim) + 3 SCT samples | Interactive HTML quiz + printable PDF answer key | **P1** |
| 3 | Exam pearls one-pager | HTML + PDF | **P1** |
| 4 | 7 explainer videos, 3b1b style on chalkboard theme | MP4 1080p + SRT subtitles | P2 |

KPrim scoring (IML standard): 4/4 correct = 1 pt, 3/4 = 0.5 pt, ≤2/4 = 0. The quiz uses the same rule.

---

## 2. Anti-hallucination controls

1. **Source lock.** Upload references to one Claude Project. Claude writes only from these. Each fact gets a tag: `[Abbas ch.4]`.
   - Abbas, *Cellular and Molecular Immunology* (latest ed.)
   - Janeway's *Immunobiology* (latest ed.)
   - EAACI exam literature list (PDF on exam page) + exam blueprint
   - IUIS Inborn Errors of Immunity classification (latest update) — for deficiencies
   - WAO/EAACI HAE guideline (2021 revision, check for newer)
2. **Fact ledger = single source of truth.** One table (`facts.csv`: fact, source, page, verified-by). HTML, MCQs and video scripts are generated from it. No fact outside the ledger.
3. **Independent review pass.** A separate Claude chat audits each module against sources. Output: list of errors + source lines.
4. **Expert sign-off.** Dad reviews the ledger (~1–2 h). Highest-value step; he is the domain expert.
5. **Volatile facts flagged.** Drug approvals, prevalence numbers → marked with date + source, or omitted.
6. **MCQ rules.** One defensible answer. Each option has a cited explanation. No "all/none of the above".

---

## 3. ASD-STE100 rules (≈80% compliance)

**Apply:**
- Max 20 words per sentence (procedures), 25 (descriptions).
- Active voice, present tense. One idea per sentence.
- Define each abbreviation at first use.
- Sequences as numbered steps.
- Same term for the same thing everywhere (e.g., always "C3 convertase").

**Relax (the 20%):**
- Keep medical technical names and verbs (opsonize, phagocytose) — STE permits technical names.
- Allow marked analogies (`Analogy:`) for easy explanation.
- Allow passive voice when the agent is unknown.

---

## 4. Module structure (HTML)

| Module | Content | Diagrams |
|---|---|---|
| M1 Foundation | Innate vs adaptive, barriers, time course, inflammation | D1, D2, D3 |
| M2 Cellular components | Neutrophil, monocyte/macrophage (M1/M2), DC, NK, mast cell, eosinophil, basophil, ILC1/2/3 | D4, D5, D6 |
| M3 PRRs & signalling | PAMP/DAMP, TLRs, NLRs/inflammasome, RLRs, cGAS-STING, CLRs, soluble PRRs, cytokine output | D7–D10 |
| M4 Phagocytosis | Extravasation, chemotaxis, opsonins, phagolysosome, respiratory burst, NETs; phagocyte defects (CGD, LAD I–III, CHS, MPO def.) | D11–D14 |
| M5 Complement (easy language) | 3 pathways, convertases, MAC, functions, regulators | D15–D17 |
| M6 Complement deficiencies & defects | Deficiency → phenotype, lab work-up, HAE/C1-INH, aHUS, PNH | D18–D20 |
| M7 Summary & exam pearls | Rapid review, high-yield tables, traps | D21 |

Each module ends with: 5 key points, 3 traps, links to related MCQs.

---

## 5. Diagram list (21 inline SVG, HTML)

| ID | Diagram | Type |
|---|---|---|
| D1 | Innate vs adaptive immunity — speed, specificity, memory, receptors | Comparison table-graphic |
| D2 | Barrier layers: physical, chemical (defensins, lysozyme), microbiota | Layered cross-section |
| D3 | Time course of infection response (0 h → 4 h → 96 h → adaptive) | Timeline |
| D4 | Haematopoiesis of innate cells (myeloid vs lymphoid origin) | Lineage tree |
| D5 | Innate cell "ID cards": markers, granules, main function, key disease | Card grid |
| D6 | NK cell "missing self": activating vs inhibitory receptors (KIR, MHC-I) | Balance diagram |
| D7 | PRR location map: cell surface, endosome, cytosol, soluble | Cell map |
| D8 | TLR4 signalling: MyD88 → NF-κB vs TRIF → IRF3 → IFN-β | Pathway flow |
| D9 | NLRP3 inflammasome: signal 1 + signal 2 → caspase-1 → IL-1β/IL-18, pyroptosis | Two-step flow |
| D10 | Cytosolic nucleic-acid sensing: RIG-I/MDA5 + cGAS-STING → type I IFN | Pathway flow |
| D11 | Leukocyte extravasation: rolling → activation → arrest → diapedesis | 4-step sequence |
| D12 | Phagocytosis steps + opsonin receptors (FcγR, CR1/CR3) | Step sequence |
| D13 | Respiratory burst: NADPH oxidase → O₂⁻ → H₂O₂ → MPO → HOCl | Reaction chain |
| D14 | Phagocyte defects map: defect → step blocked → clinical clue → test | Mapping table |
| D15 | Complement: classical, lectin, alternative → C3 convertase | Convergence diagram |
| D16 | C3/C5 convertases + MAC (C5b-9) assembly | Assembly sequence |
| D17 | Complement regulators: C1-INH, C4BP, factor H/I, CD46, CD55, CD59 — where each acts | Pathway overlay |
| D18 | Deficiency → disease map (early: SLE-like; C3: pyogenic; C5–C9/properdin: *Neisseria*; regulators: HAE, aHUS, PNH) | Pathway heat-map |
| D19 | Lab work-up decision tree: CH50 / AH50 / C3 / C4 / C1-INH level + function / C1q | Decision tree |
| D20 | HAE bradykinin cascade + drug targets (on-demand vs prophylaxis) | Pathway + target pins |
| D21 | One-page innate immunity master map | Summary map |

---

## 6. Video list (Manim, 3b1b style, chalkboard theme)

| ID | Title | Length | Visual core |
|---|---|---|---|
| V1 | Innate immunity: the first 4 hours | ~6 min | Barriers, time course, innate vs adaptive (D1–D3) |
| V2 | The cells of innate immunity | ~7 min | Lineage tree animates, NK balance (D4–D6) |
| V3 | How cells sense danger: PRRs & signalling | ~8 min | TLR4 two-branch animation, inflammasome (D7–D10) |
| V4 | Phagocytosis & the respiratory burst | ~7 min | Extravasation, engulfment, ROS chain, CGD (D11–D14) |
| V5 | Complement made easy | ~8 min | 3 pathways merge, amplification loop, MAC builds (D15–D17) |
| V6 | Complement deficiencies & HAE | ~7 min | Knock-out a component → see disease (D18–D20) |
| V7 | 10-minute exam rapid review | ~10 min | Pearls + traps (D21) |

Total ≈ 53 min of video.

**Video pipeline (Claude Code):**
1. Script per video (STE, from fact ledger, ~140 words/min).
2. Split into beats; ElevenLabs TTS per beat → audio + duration.
3. Manim CE + `manim-voiceover` syncs animation to audio.
4. Theme: dark-green board, chalk-white/yellow/pink strokes, handwriting font.
5. Render 1080p → ffmpeg concat → SRT subtitles from script.

ElevenLabs budget: ~53 min ≈ 45–50k characters. Check plan quota before start.

---

## 7. MCQ bank (50 + 3)

| Module | Type A (vignette) | KPrim |
|---|---|---|
| M1 Foundation | 3 | 2 |
| M2 Cells | 6 | 2 |
| M3 PRRs & signalling | 6 | 3 |
| M4 Phagocytosis & defects | 7 | 3 |
| M5 Complement | 5 | 2 |
| M6 Deficiencies & HAE | 8 | 3 |
| **Total** | **35** | **15** |

- Plus 3 optional SCT samples (exam uses a minor SCT part).
- Quiz HTML: timer (90 s/item), KPrim scoring rule, explanation + source per option, score by module.

---

## 8. Timeline (today: Sun 4 Oct → exam Mon 19 Oct)

| Dates | Work | Owner |
|---|---|---|
| 4–5 Oct | Collect sources, build Claude Project, draft fact ledger | Madhav + Claude |
| 6 Oct | Dad reviews fact ledger | Dad |
| 6–9 Oct | M1–M7 HTML + diagrams; review pass | Claude → Dad |
| 8–10 Oct | 50 MCQs + quiz HTML; answer-key audit | Claude → Dad |
| **10 Oct** | **P1 complete (notes + MCQs + pearls)** | — |
| 9–14 Oct | Videos V5, V6, V7 first (highest yield), then V1–V4 | Claude Code |
| 15–18 Oct | Revision only. No new material. | Dad |

If time is short: drop V1–V4. Keep V5–V7.

---

## 9. Tool map

| Task | Tool |
|---|---|
| Source-grounded writing | Claude Project (claude.ai) with uploaded PDFs |
| Independent fact audit | Separate Claude chat, sources attached |
| HTML / SVG / quiz build | Claude (artifacts) or Claude Code |
| Manim + TTS pipeline | Claude Code |
| Narration | ElevenLabs API |
| Render / merge | Manim CE, manim-voiceover, ffmpeg |

---

## 10. Inputs needed from you

- [ ] Reference PDFs (textbook chapters, EAACI literature list items)
- [ ] Dad's 1–2 h for fact-ledger review on 6 Oct
- [ ] ElevenLabs API key + chosen voice
- [ ] Machine for Manim render (local or your VPS)

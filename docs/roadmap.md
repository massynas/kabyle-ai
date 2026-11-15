# Roadmap

## Phase 0 — Foundation
- [x] Define scope and repository structure.
- [x] Add CI and automated checks.

## Phase 1 — Baseline
- [ ] Create 100–300 native-speaker prompts.
- [ ] Cover conversation, comprehension, idioms and translation in both directions.
- [ ] Freeze a held-out test set and scoring rubric.
- [ ] Evaluate candidate models and tokenizer handling.

## Phase 2 — Legal corpus
- [ ] Inventory dictionaries, learning resources and parallel texts.
- [ ] Verify license or permission for every source, including row-level audio/transcript rights.
- [ ] Audit TutlaytAI Kabyle audio/transcript datasets; quarantine sources with missing license evidence.
- [ ] Record dialect, register, orthography, provenance and review status.
- [ ] Build a high-quality seed dataset.

## Phase 3 — Adaptation
- [ ] Select a base model using benchmark evidence.
- [ ] Run a small LoRA/QLoRA SFT experiment.
- [ ] Compare base and adapted checkpoints; publish error analysis.

## Phase 4 — Evidence-led improvement
- [ ] Expand native-reviewed data.
- [ ] Consider continued pretraining only if data and diagnostics justify it.
- [ ] Add retrieval only for demonstrated terminology gaps.

## Phase 5 — Later deployment and speech
- [ ] Estimate hosting costs and consider a private text endpoint.
- [ ] Evaluate speech recognition and synthesis separately.
- [ ] Preserve aligned audio/transcript/translation metadata; never mix audio bytes into text-only SFT exports.

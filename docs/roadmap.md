# Roadmap

## Phase 0 — Foundation
- [x] Define scope and repository structure.
- [x] Add CI and automated checks.

## Phase 1 — Baseline
- [x] Add native benchmark JSONL validation, unique-ID checks and a reviewed-only freeze gate.
- [x] Define the native-speaker scoring rubric, register labels and evaluation leakage rules.
- [x] Add a tokenizer-only Unicode probe for Qwen3-1.7B and Qwen2.5-1.5B-Instruct.
- [ ] Create 100–300 native-speaker prompts and reference answers.
- [ ] Cover conversation, comprehension, idioms and translation in both directions.
- [ ] Freeze a held-out test set and scoring rubric after native review.
- [ ] Run tokenizer probes and compare candidate models on the frozen benchmark.

## Phase 2 — Legal corpus
- [ ] Inventory dictionaries, learning resources and parallel texts.
- [ ] Verify license or permission for every source, including row-level audio/transcript rights.
- [ ] Audit ParaKab Kabyle–Arabic rows and source-level rights before any training import.
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

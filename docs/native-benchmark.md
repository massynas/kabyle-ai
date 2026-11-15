# Native-speaker benchmark

## Purpose

The first model decision must be evidence-led. This benchmark measures whether a
candidate can understand and produce natural Kabyle, preserve meaning in
Kabyle/French translation, handle orthographic variation, and respond across
everyday and literary registers. Literary Kabyle is a valid register of the
language; it must not be treated as noise or automatically excluded.

The benchmark is authored and reviewed by native speakers. Machine-generated
prompts or answers may be used only as drafts and must never be marked reviewed
without human validation.

## Coverage

Build an initial 100–300 items across these areas:

- Conversation: greetings, requests, explanations, follow-up turns and natural
  short answers.
- Comprehension: infer meaning from a short passage and answer precisely.
- Idioms: understand and use expressions in context; record regional variants.
- Kabyle-to-French and French-to-Kabyle translation.
- Orthography: Latin-script diacritics, apostrophes, spacing and common variants.
- Literary register: understand and generate literary Kabyle without confusing
  it with everyday conversational style.

For each item, record the register (everyday, literary, mixed, unspecified),
category, expected answer, and review status. Preserve original wording exactly.
Do not silently normalize ɣ ɛ č ḍ ṛ ṣ ṭ or Tifinagh.

## Splits and leakage prevention

- Use only dev and test in the evaluation benchmark.
- Keep test items private and access-controlled until final evaluation.
- Never put benchmark prompts or reference answers in SFT/training exports,
  retrieval indexes, or synthetic-data generation prompts.
- Assign stable unique IDs. Do not duplicate paraphrases across splits.
- Mark an item reviewed only after a native speaker has checked naturalness,
  meaning, register, orthography and reference answer.
- Record provenance and permissions for any sourced example. Prefer original
  examples authored for this benchmark.

## JSONL format

One UTF-8 JSON object per line. Example:

    {"id":"kab-dev-0001","split":"dev","category":"conversation","register":"everyday","prompt":"...","reference_answer":"...","review_status":"draft"}

Allowed categories: conversation, comprehension, idiom, translation_kab_fr,
translation_fr_kab, translation_kab_ar, translation_ar_kab, orthography,
literary_register.

Do not commit the real held-out test set to a public repository. During private
development it may be stored in an access-controlled private location. The
repository may contain schemas, tooling and empty templates only.

## Validation

Install development dependencies and validate a file:

    python -m pip install -e ".[dev]"
    python scripts/validate_benchmark.py path/to/benchmark.jsonl
    python scripts/validate_benchmark.py path/to/benchmark.jsonl --require-reviewed

The strict flag is required before freezing a benchmark for model comparison.
The validator checks JSONL syntax, required fields, IDs, categories, registers,
evaluation-only splits and human-review status. It does not judge linguistic
quality; that remains the responsibility of native speakers.

## Scoring rubric

Score each generated answer independently on a 0–4 scale:

| Dimension | What to assess |
|---|---|
| Meaning | Does it answer the question and preserve the intended meaning? |
| Naturalness | Would a native speaker plausibly say/write it in this context? |
| Grammar | Morphology, agreement, syntax and particles |
| Orthography | Consistent and readable spelling without damaging meaning |
| Register | Appropriate everyday/literary style for the prompt |

A translation item also receives a meaning-preservation score. Do not reward
verbosity when a short answer is more natural. Report per-category and
per-register results, not only one aggregate score. Keep evaluator notes and
disagreements; resolve them through a second native-speaker review.

## Model comparison protocol

1. Freeze the reviewed benchmark version and its checksum.
2. Run every candidate with the same prompt template and decoding settings.
3. Store model ID/revision, tokenizer revision, parameters, outputs and run date.
4. Blind model identities during human scoring where practical.
5. Report per-category and per-register results, failure examples and
   confidence intervals where sample size permits.
6. Select a base model only after native-speaker results and tokenizer tests.

## Reproducible local model run

After a benchmark file has been reviewed and frozen, run one model at a time:

    python -m pip install -e ".[train,dev]"
    python scripts/run_benchmark.py --input private/benchmark.jsonl --output private/predictions-qwen3.jsonl --model Qwen/Qwen3-1.7B --split dev

Pin the model with --revision and record that SHA in experiment notes. The
runner validates that every benchmark record is marked reviewed, selects only
the requested dev or test split, uses deterministic greedy decoding, and saves
predictions with model and generation metadata. It loads the model locally via
Transformers and may use a GPU when available; no hosted compute is started.

Keep the held-out test file and prediction outputs private. Do not commit
benchmark data or predictions to Git. Run the same protocol and decoding
settings for every candidate. The runner does not calculate an automatic
linguistic score: native-speaker human scoring remains authoritative.

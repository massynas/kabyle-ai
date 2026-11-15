# Rights-gated LoRA training

This repository includes a minimal supervised fine-tuning runner, but it is
deliberately impossible to start training from unapproved or evaluation data.

## Record format

Each JSONL row must contain:

- a stable unique ID and split set to train;
- a messages array containing user and assistant turns;
- training_approved set to true;
- a rights_review object with status approved, model_training_allowed true,
  explicit true/false values for commercial_use_allowed and
  weights_distribution_allowed, an evidence reference and ISO review date;
- source metadata: dataset ID, immutable source revision, row ID, exact license,
  source URL and attribution.

A general dataset-card license is not sufficient when row-level rights differ.
Do not mark a row approved until the source and any upstream works have been
reviewed. A permission to train does not necessarily permit publication of the
dataset or distribution of derived weights; those decisions must be recorded
separately before an open-source release.

## Validate without downloading weights

    python -m pip install -e ".[dev]"
    python scripts/train_lora.py --input private/train-approved.jsonl --model Qwen/Qwen3-1.7B --revision IMMUTABLE_40_CHAR_SHA --output-dir outputs/qwen3-kabyle-lora

Without --confirm-training the command validates the file and prints a summary
only. It does not download model weights, create an output directory or start
training.

## Start an explicitly approved run

    python -m pip install -e ".[train,dev]"
    python scripts/train_lora.py --input private/train-approved.jsonl --model Qwen/Qwen3-1.7B --revision IMMUTABLE_40_CHAR_SHA --output-dir outputs/qwen3-kabyle-lora --confirm-training

The runner trains a LoRA adapter using the chat template and deterministic
supervised fine-tuning settings. It uses CUDA when available and falls back to
CPU (which may be very slow). No hosted GPU is started. Review VRAM, runtime
and disk needs before running a real experiment.

The first implementation applies causal-language-model loss to the rendered
conversation sequence, including user and assistant turns. It is a baseline
pipeline, not a claim of optimal assistant-only loss. The resulting adapter is
not automatically approved for redistribution.

## Non-negotiable separation

- Never include dev/test or native benchmark records in the training file.
- Never train on KabBench or other held-out evaluation sets.
- Keep original source text, row IDs, exact licenses and attribution in the
  private curation record.
- Do not include data whose rights status is unknown, non-commercial where
  commercial use is intended, or otherwise incompatible with the intended use.
- Keep private source corpora, training JSONL and model outputs out of Git.
- Compare the adapter against the untouched base model on the frozen native
  benchmark before deciding whether it improves Kabyle.

The run manifest records whether every training row also permits commercial use
and distribution of model weights. A private training run can be allowed while
open-source weight release remains blocked; do not publish an adapter unless the
rights review explicitly clears that separate use.

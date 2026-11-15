# Kabyle AI

An open-source research project for a small language model focused on everyday Kabyle (Taqbaylit), with French and Arabic support.

Status: repository foundation only. No model has been trained or evaluated yet.

## Initial goals
- Understand and generate natural everyday Kabyle.
- Support practical Kabyle/French/Arabic translation.
- Preserve regional, lexical and orthographic variation.
- Build reproducible datasets and native-speaker evaluation.
- Adapt an existing multilingual model; do not train from scratch.

## Milestones
1. Build a 100–300 example native-speaker benchmark.
2. Inventory legally usable Kabyle resources.
3. Curate and validate a seed dataset.
4. Evaluate candidate models and tokenizer handling.
5. Run LoRA/QLoRA supervised fine-tuning and compare with the base model.

Qwen2.5-1.5B-Instruct is a candidate only. License, tokenizer behaviour on Kabyle characters, language coverage and benchmark performance must be checked before selection.

Speech and a full application are postponed. Retrieval may support terminology but cannot replace language adaptation. Public accessibility does not imply permission to train on books, articles or translations; see docs/data-policy.md.

## Resource inventory
The first-pass catalog of existing Kabyle datasets, corpora and their license/quality caveats is in [docs/resource-inventory.md](docs/resource-inventory.md). No external corpus is copied into this repository at this stage.


## Corpus collection

See [docs/corpus-staging-policy.md](docs/corpus-staging-policy.md) for the private staging workflow. The downloader pins Hugging Face revisions and stores datasets outside Git; downloading does not mark a source as approved for training.

# Kabyle AI

An open-source research project for a small language model focused on everyday Kabyle (Taqbaylit), with French and Arabic support.

Status: project foundation and corpus-ingestion tooling are under review. No model has been trained or evaluated yet, and no external corpus data is committed to this repository.

## Initial goals
- Understand and generate natural everyday Kabyle.
- Support practical Kabyle/French/Arabic translation.
- Preserve regional, lexical and orthographic variation.
- Build reproducible datasets and native-speaker evaluation.
- Adapt an existing multilingual model; do not train from scratch.

## Milestones
1. Build a 100–300 example native-speaker benchmark.
2. Inventory and stage candidate Kabyle resources with provenance.
3. Resolve source rights and curate a high-quality seed dataset.
4. Evaluate candidate models and tokenizer handling.
5. Run LoRA/QLoRA supervised fine-tuning and compare with the base model.

The initial base-model review currently favours probing [Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B), with [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) retained as a control. This is not a final selection: Kabyle tokenizer behaviour and native-speaker benchmark results must decide.

Speech and a full application are postponed. Retrieval may support terminology but cannot replace language adaptation. Public accessibility does not imply permission to train on books, articles or translations; see [docs/data-policy.md](docs/data-policy.md).

## Resource inventory and corpus audit
- [docs/resource-inventory.md](docs/resource-inventory.md): source catalogue and initial rights assessment.
- [docs/corpus-staging-policy.md](docs/corpus-staging-policy.md): private staging and provenance rules.
- [docs/corpus-preview-audit.md](docs/corpus-preview-audit.md): first Hugging Face schema/sample inspection and data-quality flags.
- [docs/model-candidate-review.md](docs/model-candidate-review.md): initial compact multilingual model comparison.
- [docs/audio-corpus-plan.md](docs/audio-corpus-plan.md): audio/text source handling.
- [docs/training-pipeline.md](docs/training-pipeline.md): rights-gated LoRA SFT and explicit training confirmation.
- [docs/open-source-release-checklist.md](docs/open-source-release-checklist.md): legal, evaluation and packaging gates before publication.

The downloader pins immutable Hugging Face revisions and stores datasets outside Git. Downloading does not approve a source for training or redistribution. Never commit raw corpora, audio, private credentials or unreviewed examples.

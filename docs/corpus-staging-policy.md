# Private corpus staging policy

The project owner has asked to collect and inspect the identified Kabyle resources during development and to contact publishers/rightsholders before any public release. The collection step is therefore separated from training approval and redistribution.

## Operating rules

- Stage each source in its own local directory, pinned to an immutable Hugging Face commit SHA.
- Keep staged corpora outside Git. The downloader writes to `staging/huggingface/`, which is ignored.
- Generate a manifest with source ID, revision, retrieval timestamp, split counts, features, intended role and rights status.
- Preserve all original text, row IDs, source IDs, per-row license fields and split names.
- Do not merge sources into one training file during collection.
- Mark every newly staged source `training_approved: false`. The flag is not automatically changed by downloading.
- Keep `agbalu/KabBench` evaluation-only. Do not train on it or index it for retrieval.
- Keep mixed-license `TutlaytAI/kabyle_asr` rows separable by the exact `Licence` value.
- Keep TutlaytAI translated audio corpora and Tatoeba-derived Sifal data in a rights-review lane until provenance and license questions are answered.
- Preserve CC-BY-SA source/work attribution and share-alike metadata for KabLiterary.
- Before publication, distribution, commercial use or release of model weights, complete the rights register and obtain any necessary permissions.

## Sources included in the staging downloader

- `TutlaytAI/Kabyle_ASR-Fr_Translation`
- `TutlaytAI/Kabyle_ASR-En_Translation`
- `TutlaytAI/kabyle_asr`
- `agbalu/KabLex`
- `agbalu/KabStandard`
- `agbalu/KabLiterary`
- `agbalu/KabBench` (evaluation only)
- `Sifal/Kabyle-French`

The downloader stages the full available splits by default. Use `--max-samples` only for a smoke test. It resolves and records an immutable revision before loading. Audio bytes remain in local staging, never in Git.

## Run

Install the data dependencies:

```bash
python -m pip install -e ".[data]"
```

Stage all listed sources:

```bash
python scripts/stage_hf_corpora.py
```

Stage a single source:

```bash
python scripts/stage_hf_corpora.py --dataset agbalu/KabLiterary
```

Small smoke test:

```bash
python scripts/stage_hf_corpora.py --dataset TutlaytAI/Kabyle_ASR-Fr_Translation --max-samples 20
```

This script downloads and stores the datasets locally. It does not train the model, create a merged corpus, or grant rights beyond the terms applicable to each source.

# Candidate tokenizer probe

The tokenizer is tested before selecting a base model. A multilingual model card
does not prove that Kabyle characters are represented efficiently or decoded
without loss.

The probe downloads tokenizer files only. It does not download model weights,
run inference, or require a GPU.

## Run

Install the training extras (which include Transformers):

    python -m pip install -e ".[train]"
    python scripts/probe_tokenizer.py --output artifacts/tokenizer-probe.json

To pin a model revision:

    python scripts/probe_tokenizer.py --model Qwen/Qwen3-1.7B --revision REVISION_SHA

The default comparison includes Qwen3-1.7B and Qwen2.5-1.5B-Instruct.

## What is measured

- Token count for each fixed Unicode sample.
- Token IDs and token strings for manual inspection.
- Unknown-token count where the tokenizer defines an unknown token.
- Exact encode/decode round-trip fidelity.
- Tokenizer class, vocabulary size and resolved repository revision.

Samples cover lowercase and uppercase Kabyle Latin characters (ɣ ɛ č ḍ ṛ ṣ ṭ),
a short Kabyle phrase, Tifinagh, French accents, Arabic script and mixed scripts.
The fixed strings are diagnostic probes, not a linguistic quality benchmark.

## Interpretation

Prefer exact round-trip preservation. Compare token counts across candidates,
but do not select a model from token efficiency alone: a tokenizer can preserve
characters while the model still produces poor Kabyle. Final selection requires
the native-speaker benchmark and the same evaluation settings for every model.

## Run from GitHub Actions

After this workflow is merged into the default branch, it can also be launched
from the repository Actions tab by selecting the tokenizer-probe workflow and
choosing Run workflow. The revision input is optional; provide an immutable
commit SHA to pin both candidates. The workflow uploads a private JSON artifact
with a seven-day retention period. It uses CPU only and does not download model
weights.

"""Probe candidate tokenizers without downloading model weights."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_MODELS = (
    "Qwen/Qwen3-1.7B",
    "Qwen/Qwen2.5-1.5B-Instruct",
)
DEFAULT_SAMPLES = (
    "ɣ ɛ č ḍ ṛ ṣ ṭ",
    "Ɣ Ɛ Č Ḍ Ṛ Ṣ Ṭ",
    "Azul fell-awen. Amek tellam?",
    "Tifinagh: ⴰⵣⵓⵍ",
    "Bonjour, comment allez-vous ?",
    "مرحبا، كيف حالك؟",
    "Azul — bonjour — مرحبا",
)


def summarize_text(tokenizer: Any, text: str) -> dict[str, Any]:
    """Return tokenization diagnostics and an exact decode round-trip check."""
    token_ids = tokenizer.encode(text, add_special_tokens=False)
    decoded = tokenizer.decode(token_ids, skip_special_tokens=False)
    unknown_id = tokenizer.unk_token_id
    return {
        "text": text,
        "token_count": len(token_ids),
        "token_ids": token_ids,
        "tokens": tokenizer.convert_ids_to_tokens(token_ids),
        "unknown_token_count": (
            sum(token_id == unknown_id for token_id in token_ids)
            if unknown_id is not None else 0
        ),
        "round_trip_exact": decoded == text,
        "decoded": decoded,
    }


def probe_model(model_id: str, revision: str | None) -> dict[str, Any]:
    """Load tokenizer assets only; no model weights are requested."""
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        revision=revision,
        use_fast=True,
        trust_remote_code=False,
    )
    return {
        "model_id": model_id,
        "requested_revision": revision or "default",
        "resolved_revision": tokenizer.init_kwargs.get("_commit_hash"),
        "tokenizer_class": tokenizer.__class__.__name__,
        "vocab_size": len(tokenizer),
        "unk_token": tokenizer.unk_token,
        "samples": [summarize_text(tokenizer, sample) for sample in DEFAULT_SAMPLES],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model", action="append", dest="models",
        help="Model ID to probe; repeat to compare. Defaults to the two reviewed candidates.",
    )
    parser.add_argument("--revision", help="Optional immutable tokenizer revision SHA.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    args = parser.parse_args()

    results = []
    for model_id in args.models or DEFAULT_MODELS:
        results.append(probe_model(model_id, args.revision))
    rendered = json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

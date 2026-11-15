"""Run a reviewed native-speaker benchmark against a local Transformers model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from kabyle_ai.benchmark import load_jsonl, validate_records

SYSTEM_PROMPT = (
    "You are a careful multilingual assistant. Follow the language and register "
    "requested by the user. Preserve meaning and orthography. Answer directly "
    "and do not add explanations unless requested."
)


def build_messages(record: dict[str, Any]) -> list[dict[str, str]]:
    """Build a stable chat prompt; task language is specified by the benchmark item."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": record["prompt"]},
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Reviewed benchmark JSONL")
    parser.add_argument("--output", type=Path, required=True, help="Output predictions JSONL")
    parser.add_argument("--model", required=True, help="Hugging Face model ID")
    parser.add_argument("--revision", help="Optional immutable model revision SHA")
    parser.add_argument("--split", choices=("dev", "test"), default="dev")
    parser.add_argument("--max-new-tokens", type=int, default=256)
    args = parser.parse_args()
    if args.max_new_tokens < 1:
        parser.error("--max-new-tokens must be positive")

    records = load_jsonl(args.input)
    errors = validate_records(records, require_reviewed=True)
    if errors:
        parser.error("Invalid benchmark: " + "; ".join(errors))
    selected = [row for row in records if row["split"] == args.split]
    if not selected:
        parser.error(f"No reviewed records found for split {args.split!r}")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        args.model, revision=args.revision, use_fast=True, trust_remote_code=False
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        revision=args.revision,
        torch_dtype="auto",
        device_map="auto",
        trust_remote_code=False,
    )
    model.eval()
    resolved_revision = (
        getattr(model.config, "_commit_hash", None)
        or tokenizer.init_kwargs.get("_commit_hash")
        or args.revision
        or "unresolved"
    )
    pad_token_id = tokenizer.pad_token_id
    if pad_token_id is None:
        pad_token_id = tokenizer.eos_token_id
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", encoding="utf-8") as output:
        for record in selected:
            encoded = tokenizer.apply_chat_template(
                build_messages(record),
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt",
                return_dict=True,
            )
            encoded = encoded.to(model.device)
            input_length = encoded["input_ids"].shape[-1]
            with torch.inference_mode():
                generated = model.generate(
                    **encoded,
                    max_new_tokens=args.max_new_tokens,
                    do_sample=False,
                    num_beams=1,
                    pad_token_id=pad_token_id,
                )
            answer = tokenizer.decode(
                generated[0][input_length:], skip_special_tokens=True
            ).strip()
            result = {
                "id": record["id"],
                "split": record["split"],
                "category": record["category"],
                "register": record["register"],
                "prompt": record["prompt"],
                "generated_answer": answer,
                "model_id": args.model,
                "requested_revision": args.revision or "default",
                "resolved_model_path": resolved_revision,
                "generation": {
                    "max_new_tokens": args.max_new_tokens,
                    "do_sample": False,
                    "num_beams": 1,
                },
            }
            output.write(json.dumps(result, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

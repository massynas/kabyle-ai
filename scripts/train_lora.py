"""Run a small LoRA SFT job only on explicitly rights-approved training records."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from kabyle_ai.training_data import validate_training_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Rights-approved training JSONL")
    parser.add_argument("--model", required=True, help="Base model ID")
    parser.add_argument("--revision", required=True, help="Immutable 40-character model commit SHA")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--epochs", type=float, default=2.0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--max-length", type=int, default=1024)
    parser.add_argument(
        "--confirm-training",
        action="store_true",
        help="required to download model weights and start training; without it only validate",
    )
    args = parser.parse_args()

    if not re.fullmatch(r"[0-9a-fA-F]{40}", args.revision):
        parser.error("--revision must be an immutable 40-character commit SHA")
    if args.epochs <= 0 or args.batch_size < 1 or args.gradient_accumulation_steps < 1:
        parser.error("epochs, batch size and gradient accumulation must be positive")
    if args.learning_rate <= 0 or args.max_length < 32:
        parser.error("learning rate must be positive and max length at least 32")

    records, errors = validate_training_file(args.input)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    sources = sorted({
        (row["source"]["dataset_id"], row["source"]["revision"], row["source"]["license"])
        for row in records
    })
    print(f"Validated {len(records)} training records from {len(sources)} source/license lanes.")
    print("Every record has explicit training approval and an auditable rights-review reference.")
    if not args.confirm_training:
        print("Dry validation only. Add --confirm-training to download weights and start LoRA training.")
        return 0

    import torch
    from datasets import Dataset
    from peft import LoraConfig, get_peft_model
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        DataCollatorForLanguageModeling,
        Trainer,
        TrainingArguments,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        args.model, revision=args.revision, use_fast=True, trust_remote_code=False
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        revision=args.revision,
        torch_dtype="auto",
        trust_remote_code=False,
    )
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
    )
    model.config.use_cache = False
    model = get_peft_model(model, lora_config)
    if hasattr(model, "enable_input_require_grads"):
        model.enable_input_require_grads()
    model.print_trainable_parameters()

    dataset = Dataset.from_list(records)

    def tokenize_batch(batch):
        rendered = [
            tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=False
            )
            for messages in batch["messages"]
        ]
        return tokenizer(
            rendered,
            truncation=True,
            max_length=args.max_length,
        )

    tokenized = dataset.map(
        tokenize_batch,
        batched=True,
        remove_columns=dataset.column_names,
        desc="Tokenizing approved Kabyle conversations",
    )
    use_cuda = torch.cuda.is_available()
    use_bf16 = use_cuda and torch.cuda.is_bf16_supported()
    training_args = TrainingArguments(
        output_dir=str(args.output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        report_to="none",
        fp16=use_cuda and not use_bf16,
        bf16=use_bf16,
        gradient_checkpointing=True,
        optim="adamw_torch",
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
        tokenizer=tokenizer,
    )
    trainer.train()
    trainer.save_model(str(args.output_dir))
    tokenizer.save_pretrained(str(args.output_dir))

    manifest = {
        "model_id": args.model,
        "model_revision": args.revision,
        "training_rows": len(records),
        "sources": [
            {"dataset_id": dataset_id, "revision": revision, "license": license_id}
            for dataset_id, revision, license_id in sources
        ],
        "rights_reviewed": True,
        "rights_evidence_refs": sorted({
            row["rights_review"]["evidence_ref"] for row in records
        }),
        "commercial_use_allowed_for_all_rows": all(
            row["rights_review"]["commercial_use_allowed"] for row in records
        ),
        "weights_distribution_allowed_for_all_rows": all(
            row["rights_review"]["weights_distribution_allowed"] for row in records
        ),
        "output_is_adapter": True,
        "hyperparameters": {
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "gradient_accumulation_steps": args.gradient_accumulation_steps,
            "learning_rate": args.learning_rate,
            "max_length": args.max_length,
            "lora_r": 16,
            "lora_alpha": 32,
        },
    }
    (args.output_dir / "training-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

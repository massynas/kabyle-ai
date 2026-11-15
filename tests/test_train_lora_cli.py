import json
import sys

from scripts.train_lora import main


def approved_record():
    return {
        "id": "train-0001",
        "split": "train",
        "messages": [
            {"role": "user", "content": "Question"},
            {"role": "assistant", "content": "Answer"},
        ],
        "training_approved": True,
        "rights_review": {
            "status": "approved",
            "model_training_allowed": True,
            "commercial_use_allowed": False,
            "weights_distribution_allowed": False,
            "evidence_ref": "private/rights/approval.pdf",
            "reviewed_at": "2026-11-15",
        },
        "source": {
            "dataset_id": "owner/dataset",
            "revision": "a" * 40,
            "row_id": "row-1",
            "license": "CC BY 4.0",
            "source_url": "https://example.org/source",
            "attribution": "Attribution",
        },
    }


def test_cli_dry_run_validates_without_creating_output(tmp_path, monkeypatch):
    source = tmp_path / "train.jsonl"
    source.write_text(json.dumps(approved_record()) + "\n", encoding="utf-8")
    output = tmp_path / "adapter"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "train_lora.py",
            "--input", str(source),
            "--model", "Qwen/Qwen3-1.7B",
            "--revision", "a" * 40,
            "--output-dir", str(output),
        ],
    )
    assert main() == 0
    assert not output.exists()


def test_cli_refuses_unapproved_training_data(tmp_path, monkeypatch):
    record = approved_record()
    record["training_approved"] = False
    source = tmp_path / "train.jsonl"
    source.write_text(json.dumps(record) + "\n", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "train_lora.py",
            "--input", str(source),
            "--model", "Qwen/Qwen3-1.7B",
            "--revision", "a" * 40,
            "--output-dir", str(tmp_path / "adapter"),
        ],
    )
    assert main() == 1

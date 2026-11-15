"""Rights-gated validation for Kabyle supervised fine-tuning records."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any


class TrainingDataError(ValueError):
    """Raised when a training JSONL file cannot be parsed."""


def validate_training_records(records: list[dict[str, Any]]) -> list[str]:
    """Reject records without explicit, auditable model-training permission."""
    errors: list[str] = []
    seen_ids: set[str] = set()
    if not records:
        return ["training file contains no records"]
    for index, record in enumerate(records, start=1):
        prefix = f"record {index}"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: expected a JSON object")
            continue

        required = ("id", "split", "messages", "training_approved", "rights_review", "source")
        missing = [field for field in required if field not in record]
        if missing:
            errors.append(f"{prefix}: missing fields: {', '.join(missing)}")
            continue

        record_id = record["id"]
        if not isinstance(record_id, str) or not record_id.strip():
            errors.append(f"{prefix}: id must be a non-empty string")
        elif record_id in seen_ids:
            errors.append(f"{prefix}: duplicate id {record_id!r}")
        else:
            seen_ids.add(record_id)

        if record["split"] != "train":
            errors.append(f"{prefix}: only split='train' is accepted")
        if record["training_approved"] is not True:
            errors.append(f"{prefix}: training_approved must be true")

        review = record["rights_review"]
        if not isinstance(review, dict):
            errors.append(f"{prefix}: rights_review must be an object")
        else:
            if review.get("status") != "approved":
                errors.append(f"{prefix}: rights_review.status must be approved")
            if review.get("model_training_allowed") is not True:
                errors.append(f"{prefix}: model_training_allowed must be true")
            if not isinstance(review.get("evidence_ref"), str) or not review["evidence_ref"].strip():
                errors.append(f"{prefix}: rights_review.evidence_ref is required")
            reviewed_at = review.get("reviewed_at")
            try:
                date.fromisoformat(reviewed_at)
            except (TypeError, ValueError):
                errors.append(f"{prefix}: rights_review.reviewed_at must be YYYY-MM-DD")

        source = record["source"]
        if not isinstance(source, dict):
            errors.append(f"{prefix}: source must be an object")
        else:
            for field in ("dataset_id", "revision", "row_id", "license", "source_url", "attribution"):
                value = source.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{prefix}: source.{field} is required")
            revision = source.get("revision")
            if isinstance(revision, str) and not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
                errors.append(f"{prefix}: source.revision must be an immutable 40-character SHA")

        messages = record["messages"]
        if not isinstance(messages, list) or len(messages) < 2:
            errors.append(f"{prefix}: messages must contain at least two chat messages")
            continue
        roles: list[str] = []
        for message_index, message in enumerate(messages, start=1):
            if not isinstance(message, dict):
                errors.append(f"{prefix}: message {message_index} must be an object")
                continue
            role, content = message.get("role"), message.get("content")
            if not isinstance(role, str) or role not in {"system", "user", "assistant"}:
                errors.append(f"{prefix}: message {message_index} has an invalid role")
            else:
                roles.append(role)
            if not isinstance(content, str) or not content.strip():
                errors.append(f"{prefix}: message {message_index} content must be non-empty")
        if "user" not in roles or roles[-1:] != ["assistant"]:
            errors.append(f"{prefix}: messages must include a user turn and end with assistant")

    return errors


def load_training_jsonl(path: str | Path) -> list[dict[str, Any]]:
    """Load UTF-8 JSONL with line-aware parse errors."""
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise TrainingDataError(
                    f"line {line_number}: invalid JSON: {exc.msg}"
                ) from exc
            if not isinstance(record, dict):
                raise TrainingDataError(f"line {line_number}: expected a JSON object")
            records.append(record)
    return records


def validate_training_file(path: str | Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Return loaded records and all policy/schema validation errors."""
    try:
        records = load_training_jsonl(path)
    except (OSError, UnicodeError, TrainingDataError) as exc:
        return [], [str(exc)]
    return records, validate_training_records(records)

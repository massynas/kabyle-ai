"""Validation helpers for the human-reviewed Kabyle evaluation benchmark."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ALLOWED_SPLITS = frozenset({"dev", "test"})
ALLOWED_CATEGORIES = frozenset({
    "conversation", "comprehension", "idiom", "translation_kab_fr",
    "translation_fr_kab", "translation_kab_ar", "translation_ar_kab",
    "orthography", "literary_register",
})
ALLOWED_REGISTERS = frozenset({"everyday", "literary", "mixed", "unspecified"})
ALLOWED_REVIEW_STATUSES = frozenset({"draft", "reviewed"})


class BenchmarkValidationError(ValueError):
    """Raised when a benchmark JSONL row cannot be parsed."""


def validate_records(
    records: list[dict[str, Any]], *, require_reviewed: bool = False
) -> list[str]:
    """Return schema errors without modifying or normalizing source strings."""
    errors: list[str] = []
    seen_ids: set[str] = set()
    required = (
        "id", "split", "category", "register", "prompt",
        "reference_answer", "review_status",
    )
    for index, record in enumerate(records, start=1):
        prefix = f"record {index}"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: expected a JSON object")
            continue
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

        enum_fields = (
            ("split", ALLOWED_SPLITS),
            ("category", ALLOWED_CATEGORIES),
            ("register", ALLOWED_REGISTERS),
            ("review_status", ALLOWED_REVIEW_STATUSES),
        )
        for field, allowed_values in enum_fields:
            value = record[field]
            if not isinstance(value, str) or value not in allowed_values:
                errors.append(
                    f"{prefix}: {field} must be one of {sorted(allowed_values)}"
                )
        for field in ("prompt", "reference_answer"):
            value = record[field]
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}: {field} must be a non-empty string")
        if require_reviewed and record["review_status"] != "reviewed":
            errors.append(f"{prefix}: record is not marked reviewed")
    return errors


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    """Load UTF-8 JSONL and report malformed rows with their line number."""
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise BenchmarkValidationError(
                    f"line {line_number}: invalid JSON: {exc.msg}"
                ) from exc
            if not isinstance(value, dict):
                raise BenchmarkValidationError(
                    f"line {line_number}: expected a JSON object"
                )
            records.append(value)
    return records


def validate_file(
    path: str | Path, *, require_reviewed: bool = False
) -> list[str]:
    """Validate a JSONL file, returning schema or I/O errors."""
    try:
        records = load_jsonl(path)
    except (OSError, UnicodeError, BenchmarkValidationError) as exc:
        return [str(exc)]
    return validate_records(records, require_reviewed=require_reviewed)

"""Conservative utilities for aligned Kabyle audio/text corpus metadata.

This module never decodes, copies, or stores audio bytes. It preserves the
source transcript verbatim and requires an explicit row-level license.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

COMMERCIAL_ATTRIBUTION_LICENSES = frozenset({"CC BY 4.0"})


def normalize_license_label(value: Any) -> str | None:
    """Normalize spacing/case only; do not collapse distinct license terms."""
    if value is None:
        return None
    label = " ".join(str(value).strip().upper().replace("-", " ").split())
    return label or None


def is_initial_training_license_allowed(value: Any) -> bool:
    """Allow only explicit CC BY 4.0 rows in the initial commercial-use lane."""
    return normalize_license_label(value) in COMMERCIAL_ATTRIBUTION_LICENSES


def build_text_record(
    row: Mapping[str, Any],
    *,
    dataset_id: str,
    revision: str,
    row_id: str | int,
    kabyle_field: str,
    license_field: str,
    translation_field: str | None = None,
    translation_language: str | None = None,
) -> dict[str, Any] | None:
    """Build a text-only aligned record from a row with an approved license.

    The original Kabyle and translation strings are copied unchanged. Audio is
    deliberately omitted; the caller must keep source metadata and audio rights
    in a separate speech pipeline.
    """
    license_value = row.get(license_field)
    if not is_initial_training_license_allowed(license_value):
        return None

    kabyle_text = row.get(kabyle_field)
    if not isinstance(kabyle_text, str) or not kabyle_text.strip():
        return None

    record: dict[str, Any] = {
        "text_original": kabyle_text,
        "source": {
            "dataset_id": dataset_id,
            "revision": revision,
            "row_id": str(row_id),
            "license": str(license_value).strip(),
        },
        "modalities": ["text"],
        "source_modalities": ["audio", "text"],
        "validation_status": "unreviewed",
    }

    if translation_field is not None:
        if not translation_language:
            raise ValueError("translation_language is required when translation_field is set")
        translation = row.get(translation_field)
        if isinstance(translation, str) and translation.strip():
            record["translation"] = {
                "text_original": translation,
                "language": translation_language,
            }

    return record

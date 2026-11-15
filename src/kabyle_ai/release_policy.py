"""Policy checks for releasing a trained adapter or model artifact."""
from __future__ import annotations

from typing import Any


def validate_release_manifest(manifest: dict[str, Any]) -> list[str]:
    """Return blockers unless all source lanes permit open-source weight release."""
    errors: list[str] = []
    if manifest.get("rights_reviewed") is not True:
        errors.append("rights_reviewed must be true")
    if manifest.get("commercial_use_allowed_for_all_rows") is not True:
        errors.append("all source rows must permit commercial use")
    if manifest.get("weights_distribution_allowed_for_all_rows") is not True:
        errors.append("all source rows must permit model-weight distribution")
    if not isinstance(manifest.get("training_rows"), int) or manifest["training_rows"] < 1:
        errors.append("training_rows must be a positive integer")

    evidence = manifest.get("rights_evidence_refs")
    if not isinstance(evidence, list) or not evidence or any(
        not isinstance(item, str) or not item.strip() for item in evidence
    ):
        errors.append("rights_evidence_refs must contain auditable references")

    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty list")
    else:
        for index, source in enumerate(sources, start=1):
            if not isinstance(source, dict):
                errors.append(f"source {index} must be an object")
                continue
            for field in ("dataset_id", "revision", "license"):
                value = source.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"source {index}: {field} is required")
    return errors

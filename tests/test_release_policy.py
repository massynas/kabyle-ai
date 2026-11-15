from kabyle_ai.release_policy import validate_release_manifest


def valid_manifest():
    return {
        "rights_reviewed": True,
        "commercial_use_allowed_for_all_rows": True,
        "weights_distribution_allowed_for_all_rows": True,
        "training_rows": 100,
        "rights_evidence_refs": ["private/rights/approval-001.pdf"],
        "sources": [
            {"dataset_id": "owner/data", "revision": "a" * 40, "license": "CC BY 4.0"}
        ],
    }


def test_fully_cleared_manifest_passes():
    assert validate_release_manifest(valid_manifest()) == []


def test_noncommercial_source_blocks_open_source_release():
    manifest = valid_manifest()
    manifest["commercial_use_allowed_for_all_rows"] = False
    assert any(
        "commercial use" in error
        for error in validate_release_manifest(manifest)
    )


def test_missing_weight_distribution_permission_blocks_release():
    manifest = valid_manifest()
    manifest["weights_distribution_allowed_for_all_rows"] = False
    assert any(
        "weight distribution" in error
        for error in validate_release_manifest(manifest)
    )


def test_missing_rights_evidence_blocks_release():
    manifest = valid_manifest()
    manifest["rights_evidence_refs"] = []
    assert any(
        "rights_evidence_refs" in error
        for error in validate_release_manifest(manifest)
    )


def test_empty_training_run_cannot_be_released():
    manifest = valid_manifest()
    manifest["training_rows"] = 0
    assert any(
        "training_rows" in error
        for error in validate_release_manifest(manifest)
    )

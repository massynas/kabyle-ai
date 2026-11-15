from kabyle_ai.training_data import validate_training_records


def valid_record(**overrides):
    record = {
        "id": "train-0001",
        "split": "train",
        "messages": [
            {"role": "user", "content": "Prompt text."},
            {"role": "assistant", "content": "Answer text."},
        ],
        "training_approved": True,
        "rights_review": {
            "status": "approved",
            "model_training_allowed": True,
            "commercial_use_allowed": False,
            "weights_distribution_allowed": False,
            "evidence_ref": "private/rights/approval-001.pdf",
            "reviewed_at": "2026-11-15",
        },
        "source": {
            "dataset_id": "owner/dataset",
            "revision": "a" * 40,
            "row_id": "row-1",
            "license": "CC BY 4.0",
            "source_url": "https://example.org/source",
            "attribution": "Required attribution text",
        },
    }
    record.update(overrides)
    return record


def test_fully_approved_training_record_passes():
    assert validate_training_records([valid_record()]) == []


def test_unapproved_record_is_rejected():
    errors = validate_training_records([valid_record(training_approved=False)])
    assert any("training_approved must be true" in error for error in errors)


def test_non_train_split_is_rejected():
    errors = validate_training_records([valid_record(split="test")])
    assert any("only split='train'" in error for error in errors)


def test_missing_rights_evidence_is_rejected():
    record = valid_record()
    record["rights_review"]["evidence_ref"] = ""
    errors = validate_training_records([record])
    assert any("evidence_ref is required" in error for error in errors)


def test_noncommercial_training_permission_must_be_explicit():
    record = valid_record()
    record["rights_review"]["model_training_allowed"] = False
    errors = validate_training_records([record])
    assert any("model_training_allowed must be true" in error for error in errors)


def test_missing_source_attribution_is_rejected():
    record = valid_record()
    record["source"]["attribution"] = ""
    errors = validate_training_records([record])
    assert any("source.attribution is required" in error for error in errors)


def test_duplicate_training_ids_are_rejected():
    errors = validate_training_records([valid_record(), valid_record(id="train-0001")])
    assert any("duplicate id" in error for error in errors)


def test_messages_must_end_with_assistant():
    record = valid_record()
    record["messages"][-1] = {"role": "user", "content": "Follow-up"}
    errors = validate_training_records([record])
    assert any("end with assistant" in error for error in errors)


def test_empty_training_file_is_rejected():
    errors = validate_training_records([])
    assert any("contains no records" in error for error in errors)


def test_malformed_message_role_is_reported_without_crashing():
    record = valid_record()
    record["messages"][0]["role"] = ["user"]
    errors = validate_training_records([record])
    assert any("invalid role" in error for error in errors)


def test_source_revision_must_be_immutable_sha():
    record = valid_record()
    record["source"]["revision"] = "main"
    errors = validate_training_records([record])
    assert any("immutable 40-character SHA" in error for error in errors)

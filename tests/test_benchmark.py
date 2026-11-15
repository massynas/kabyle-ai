import json

import pytest

from kabyle_ai.benchmark import BenchmarkValidationError, load_jsonl, validate_records


def valid_record(**overrides):
    record = {
        "id": "kab-dev-0001",
        "split": "dev",
        "category": "conversation",
        "register": "everyday",
        "prompt": "Replace with a native-reviewed prompt.",
        "reference_answer": "Replace with a native-reviewed answer.",
        "review_status": "reviewed",
    }
    record.update(overrides)
    return record


def test_valid_record_passes_reviewed_gate():
    assert validate_records([valid_record()], require_reviewed=True) == []


def test_duplicate_ids_are_rejected():
    errors = validate_records([valid_record(), valid_record()])
    assert any("duplicate id" in error for error in errors)


def test_unreviewed_record_fails_strict_gate():
    errors = validate_records([valid_record(review_status="draft")], require_reviewed=True)
    assert any("not marked reviewed" in error for error in errors)


def test_training_split_is_not_an_evaluation_split():
    errors = validate_records([valid_record(split="train")])
    assert any("split must be" in error for error in errors)


def test_literary_register_is_supported():
    record = valid_record(category="literary_register", register="literary")
    assert validate_records([record]) == []


def test_jsonl_loader_reports_bad_line(tmp_path):
    path = tmp_path / "benchmark.jsonl"
    path.write_text('{"id":"ok"}\nnot-json\n', encoding="utf-8")
    with pytest.raises(BenchmarkValidationError, match="line 2"):
        load_jsonl(path)


def test_jsonl_loader_preserves_unicode_verbatim(tmp_path):
    record = valid_record(prompt="ɣ ɛ č ḍ ṛ ṣ ṭ — ⴰ")
    path = tmp_path / "benchmark.jsonl"
    path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
    assert load_jsonl(path)[0]["prompt"] == record["prompt"]


def test_malformed_enum_types_are_reported_without_crashing():
    errors = validate_records([valid_record(category=["not", "a", "category"])])
    assert any("category must be one of" in error for error in errors)


def test_validate_file_reports_invalid_utf8(tmp_path):
    from kabyle_ai.benchmark import validate_file

    path = tmp_path / "invalid.jsonl"
    path.write_bytes(bytes([255]))
    errors = validate_file(path)
    assert errors and "utf-8" in errors[0].lower()


def test_kabyle_arabic_translation_categories_are_supported():
    kabyle_to_arabic = valid_record(category="translation_kab_ar")
    arabic_to_kabyle = valid_record(category="translation_ar_kab")
    assert validate_records([kabyle_to_arabic, arabic_to_kabyle]) == []

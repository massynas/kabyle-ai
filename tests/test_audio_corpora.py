from kabyle_ai.audio_corpora import (
    build_text_record,
    is_initial_training_license_allowed,
    normalize_license_label,
)


def test_only_explicit_cc_by_4_is_allowed():
    assert is_initial_training_license_allowed("CC BY 4.0")
    assert is_initial_training_license_allowed(" cc by 4.0 ")
    assert not is_initial_training_license_allowed("CC BY-NC 4.0")
    assert not is_initial_training_license_allowed(None)
    assert not is_initial_training_license_allowed("CC")


def test_license_normalization_does_not_remove_noncommercial_term():
    assert normalize_license_label("CC BY-NC 4.0") == "CC BY NC 4.0"
    assert not is_initial_training_license_allowed("CC BY-NC 4.0")


def test_text_record_preserves_original_unicode_and_translation():
    original = "Ur εlimeɣ — ɣ, ɛ, č, ḍ, ṛ, ṣ, ṭ."
    row = {
        "Text": original,
        "French": "Je ne sais pas.",
        "Licence": "CC BY 4.0",
        "audio": {"path": "must-not-be-copied.wav"},
    }
    record = build_text_record(
        row,
        dataset_id="example/kabyle_asr",
        revision="abc123",
        row_id=7,
        kabyle_field="Text",
        license_field="Licence",
        translation_field="French",
        translation_language="fr",
    )
    assert record is not None
    assert record["text_original"] == original
    assert record["translation"]["text_original"] == "Je ne sais pas."
    assert "audio" not in record
    assert record["source"]["row_id"] == "7"


def test_noncommercial_row_is_rejected():
    row = {"Text": "Tafukt.", "Licence": "CC BY-NC 4.0"}
    assert build_text_record(
        row,
        dataset_id="example/kabyle_asr",
        revision="abc123",
        row_id=1,
        kabyle_field="Text",
        license_field="Licence",
    ) is None


def test_missing_license_field_is_rejected():
    row = {"Text": "Tafukt."}
    assert build_text_record(
        row,
        dataset_id="example/unknown",
        revision="abc123",
        row_id=1,
        kabyle_field="Text",
        license_field="Licence",
    ) is None

from scripts.stage_hf_corpora import (
    SOURCES,
    SIFAL_COLUMNS,
    load_sifal_tsv,
    slug,
)


def test_all_known_sources_have_separate_roles_and_rights_status():
    assert "TutlaytAI/Kabyle_ASR-Fr_Translation" in SOURCES
    assert "TutlaytAI/Kabyle_ASR-En_Translation" in SOURCES
    assert "agbalu/KabBench" in SOURCES
    assert SOURCES["agbalu/KabBench"]["role"] == "evaluation_only"
    assert "NC" in SOURCES["TutlaytAI/kabyle_asr"]["rights"]


def test_dataset_slug_is_filesystem_safe():
    assert slug("agbalu/KabLiterary") == "agbalu__KabLiterary"


def test_sifal_tsv_keeps_first_record_and_maps_columns(tmp_path):
    source = tmp_path / "sample.tsv"
    source.write_text(
        "3674822\tẒriɣ dacu ara d-tiniḍ.\t3674816\tJe sais ce que tu vas dire.\n"
        "3675223\tƔur-went sebεa warrac.\t3675232\tVous avez sept enfants.\n",
        encoding="utf-8",
    )

    dataset = load_sifal_tsv(source)
    rows = dataset["train"]

    assert rows.column_names == SIFAL_COLUMNS
    assert len(rows) == 2
    assert rows[0]["kabyle_sentence_id"] == "3674822"
    assert rows[0]["kabyle_text"] == "Ẓriɣ dacu ara d-tiniḍ."
    assert rows[0]["french_sentence_id"] == "3674816"
    assert rows[0]["french_text"] == "Je sais ce que tu vas dire."

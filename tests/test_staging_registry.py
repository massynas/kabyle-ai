from scripts.stage_hf_corpora import SOURCES, slug


def test_all_known_sources_have_separate_roles_and_rights_status():
    assert "TutlaytAI/Kabyle_ASR-Fr_Translation" in SOURCES
    assert "TutlaytAI/Kabyle_ASR-En_Translation" in SOURCES
    assert "agbalu/KabBench" in SOURCES
    assert SOURCES["agbalu/KabBench"]["role"] == "evaluation_only"
    assert "NC" in SOURCES["TutlaytAI/kabyle_asr"]["rights"]


def test_dataset_slug_is_filesystem_safe():
    assert slug("agbalu/KabLiterary") == "agbalu__KabLiterary"

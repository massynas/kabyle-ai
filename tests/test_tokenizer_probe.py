from scripts.probe_tokenizer import summarize_text


class FakeTokenizer:
    unk_token_id = 0

    def encode(self, text, add_special_tokens=False):
        assert add_special_tokens is False
        return [ord(character) for character in text]

    def decode(self, token_ids, skip_special_tokens=False):
        return "".join(chr(token_id) for token_id in token_ids)

    def convert_ids_to_tokens(self, token_ids):
        return [str(token_id) for token_id in token_ids]


def test_probe_preserves_kabyle_and_tifinagh_unicode():
    text = "ɣ ɛ č ḍ ṛ ṣ ṭ — ⴰⵣⵓⵍ"
    result = summarize_text(FakeTokenizer(), text)
    assert result["round_trip_exact"] is True
    assert result["decoded"] == text
    assert result["unknown_token_count"] == 0


def test_probe_counts_unknown_tokens():
    tokenizer = FakeTokenizer()
    result = summarize_text(tokenizer, "A")
    assert result["unknown_token_count"] == 0

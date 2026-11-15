from scripts.run_benchmark import SYSTEM_PROMPT, build_messages


def test_build_messages_preserves_prompt_exactly():
    prompt = "ɣ ɛ č ḍ ṛ ṣ ṭ — ⴰⵣⵓⵍ"
    messages = build_messages({"prompt": prompt})
    assert messages[0] == {"role": "system", "content": SYSTEM_PROMPT}
    assert messages[1] == {"role": "user", "content": prompt}


def test_system_prompt_does_not_force_every_task_into_kabyle():
    assert "Follow the language and register requested" in SYSTEM_PROMPT

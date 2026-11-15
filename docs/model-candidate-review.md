# Initial base-model candidate review

**Review date:** 15 November 2026  
**Decision:** keep model selection provisional until we run the same native-speaker Kabyle benchmark and tokenizer probe on each candidate.

## Candidates

| Model | Size | Model-card license | Declared language coverage | Initial assessment |
|---|---:|---|---|---|
| [Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) | 1.7B | Apache-2.0 | Qwen states support for 100+ languages and dialects | **Preferred first baseline candidate.** Best balance found so far between compact size, multilingual instruction/translation claims and a permissive model license. Kabyle is not explicitly confirmed; test it rather than infer support. |
| [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) | 1.5B | Apache-2.0 | Model card metadata is less explicit about language coverage | Keep as a smaller control/baseline. Do not assume it is better just because the initial project scaffold named it. |
| [SmolLM3-3B](https://huggingface.co/HuggingFaceTB/SmolLM3-3B) | 3B | Apache-2.0 | Six native languages: English, French, Spanish, German, Italian and Portuguese; Arabic is reported as having fewer training tokens | Useful larger comparison for French quality and open training transparency, but its published native-language list does not include Kabyle or Arabic as a primary language. |
| [Gemma 3 1B IT](https://huggingface.co/google/gemma-3-1b-it) | 1B | Gemma terms | Multilingual | Not selected for the first open-source path: its repository is gated in the connected account and its license is not Apache-2.0. Revisit only if the terms and access are acceptable. |

## Why Qwen3-1.7B is the leading candidate

- The official model card declares Apache-2.0.
- The official card describes support for more than 100 languages and dialects, multilingual instruction following and translation.
- It is only modestly larger than Qwen2.5-1.5B while offering a newer instruction-tuned architecture.
- Its chat template exposes a non-thinking mode, which is the sensible default for a lightweight conversational Kabyle assistant and avoids emitting reasoning traces.

This is a candidate ranking, not a performance claim. General multilingual coverage does not establish Kabyle fluency.

## Required checks before selection

1. **Tokenizer probe:** encode/decode `ɣ ɛ č ḍ ṛ ṣ ṭ`, uppercase forms, Tifinagh, French accents, Arabic script and mixed-script examples. Record unknown-token behaviour, token counts and round-trip fidelity.
2. **Native-speaker benchmark:** evaluate natural everyday conversation, comprehension, idioms, register variation and Kabyle↔French/Arabic translation. Score naturalness and meaning separately.
3. **Base comparison:** use identical prompts, decoding settings and evaluation splits for Qwen3-1.7B and Qwen2.5-1.5B.
4. **Fine-tuning pilot:** only after the benchmark and rights-cleared seed set exist, run a small LoRA/QLoRA experiment and compare against the untouched base model.
5. **Open-source release audit:** check the model license, dataset licenses, attribution, share-alike obligations, source permissions and any restrictions on derived weights.

## Current conclusion

Use `Qwen/Qwen3-1.7B` as the first candidate to probe, not as a final selection. Keep `Qwen/Qwen2.5-1.5B-Instruct` as the control. No model weights have been downloaded or fine-tuned in this step.

# Kabyle open-resource inventory

**Review status:** first-pass desk research, 15 November 2026. This is a source register, not a statement that every item is cleared for our training pipeline. Re-check the dataset card, upstream source licenses, terms and current revision before each import.

## Highest-priority candidates

| Resource | Contents / scale reported by publisher | License shown | Intended use in Kabyle AI | Decision |
|---|---|---|---|---|
| [AƔBALU project](https://github.com/abderahmane-ai/agbalu) | Kabyle NLP code, corpus pipeline, normalisation, datasets and models | Repository code: Apache-2.0; data retains upstream licenses | Study its methodology, data provenance, normalisation and existing Kabyle models before duplicating work | **Inspect deeply; do not mirror wholesale** |
| [KabLex](https://huggingface.co/datasets/agbalu/KabLex) | 366,892 lexical entries; 25,642 word–IPA pronunciation pairs. About 94% of entries are inflected verb forms; only a subset has glosses | CC-BY-4.0 | Lexical lookup, morphology, vocabulary checks and possible auxiliary training | **Candidate for use with attribution**; not a conversational corpus |
| [KabStandard](https://huggingface.co/datasets/agbalu/KabStandard) | 497,944 synthetic pairs mapping informal/French-keyboard/Arabizi Kabyle to canonical Latin spelling; train/dev/test splits | Apache-2.0 shown on dataset card | Orthographic robustness and a separate normalisation component | **Candidate**, but do not treat synthetic corruptions as real conversational examples |
| [KabBench](https://huggingface.co/datasets/agbalu/KabBench) | 2,009 Kabyle MT reference sentences and 1,500 language-identification examples across six Amazigh varieties | CC-BY-SA-4.0 | Evaluation only: translation scoring, spelling and distinguishing Kabyle from related languages | **Keep out of training**; preserve as a held-out benchmark |
| [Kabyle-French (Tatoeba export)](https://huggingface.co/datasets/Sifal/Kabyle-French) | 115,269 French↔Kabyle sentence pairs | Hugging Face card says only “CC”; upstream Tatoeba uses sentence-level licensing | Potentially the most directly relevant parallel text for French↔Kabyle | **Quarantine pending license audit and quality sampling**; export is unverified and may contain errors |

## Audio and aligned speech-text resources

| Resource | Contents / scale reported by publisher | License shown | Intended use | Decision |
|---|---|---|---|---|
| [TutlaytAI/Kabyle_ASR-Fr_Translation](https://huggingface.co/datasets/TutlaytAI/Kabyle_ASR-Fr_Translation) | 22,337 rows with audio, Kabyle sentence and French translation | No clear license declaration visible on the dataset card | Aligned Kabyle/French text and future ASR/translation experiments | **Quarantine** until publisher confirms rights and upstream provenance |
| [TutlaytAI/Kabyle_ASR-En_Translation](https://huggingface.co/datasets/TutlaytAI/Kabyle_ASR-En_Translation) | 29,144 rows with audio, Kabyle sentence and English translation | No clear license declaration visible on the dataset card | Aligned Kabyle/English text and future ASR/translation experiments | **Quarantine** until publisher confirms rights and upstream provenance |
| [TutlaytAI/kabyle_asr](https://huggingface.co/datasets/TutlaytAI/kabyle_asr) | About 32.8k rows in the visible train split, with audio, Kabyle text and a row-level `Licence` field | Mixed CC BY 4.0 and CC BY-NC 4.0 | ASR and possible text-only use of individually cleared rows | **Row-level filtering required**; exclude NC and unknown rows, pin revision and verify audio/source rights |
| [Common Voice Kabyle 27.0](https://mozilladatacollective.com/datasets/cmu5xcvp800eao107zfex7alc) | 747,922 clips; 571.72 validated hours reported | CC0-1.0, with no-rehosting/re-sharing and no speaker-identification restrictions | Later ASR and speech work | **Speech milestone**; never re-host/re-share audio |

The two translated datasets are especially promising linguistically, but their visible cards do not provide a clear license declaration. Their 22k/29k examples must not be imported until the publisher confirms rights and provenance. The raw ASR dataset exposes mixed row-level licenses: a dataset-level `cc` label is not sufficient to clear every row. The initial commercial-use filter accepts only explicit CC BY 4.0 rows and excludes CC BY-NC 4.0.

Implementation notes and the conservative ingestion tooling are in [docs/audio-corpus-plan.md](audio-corpus-plan.md). No audio bytes or external corpus rows have been copied into this repository.

## Useful but not first-wave conversational training

| Resource | Contents / scale reported by publisher | License shown | Intended use | Decision |
|---|---|---|---|---|
| [KabLiterary](https://huggingface.co/datasets/agbalu/KabLiterary) | 28,907 paragraphs / 657,713 words from 11 works. Ten works are machine-translated; one is original Kabyle poetry | CC-BY-SA-4.0 | Literary/high-register language exposure and translation research | **Optional later experiment**; share-alike obligations apply and machine-translated syntax must be reviewed |
| [Common Voice Kabyle 27.0](https://mozilladatacollective.com/datasets/cmu5xcvp800eao107zfex7alc) | Publisher reports 747,922 clips, 694.63 recorded hours, 571.72 validated hours, 1,608 speakers and 389,279 source sentences | CC0-1.0; dataset terms forbid speaker identification and re-hosting | Speech recognition / future speech work; transcripts may help identify text but are not spontaneous dialogue | **Defer** because the first milestone is text-only; do not re-host audio |
| [FLORES+ Kabyle references via KabBench](https://huggingface.co/datasets/agbalu/KabBench) | Corrected Kabyle side of a multilingual translation benchmark | CC-BY-SA-4.0 | Held-out translation evaluation | **Evaluation only**, not training |

## Important observations

### AƔBALU is a major existing effort
The public repository describes a full Kabyle NLP stack, including corpora, a normaliser, tokenizer experiments, translation, speech and evaluation assets. Its published datasets include lexical/morphological resources and literary text. We should learn from it and compare its existing models before deciding whether to fine-tune a generic model. The fact that model weights are Apache-2.0 does **not** make all underlying text data Apache-2.0; the project explicitly preserves upstream dataset licenses.

### The biggest directly relevant text candidate needs human review
The Tatoeba-derived Kabyle-French export has over 115k rows, but the dataset page says it was exported automatically and not manually verified. Its displayed license field is broad/ambiguous (“CC”), so the precise sentence-level license and attribution obligations must be resolved from the upstream records before training. Sample for duplicate translations, dialect, register, unnatural examples and incorrect alignment.

### Literary text is not everyday speech
KabLiterary is a substantial source of well-formed Kabyle text, but ten of eleven works are machine-translated and the publisher itself notes source-language influence and specialist vocabulary. It should not dominate an everyday conversational model. The CC-BY-SA-4.0 terms also need to be respected in any redistributed derivative dataset.

### Common Voice is primarily a speech resource
Common Voice 27.0 reports a substantial Kabyle speech collection under CC0-1.0, but it is designed for ASR. It is not evidence of 694 hours of spontaneous conversation: recordings are read from a text corpus. Speaker-identification prohibition and no-rehosting terms must be observed.

### Orthography and language identity
Keep the original text and a separate normalised representation. Watch for Latin/Greek homoglyphs (notably Greek epsilon versus Latin ɛ), missing diacritics, French-keyboard spellings, Arabizi, and mixed Amazigh varieties. Kabyle must not be merged indiscriminately with Tarifit, Tashelhit, Shawiya or Central Atlas Tamazight.

## Import policy

Before downloading any source into the training pipeline:
1. Pin the exact dataset revision/commit and save the dataset card.
2. Record license identifier, upstream license, attribution text, source URL and retrieval date.
3. Confirm whether commercial use, modification, redistribution and model training are allowed.
4. Preserve source IDs and per-row licenses where available.
5. Run duplicate, language-ID, orthography and quality checks.
6. Sample and validate examples with a native Kabyle speaker.
7. Keep benchmark/test data out of training and retrieval indexes.
8. Store corpora outside Git; commit only manifests, scripts and small permitted examples.

## First collection order

1. **Audit KabLex and KabStandard**: relatively clear license metadata and useful auxiliary tasks.
2. **Audit Tatoeba row-level licensing** and inspect a representative sample before any training import.
3. **Inspect AƔBALU corpus manifests and source registry** to find further reusable raw text and avoid duplicating its work.
4. **Review KabLiterary** as a separate literary-domain corpus.
5. Keep KabBench/FLORES+ frozen for evaluation.
6. Audit TutlaytAI audio datasets: request license/provenance clarification for translated corpora; count and filter row-level licenses in kabyle_asr.\n7. Defer Common Voice audio until a speech milestone.

## Source notes

All quantities and license labels above are publisher-reported, not independently re-counted by this repository. A dataset card is evidence to investigate, not a substitute for legal review of upstream works. Where the license is ambiguous or share-alike, do not combine the data into a permissively licensed release by default.

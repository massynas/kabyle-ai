# Kabyle audio and aligned-text corpus plan

**Status:** discovery and ingestion tooling only. No audio or corpus rows are copied into this repository.

## Why these sources matter

Audio paired with an exact Kabyle transcript and a translation provides three aligned views of the same utterance. It can support:
- text-only Kabyle learning from the transcript and translation;
- later automatic speech recognition (audio → Kabyle text);
- later speech translation experiments;
- pronunciation and orthography analysis, while keeping those tasks separate from the text model.

The text model can use legally cleared transcript/translation pairs without ingesting audio bytes. The audio pipeline must remain a separate modality and must not silently turn speech data into text-only training data without retaining provenance.

## First discovered sources

| Dataset | Publisher-reported rows | Fields / languages | Current decision |
|---|---:|---|---|
| [TutlaytAI/Kabyle_ASR-Fr_Translation](https://huggingface.co/datasets/TutlaytAI/Kabyle_ASR-Fr_Translation) | 22,337 | audio, Kabyle sentence, French translation | **Quarantine**: the visible dataset card exposes no clear license identifier or per-row license field. Do not train on it until the publisher clarifies the rights and upstream provenance. |
| [TutlaytAI/Kabyle_ASR-En_Translation](https://huggingface.co/datasets/TutlaytAI/Kabyle_ASR-En_Translation) | 29,144 | audio, Kabyle sentence, English translation | **Quarantine**: same missing license/provenance evidence. |
| [TutlaytAI/kabyle_asr](https://huggingface.co/datasets/TutlaytAI/kabyle_asr) | 32.8k rows in the visible train split | audio, Kabyle text, row-level `Licence` | **Inspect row-level rights**. The viewer shows both CC BY 4.0 and CC BY-NC 4.0. Only exact CC BY 4.0 rows may pass the initial commercial-use filter; exclude NC rows. Confirm the source and audio rights before production use. |
| [Mozilla Common Voice Kabyle 27.0](https://mozilladatacollective.com/datasets/cmu5xcvp800eao107zfex7alc) | 747,922 clips; 571.72 validated hours reported | audio and prompted transcript | **Speech milestone**. CC0-1.0, but do not re-host/re-share the dataset or attempt speaker identification. These are read recordings, not spontaneous conversation. |

The two translation datasets show useful examples and audio/text columns, but a missing license declaration is not permission. The raw ASR dataset is especially important because its viewer exposes mixed row-level licensing. Never treat the dataset-level generic `cc` label as overriding a more restrictive row-level license.

## Import rules

1. Pin an immutable Hugging Face revision before every audit or import. Do not use a moving `main` revision for a reproducible training run.
2. Record dataset ID, revision, retrieval date, original row ID, exact license string, source URL and field mapping.
3. Preserve Kabyle text exactly in `text_original`; never overwrite it with normalized text.
4. Store any normalized spelling in a separate field and preserve the original Unicode code points.
5. For the initial commercial-use candidate pipeline, allow only an exact row-level `CC BY 4.0` declaration. Exclude `CC BY-NC 4.0`, unknown, missing, ambiguous and conflicting licenses.
6. A license filter is not a substitute for confirming the dataset's upstream provenance, attribution requirements and rights in the audio itself.
7. Keep audio bytes outside Git. Do not copy dataset audio into this repository.
8. Keep train/dev/test partitions source-aware. Do not leak held-out benchmark material into training or retrieval.
9. Sample transcripts and translations for alignment, dialect, transcription accuracy, duplicates and unnatural examples. Native-speaker review remains necessary.

## Current technical implementation

- `src/kabyle_ai/audio_corpora.py` contains a conservative row-level license gate and a text-only record builder.
- `scripts/audit_hf_audio_corpus.py` inspects a pinned Hugging Face dataset revision in streaming mode. It reports columns and license counts without writing audio.
- `configs/audio-corpora.yaml` records source IDs, field names, and current rights decisions.
- The scripts intentionally do not download or export training data automatically. An explicit revision and an approved license field are required.

## Next steps

1. Ask the TutlaytAI publisher for the license and upstream provenance of both translated audio datasets.
2. Audit a pinned revision of `TutlaytAI/kabyle_asr`, count rows by exact license, and inspect only the CC BY 4.0 subset.
3. Confirm whether the audio recording rights follow the row-level license and retain required attribution.
4. Run native-speaker review on a stratified sample before any SFT export.
5. Later, evaluate ASR separately using held-out speakers and clips; never identify speakers.

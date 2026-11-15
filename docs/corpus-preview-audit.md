# First Hugging Face preview audit

**Audit date:** 15 November 2026  
**Scope:** metadata plus the first three visible rows of selected configurations through the Hugging Face Dataset Viewer. This is a smoke inspection, not a representative quality assessment and not a local corpus download.

## Findings

| Dataset | Preview observations | Follow-up |
|---|---|---|
| `agbalu/KabLex` / `lexicon` | The schema exposes form, lemma, UPOS, features, multilingual glosses, source and a row-level `licence`. The first visible entries are domain-labelled mathematical terminology. | Preserve domain tags and row-level source/licence. Do not assume every entry is everyday vocabulary. |
| `agbalu/KabStandard` | The source/target structure is suitable for a separate orthographic-normalisation task. The preview includes synthetic keyboard/diacritic variants and at least one visibly awkward punctuation/quoting example. | Keep it as a distinct normalisation objective; run automated corruption and native-speaker quality checks before use. |
| `agbalu/KabLiterary` | The schema preserves book, author, year, genre, source language, chapter, paragraph IDs, Kabyle text and source text. The preview confirms long-form literary provenance is retained. | Keep literary material as its own register/source lane; do not discard it merely for being literary. Preserve work-level attribution and CC-BY-SA metadata. |
| `agbalu/KabBench` / `mt` | The evaluation configuration has IDs, split labels, text and a correction flag. | Freeze all benchmark splits; never train on them or add them to retrieval. |
| `TutlaytAI/Kabyle_ASR-Fr_Translation` | Rows align audio, Kabyle transcript and French translation. No explicit license field is exposed in the preview schema. | Quarantine pending publisher permission and upstream audio/transcript provenance. |
| `TutlaytAI/kabyle_asr` | Rows expose audio, Kabyle text and a per-row `Licence`; the first three rows already demonstrate mixed CC-BY-NC and CC-BY labels. | Never infer permission from the dataset-level generic `cc` tag. Filter on exact row-level license only after checking upstream rights; exclude NC from any commercial-use lane absent permission. |
| `Sifal/Kabyle-French` | The raw source is a tab-separated `.tsv` with no header. The first four fields are Kabyle sentence ID, Kabyle text, French sentence ID and French text. The Dataset Viewer treats the first data record as column names, confirming that its generated schema loses the first pair and gives the remaining fields misleading names. | The staging loader now reads the raw TSV with explicit column names and `header=None`, preserving the first sentence pair and both Tatoeba IDs. Investigate sentence-level license/attribution before training. |

## What this audit does not establish

- Three rows are not enough to estimate linguistic quality, dialect coverage, duplication or conversational naturalness.
- A dataset card or Hub preview does not prove that every underlying recording, translation or source work is cleared for training or redistribution.
- No corpus was downloaded to durable storage by this preview operation.
- No source text or audio has been copied into this repository.
- The Sifal staging parser has been corrected in code, but its test has not yet completed in GitHub Actions.

## Next validation tasks

1. Run the new Sifal TSV parser test in CI and verify the complete staged split count against the raw source.
2. Sample KabLex across source/domain and gloss availability, not just its first rows.
3. Measure exact license counts across the full `TutlaytAI/kabyle_asr` split in a compute environment.
4. Request written provenance and license clarification for both TutlaytAI translated audio datasets.
5. Ask a native Kabyle reviewer to score stratified samples for naturalness, meaning, spelling and dialect/register, while retaining literary and spoken registers as separate labels.

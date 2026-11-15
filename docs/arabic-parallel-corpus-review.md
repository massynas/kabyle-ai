# Kabyle–Arabic parallel-data review

**Review date:** 15 November 2026  
**Status:** promising lead found; not cleared for training or redistribution.

## ParaKab — primary lead

[ParaKab: Many Languages, One Kabyle](https://lanfrica.com/en/record/parakab-many-languages-one-kabyle-a-multilingual-parallel-corpus-for-a-low-resource-language) is catalogued as a Zenodo dataset by Mes TAG Bou Bad. The record describes three Kabyle-centric parallel corpora:

- Kabyle–Arabic
- Kabyle–French
- Kabyle–English

The catalogue reports approximately one million aligned sentence pairs across the three language pairs. It says the data were compiled from OPUS resources and selected public websites, then cleaned, normalized, aligned, verified and deduplicated. It also says each pair is linked to its original source and, where applicable, the source license or rights holder. The catalogue lists a general CC BY 4.0 license for the corpus, while explicitly retaining source-specific rights and requiring users to respect the original licenses.

**DOI:** [10.5281/zenodo.18875317](https://doi.org/10.5281/zenodo.18875317)

### Decision

Keep ParaKab in a dedicated legal/provenance review lane. Do not ingest it into training yet. The general CC BY 4.0 label is not enough to clear every row when the record itself says that source-specific licenses and rights holders remain attached to individual pairs.

Before use:

1. Retrieve the original Zenodo archive and metadata from the DOI record.
2. Inspect the schema and identify the Kabyle–Arabic subset, scripts, direction and language variety.
3. Preserve every row's source dataset, source URL/ID, license and rights-holder fields.
4. Count rows by source and license; quarantine missing, conflicting, non-commercial or unclear records.
5. Review Arabic-script conventions and Kabyle spelling with a native speaker.
6. Check duplicates and overlap with the existing Kabyle–French sources and the held-out benchmark.
7. Obtain written permission where source terms are unclear or do not permit the intended model use.

No archive has been downloaded by this repository change.

## Other leads and exclusions

- [taqbaylit/timucuha-kabyle-tales](https://huggingface.co/datasets/taqbaylit/timucuha-kabyle-tales): 920 Kabyle/French/English folklore segments; the Hub metadata declares CC BY-NC 4.0. Useful for research and linguistic review, but excluded from the initial commercial-use training lane unless the rights holder grants additional permission.
- [taqbaylit/nllb_en_kab](https://huggingface.co/datasets/taqbaylit/nllb_en_kab): about 2.8 million English–Kabyle pairs; Hub metadata declares CC BY-NC 4.0. It does not provide Arabic pairs and is not eligible for commercial-use training without additional permission.
- [Imsidag-community/english-kabyle-parallel](https://huggingface.co/datasets/Imsidag-community/english-kabyle-parallel): about 130,883 English–Kabyle Tatoeba pairs; the repository is gated and the Hub metadata shows CC BY 2.0. Access conditions and sentence-level Tatoeba attribution still need review. It does not provide Arabic pairs.
- [Tamazight-NLP/Tamazight-Speech-to-Arabic-Text](https://huggingface.co/datasets/Tamazight-NLP/Tamazight-Speech-to-Arabic-Text): surfaced in discovery as a Tamazight speech-to-Arabic resource, but the language variety is not established as Kabyle. Do not mix it into a Kabyle corpus unless the source proves the variety and rights.

## Implication for the benchmark

The native-speaker benchmark now includes both Kabyle→Arabic and Arabic→Kabyle categories. Until ParaKab's row-level provenance and rights are audited, these benchmark items should be authored independently and reviewed by a native Kabyle speaker. Do not use ParaKab evaluation examples as training data.

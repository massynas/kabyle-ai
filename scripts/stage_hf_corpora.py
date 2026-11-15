#!/usr/bin/env python3
"""Stage known Kabyle Hugging Face datasets locally, pinned to immutable revisions.

This is a collection/audit step, not a training-data approval step. It stores
each source separately, writes a provenance manifest, and never writes corpus
files into Git. Evaluation-only sources remain explicitly marked as such.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from datasets import DatasetDict, load_dataset
from huggingface_hub import HfApi, hf_hub_download


SIFAL_TSV_NAME = "Sentence pairs in Kabyle-French - 2023-07-18.tsv"
SIFAL_COLUMNS = ["kabyle_sentence_id", "kabyle_text", "french_sentence_id", "french_text"]

SOURCES = {
    "TutlaytAI/Kabyle_ASR-Fr_Translation": {
        "role": "quarantine_research",
        "rights": "license_and_upstream_provenance_to_confirm",
        "notes": "Audio + Kabyle transcript + French translation; do not train until rights confirmed.",
    },
    "TutlaytAI/Kabyle_ASR-En_Translation": {
        "role": "quarantine_research",
        "rights": "license_and_upstream_provenance_to_confirm",
        "notes": "Audio + Kabyle transcript + English translation; do not train until rights confirmed.",
    },
    "TutlaytAI/kabyle_asr": {
        "role": "quarantine_row_level_license_review",
        "rights": "mixed_CC_BY_4.0_and_CC_BY_NC_4.0",
        "notes": "Keep row-level Licence field; separate CC BY from CC BY-NC; verify audio/source rights.",
    },
    "agbalu/KabLex": {
        "configs": ["lexicon", "pronunciations"],
        "role": "lexicon_and_pronunciation",
        "rights": "CC_BY_4.0_dataset_with_row_level_upstream_licences",
        "notes": "Keep lexicon and pronunciation configs separate; retain row-level licence and upstream citations.",
    },
    "agbalu/KabStandard": {
        "role": "orthography_normalisation",
        "rights": "Apache_2.0_card_derived_source_chain_to_review",
        "notes": "Derived from KabTifinagh; preserve source/target pairs and review upstream chain.",
    },
    "agbalu/KabLiterary": {
        "role": "language_modeling_candidate",
        "rights": "CC_BY_SA_4.0",
        "notes": "Attribution and share-alike obligations; retain book/work metadata and source_text alignment.",
    },
    "agbalu/KabBench": {
        "role": "evaluation_only",
        "rights": "CC_BY_SA_4.0",
        "notes": "Never place in training or retrieval indexes; keep official splits intact.",
    },
    "Sifal/Kabyle-French": {
        "role": "quarantine_research",
        "rights": "generic_CC_label_sentence_level_rights_to_confirm",
        "notes": "Tatoeba-derived; preserve source IDs and investigate per-sentence licensing and attribution.",
        "format": "tab_separated_no_header",
    },
}


def slug(dataset_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "__", dataset_id)


def load_sifal_tsv(path: str | Path):
    """Load the raw Tatoeba TSV without treating its first sentence as a header."""
    return load_dataset(
        "csv",
        data_files={"train": str(path)},
        delimiter="\t",
        column_names=SIFAL_COLUMNS,
        header=None,
        keep_default_na=False,
    )


def load_source_dataset(dataset_id: str, revision: str, config_name: str | None):
    """Load one source, applying source-specific parsing where required."""
    if dataset_id == "Sifal/Kabyle-French":
        path = hf_hub_download(
            repo_id=dataset_id,
            filename=SIFAL_TSV_NAME,
            repo_type="dataset",
            revision=revision,
        )
        return load_sifal_tsv(path)

    return load_dataset(
        dataset_id,
        name=config_name,
        revision=revision,
        streaming=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("staging/huggingface"))
    parser.add_argument("--dataset", action="append", dest="datasets",
                        help="Stage only this dataset ID; may be repeated.")
    parser.add_argument("--max-samples", type=int, default=0,
                        help="Optional small smoke-test limit; 0 stages the full dataset.")
    args = parser.parse_args()

    selected = args.datasets or list(SOURCES)
    unknown = sorted(set(selected) - set(SOURCES))
    if unknown:
        parser.error(f"Unknown dataset IDs: {', '.join(unknown)}")

    api = HfApi()
    args.output.mkdir(parents=True, exist_ok=True)

    for dataset_id in selected:
        info = api.dataset_info(dataset_id)
        revision = info.sha
        if not revision:
            raise RuntimeError(f"Could not resolve immutable revision for {dataset_id}")

        destination = args.output / slug(dataset_id) / revision
        destination.mkdir(parents=True, exist_ok=True)
        config_names = SOURCES[dataset_id].get("configs", [None])
        for config_name in config_names:
            dataset = load_source_dataset(dataset_id, revision, config_name)

            if args.max_samples:
                dataset = DatasetDict({
                    split: rows.select(range(min(args.max_samples, len(rows))))
                    for split, rows in dataset.items()
                })

            config_destination = destination / (config_name or "default")
            config_destination.mkdir(parents=True, exist_ok=True)
            dataset.save_to_disk(str(config_destination / "dataset"))
            manifest = {
                "dataset_id": dataset_id,
                "config": config_name or "default",
                "revision": revision,
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "role": SOURCES[dataset_id]["role"],
                "rights_status": SOURCES[dataset_id]["rights"],
                "notes": SOURCES[dataset_id]["notes"],
                "parser_overrides": {
                    "format": SOURCES[dataset_id].get("format"),
                    "columns": SIFAL_COLUMNS if dataset_id == "Sifal/Kabyle-French" else None,
                    "header": None if dataset_id == "Sifal/Kabyle-French" else "dataset_default",
                },
                "splits": {split: len(rows) for split, rows in dataset.items()},
                "features": {split: str(rows.features) for split, rows in dataset.items()},
                "max_samples": args.max_samples or None,
                "training_approved": False,
            }
            (config_destination / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"staged {dataset_id}[{config_name or 'default'}]@{revision} -> {config_destination}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Inspect Hugging Face audio corpus metadata without exporting audio or text."""

from __future__ import annotations

import argparse
from collections import Counter

from datasets import load_dataset


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, help="Hugging Face dataset ID")
    parser.add_argument("--revision", required=True, help="Immutable commit SHA")
    parser.add_argument("--split", default="train")
    parser.add_argument("--license-field", default="Licence")
    parser.add_argument("--max-rows", type=int, default=0, help="0 means scan the full split")
    args = parser.parse_args()

    dataset = load_dataset(
        args.dataset,
        split=args.split,
        revision=args.revision,
        streaming=True,
    )
    counts: Counter[str] = Counter()
    inspected = 0

    for row in dataset:
        inspected += 1
        value = row.get(args.license_field)
        label = "<MISSING>" if value is None else str(value).strip()
        counts[label] += 1
        # Intentionally do not access row["audio"]: no decoding or audio export.
        if args.max_rows and inspected >= args.max_rows:
            break

    print(f"dataset={args.dataset}")
    print(f"revision={args.revision}")
    print(f"split={args.split}")
    print(f"rows_inspected={inspected}")
    print(f"license_field={args.license_field}")
    for label, count in sorted(counts.items()):
        print(f"{count}\t{label}")


if __name__ == "__main__":
    main()

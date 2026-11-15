# Open-source model release checklist

Do not publish model weights or adapters until every applicable item is checked.
A public dataset page or a general dataset license is not enough when the
underlying rows come from different source works.

## Data and rights

- [ ] Every training source is pinned to an immutable revision.
- [ ] Every row retains its source ID, exact license and attribution.
- [ ] Written permission or license evidence is stored in the private rights register.
- [ ] Training permission is confirmed separately from commercial-use permission.
- [ ] Model-weight distribution is explicitly permitted for every source lane.
- [ ] Share-alike obligations and attribution notices are resolved.
- [ ] No non-commercial, unknown, conflicting or quarantined source rows remain.
- [ ] ParaKab and other mixed-source collections have been checked at row level.

## Model and evaluation

- [ ] Base-model license permits the intended adapter/weight distribution.
- [ ] Native-speaker dev/test benchmark is frozen and has not leaked into training.
- [ ] Base model and adapted model are compared with identical prompts and decoding settings.
- [ ] Report everyday and literary register results separately.
- [ ] Report Kabyle↔French and Kabyle↔Arabic results separately.
- [ ] Native-speaker reviewers have checked naturalness, meaning, grammar, orthography and register.
- [ ] Known failure modes, dialect coverage and limitations are documented.

## Privacy and security

- [ ] No private conversations, personal identifiers, credentials or private source files are included.
- [ ] Memorization and extraction checks have been performed on sensitive or restricted source material.
- [ ] No raw corpus files, held-out benchmark answers or private predictions are included in the release repository.

## Reproducibility and packaging

- [ ] Record base-model revision, tokenizer revision, adapter configuration and training parameters.
- [ ] Include a model card with source families, licenses, intended use and limitations.
- [ ] Include required attribution and license notices.
- [ ] Verify the release rights gate:

      python scripts/check_release_rights.py path/to/training-manifest.json

- [ ] Obtain explicit project-owner approval before making the repository or weights public.

The automated gate is necessary but not sufficient. It checks the rights flags
recorded in the training manifest; it does not interpret licenses or replace
legal review and permission from rightsholders.

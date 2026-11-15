import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_dataset_schema_is_valid_json():
    schema = json.loads((ROOT / "data/schemas/example.schema.json").read_text(encoding="utf-8"))
    assert schema["title"] == "Kabyle AI dataset example"

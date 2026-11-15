# Native benchmark data boundary

This directory intentionally contains no real benchmark prompts or answers.
The actual held-out evaluation set must remain in an access-controlled private
location and must never be included in training or retrieval data.

Use the JSONL format and workflow in ../../docs/native-benchmark.md. The
validator accepts only dev and test splits. Keep test private and require every
record to be marked reviewed before freezing a benchmark.

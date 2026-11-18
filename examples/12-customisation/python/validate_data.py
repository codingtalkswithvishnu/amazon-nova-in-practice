"""Validate the teaching file locally; no training job is submitted."""

from pathlib import Path

from nova_book.training import read_records

path = Path(__file__).resolve().parents[1] / "training_example.jsonl"
print(f"Validated {len(read_records(path))} fictional conversation records.")

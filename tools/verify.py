"""Check source syntax, companion paths and fictional training fixtures locally."""

import ast
import json
from pathlib import Path

from nova_book.training import read_records

ROOT = Path(__file__).resolve().parents[1]
files = []
for folder in ["src", "examples", "tests", "tools"]:
    for path in (ROOT / folder).rglob("*.py"):
        ast.parse(path.read_text(), filename=str(path))
        files.append(path)
for item in json.loads((ROOT / "sample-map.json").read_text()):
    path = (ROOT / item["path"]).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise SystemExit(f"Missing or outside-root companion path: {item['path']}")
for path in [
    ROOT / "fixtures/synthetic_referral.pdf",
    ROOT / "fixtures/synthetic_form_photo.jpg",
]:
    if not path.is_file() or not path.stat().st_size:
        raise SystemExit(f"Missing fixture: {path.name}")
read_records(ROOT / "examples/12-customisation/training_example.jsonl")
print(f"Parsed {len(files)} Python files; mapped sources and fixtures exist.")

# Training preparation

training_example.jsonl contains three fictional teaching records in Nova's
conversation format. Validate it locally before adapting anything. Three rows do
not establish sufficient data, clinical labels or cloud training readiness.

Choose a supported model, method, region and serving route. Separate near-related
records before assigning training and holdout splits. Keep labels and source
provenance reviewed. No sample submits a training job or creates a paid endpoint.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [training_example.jsonl](training_example.jsonl) | Fictional fixture / reference input |

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.

Run `python examples/12-customisation/python/validate_data.py` from the repository root to validate the teaching records.

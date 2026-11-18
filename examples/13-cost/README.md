# Chapter 13 examples

Use the linked complete sources with the chapter explanation.

Run commands from the **repository root** after completing the root README setup.

| File | Command or purpose |
| --- | --- |
| [python/estimate.py](python/estimate.py) | `python examples/13-cost/python/estimate.py` |

Run `python examples/13-cost/python/estimate.py --input-price 0.035 --output-price 0.14`.
These are illustrative rates: expected daily model cost is Decimal("3.15"), monthly
Decimal("94.50") for a 30-day month. Replace the rates with current prices.

Local verification: `python -m unittest discover -s tests -v`. Passing checks do
not establish live account access or task quality on your data.

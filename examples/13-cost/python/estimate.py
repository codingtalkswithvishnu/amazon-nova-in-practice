"""Local calculation; rates supplied by the caller, no AWS request."""

import argparse

from nova_book.cost import estimate

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--input-price", required=True, help="USD per million input tokens")
parser.add_argument(
    "--output-price", required=True, help="USD per million output tokens"
)
args = parser.parse_args()
print(estimate(1000, 200, 50_000, args.input_price, args.output_price))

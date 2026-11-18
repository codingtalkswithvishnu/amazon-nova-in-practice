"""Decimal arithmetic with explicit per-million prices and calendar assumptions."""

from decimal import Decimal


def estimate(
    input_tokens, output_tokens, calls_per_day, input_price, output_price, *, days=30
):
    quantities = (input_tokens, output_tokens, calls_per_day, days)
    if any(type(v) is not int or v < 0 for v in quantities) or days < 1:
        raise ValueError("Token counts, calls and days must be non-negative integers")
    prices = [Decimal(str(input_price)), Decimal(str(output_price))]
    if any(not p.is_finite() or p < 0 for p in prices):
        raise ValueError("Prices must be finite and non-negative")
    input_daily = Decimal(input_tokens * calls_per_day) * prices[0] / 1_000_000
    output_daily = Decimal(output_tokens * calls_per_day) * prices[1] / 1_000_000
    return {
        "input_daily": input_daily,
        "output_daily": output_daily,
        "daily": input_daily + output_daily,
        "monthly": (input_daily + output_daily) * days,
        "days": days,
    }

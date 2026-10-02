from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AmountComparison:
    previous: Decimal | None
    current: Decimal
    delta: Decimal | None
    percentage_change: Decimal | None


def compare_amounts(previous: Decimal | None, current: Decimal) -> AmountComparison:
    """Compare compatible amounts without inventing a missing baseline."""
    if not current.is_finite() or current < 0:
        raise ValueError("Current amount must be finite and non-negative.")
    if previous is None:
        return AmountComparison(
            previous=None,
            current=current,
            delta=None,
            percentage_change=None,
        )
    if not previous.is_finite() or previous < 0:
        raise ValueError("Previous amount must be finite and non-negative.")

    delta = current - previous
    percentage_change = (
        delta / previous * Decimal("100")
        if previous != 0
        else None
    )
    return AmountComparison(
        previous=previous,
        current=current,
        delta=delta,
        percentage_change=percentage_change,
    )

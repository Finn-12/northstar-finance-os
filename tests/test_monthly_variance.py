import unittest
from decimal import Decimal

from src.forecasting.monthly_variance import compare_amounts


class CompareAmountsTests(unittest.TestCase):
    def test_calculates_increase_and_percentage(self) -> None:
        result = compare_amounts(Decimal("1000"), Decimal("1250"))

        self.assertEqual(result.delta, Decimal("250"))
        self.assertEqual(result.percentage_change, Decimal("25"))

    def test_calculates_decrease(self) -> None:
        result = compare_amounts(Decimal("1000"), Decimal("750"))

        self.assertEqual(result.delta, Decimal("-250"))
        self.assertEqual(result.percentage_change, Decimal("-25"))

    def test_missing_prior_value_has_no_variance(self) -> None:
        result = compare_amounts(None, Decimal("750"))

        self.assertIsNone(result.previous)
        self.assertIsNone(result.delta)
        self.assertIsNone(result.percentage_change)

    def test_zero_prior_value_has_delta_but_no_percentage(self) -> None:
        result = compare_amounts(Decimal("0"), Decimal("750"))

        self.assertEqual(result.delta, Decimal("750"))
        self.assertIsNone(result.percentage_change)

    def test_rejects_negative_amount(self) -> None:
        with self.assertRaises(ValueError):
            compare_amounts(Decimal("1000"), Decimal("-1"))

    def test_rejects_non_finite_amount(self) -> None:
        with self.assertRaises(ValueError):
            compare_amounts(Decimal("1000"), Decimal("Infinity"))


if __name__ == "__main__":
    unittest.main()

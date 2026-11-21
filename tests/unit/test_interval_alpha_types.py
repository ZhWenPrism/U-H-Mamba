from decimal import Decimal
import unittest

from u_h_mamba.evaluation import interval_metrics


class IntervalAlphaTypesTest(unittest.TestCase):
    def test_decimal_alpha_preserves_interval_scores(self):
        actual = interval_metrics([0, 4], [1, 2], [3, 3], alpha=Decimal("0.2"))
        expected = interval_metrics([0, 4], [1, 2], [3, 3], alpha=0.2)
        self.assertEqual(actual, expected)
        self.assertAlmostEqual(actual.interval_score, 11.5)

    def test_invalid_decimal_alpha_is_rejected(self):
        for alpha in map(Decimal, ("NaN", "Infinity", "0", "1")):
            with self.subTest(alpha=alpha):
                with self.assertRaises(ValueError):
                    interval_metrics([0], [0], [1], alpha=alpha)

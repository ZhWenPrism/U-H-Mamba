from decimal import Decimal
import unittest
from u_h_mamba.calibration.conformal import ConformalCalibrator


class CalibratorScalarTypesTest(unittest.TestCase):
    def test_decimal_correction_can_form_and_expand_float_intervals(self):
        calibrator = ConformalCalibrator(Decimal("0.25"), Decimal("2.5"), 3)
        self.assertEqual(calibrator.intervals([10, 20]), ((7.5, 17.5), (12.5, 22.5)))
        self.assertEqual(calibrator.expand([8, 18], [12, 22]), ((5.5, 15.5), (14.5, 24.5)))
        self.assertIsInstance(calibrator.alpha, float)
        self.assertIsInstance(calibrator.correction, float)

    def test_numeric_normalization_preserves_validation(self):
        for correction in ("-1", "NaN", "Infinity"):
            with self.subTest(correction=correction), self.assertRaises(ValueError):
                ConformalCalibrator(Decimal("0.25"), Decimal(correction), 3)

    def test_fitted_corrections_and_quantile_rank_are_preserved(self):
        fitted = ConformalCalibrator.fit([1, 2, 3], [0, 0, 0], alpha=0.25)
        self.assertEqual(fitted.correction, 3)
        self.assertEqual(fitted.calibration_size, 3)

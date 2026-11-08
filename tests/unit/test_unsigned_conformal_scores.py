import unittest

from u_h_mamba.calibration import ConformalCalibrator

try:
    import numpy as np
except ImportError:
    np = None


@unittest.skipIf(np is None, "NumPy is not installed")
class UnsignedConformalTest(unittest.TestCase):
    def test_point_scores_handle_prediction_on_either_side(self):
        with np.errstate(over="raise"):
            cal = ConformalCalibrator.fit(np.array([10, 20], dtype=np.uint8),
                                          np.array([12, 19], dtype=np.uint8), alpha=0.5)
        self.assertEqual(cal.correction, 2.0)
        self.assertEqual(cal.intervals([15]), ((13.0,), (17.0,)))

    def test_covered_values_require_no_interval_expansion(self):
        with np.errstate(over="raise"):
            cal = ConformalCalibrator.fit_existing_intervals(
                np.array([10], dtype=np.uint8), np.array([8], dtype=np.uint8),
                np.array([12], dtype=np.uint8), alpha=0.5,
            )
        self.assertEqual(cal.correction, 0.0)
        self.assertEqual(cal.expand([8], [12]), ((8.0,), (12.0,)))

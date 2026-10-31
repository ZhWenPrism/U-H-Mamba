import unittest

from u_h_mamba.calibration import ConformalCalibrator


class CalibrationSizeTests(unittest.TestCase):
    def test_sample_count_must_be_a_positive_integer(self):
        for size in (1.5, float("nan"), float("inf"), True, 0, -1):
            with self.subTest(size=size), self.assertRaises(ValueError):
                ConformalCalibrator(0.1, 2.0, size)

    def test_fitted_count_matches_calibration_samples(self):
        calibrator = ConformalCalibrator.fit([10.0, 20.0], [9.0, 18.0], alpha=0.5)
        self.assertEqual(calibrator.calibration_size, 2)
        self.assertEqual(calibrator.intervals([5.0]), ((3.0,), (7.0,)))

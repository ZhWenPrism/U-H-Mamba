import unittest

from u_h_mamba.evaluation.metrics import (
    end_of_life_error,
    interval_metrics,
    knee_point_error,
    regression_metrics,
)

try:
    import numpy as np
except ImportError:
    np = None


@unittest.skipIf(np is None, "NumPy is not installed")
class UnsignedCycleMetricsTest(unittest.TestCase):
    def test_point_and_timing_errors_match_python_numbers(self):
        with np.errstate(over="raise"):
            result = regression_metrics(np.array([10, 20], dtype=np.uint8),
                                        np.array([8, 21], dtype=np.uint8))
            self.assertEqual(end_of_life_error(np.uint8(20), np.uint8(17)), -3.0)
            self.assertEqual(knee_point_error(np.uint8(20), np.uint8(17)), 3.0)
        self.assertEqual(result, regression_metrics([10, 20], [8, 21]))

    def test_interval_widths_do_not_overflow_during_aggregation(self):
        actual = [100, 100, 100]
        lower = [0, 0, 0]
        upper = [200, 200, 200]
        with np.errstate(over="raise"):
            result = interval_metrics(*(np.array(x, dtype=np.uint8) for x in (actual, lower, upper)))
        self.assertEqual(result, interval_metrics(actual, lower, upper))

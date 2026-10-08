import unittest

from u_h_mamba.calibration import ConformalCalibrator
from u_h_mamba.datasets import BatterySequence, CycleObservation, SplitRole
from u_h_mamba.evaluation.metrics import (
    end_of_life_error,
    interval_metrics,
    knee_point_error,
    regression_metrics,
)


class SchemaTests(unittest.TestCase):
    def test_sequence_validates_width_and_order(self):
        sequence = BatterySequence(
            "cell-01",
            "NASA",
            SplitRole.TRAIN,
            ("voltage", "temperature"),
            (
                CycleObservation(0, (4.1, 25.0), 100.0),
                CycleObservation(1, (4.0, 25.2), 99.0),
            ),
        )
        self.assertEqual(sequence.observed_cycles, 2)
        self.assertEqual(sequence.target_coverage, 1.0)

    def test_duplicate_cycle_is_rejected(self):
        with self.assertRaises(ValueError):
            BatterySequence(
                "cell-01",
                "NASA",
                SplitRole.TRAIN,
                ("voltage",),
                (CycleObservation(0, (4.1,)), CycleObservation(0, (4.0,))),
            )


class MetricTests(unittest.TestCase):
    def test_regression_metrics_include_bias(self):
        metrics = regression_metrics([10.0, 20.0], [12.0, 18.0])
        self.assertAlmostEqual(metrics.mae, 2.0)
        self.assertAlmostEqual(metrics.rmse, 2.0)
        self.assertAlmostEqual(metrics.bias, 0.0)

    def test_interval_metrics_penalize_misses(self):
        metrics = interval_metrics([10.0, 20.0], [8.0, 18.0], [12.0, 19.0], alpha=0.1)
        self.assertAlmostEqual(metrics.coverage, 0.5)
        self.assertGreater(metrics.interval_score, metrics.mean_width)

    def test_timing_errors_preserve_semantics(self):
        self.assertEqual(end_of_life_error(100.0, 95.0), -5.0)
        self.assertEqual(knee_point_error(60.0, 65.0), 5.0)


class CalibrationTests(unittest.TestCase):
    def test_point_calibrator_uses_finite_sample_quantile(self):
        calibrator = ConformalCalibrator.fit([10.0, 20.0, 30.0], [9.0, 18.0, 33.0], alpha=0.2)
        self.assertEqual(calibrator.correction, 3.0)
        lower, upper = calibrator.intervals([50.0])
        self.assertEqual((lower, upper), ((47.0,), (53.0,)))

    def test_existing_intervals_are_expanded(self):
        calibrator = ConformalCalibrator.fit_existing_intervals(
            [10.0, 20.0], [9.0, 17.0], [11.0, 19.0], alpha=0.5
        )
        lower, upper = calibrator.expand([4.0], [6.0])
        self.assertEqual((lower, upper), ((3.0,), (7.0,)))


if __name__ == "__main__":
    unittest.main()

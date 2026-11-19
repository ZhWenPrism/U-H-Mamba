import unittest
from u_h_mamba.datasets import BatterySequence, CycleObservation, SplitRole


class FeatureColumnNamesTest(unittest.TestCase):
    def test_invalid_column_names_cannot_enter_a_sequence(self):
        for names in (("",), (" ",), (1,), ("voltage", " voltage ")):
            with self.subTest(names=names), self.assertRaisesRegex(ValueError, "column names"):
                BatterySequence("cell-01", "synthetic", SplitRole.TRAIN, names,
                                (CycleObservation(0, (1.,) * len(names)),))
    def test_valid_names_retain_order(self):
        sequence = BatterySequence("cell-01", "synthetic", SplitRole.TRAIN,
                                   ("voltage", "temperature"), (CycleObservation(0, (4., 25.)),))
        self.assertEqual(sequence.feature_names, ("voltage", "temperature"))

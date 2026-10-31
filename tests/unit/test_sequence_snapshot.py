import unittest

from u_h_mamba.datasets import BatterySequence, CycleObservation, SplitRole


class SequenceSnapshotTests(unittest.TestCase):
    def test_cycle_features_do_not_follow_caller_mutation(self):
        features = [4.1, 25.0]
        observation = CycleObservation(0, features, 10.0)
        features.clear()
        self.assertEqual(observation.features, (4.1, 25.0))

    def test_sequence_keeps_validated_width_order_and_targets(self):
        names = ["voltage"]
        observations = [CycleObservation(0, (4.1,), 10.0), CycleObservation(1, (4.0,), 9.0)]
        sequence = BatterySequence("cell-01", "NASA", SplitRole.TRAIN, names, observations)
        names.append("temperature")
        observations.clear()
        self.assertEqual(sequence.feature_names, ("voltage",))
        self.assertEqual(sequence.observed_cycles, 2)
        self.assertEqual(sequence.target_coverage, 1.0)

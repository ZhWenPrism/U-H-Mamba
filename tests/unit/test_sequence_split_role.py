import unittest

from u_h_mamba.datasets import BatterySequence, CycleObservation, SplitRole


class SequenceSplitRoleTest(unittest.TestCase):
    def test_sheet_or_json_split_names_use_the_declared_roles(self):
        rows = (CycleObservation(0, (4.0,)),)
        for split in SplitRole:
            record = BatterySequence("cell-01", "lab", split.value, ("voltage",), rows)
            self.assertIs(record.split, split)
        for split in ("val", "", None):
            with self.subTest(split=split), self.assertRaisesRegex(ValueError, "split must be"):
                BatterySequence("cell-01", "lab", split, ("voltage",), rows)

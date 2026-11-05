import unittest
from enum import IntEnum

from u_h_mamba.datasets import CycleObservation


class CycleIndicesTests(unittest.TestCase):
    def test_invalid_cycle_indices_are_rejected(self):
        for value in (-1, 0.5, 1.0, True, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "cycle_index"):
                CycleObservation(value, (4.,))

    def test_zero_and_integer_enums_remain_valid(self):
        class Cycle(IntEnum):
            FIRST = 0
        for value in (0, 1, Cycle.FIRST):
            self.assertEqual(CycleObservation(value, (4.,)).cycle_index, int(value))

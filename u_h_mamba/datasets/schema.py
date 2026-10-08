"""Validated, framework-independent battery sequence records."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite


class SplitRole(str, Enum):
    TRAIN = "train"
    VALIDATION = "validation"
    CALIBRATION = "calibration"
    TEST = "test"


@dataclass(frozen=True, slots=True)
class CycleObservation:
    cycle_index: int
    features: tuple[float, ...]
    rul_cycles: float | None = None

    def __post_init__(self) -> None:
        if self.cycle_index < 0:
            raise ValueError("cycle_index must be non-negative")
        if not self.features or any(not isfinite(value) for value in self.features):
            raise ValueError("features must be a non-empty finite vector")
        if self.rul_cycles is not None and (
            not isfinite(self.rul_cycles) or self.rul_cycles < 0
        ):
            raise ValueError("rul_cycles must be finite and non-negative")


@dataclass(frozen=True, slots=True)
class BatterySequence:
    unit_id: str
    domain: str
    split: SplitRole
    feature_names: tuple[str, ...]
    observations: tuple[CycleObservation, ...]

    def __post_init__(self) -> None:
        if not self.unit_id.strip() or any(ch.isspace() for ch in self.unit_id):
            raise ValueError("unit_id must be a non-empty token")
        if not self.domain.strip():
            raise ValueError("domain must not be empty")
        if not self.feature_names or len(set(self.feature_names)) != len(self.feature_names):
            raise ValueError("feature_names must be non-empty and unique")
        if not self.observations:
            raise ValueError("observations must not be empty")
        indices = [item.cycle_index for item in self.observations]
        if indices != sorted(indices) or len(set(indices)) != len(indices):
            raise ValueError("cycle indices must be strictly increasing")
        width = len(self.feature_names)
        if any(len(item.features) != width for item in self.observations):
            raise ValueError("every observation must match feature_names")

    @property
    def observed_cycles(self) -> int:
        return len(self.observations)

    @property
    def target_coverage(self) -> float:
        present = sum(item.rul_cycles is not None for item in self.observations)
        return present / len(self.observations)

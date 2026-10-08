"""Finite-sample split-conformal calibration for RUL intervals."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, isfinite
from typing import Iterable


def _finite(values: Iterable[float], name: str) -> tuple[float, ...]:
    result = tuple(values)
    if not result or any(not isfinite(value) for value in result):
        raise ValueError(f"{name} must contain finite values")
    return result


def _quantile_correction(scores: Iterable[float], alpha: float) -> float:
    values = sorted(_finite(scores, "nonconformity scores"))
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie between 0 and 1")
    rank = ceil((len(values) + 1) * (1 - alpha)) - 1
    return values[min(max(rank, 0), len(values) - 1)]


@dataclass(frozen=True, slots=True)
class ConformalCalibrator:
    alpha: float
    correction: float
    calibration_size: int

    def __post_init__(self) -> None:
        if not 0 < self.alpha < 1:
            raise ValueError("alpha must lie between 0 and 1")
        if not isfinite(self.correction) or self.correction < 0:
            raise ValueError("correction must be finite and non-negative")
        if self.calibration_size <= 0:
            raise ValueError("calibration_size must be positive")

    @classmethod
    def fit(
        cls,
        y_true: Iterable[float],
        point_predictions: Iterable[float],
        alpha: float = 0.05,
    ) -> "ConformalCalibrator":
        truth = _finite(y_true, "y_true")
        predictions = _finite(point_predictions, "point_predictions")
        if len(truth) != len(predictions):
            raise ValueError("calibration inputs must have equal length")
        scores = [abs(actual - predicted) for actual, predicted in zip(truth, predictions)]
        return cls(alpha, _quantile_correction(scores, alpha), len(scores))

    @classmethod
    def fit_existing_intervals(
        cls,
        y_true: Iterable[float],
        lower: Iterable[float],
        upper: Iterable[float],
        alpha: float = 0.05,
    ) -> "ConformalCalibrator":
        truth, lows, highs = _finite(y_true, "y_true"), _finite(lower, "lower"), _finite(upper, "upper")
        if not (len(truth) == len(lows) == len(highs)):
            raise ValueError("calibration inputs must have equal length")
        if any(low > high for low, high in zip(lows, highs)):
            raise ValueError("lower bounds must not exceed upper bounds")
        scores = [max(low - actual, actual - high, 0.0) for actual, low, high in zip(truth, lows, highs)]
        return cls(alpha, _quantile_correction(scores, alpha), len(scores))

    def intervals(self, predictions: Iterable[float]) -> tuple[tuple[float, ...], tuple[float, ...]]:
        values = _finite(predictions, "predictions")
        return (
            tuple(value - self.correction for value in values),
            tuple(value + self.correction for value in values),
        )

    def expand(
        self, lower: Iterable[float], upper: Iterable[float]
    ) -> tuple[tuple[float, ...], tuple[float, ...]]:
        lows, highs = _finite(lower, "lower"), _finite(upper, "upper")
        if len(lows) != len(highs) or any(low > high for low, high in zip(lows, highs)):
            raise ValueError("base intervals must be aligned and ordered")
        return (
            tuple(value - self.correction for value in lows),
            tuple(value + self.correction for value in highs),
        )

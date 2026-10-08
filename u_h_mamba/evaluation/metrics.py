"""Metrics for RUL accuracy, timing, and predictive intervals."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Iterable


def _values(items: Iterable[float], name: str) -> tuple[float, ...]:
    values = tuple(items)
    if not values or any(not isfinite(value) for value in values):
        raise ValueError(f"{name} must contain finite values")
    return values


def _paired(y_true: Iterable[float], y_pred: Iterable[float]) -> tuple[tuple[float, ...], tuple[float, ...]]:
    left = _values(y_true, "y_true")
    right = _values(y_pred, "y_pred")
    if len(left) != len(right):
        raise ValueError("y_true and y_pred must have equal length")
    return left, right


@dataclass(frozen=True, slots=True)
class RegressionMetrics:
    mae: float
    rmse: float
    mape: float
    bias: float


def regression_metrics(y_true: Iterable[float], y_pred: Iterable[float]) -> RegressionMetrics:
    left, right = _paired(y_true, y_pred)
    residuals = [predicted - actual for actual, predicted in zip(left, right)]
    nonzero = [(actual, predicted) for actual, predicted in zip(left, right) if actual != 0]
    mape = (
        sum(abs(predicted - actual) / abs(actual) for actual, predicted in nonzero) / len(nonzero)
        if nonzero
        else 0.0
    )
    return RegressionMetrics(
        mae=sum(abs(value) for value in residuals) / len(residuals),
        rmse=sqrt(sum(value * value for value in residuals) / len(residuals)),
        mape=mape,
        bias=sum(residuals) / len(residuals),
    )


@dataclass(frozen=True, slots=True)
class IntervalMetrics:
    coverage: float
    mean_width: float
    interval_score: float


def interval_metrics(
    y_true: Iterable[float],
    lower: Iterable[float],
    upper: Iterable[float],
    alpha: float = 0.05,
) -> IntervalMetrics:
    truth = _values(y_true, "y_true")
    lows = _values(lower, "lower")
    highs = _values(upper, "upper")
    if not (len(truth) == len(lows) == len(highs)):
        raise ValueError("interval inputs must have equal length")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if any(low > high for low, high in zip(lows, highs)):
        raise ValueError("lower bounds must not exceed upper bounds")
    covered = [low <= actual <= high for actual, low, high in zip(truth, lows, highs)]
    widths = [high - low for low, high in zip(lows, highs)]
    scores = []
    for actual, low, high, width in zip(truth, lows, highs, widths):
        penalty = 0.0
        if actual < low:
            penalty = 2 * (low - actual) / alpha
        elif actual > high:
            penalty = 2 * (actual - high) / alpha
        scores.append(width + penalty)
    return IntervalMetrics(sum(covered) / len(covered), sum(widths) / len(widths), sum(scores) / len(scores))


def end_of_life_error(observed_cycle: float, predicted_cycle: float) -> float:
    if not isfinite(observed_cycle) or not isfinite(predicted_cycle):
        raise ValueError("EOL cycles must be finite")
    return predicted_cycle - observed_cycle


def knee_point_error(observed_cycle: float, predicted_cycle: float) -> float:
    if not isfinite(observed_cycle) or not isfinite(predicted_cycle):
        raise ValueError("knee-point cycles must be finite")
    return abs(predicted_cycle - observed_cycle)

# Failure Analysis

U-H-Mamba failures include inaccurate RUL estimates and misleading uncertainty. Both dimensions require explicit review.

## Error taxonomy

| Failure class | Diagnostic view | Risk signal |
|:---|:---|:---|
| Early-life error | Error versus observed life fraction | Weak degradation signal |
| Late-life error | Absolute and signed RUL residual | Missed imminent EOL |
| Knee-point error | Predicted versus observed transition | Delayed regime change |
| Cross-domain shift | Residual by dataset and operating domain | Source-target mismatch |
| Under-coverage | Misses outside prediction interval | Overconfident uncertainty |
| Excess width | Interval width at fixed nominal coverage | Uninformative uncertainty |

## Required stratification

Report by dataset, laboratory or operational domain, chemistry where available, life stage, prediction horizon, and transfer regime. Unit-level summaries precede cycle-pooled values.

## Case review

For the largest signed errors and every interval miss, record unit, observation horizon, domain, signal availability, feature-quality flags, point residual, interval, calibration state, and nearest training-domain evidence.

## Corrective-action rule

Architecture, feature, adaptation, or recalibration changes must be tested on unchanged unit partitions. A wider interval is not accepted as a correction unless coverage and sharpness improve under a declared objective.

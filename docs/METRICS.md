# Evaluation Metrics

U-H-Mamba evaluates point prediction, degradation timing, uncertainty, transfer, and deployment cost as separate dimensions.

| Dimension | Metrics | Required context |
|:---|:---|:---|
| Remaining useful life | RMSE, MAE, MAPE | Dataset, prediction horizon, cycle unit |
| End of life | EOL error, relative EOL error | Failure threshold definition |
| Degradation transition | Knee-point error | Detection rule and tolerance |
| Interval reliability | Coverage probability, calibration error | Nominal coverage and calibration set |
| Interval sharpness | Mean prediction-interval width | Same scale as RUL |
| Probabilistic quality | Negative log-likelihood | Predictive distribution |
| Efficiency | Parameters, latency, memory | Hardware and batch size |

## Transfer protocol

Report **within-domain**, **zero-shot cross-domain**, and **target-adapted** results separately. For adaptation, state the target fraction, sampled batteries or vehicles, seed count, and whether the uncertainty layer was recalibrated.

## Calibration protocol

Calibration data must remain disjoint from final test units. Always pair coverage with interval width: high coverage alone can be achieved with uninformatively wide intervals. Report results by dataset and operating domain before pooling.

## Minimum result record

Record the battery-level split, feature profile, RUL/EOL definition, sequence window, checkpoint, calibration method, target-domain exposure, hardware, and uncertainty over repeated runs.

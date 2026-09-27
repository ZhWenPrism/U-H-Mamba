# Contributing

Contributions should improve reproducibility, uncertainty evaluation, or cross-domain battery-health modeling while respecting dataset licenses.

## Suitable contributions

- Dataset adapters and schemas that do not redistribute restricted benchmark files.
- Evaluation utilities for RUL, EOL, knee-point, calibration, and transfer metrics.
- Configuration, documentation, tests, and lightweight deployment interfaces.
- Corrections that keep repository claims aligned with the published article.

## Evaluation safeguards

- Split at battery or vehicle level; never distribute cycles from one unit across train and test sets.
- Identify each dataset, operating domain, prediction horizon, and target fine-tuning fraction.
- Report point accuracy and interval calibration together.
- Separate zero-shot transfer from target-domain adaptation and document all recalibration data.

## Pull requests

Use a focused branch and describe the data domain, affected component, validation protocol, and computational impact. Do not commit raw datasets, credentials, or large checkpoints.

# Documentation

Technical notes for the public U-H-Mamba research repository.

| Document | Purpose |
|:---|:---|
| [Data interface](DATA_INTERFACE.md) | Defines unit-level sequences, features, targets, and transfer domains |
| [Experiment record](EXPERIMENT_RECORD.md) | Captures model, transfer, calibration, and environment settings |
| [Evaluation metrics](METRICS.md) | Covers RUL, EOL, knee-point, calibration, sharpness, and efficiency |
| [Artifact manifest](ARTIFACT_MANIFEST.md) | Links licensed data revisions to models, calibration, and figures |
| [Failure analysis](FAILURE_ANALYSIS.md) | Reviews life-stage, domain-shift, and uncertainty failures |
| [Reproducibility scope](REPRODUCIBILITY.md) | States unit-level split rules and release boundaries |
| [Release checklist](RELEASE_CHECKLIST.md) | Verifies dataset licensing, calibration, transfer, and deployment evidence |

## Recommended order

Freeze unit-level partitions and feature definitions first, record each model and transfer configuration, fit calibration on its designated subset, evaluate accuracy and uncertainty together, then audit domain-specific failures.

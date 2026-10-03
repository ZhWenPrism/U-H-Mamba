# Experiment Record

Use one immutable record for every U-H-Mamba training, transfer, or calibration run.

## Identity

| Field | Value |
|:---|:---|
| Experiment ID |  |
| Git revision |  |
| Dataset revisions |  |
| Unit-level split hash |  |
| Feature-schema version |  |
| Random seeds |  |
| Hardware and software environment |  |

## Model and domain configuration

- Source and target domains:
- EOL definition and prediction horizon:
- Intra-cycle window and TCN configuration:
- Mamba depth, state size, and pressure-proxy version:
- MC Dropout sampling configuration:
- Conformal calibration subset and nominal coverage:
- Target-domain exposure and fine-tuning fraction:

## Evaluation record

Record RUL, EOL, knee-point, coverage, interval width, likelihood, and efficiency metrics by dataset. Keep within-domain, zero-shot, and adapted results in separate tables.

## Release gate

- [ ] Battery or vehicle units are disjoint across partitions.
- [ ] Calibration and test units do not overlap.
- [ ] Coverage is paired with interval width.
- [ ] Latency includes hardware, batch size, and repetition count.
- [ ] Raw or restricted datasets are absent from exported artifacts.

# Reproducibility scope

This repository currently provides the paper-level architecture, results, citation metadata, and a package scaffold for a future implementation release.

## Evaluation protocol

- Partition batteries or vehicles rather than individual cycles.
- Keep normalization statistics confined to each training split.
- Report early-, middle-, and late-life RUL performance separately.
- Evaluate point accuracy, EOL error, knee-point error, interval coverage, and interval width.

## Transfer protocol

- Distinguish zero-shot transfer from target-domain fine-tuning.
- Fit conformal calibration only on the designated calibration subset.
- Preserve laboratory and operational dataset identities in every result table.

## Determinism controls

Record seeds, dataset revisions, feature definitions, software versions, hardware, and the exact pressure-proxy construction used by each experiment.

## Release boundary

Raw datasets, derived private caches, model checkpoints, and experiment logs are intentionally excluded from version control.

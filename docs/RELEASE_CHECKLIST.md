# Release Checklist

Complete this checklist before publishing a U-H-Mamba result, model artifact, or implementation update.

## Evidence

- [ ] Dataset revisions, licenses, unit counts, and EOL definitions are recorded.
- [ ] Battery- or vehicle-level partitions are frozen and disjoint.
- [ ] Within-domain, zero-shot, and target-adapted results remain separate.
- [ ] Point accuracy, interval coverage, and interval width are reported together.
- [ ] Tables and figures resolve to model and calibration artifact IDs.

## Generalization review

- [ ] Calibration units do not overlap final test units.
- [ ] Target-domain exposure and fine-tuning fractions are disclosed.
- [ ] Early-, middle-, and late-life errors have been reviewed.
- [ ] Under-coverage and excessively wide intervals are documented.

## Repository quality

- [ ] Feature definitions, seeds, environment, hardware, and latency settings are recorded.
- [ ] Raw licensed datasets and private fleet telemetry are absent.
- [ ] Documentation and citation metadata match the released scope.
- [ ] Caches, checkpoints, logs, and credentials follow the declared access boundary.
- [ ] The tagged revision reproduces every public-safe result artifact.

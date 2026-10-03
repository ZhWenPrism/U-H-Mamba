# Data Interface

This specification separates licensed battery datasets from the future U-H-Mamba implementation. Raw benchmark and fleet records are not redistributed.

## Sequence record

| Field group | Required content |
|:---|:---|
| Unit identity | Stable `unit_id` for one battery or vehicle |
| Sequence index | Monotonic cycle index and observation timestamp where available |
| Signals | Charge, discharge, voltage, current, temperature, and source-defined traces |
| Derived inputs | Versioned physical and virtual features, including cumulative-energy and impedance proxies |
| Targets | RUL with an explicit EOL threshold and cycle unit |
| Domain metadata | Dataset, laboratory or operational domain, chemistry, and protocol |
| Provenance | Dataset revision, preprocessing profile, and feature-schema version |

## Split manifest

All cycles from one `unit_id` remain in one partition. Manifests distinguish `train`, `validation`, `calibration`, and `test`; transfer experiments additionally record source and target domains plus target-data fraction.

## Validation checks

- Cycle order is strictly increasing within each unit.
- RUL is non-negative and consistent with the declared EOL rule.
- Feature statistics are fitted on training units only.
- Missing channels and irregular sampling are represented explicitly.
- Calibration and test units do not overlap.

## Public boundary

Publish adapters, schemas, and synthetic fixtures only. Dataset archives, private fleet telemetry, derived caches, and checkpoints remain outside version control.

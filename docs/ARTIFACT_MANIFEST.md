# Artifact Manifest

Every U-H-Mamba result should retain a traceable chain from licensed source data to calibrated prediction.

| Artifact | Visibility | Required identity |
|:---|:---:|:---|
| Dataset inventory | Metadata only | Provider, release, license, unit count |
| Unit split manifest | Private | Unit IDs, role, source/target domain, hash |
| Feature cache | Private | Schema, preprocessing profile, source hash |
| Model checkpoint | Controlled | Config, seed, training split, weight hash |
| Calibration state | Controlled | Checkpoint, calibration units, nominal coverage |
| Prediction table | Public-safe | Unit role, horizon, checkpoint and calibration IDs |
| Metric table | Public-safe | Dataset, domain, metric implementation, uncertainty |
| Figure | Public | Source-table hash and rendering revision |

## Required metadata

Each record stores `artifact_id`, role, parent IDs, Git revision, configuration hash, content hash, creation time, dataset license class, and access class.

## Lineage rule

Point predictions and intervals must reference both the model checkpoint and, when used, the calibration state. Transfer results additionally reference the target-exposure manifest so zero-shot and adapted evaluations cannot be mixed.

## Integrity checks

- Split manifests contain disjoint battery or vehicle units.
- Calibration artifacts never reference test units.
- Dataset licenses permit the selected publication boundary.
- Replaced artifacts receive new IDs rather than silent updates.

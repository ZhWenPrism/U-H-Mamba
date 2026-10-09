<div align="center">

# U-H-Mamba

**Uncertainty-aware hierarchical state-space modeling for battery RUL prediction**

[![Paper](https://img.shields.io/badge/Paper-Energies_2026-0B7285?style=flat-square)](https://doi.org/10.3390/en19020414)
[![Open Access](https://img.shields.io/badge/Open_Access-CC_BY_4.0-2A9D8F?style=flat-square)](https://doi.org/10.3390/en19020414)
[![Complexity](https://img.shields.io/badge/Sequence-O(N)-7C3AED?style=flat-square)](#model-design)
[![Repository](https://img.shields.io/badge/Repository-public-2563EB?style=flat-square)](#codebase-blueprint)

<sub>146k+ cycles · physics-informed features · calibrated uncertainty · cross-domain transfer</sub>

</div>

U-H-Mamba separates fast intra-cycle electrochemical dynamics from slow inter-cycle degradation, producing accurate RUL estimates together with calibrated prediction intervals.

## At a glance

| Input | Hierarchy | Reliability layer | Deployment target |
|:---|:---|:---|:---|
| 25 physical and virtual features | Multi-scale TCN → pressure-aware Mamba | MC Dropout + inductive conformal prediction | Edge BMS and fleet analytics |

| Laboratory benchmarks | Operational datasets | Training scale | Model footprint |
|:---:|:---:|:---:|:---:|
| NASA · CALCE · Oxford | NDANEV · BatteryML | **146k+ cycles** | **1.3 M parameters** |

## Model design

1. **Physics-informed preprocessing** — measured signals are combined with cumulative-energy and virtual-impedance proxies.
2. **Intra-cycle encoder** — dilated temporal convolutions compress high-frequency charge–discharge traces into cycle fingerprints.
3. **Inter-cycle decoder** — pressure-aware multi-head Mamba models long-range degradation with linear sequence complexity.
4. **Hierarchical fusion** — local electrochemical patterns and lifetime-level state evolution are aligned in a shared latent space.
5. **Uncertainty calibration** — Monte Carlo Dropout estimates epistemic variation; conformal recalibration controls interval coverage under domain shift.
6. **Transfer and interpretation** — low-data adaptation and SHAP analysis test robustness across laboratory and real-world conditions.

## Architecture

<p align="center">
  <img src="assets/architecture.png" width="920" alt="U-H-Mamba architecture">
</p>

## Published results

| NASA average RMSE | NDANEV overall RMSE | Zero-shot lab → EV | 10% target fine-tuning |
|:---:|:---:|:---:|:---:|
| **3.7 ± 0.4 cycles** | **5.8 ± 0.6 cycles** | **6.4 ± 0.7 cycles** | **5.2 ± 0.5 cycles** |

| Overall coverage | Mean interval width | Inference latency | Parameters |
|:---:|:---:|:---:|:---:|
| **98.4 ± 0.8%** | **10.1 ± 1.1 cycles** | **0.09 s/sample** | **1.3 M** |

<p align="center">
  <img src="assets/results.png" width="920" alt="U-H-Mamba prediction and uncertainty results">
</p>

### Degradation and uncertainty

<table>
  <tr>
    <td width="50%"><img src="assets/degradation-analysis.png" alt="Battery degradation analysis"></td>
    <td width="50%"><img src="assets/rul-trajectories.png" alt="RUL prediction trajectories"></td>
  </tr>
  <tr>
    <td align="center"><sub>Degradation signatures</sub></td>
    <td align="center"><sub>RUL trajectories and error profiles</sub></td>
  </tr>
</table>

<p align="center">
  <img src="assets/uncertainty-quantification.png" width="900" alt="Calibrated uncertainty across four battery datasets">
</p>

### Interpretation

<table>
  <tr>
    <td width="50%"><img src="assets/global-shap.png" alt="Global SHAP summary"></td>
    <td width="50%"><img src="assets/local-shap.png" alt="Stage-specific local SHAP analysis"></td>
  </tr>
</table>

Published tables: [RUL performance](results/rul_performance.csv) · [uncertainty](results/uncertainty_quantification.csv) · [ablation](results/ablation.csv) · [transfer](results/cross_dataset_transfer.csv) · [data sensitivity](results/data_sensitivity.csv) · [efficiency](results/computational_efficiency.csv)

## Codebase blueprint

```text
U-H-Mamba/
├── assets/                         # architecture and published result figures
├── results/                        # machine-readable published tables
├── configs/
│   ├── data/                       # dataset-specific feature profiles
│   ├── model/                      # encoder, decoder, and UQ settings
│   └── experiment/                 # transfer and ablation protocols
├── data/
│   ├── raw/                        # local benchmark archives
│   ├── processed/                  # cycle-aligned feature tensors
│   └── splits/                     # battery- and vehicle-level manifests
├── u_h_mamba/
│   ├── datasets/                   # NASA, CALCE, Oxford, NDANEV adapters
│   ├── models/
│   │   ├── tcn_encoder/            # multi-scale intra-cycle encoder
│   │   ├── mamba_decoder/          # pressure-aware state-space decoder
│   │   ├── feature_fusion/         # hierarchical feature alignment
│   │   └── uncertainty/            # MC Dropout prediction heads
│   ├── calibration/                # inductive conformal calibration
│   ├── transfer/                   # zero-shot and low-data adaptation
│   ├── evaluation/                 # RUL, EOL, knee-point, UQ metrics
│   ├── interpretability/           # SHAP and degradation analysis
│   └── utils/                      # logging, seeds, checkpoints, IO
├── scripts/                        # future train/evaluate/infer entry points
├── tests/
│   ├── unit/
│   └── integration/
└── README.md
```

The repository now includes a dependency-light public utility layer for validated battery sequences, point and interval metrics, and finite-sample split-conformal calibration, with unit tests and CI. The trained hierarchical state-space model, checkpoints, and source datasets are not included in this release.

<details>
<summary><b>Citation</b></summary>

```bibtex
@article{wen2026uhmamba,
  title   = {U-H-Mamba: An Uncertainty-Aware Hierarchical State-Space Model for Lithium-Ion Battery Remaining Useful Life Prediction Using Hybrid Laboratory and Real-World Datasets},
  author  = {Wen, Zhihong and Liu, Xiangpeng and Niu, Wenshu and Zhang, Hui and Cheng, Yuhua},
  journal = {Energies},
  volume  = {19},
  number  = {2},
  pages   = {414},
  year    = {2026},
  doi     = {10.3390/en19020414}
}
```

</details>

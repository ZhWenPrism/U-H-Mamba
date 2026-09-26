<div align="center">

# U-H-Mamba

**Uncertainty-aware hierarchical state-space modeling for battery RUL prediction**

[![Paper](https://img.shields.io/badge/Paper-Energies_2026-0B7285?style=flat-square)](https://doi.org/10.3390/en19020414)
[![Open Access](https://img.shields.io/badge/Open_Access-CC_BY_4.0-2A9D8F?style=flat-square)](https://doi.org/10.3390/en19020414)
[![Code](https://img.shields.io/badge/Code-structure_only-6B7280?style=flat-square)](#repository-layout)

</div>

U-H-Mamba couples multi-scale temporal encoding, pressure-aware Mamba decoding, and calibrated uncertainty across laboratory and real-world EV data.

## Architecture

<p align="center">
  <img src="assets/architecture.png" width="900" alt="U-H-Mamba architecture">
</p>

## Results

| Training scale | NASA RMSE | NDANEV RMSE |
|:---:|:---:|:---:|
| **146k+ cycles** | **3.2 cycles** | **5.4 cycles** |

<p align="center">
  <img src="assets/results.png" width="900" alt="U-H-Mamba results">
</p>

## Repository layout

```text
U-H-Mamba/
├── assets/                 # architecture and result figures
├── configs/                # dataset and experiment settings
├── data/                   # hybrid battery data interfaces
├── models/
│   ├── tcn_encoder/        # intra-cycle feature encoder
│   ├── mamba_decoder/      # inter-cycle state-space decoder
│   └── uncertainty/        # MC dropout and conformal prediction
├── evaluation/             # RUL metrics and calibration
└── README.md
```

> Model implementation is not included in this release.

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

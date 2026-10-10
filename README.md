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

The framework is designed for the domain gap between controlled laboratory cycling and operational electric-vehicle data. It combines measured electrical signals with cumulative-energy, virtual-impedance, and pressure-aware descriptors, then evaluates whether the learned degradation representation transfers across cells, datasets, and operating regimes without losing uncertainty awareness.

Developed in collaboration with the **Institute of Microelectronics, Peking University**, the project treats battery prognostics as a hierarchical and reliability-sensitive sequence problem. A useful remaining-useful-life model must recognize local electrochemical changes within an individual cycle, accumulate evidence across a long degradation history, adapt to different operating regimes, and indicate when its estimate has become uncertain. U-H-Mamba addresses these requirements within one compact state-space framework.

## Research overview

Battery degradation is observed at several temporal resolutions. Voltage, current, temperature, and impedance evolve within each charge–discharge cycle, while capacity fade, resistance growth, and the approach to the degradation knee emerge over tens or hundreds of cycles. Flattening these signals into one undifferentiated sequence makes it difficult to preserve both local waveform structure and long-horizon state evolution. It also increases computational cost when the observation history becomes long.

U-H-Mamba decomposes the problem into an intra-cycle encoder and an inter-cycle state-space decoder. The first module learns compact cycle-level fingerprints from multiscale local dynamics. The second propagates these fingerprints through the battery lifetime using selective state-space updates with linear sequence complexity. Physics-informed descriptors provide cumulative context that may not be recoverable from a short waveform alone, while the uncertainty layer converts the final estimate into a point prediction accompanied by an empirical prediction interval.

The study is designed around three distinct questions. First, can the model estimate RUL accurately across multiple laboratory benchmarks? Second, can the representation transfer to operational electric-vehicle data whose usage patterns differ from controlled cycling? Third, do the reported uncertainty intervals respond to domain shift instead of remaining artificially narrow? These questions are evaluated separately through point-error metrics, cross-dataset transfer experiments, stage-specific trajectories, and conformal coverage analysis.

## At a glance

<table align="center">
  <tr align="center">
    <th>Input</th><th>Hierarchy</th><th>Reliability layer</th><th>Deployment target</th>
  </tr>
  <tr align="center">
    <td>25 physical and<br>virtual features</td>
    <td>Multi-scale TCN →<br>pressure-aware Mamba</td>
    <td>MC Dropout + inductive<br>conformal prediction</td>
    <td>Edge BMS and<br>fleet analytics</td>
  </tr>
</table>

<table align="center">
  <tr align="center">
    <th>Laboratory benchmarks</th><th>Operational datasets</th><th>Training scale</th><th>Model footprint</th>
  </tr>
  <tr align="center">
    <td>NASA · CALCE · Oxford</td><td>NDANEV · BatteryML</td><td><b>146k+ cycles</b></td><td><b>1.3 M parameters</b></td>
  </tr>
</table>

## Model design

1. **Physics-informed preprocessing** — measured signals are combined with cumulative-energy and virtual-impedance proxies.
2. **Intra-cycle encoder** — dilated temporal convolutions compress high-frequency charge–discharge traces into cycle fingerprints.
3. **Inter-cycle decoder** — pressure-aware multi-head Mamba models long-range degradation with linear sequence complexity.
4. **Hierarchical fusion** — local electrochemical patterns and lifetime-level state evolution are aligned in a shared latent space.
5. **Uncertainty calibration** — Monte Carlo Dropout estimates epistemic variation; conformal recalibration controls interval coverage under domain shift.
6. **Transfer and interpretation** — low-data adaptation and SHAP analysis test robustness across laboratory and real-world conditions.

## Problem formulation

### Hierarchical sequence construction

Each battery history is represented as an ordered collection of cycles rather than a single static record. Within a cycle, measurements describe short-range electrochemical behavior. Across cycles, derived health indicators describe the slower evolution of degradation. The data contract therefore preserves battery identity, cycle order, feature availability, observation cutoff, and the end-of-life definition used to construct the target.

This ordering is essential for leakage control. A prediction at cycle *t* may use only information available up to that cycle. Future capacity, future operating conditions, and statistics fitted with access to the complete lifetime must not enter the feature pipeline. Battery- or vehicle-level splitting is used to prevent later observations from the same physical unit appearing in both model development and evaluation.

### Physics-informed feature space

The model combines directly measured variables with derived indicators that summarize cumulative usage and electrochemical response. Voltage, current, temperature, state of charge, and impedance-related measurements describe the observed cycle. Cumulative-energy and mileage-like exposure variables encode how much work the battery has performed. Virtual-impedance and pressure-aware descriptors provide additional proxies for resistance growth, swelling-related behavior, and evolving internal condition.

These engineered variables are not treated as substitutes for the raw sequence. They provide complementary context to the learned representation. The convolutional encoder can detect local changes in the waveform, while cumulative descriptors anchor those changes within the lifetime of the cell or vehicle. The resulting feature space supports both short-horizon pattern recognition and long-range degradation tracking.

### Remaining-life target and observation stage

RUL is defined relative to a declared end-of-life criterion and the current observation cutoff. The same battery can therefore yield multiple supervised examples at different stages of degradation. Early-stage prediction is intrinsically more uncertain because the model has not yet observed the knee region; late-stage prediction has more direct evidence but may be more operationally urgent.

The repository reports stage-specific behavior rather than assuming constant difficulty across the lifetime. Early, middle, knee, and late views reveal whether a low aggregate RMSE is driven primarily by easier late-stage examples or whether the model remains informative when limited degradation history is available.

## Architecture

U-H-Mamba separates within-cycle signal encoding from across-cycle degradation modeling. A multi-scale TCN extracts local electrochemical fingerprints, the enhanced Mamba block propagates long-horizon state evolution, and the uncertainty head couples Monte Carlo dropout with conformal recalibration.

This hierarchy gives each module a specific role. Dilated temporal convolutions summarize local voltage, current, temperature, impedance, and state-of-charge behavior; the pressure-aware state-space decoder tracks the slower transition toward the degradation knee and end of life. The final probabilistic layer reports both an RUL estimate and a calibrated interval, so predictive confidence can widen when the operating domain becomes less familiar.

<p align="center">
  <img src="assets/architecture.png" alt="U-H-Mamba architecture"><br>
  <sub>Figure 2. Hierarchical architecture and uncertainty-calibration workflow.</sub>
</p>

### Multi-scale intra-cycle encoder

The temporal-convolutional encoder uses multiple receptive fields to summarize local patterns at different durations. Short filters capture abrupt changes and transient response; wider dilated filters capture slower variation across the charge–discharge profile. Their outputs are aligned into a cycle-level embedding that retains information about local dynamics without forcing the inter-cycle module to process every raw time point.

This separation is computationally and scientifically motivated. High-frequency measurements can be long and irregular, but the degradation model primarily needs a stable representation of how each cycle differs from the preceding history. Compressing the waveform at the cycle level reduces sequence length while preserving the local signals associated with emerging aging mechanisms.

### Pressure-aware selective state-space decoder

The inter-cycle decoder receives the ordered cycle embeddings together with physics-informed context. Selective state-space updates determine which parts of the current input should modify the latent degradation state and which information should be retained over long horizons. The pressure-aware pathway adds a structured signal for mechanical or swelling-related change when such information is available.

Unlike quadratic self-attention over the complete lifetime, the state-space formulation scales linearly with sequence length. This allows the model to process long histories without discarding early-cycle evidence. The multi-head design supports several complementary degradation trajectories, after which hierarchical fusion integrates the state-space output with the local cycle representation.

### Point estimation and calibrated intervals

The prediction head first produces an RUL estimate. Monte Carlo dropout is used at inference to sample variation associated with the learned model, providing an empirical estimate of epistemic uncertainty. These samples alone do not guarantee frequentist coverage, particularly when the target domain differs from the training data. Inductive conformal prediction therefore recalibrates residuals on a held-out calibration set and expands the interval by a finite-sample quantile.

The interval should be interpreted jointly with the point prediction. A narrow interval indicates that the case resembles patterns supported by the calibration distribution; a wider interval signals greater residual uncertainty. Coverage and interval width must be reported together, because very wide intervals can achieve high coverage without being operationally informative.

## Published results

<table align="center">
  <tr align="center">
    <th>NASA average RMSE</th><th>NDANEV overall RMSE</th><th>Zero-shot lab → EV</th><th>10% target fine-tuning</th>
  </tr>
  <tr align="center">
    <td><b>3.7 ± 0.4 cycles</b></td><td><b>5.8 ± 0.6 cycles</b></td><td><b>6.4 ± 0.7 cycles</b></td><td><b>5.2 ± 0.5 cycles</b></td>
  </tr>
</table>

<table align="center">
  <tr align="center">
    <th>Overall coverage</th><th>Mean interval width</th><th>Inference latency</th><th>Parameters</th>
  </tr>
  <tr align="center">
    <td><b>98.4 ± 0.8%</b></td><td><b>10.1 ± 1.1 cycles</b></td><td><b>0.09 s/sample</b></td><td><b>1.3 M</b></td>
  </tr>
</table>

The comparative evaluation places the proposed model against conventional sequence models across early, middle, and late degradation. The error landscape highlights the benefit of jointly modeling local cycle signatures, long-range state transitions, and calibrated uncertainty.

Across all datasets, U-H-Mamba achieved an average RMSE of 4.5 ± 0.5 cycles and an R² of 0.990 ± 0.003. Performance improved as more of the degradation trajectory became available, with NASA B0005 RMSE decreasing from 5.2 ± 0.6 cycles in the early phase to 2.2 ± 0.3 cycles in the late phase. On the operational NDANEV dataset, the overall RMSE remained 5.8 ± 0.6 cycles despite substantially greater environmental variability.

<p align="center">
  <img src="assets/results.png" alt="U-H-Mamba prediction and uncertainty results"><br>
  <sub>Figure 7. Comparative performance across degradation stages.</sub>
</p>

### Degradation representation

Capacity trajectories, smoothed derivatives, and error distributions reveal how degradation signatures change around the knee point. These signals motivate the separation of fast intra-cycle dynamics from slow lifetime evolution.

The figure also shows why a single global trend is insufficient: voltage and capacity evolve smoothly over long horizons, whereas derivative-based indicators respond sharply to local transitions and measurement noise. Multi-scale encoding allows the model to retain both behaviors, using short-range fingerprints to detect emerging change and long-range state dynamics to stabilize lifetime prediction.

<p align="center">
  <img src="assets/degradation-analysis.png" alt="Battery degradation analysis"><br>
  <sub>Figure 3. Degradation trajectories and smoothing-error analysis.</sub>
</p>

### RUL trajectories

The predicted RUL curve remains close to the observed lifetime trajectory while retaining stable error behavior near the nonlinear transition region. Error and relative-error panels make the temporal failure modes directly inspectable.

Most deviations remain within a narrow cycle-level range, and the average error decreases after the knee is identified. This behavior is important because delayed adaptation around the knee can inflate remaining-life estimates precisely when maintenance decisions become time-sensitive. The trajectory view therefore complements aggregate RMSE by showing when errors occur and whether they persist.

<p align="center">
  <img src="assets/rul-trajectories.png" alt="RUL prediction trajectories"><br>
  <sub>Figure 8. RUL prediction and error trajectories.</sub>
</p>

### Uncertainty calibration

Prediction intervals adapt to dataset-specific operating variability while maintaining high empirical coverage. Wider bands appear in noisier operational regimes, providing an explicit reliability signal instead of a point estimate alone.

Across the five evaluation settings, mean 95% coverage was 98.4 ± 0.8% with a mean interval width of 10.1 ± 1.1 cycles. Oxford Cell 1 produced the narrowest intervals, whereas NDANEV required wider bands to accommodate real-world operating variation. The calibration results indicate that the model becomes appropriately less confident under domain shift rather than expressing the same uncertainty everywhere.

<p align="center">
  <img src="assets/uncertainty-quantification.png" alt="Calibrated uncertainty across four battery datasets"><br>
  <sub>Figure 9. Calibrated prediction intervals across four datasets.</sub>
</p>

### Global interpretation

Global SHAP analysis ranks cumulative-energy, mileage, and impedance-related variables among the dominant contributors. The attribution pattern connects long-horizon usage exposure with measurable electrochemical degradation.

Cumulative energy and mileage carry the largest mean absolute contributions, followed by the real and imaginary components of impedance. This ordering is physically coherent with progressive throughput exposure, resistance growth, and loss of active lithium. Pressure-aware variables contribute additional information about swelling-related degradation, particularly when voltage and current profiles change across domains.

<p align="center">
  <img src="assets/global-shap.png" alt="Global SHAP summary"><br>
  <sub>Figure 10. Global feature attribution.</sub>
</p>

### Stage-specific interpretation

Local attribution views complement the global ranking by showing how feature influence changes between early, knee, and late degradation. This separates persistent drivers from stage-dependent effects.

The local panels show that identical feature values need not have the same effect throughout battery life. Usage accumulation dominates the long-horizon decline, while impedance, pressure proxies, and thermal variables become more influential around specific transition regions. This stage-dependent view helps distinguish a global correlate of aging from a feature that is informative only near a particular failure regime.

<p align="center">
  <img src="assets/local-shap.png" alt="Stage-specific local SHAP analysis"><br>
  <sub>Figure 11. Stage-specific SHAP analysis.</sub>
</p>

Published tables: [RUL performance](results/rul_performance.csv) · [uncertainty](results/uncertainty_quantification.csv) · [ablation](results/ablation.csv) · [transfer](results/cross_dataset_transfer.csv) · [data sensitivity](results/data_sensitivity.csv) · [efficiency](results/computational_efficiency.csv)

## Evaluation design

### Multi-domain benchmarks

The evaluation combines laboratory datasets with operational electric-vehicle records. NASA, CALCE, and Oxford provide controlled but heterogeneous cell-level benchmarks; NDANEV and BatteryML broaden the setting toward real-world usage patterns and larger operational variation. Dataset-specific preprocessing preserves the identity and sampling structure of each source before features are mapped into the shared model interface.

Point performance is summarized with RMSE, MAE, and coefficient of determination, but the primary interpretation remains dataset- and stage-aware. A model can achieve a favorable global average while failing on one battery, one degradation phase, or one deployment domain. The accompanying machine-readable tables therefore preserve the individual evaluation settings and do not rely on a single pooled number.

### Cross-domain transfer

Zero-shot transfer tests whether a model trained on laboratory data can be applied directly to operational EV sequences. Low-data adaptation then measures how much performance changes when a small fraction of target-domain data is made available. The reported zero-shot RMSE of 6.4 ± 0.7 cycles and 10% fine-tuning RMSE of 5.2 ± 0.5 cycles describe two different deployment assumptions and should not be compared as if they used the same information.

This transfer design isolates the practical value of the learned representation. If the hierarchy captures only dataset-specific correlations, performance should deteriorate sharply outside the source domain. If the representation encodes more portable degradation dynamics, a limited target-domain calibration set should recover performance without requiring complete retraining.

### Uncertainty and reliability

The reported mean coverage of 98.4 ± 0.8% is evaluated together with a mean interval width of 10.1 ± 1.1 cycles. Wider bands on operational data are expected because usage patterns, temperatures, loads, and measurement quality are less controlled than in laboratory cycling. The purpose of the interval is not to decorate a point prediction; it is to expose when the system has weaker support for a precise estimate.

Coverage alone does not establish calibration under every future fleet condition. Conformal guarantees depend on the exchangeability assumptions of the calibration setting, and severe domain shift can invalidate them. Any deployment-oriented evaluation should therefore repeat coverage, width, conditional coverage, and failure analysis on the target fleet rather than importing an interval calibrated elsewhere.

### Efficiency and deployment profile

The reported model contains approximately 1.3 million parameters and has an inference latency of 0.09 seconds per sample in the evaluated environment. These measurements support the feasibility of integration into edge-oriented battery-management or fleet-analysis workflows, but latency is hardware- and implementation-dependent. The repository reports it as an experimental characteristic, not a universal runtime guarantee.

## Interpreting the findings

The main contribution is the alignment of model structure with the physical hierarchy of degradation. Local waveform changes and long-term health evolution are not forced into the same operator. This makes it possible to reason about why the system benefits from both a multiscale temporal encoder and a selective state-space decoder, and why removing either component affects different parts of the prediction problem.

The results also separate predictive accuracy from predictive reliability. A low-RMSE model can still be unsafe if it reports the same confidence under familiar and unfamiliar conditions. By combining stochastic inference with conformal recalibration, U-H-Mamba provides a mechanism for increasing uncertainty when the operating domain becomes less familiar. The transfer and interval experiments therefore form part of the model contribution rather than a post hoc visualization.

SHAP analysis is used to inspect which variables support a prediction at global and stage-specific levels. Cumulative exposure, mileage, and impedance-related features rank highly across the reported analyses, while temperature, pressure proxies, and local electrochemical measurements vary in importance across degradation stages. These attributions describe model dependence, not causal mechanisms, and should be interpreted alongside domain knowledge and measurement quality.

## Scope and limitations

RUL depends on the chosen end-of-life definition, observation policy, feature availability, and operating environment. Results obtained for one threshold or cycling protocol do not automatically transfer to another. Operational datasets may contain maintenance interventions, missing intervals, changing sensor calibration, and usage patterns that are not represented in laboratory benchmarks.

The current public repository provides validated data contracts, evaluation metrics, conformal-calibration utilities, result tables, and the planned package structure. It does not include the complete trained architecture, model checkpoints, or redistributed copies of source datasets. Reproducing the published model therefore requires lawful access to the underlying data and a future release of the full training pipeline.

The framework is intended for research on battery prognostics and maintenance support. It does not by itself define a safety policy for vehicle operation, warranty decisions, or battery retirement. Such decisions require target-domain validation, cost-sensitive thresholds, monitoring for distribution shift, and integration with engineering safeguards outside the scope of the present study.

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

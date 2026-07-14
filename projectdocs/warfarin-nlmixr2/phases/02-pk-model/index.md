---
title: "Phase 2 — Structural Population PK Model"
phase: "02-pk-model"
status: in-progress
started: 2026-07-14
---

# Phase 2 — Structural Population PK Model

## Objective

Fit a 1-compartment oral absorption model to the warfarin PK data using SAEM estimation
in nlmixr2. Estimate IIV on CL, V, ka and proportional residual error. Assess convergence
and produce a parameter table with RSE%.

## Model specification

- **Structural:** 1-cpt, first-order absorption (ka), first-order elimination (CL, V)
- **IIV:** log-normal on CL, V, ka (eta ~ N(0, omega²))
- **RUV:** proportional error (sigma)
- **Estimator:** SAEM (stochastic approximation EM), 200 burn-in + 300 EM iterations
- **Initial estimates:** CL=0.13 L/h, V=7 L, ka=1.15 h⁻¹ (from literature / EDA Tmax)

## Plankton foton (pre-registered)

```
F_pk_saem (pre-registered):
  inputs:
    - warfarin dataset: nlmixr2data v2.0.10
      (content-address proxy: same as F_eda — nca_summary.csv artifact 71ba3f0b)
  protocol:
    kind: "nlmixr2-saem"
    ref:  pk_model_warfarin.R (to be recorded on completion)
    env:  { image: rocker/r2u:24.04, R: 4.6.1, nlmixr2: 5.0.0, rxode2: 5.1.2 }
    executor: ssh:pmx-docker
  outputs (expected):
    - fit_pk_summary.txt   — parameter table (THETA, OMEGA, SIGMA + RSE%)
    - fit_pk_plots.pdf     — GOF plots (DV vs PRED, DV vs IPRED, CWRES vs time)
    - fit_pk_plots.png     — same, raster
    - fit_pk_params.csv    — machine-readable parameter table
  plankton notes: SAEM is stochastic → outputs not byte-identical across runs.
                  Qualification requires L2 tolerance comparison (per ADR-001).
                  rxode2 JIT-compiles ODE to C++ at runtime — pinned by rxode2 version.
```

## Actual foton record (run 2026-07-14)

```
F_pk_saem (completed):
  inputs:
    - warfarin dataset: nlmixr2data v2.0.10
      (same content-address proxy as F_eda)
  protocol:
    kind: "nlmixr2-saem"
    ref:  pk_model_warfarin.R (Claude Science session 1e69227b)
    env:  { image: rocker/r2u:24.04, R: 4.6.1, nlmixr2: 5.0.0, rxode2: 5.1.2 }
    executor: ssh:pmx-docker (job 5c326d67)
    saem_control: { nBurn: 200, nEm: 300 }
  outputs:
    - fit_pk_summary.txt  → artifact 63a9a00e (v6a9ec84f)  903 B
    - fit_pk_params.csv   → artifact 6d39100e (v704cb377)  321 B
    - fit_pk_plots.pdf    → artifact df1a2218 (v16dfbb22)   73 KB
    - fit_pk_plots.png    → artifact a81cfa28 (v49fd2ebc)  642 KB
    - fit_pk_indplots.pdf → artifact 91ebc179 (v1e3348db)   34 KB
    - fit_pk_indplots.png → artifact 4fff92ca (vf88ad43b)  126 KB
  status: PASS (exit 0) — 2026-07-14
  plankton notes: L2 reproduction identity applies — SAEM is stochastic.
                  CL/V well-identified; ka poorly identified (η-shrinkage 48%,
                  %RSE 54%) — known warfarin absorption challenge.
```

## Key results

| Parameter | Estimate | %RSE | BSV CV% | η-shrinkage |
|-----------|----------|------|---------|-------------|
| CL (L/h) | 0.133 | 2.4% | 26.7% | 3.3% ✓ |
| V (L) | 8.08 | 2.1% | 19.4% | 21.1% = |
| ka (h⁻¹) | 0.648 | 53.9% | 71.0% | 48.2% ⚠ |
| prop. error | 0.225 | — | — | — |

OFV: 489.0 | AIC: 964.3 | BIC: 989.0

## Forward to Phase 3

- ka poorly identified → consider fixing to literature value or collapsing IIV on ka
- Weight covariate on CL and V (allometric scaling) — motivated by Phase 1 EDA
- PD turnover model linking Cp to PCA inhibition


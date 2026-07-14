---
title: "Phase 1 — Exploratory Data Analysis"
phase: "01-eda"
status: complete
started: 2026-07-14
completed: 2026-07-14
---

# Phase 1 — Exploratory Data Analysis

## Objective

Characterise the warfarin dataset before modeling: data structure, subject demographics,
PK/PD profile shapes, covariate distributions, and data quality.

## Plankton foton

```
F_eda:
  inputs:   [ warfarin_dataset (nlmixr2data v2.0.10) ]
  protocol: { kind: "r-eda",
              ref:  sha256(eda_warfarin.R + environment),
              env:  { image: rocker/r2u:24.04, R: 4.6.1, nlmixr2data: 2.0.10 } }
  outputs:  [ eda_plots.pdf, nca_summary.csv, demographics.csv ]
```

## Actual foton record (run 2026-07-14)

```
F_eda (completed):
  inputs:
    - warfarin dataset: nlmixr2data v2.0.10
      (content-address proxy: artifact id 71ba3f0b / nca_summary.csv checksum 0d6dab23)
  protocol:
    kind: "r-eda"
    ref:  eda_warfarin.R (Claude Science artifact, session 1e69227b)
    env:  { image: rocker/r2u:24.04, R: 4.6.1, nlmixr2data: 2.0.10,
            ggplot2: 4.0.3, patchwork: latest }
    executor: ssh:pmx-docker (/home/pmx/work, job 99b516c9)
  outputs:
    - eda_plots.pdf   → artifact d6ea3085 (v511334a2)  32 KB
    - eda_plots.png   → artifact 9263a7bb (vf685f396)  967 KB
    - nca_summary.csv → artifact 71ba3f0b (v1dde34a6)  519 B
    - demographics.csv→ artifact b53b2ed9 (vad9d8960)  568 B
  status: PASS (exit 0)
```

> **Plankton note (ADR-002):** In a live plankton registry this foton would be recorded by its
> action key `sha256(canonical(inputs) + protocol)`. Claude Science artifact version IDs
> serve the same content-addressing role here — each output is immutable and hash-verified.
> The Docker image digest (`rocker/r2u:24.04@sha256:...`) would be the pinned Environment
> in the protocol, providing the tool-qualification anchor.

## Key EDA findings

| Metric | Value |
|--------|-------|
| Subjects | 32 |
| WT (kg) | 70 ± 12.7, range 40–102 |
| AGE (yr) | 31 ± 10.5, range 21–63 |
| Cmax (mg/L) | 10.72 ± 2.73 |
| Tmax (h) | 16.9 ± 8.9 |
| AUC (mg/L·h) | 528.5 ± 136.7 |

Weight-tertile plot shows higher-weight subjects have higher Cmax (Low WT mean 10.34, Mid 10.40, High 11.50 mg/L) — a positive weight-exposure relationship consistent with larger volume of distribution in heavier subjects. Allometric weight scaling on V (and CL) warranted in Phase 2.

## Verification foton (ADR-002)

```
F_eda_verify (completed):
  inputs:
    - nca_summary.csv  → artifact 71ba3f0b (v1dde34a6)
    - demographics.csv → artifact b53b2ed9 (vad9d8960)
  protocol:
    kind: "python-verify"
    ref:  pandas merge + np.quantile tertile cut (Claude Science kernel, session 1e69227b)
    env:  { python: 3.11, pandas: <2, numpy: latest }
    executor: Claude Science sandbox (local kernel)
  outputs:
    - Cmax by tertile: Low=10.34, Mid=10.40, High=11.50 mg/L (computed inline, no artifact)
  status: PASS — 2026-07-14
  plankton notes: Corrected earlier reversed claim. This is a lineage-only foton
                  (no output artifact, result embedded in docs). Demonstrates that
                  even verification/correction steps are traceable as fotons.
```

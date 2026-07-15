---
title: "Phase 3 — Covariate Analysis + PD Turnover Model"
phase: "03-covariate-pd"
status: in-progress
started: 2026-07-15
---

# Phase 3 — Covariate Analysis + PD Turnover Model

## Objective

Two steps:
1. **Covariate step**: add allometric weight scaling on CL (exponent 0.75) and V
   (exponent 1.0), compare OFV vs base model (ΔOFV > 3.84 = p<0.05, 1 df per parameter)
2. **PD turnover model**: Kin/Kout indirect response model; warfarin inhibits Kin
   (Imax model), simultaneous PK-PD fit

## Plankton fotons (pre-registered)

```
F_pk_cov (pre-registered):
  inputs:   [ warfarin dataset (nlmixr2data v2.0.10) ]
  protocol: { kind: "nlmixr2-saem",
              ref:  pk_cov_model_warfarin.R,
              env:  { image: rocker/r2u:24.04, R: 4.6.1, nlmixr2: 5.0.0 } }
  outputs:  [ fit_pk_cov_summary.txt, fit_pk_cov_params.csv,
              fit_pk_cov_plots.pdf, fit_pk_cov_plots.png ]

F_pkpd (pre-registered):
  inputs:   [ warfarin dataset (nlmixr2data v2.0.10) ]
  protocol: { kind: "nlmixr2-saem",
              ref:  pkpd_model_warfarin.R,
              env:  { image: rocker/r2u:24.04, R: 4.6.1, nlmixr2: 5.0.0 } }
  outputs:  [ fit_pkpd_summary.txt, fit_pkpd_params.csv,
              fit_pkpd_plots.pdf, fit_pkpd_plots.png ]
```

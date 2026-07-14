---
title: "warfarin-nlmixr2"
created: 2026-07-14
tags: [pharmacometrics, nlmixr2, warfarin, pkpd, plankton]
---

# Warfarin PK-PD — nlmixr2 Demonstration Workflow

## Vision

A complete, reproducible pharmacometric modeling workflow using the `nlmixr2` warfarin
dataset as the canonical demo — replacing the classic remifentanil/theophylline examples
with the modern open-source R toolchain. Every step is executed on a dedicated Docker
container (`pmx-nlmixr2`, rocker/r2u base) via Claude Science's SSH compute dispatch.

The workflow also serves as a **concrete plankton use-case**: each modeling step maps
directly to plankton's File/Foton/Protocol/Registry model, making it a living counterpart
to Michi's `walkthrough-warfarin.md` (NONMEM/DDMoRe perspective) — this time from the
nlmixr2/open-source side.

## Goals

1. Run a full population PK-PD analysis (EDA → structural model → IIV/RUV → covariates
   → PD → diagnostics → VPC → simulation) on the warfarin dataset
2. Produce publication-quality figures and a structured results report
3. Map each analysis step explicitly to plankton concepts (File, Foton, Protocol, Registry)
4. Establish a reusable template for future pharmacometric analyses

## Dataset

**warfarin** from `nlmixr2data` (v2.0.10):
- 32 subjects, oral dosing, single-dose PK + PD
- Endpoints: plasma concentration (PK) + prothrombin complex activity / PCA (PD)
- Covariates: weight (WT), age (AGE), sex (SEX)
- Reference: Holford (1986), re-analyzed as DDMoRe UseCase1

## Tech Stack

| Technology | Purpose |
|---|---|
| nlmixr2 5.0.0 | SAEM/FOCEI population PK-PD estimation |
| rxode2 5.1.2 | ODE model definition + forward simulation |
| xpose.nlmixr2 0.4.2 | GOF diagnostics |
| vpc 1.2.4 | Visual predictive checks |
| ggplot2 4.0.3 / patchwork | Publication-quality figures |
| rocker/r2u Docker | Reproducible compute environment |
| Claude Science | Orchestration, lineage, dispatch |

## Plankton Mapping

Each modeling step = one **foton**: `inputs + protocol → outputs`.
The Docker image digest is the **Environment** in each protocol.
See `decisions/adr-001-plankton-mapping-approach.md`.

## In Scope

- Full EDA → fit → diagnostics → VPC → simulation pipeline
- Plankton conceptual mapping per step
- Claude Science lineage vs plankton registry comparison

## Out of Scope

- Actual plankton registry implementation
- Regulatory submission documentation
- NONMEM comparison runs

## Team

- Wolfgang Schwarzenbrunner — analysis lead
- Claude Science — orchestration, code generation, compute dispatch

## Progress

See [progress.md](./progress.md)

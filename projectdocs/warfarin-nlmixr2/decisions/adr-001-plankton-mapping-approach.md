---
title: "ADR-001: Plankton mapping approach for nlmixr2 workflow"
date: 2026-07-14
status: accepted
---

# ADR-001: How to map the nlmixr2 warfarin workflow to plankton

## Context

Michi's `walkthrough-warfarin.md` maps the DDMoRe/NONMEM warfarin entry to plankton's
File/Foton/Protocol model. This workflow uses nlmixr2 instead. We document the mapping
conceptually without implementing an actual registry.

## Decision

Document the plankton mapping alongside each phase:
- Each R script dispatch → one foton definition (inputs, protocol, outputs)
- Docker image digest (`rocker/r2u:24.04@sha256:...`) = Environment in the protocol
- Claude Science artifact version_ids ≈ plankton FileRef hashes (content-addressed)
- Claude Science lineage graph ≈ plankton registry (same DAG, different wire format)

Phase 5 will compare Claude Science's native lineage with what a plankton registry
would look like for this same workflow.

## Consequences

- No plankton implementation needed — conceptual mapping is sufficient
- Creates an nlmixr2-side counterpart to Michi's NONMEM walkthrough
- Demonstrates plankton's tool-neutrality (same substrate for NONMEM and nlmixr2)

## Open questions

- rxode2 JIT-compiles ODE models to C++ at runtime — does this count as part of the
  protocol environment? Likely yes, pinned by rxode2 version.
- nlmixr2 SAEM is stochastic → L2 tolerance comparison needed, same as NONMEM.

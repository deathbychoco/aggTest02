---
title: "ADR-002: Plankton foton record required after every data access or change"
date: 2026-07-14
status: accepted
---

# ADR-002: Plankton-always policy

## Context

ADR-001 established the conceptual mapping approach. After Phase 1 EDA, it became clear
that the mapping is only meaningful if it is applied consistently and immediately — not
as a retrospective summary. A foton recorded after the fact from memory is less trustworthy
than one recorded at the moment of execution with real artifact IDs.

## Decision

**Every phase index.md must contain a completed foton record before that phase is
considered done.** Specifically:

1. **Before dispatch** — write the foton *definition* (inputs, protocol kind, expected outputs)
   in the phase `index.md` as a pre-registration.
2. **After dispatch, immediately on success** — update the record with:
   - Actual artifact version IDs for every output (the content-address proxy)
   - Job ID and executor (ssh:pmx-docker / job UUID)
   - Exit status and date
   - Any plankton-specific notes (completeness level, reproduction identity observations)
3. **Any intermediate data access or transformation** (e.g. a correction to results,
   a re-run, a verification computation) also gets a foton entry — either as an update
   to the existing phase record or as a new named foton (e.g. `F_eda_verify`).

## Foton record template

```
F_<name> (status: pre-registered | completed | failed):
  inputs:
    - <description>: <package/source> v<version>
      (content-address proxy: artifact id <short-id> / checksum <short-hash>)
  protocol:
    kind: "<r-eda | nlmixr2-saem | xpose-gof | nlmixr2-vpc | rxode2-sim | r-verify>"
    ref:  <script filename> (Claude Science artifact, session <frame-id-prefix>)
    env:  { image: rocker/r2u:24.04, R: <version>, <key packages and versions> }
    executor: ssh:pmx-docker (job <job-uuid>)
  outputs:
    - <filename> → artifact <artifact-id> (v<version-id>)  <size>
  status: PASS/FAIL (exit <code>) — <date>
  plankton notes: <completeness level, reproduction identity observations, open findings>
```

## Rationale

- Keeps the project docs as a faithful, auditable trace of what actually ran
- Makes the plankton mapping concrete rather than theoretical
- Directly comparable to Michi's `walkthrough-warfarin.md` — same foton structure,
  different toolchain
- Any future plankton registry ingest could use these records directly

## Consequences

- Small overhead per phase (2–3 min to update the record)
- Claude Science will update `index.md` immediately after each successful job
- If a job fails, the foton record is marked FAIL with the error — not deleted
- Verification/correction runs (like the Cmax-by-tertile check in Phase 1) are
  recorded as `F_<phase>_verify` fotons in the same index.md

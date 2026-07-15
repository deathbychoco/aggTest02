# MCP E2E Acceptance Test — improve-api
**Date:** 2026-07-13
**Server:** `http://envhost1.hc.scintecodev.internal:4210/repository/api/v1`, Version `4.4.1-16`
**User:** admin (Administrator)
**Workspace:** `/_MCP_Integration/e2e-run` (deleted after the run)
**Result: 48 / 48 PASS, 0 FAIL.** All six Guard steps (9, 17, 22, 27, 41, 47) correctly rejected or redacted data—no Guard slipped through. Both NONMEM runs actually completed their calculations (`MINIMIZATION SUCCESSFUL`, OFV 2085.993).
## Results Table
| # | Tool | Expected | Observed | Status |
|---|---|---|---|---|
| 1 | (Instructions) | Doctrine delivered in advance | 9 rules including Ownership/Branching + “rerun to fix, branch to progress” | PASS |
| 2 | `improve://authoring-guide` | same text | identical, plus PRECEDENCE paragraph | PASS |
| 3 | get_server_info | baseUrl + Version | envhost1:4210, 4.4.1-16 | PASS |
| 4 | get_current_user | loggedIn + Username | `true`, admin (Administrator) | PASS |
| 5 | list_children | Success | 3 children | PASS |
| 6 | create_folder | Folder | `/…/e2e-run` | PASS |
| 7 | create_tree | Analysis Tree | `…/e2e-run/wf` | PASS |
| 8 | create_step | Server Name + both fields | `Step 1`, rationale + description saved | PASS |
| 9 | create_step (`name`) | **Refusal** | Error: “Steps are named by the server…”; no step created | **PASS (Guard)** |
| 10 | upload_file | committed file | note.txt, 6 bytes | PASS |
| 11 | read_resource | `hello\n` | `hello\n` | PASS |
| 12 | get_revisions | ≥ 1 revision | 2 | PASS |
| 13 | get_metadata | Success | `metadata: []` | PASS |
| 14 | search_resources | Usable paths | 237 hits with full paths | PASS |
| 15 | checkout | Lock | `locked: true` | PASS |
| 16 | edit_content | `replacements: 1` | 1 | PASS |
| 17 | edit_content (`zzz`) | **Refusal** | “`find` text not found… Nothing was changed.” | **PASS (Guard)** |
| 18 | read_resource (workingCopy) | `hello world\n` | `hello world\n` | PASS |
| 19 | commit | committed + unlocked | both `true` | PASS |
| 20 | describe_step | rationale/description/owner, `isOwnedByYou`, no note | all present, `isOwnedByYou: true`, no ownership note | PASS |
| 21 | set_documentation (rationale only) | description unchanged | rationale new, description still “NONMEM base run” | PASS |
| 22 | set_documentation (empty) | **Refusal** | “there is nothing to set” | **PASS (Guard)** |
| 23 | set_step_tool | `toolChanged` + 2 inputs | `true`, command file + dataset | PASS |
| 24 | set_step_input (copy) | Copy to StepA | `copied: true`, `…/Step 1/base.ctl` | PASS |
| 25 | get_copy_ancestry | Back to `/robert/lib/base.ctl` | First ancestor = exactly this file (plus older chain) | PASS |
| 26 | set_step_input (dataset) | Link, no copy | `linked: true` → `/robert/lib/concentrations.dat`, no `copied` | PASS |
| 27 | set_step_input (no name) | **Refusal** | “Pass `name`, or asCommandFile: true” | **PASS (Guard)** |
| 28 | describe_step | both fileRefs resolved | valuePath for command-file + dataset | PASS |
| 29 | clear + set | empty, then set again | `cleared: dataset`, then linked again | PASS |
| 30 | run_step_and_wait | FINISHED / succeeded | FINISHED, OK, 63 s | PASS |
| 31 | list_step_outputs | ≥ 1, including `STEP*.lst` | 25 outputs, including `STEP1.lst` | PASS |
| 32 | get_run_output | Command + terminal status | `nmfe74 base.ctl STEP1.lst`, FINISHED | PASS |
| 33 | read STEP1.lst | `MINIMIZATION SUCCESSFUL` | present, OFV 2085.993 | PASS |
| 34 | create_step (Branch) | inheritedTool + Note + Server name | `inheritedTool: true`, Copy Note, `Step 2` | PASS |
| 35 | describe_step StepB | Tool + both inputs inherited, own copies | nonmem_7.4-lsf, `…/Step 2/base.ctl` + `…/Step 2/concentrations.dat` | PASS |
| 36 | get_step_tree | children + tree with parent links | Step 2 as a child, tree with `parentStepId` | PASS |
| 37 | run (resetInventory) | FINISHED + MIN. SUCCESSFUL | FINISHED, 50 s, STEP2.lst contains it | PASS |
| 38 | call_endpoint references | Link | `nodeType: Link` → STEP1.lst, Parent = Step 3 | PASS |
| 39 | get_dependencies StepC | exactly StepA | count 1, Step 1 | PASS |
| 40 | get_usages StepA | StepC | count 1, Step 3 | PASS |
| 41 | get_dependencies (File) | **Refusal** | “is a File, not a Step” | **PASS (Guard)** |
| 42 | call_endpoint copy | Copy in the tree | `/…/wf/note.txt` | PASS |
| 43 | get_copy_descendants | the copy | count 1 | PASS |
| 44 | get_copy_ancestry | Original **exactly once** | count 1, no duplicates | PASS |
| 45 | search_endpoints | `/resources/{id}/usages` | Top match | PASS |
| 46 | describe_endpoint | Signature | Params, Query, 200 response | PASS |
| 47 | call_endpoint GET | 200 + `authorization: <redacted>` | Both confirmed | **PASS (Guard)** |
| 48 | delete_resource | `deleted: true` + gone | `true`; container completely removed | PASS |
## Observations (no FAIL)
**Step 26 — A link’s `valuePath` points to the step.** The server correctly reports `linked: true` with `linkedTo: /robert/lib/concentrations.dat`, but the input’s `valuePath` points to `/…/Step 1/concentrations.dat`. This is the link node in the step (`nodeType: Link`, as also shown in `list_step_outputs`), not a copy. Semantically, therefore, it is a true link; anyone looking only at `valuePath` might mistake it for a copy.
**Step 25 — Ancestry returns the entire chain.** For the copy of `/robert/lib/base.ctl`, four entries are returned: the immediate original plus its own history from `/robertWFTests`. This is a chain, not a duplicate bloat—in the case of the newly created copy in step 44, the original appeared exactly once, as required.




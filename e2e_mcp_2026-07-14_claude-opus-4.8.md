# improve MCP — End-to-End Acceptance Test Report

- **Date:** 2026-07-14
- **Model:** OpenCode Zen / Claude Opus 4.8
- **Server:** `http://envhost1.hc.scintecodev.internal:4210/repository/api/v1` — version **4.4.1-16**
- **User:** `admin` (Administrator), `loggedIn: true`
- **Working area:** `/_MCP_Integration/e2e-run`

## Result: 48 / 48 PASS — 0 FAIL

All six guard steps (9, 17, 22, 27, 41, 47) refused exactly as required. No guard succeeded where it must refuse.

## Pass/Fail table

| Step | Tool | Expected | Observed | Result |
|------|------|----------|----------|--------|
| 1 | (server instructions) | Doctrine advertised, covers ownership/branching + "rerun to fix, branch to progress" | Received full doctrine as server instructions, both topics present | PASS |
| 2 | improve_get_authoring_guide | Same doctrine text | Identical text returned. MCP **resources** channel not supported by this (tool-bridging) client → `improve://authoring-guide` resource read skipped (client limitation, not a FAIL) | PASS |
| 3 | improve_get_server_info | Base URL + version | baseUrl set, version `4.4.1-16` | PASS |
| 4 | improve_get_current_user | `loggedIn: true` + username | `loggedIn: true`, username `admin` | PASS |
| 5 | improve_list_children `/_MCP_Integration` | Succeeds | 3 children returned | PASS |
| 6 | improve_create_folder `e2e-run` | A Folder | Folder created | PASS |
| 7 | improve_create_tree `wf` | An Analysis Tree | Analysis Tree created | PASS |
| 8 | improve_create_step (rationale+description) | Server-named `Step N`, both fields stored | `Step 1`, rationale + description stored (**StepA**) | PASS |
| 9 | improve_create_step `name:"my base model"` | **Refuse** (name is server-assigned) | Refused; verified no stray step (only Step 1 present) | PASS (guard) |
| 10 | improve_upload_file `note.txt` = `hello\n` | Committed File | File created, byteLength 6 | PASS |
| 11 | improve_read_resource note.txt | text = `hello\n` | `hello\n` | PASS |
| 12 | improve_get_revisions | ≥1 revision | 2 revisions | PASS |
| 13 | improve_get_metadata | Succeeds (may be empty) | Succeeded, `metadata: []` | PASS |
| 14 | improve_search_resources `note` | Hits with usable paths | 237 hits, each with full `path` | PASS |
| 15 | improve_checkout note.txt | Locked | `locked: true` | PASS |
| 16 | improve_edit_content `hello`→`hello world` | `replacements: 1` | `replacements: 1` | PASS |
| 17 | improve_edit_content `zzz`→`q` | **Refuse** ("not found") | Refused, nothing changed | PASS (guard) |
| 18 | improve_read_resource workingCopy | `hello world\n` | `hello world\n` | PASS |
| 19 | improve_commit | Committed + unlocked | `committed: true`, `unlocked: true` | PASS |
| 20 | improve_describe_step StepA | rationale, description, ownedByName, isOwnedByYou:true, no ownership note | All present, `isOwnedByYou: true`, no ownership note | PASS |
| 21 | improve_set_documentation (rationale only) | Rationale stored, description unchanged | Rationale updated, description still `NONMEM base run` | PASS |
| 22 | improve_set_documentation (neither) | **Refuse** ("nothing to set") | Refused | PASS (guard) |
| 23 | improve_set_step_tool nonmem_7.4-lsf | `toolChanged:true`, seeds `command-file`+`dataset` | `toolChanged: true`, both inputs seeded | PASS |
| 24 | improve_set_step_input asCommandFile+asCopy base.ctl | `copied:true`, command-file points INSIDE StepA | `copied: true`, valuePath `…/Step 1/base.ctl` | PASS |
| 25 | improve_get_copy_ancestry base.ctl copy | Traces to `/robert/lib/base.ctl` | Ancestry chain starts at `/robert/lib/base.ctl` | PASS |
| 26 | improve_set_step_input dataset (link) | `linked:true`, linkedTo source, Step-local Link resource | `linked: true`, linkedTo `/robert/lib/concentrations.dat`, resolves to `…/Step 1/concentrations.dat` Link | PASS |
| 27 | improve_set_step_input (no name/asCommandFile) | **Refuse** | Refused | PASS (guard) |
| 28 | improve_describe_step StepA | Both fileRef inputs resolved to paths | base.ctl + concentrations.dat both resolved | PASS |
| 29 | improve_clear_step_input + re-set dataset | Clear empties, set restores | Cleared then restored (`linked: true`) | PASS |
| 30 | improve_run_step_and_wait StepA (300s) | `FINISHED`, `succeeded:true` | `FINISHED`, `succeeded: true`, ~50s | PASS |
| 31 | improve_list_step_outputs StepA | ≥1 output incl. `STEP*.lst` | 25 outputs incl. `STEP1.lst` | PASS |
| 32 | improve_get_run_output StepA | Command line + terminal run status | commandLine `…nmfe74 base.ctl STEP1.lst`, runStatus `FINISHED` | PASS |
| 33 | improve_read_resource STEP1.lst find "MINIMIZATION SUCCESSFUL" | matchCount ≥1 | `matchCount: 1` (line 263) | PASS |
| 34 | improve_create_step child of StepA | `inheritedTool:true`, tracked-copy note, server name | `Step 2`, `inheritedTool: true`, note present (**StepB**) | PASS |
| 35 | improve_describe_step StepB | Parent tool + both inputs inherited, pointing at StepB's own copies | Tool inherited; inputs at `…/Step 2/base.ctl` + `…/Step 2/concentrations.dat` | PASS |
| 36 | improve_get_step_tree StepA | children incl. StepB, tree with parent links | children = Step 2; tree lists both, Step 2→parent Step 1 | PASS |
| 37 | improve_run_step_and_wait StepB resetInventory:true | `FINISHED`, `succeeded:true`, STEP*.lst MINIMIZATION SUCCESSFUL | `FINISHED`, `succeeded: true`; STEP2.lst matchCount 1 | PASS |
| 38 | improve_call_endpoint POST references (StepA lst → StepC) | A Link | Link created inside StepC → StepA's STEP1.lst | PASS |
| 39 | improve_get_dependencies StepC | Exactly StepA upstream | count 1 = Step 1 | PASS |
| 40 | improve_get_usages StepA | StepC downstream | count 1 = Step 3 | PASS |
| 41 | improve_get_dependencies on file (note.txt) | **Refuse** ("not a Step") | Refused | PASS (guard) |
| 42 | improve_call_endpoint POST copy?targetId=wf | Copy of note.txt into tree | Copied to `…/wf/note.txt` | PASS |
| 43 | improve_get_copy_descendants original | The copy | count 1 = the copy | PASS |
| 44 | improve_get_copy_ancestry copy | Original, exactly once | count 1 = original, no duplicates | PASS |
| 45 | improve_search_endpoints `usages` | `/resources/{id}/usages` present | Present (score 50) | PASS |
| 46 | improve_describe_endpoint GET dependencies | A signature | Full signature (uriParams, queryParams, responses) | PASS |
| 47 | improve_call_endpoint GET resource | 200 + headers show `authorization: <redacted>` | 200, `authorization: <redacted>`, no token leak | PASS (guard) |
| 48 | improve_delete_resource e2e-run confirm:true | `deleted:true`, folder gone | `deleted: true`; folder absent on re-list | PASS |

## Counts

- **PASS: 48**
- **FAIL: 0**

## Guard-step summary

All guard steps refused as required — **no guard succeeded where it should have refused**:

- **9** create_step with `name` → refused (name is server-assigned; wording belongs in rationale/description). No stray step created.
- **17** edit_content with absent `find` → refused ("not found"), nothing changed.
- **22** set_documentation with neither field → refused ("nothing to set").
- **27** set_step_input with neither `name` nor `asCommandFile` → refused.
- **41** get_dependencies on a File → refused ("not a Step").
- **47** GET endpoint → token redacted in headers (`authorization: <redacted>`).

## Issues encountered

- **None affecting the test outcome.** Every step passed and every guard refused correctly.
- **Client limitation (not a FAIL):** This MCP client bridges tools only and does not expose the MCP
  **resources** channel, so the `improve://authoring-guide` resource half of step 2 was skipped as
  instructed. The tool channel (`improve_get_authoring_guide`) returned the doctrine correctly and
  matched the server instructions.
- **Observation:** copy ancestry of the command-file (step 25) returned the full upstream copy chain
  (4 entries) rather than only the immediate source; the required source `/robert/lib/base.ctl` is
  present as the first entry, so this is correct provenance behaviour and not an issue.

# improve MCP — End-to-End Acceptance Test

**How to use:** open this repository's workspace in VS Code with the improve
extensions installed and signed in, then paste the prompt below to Claude (it has
the `improve_*` MCP tools). It drives every MCP tool against the **live** server
under `/_MCP_Integration`, checks each result, and prints a pass/fail table.

This is a live test, not a unit test. It creates real resources and runs a real
NONMEM step twice (~60 s each). It is safe to re-run: it works inside its own
subfolder and deletes that subfolder at the end.

**Prerequisites**
- Signed in to improve in VS Code (the MCP server shares that session).
- **Write mode is on.** The server is read-only by default, so the write/execute
  tools (create, checkout, edit, commit, run) are not exposed and this test cannot
  run. Turn on `improve.devtools.mcp.writable`, reload the window, and for Claude
  Code re-run **Register MCP Server with Claude Code** (or re-add with
  `-e IMPROVE_MCP_WRITABLE=1`). Verify by checking that `improve_create_folder`
  appears in the tool list.
- `/robert/lib` holds `base.ctl`, `concentrations.dat`, `GoF_plot.r` — a NONMEM
  control file, its dataset, and an R post-processing script.
- `/_MCP_Integration` exists and is writable (a dev-server scratch area).

**Two conventions this test enforces**
- **Steps are named by the server** (`Step 1`, `Step 2`, …). `improve_create_step`
  refuses a custom name, because tool arguments derive `<step-number>` from it and
  a custom name silently breaks the run. Wording belongs in `rationale` and
  `description`.
- **Branching a child step inherits the parent's tool**, which makes improve copy
  the parent's whole configuration (tool + inputs) in as a *tracked copy*.

---

## Prompt to paste

> You have the improve MCP tools (`improve_*`). Run the following end-to-end
> acceptance test against the live server and report a **pass/fail table** at the
> end — one row per step, with the observed result and, on failure, the error.
> Do not stop at the first failure; record it and continue where later steps don't
> depend on it. Work inside `/_MCP_Integration/e2e-run`.
>
> Treat an unexpected error, a wrong shape, or a missing field as a **FAIL**. When
> a step says "expect X", verify X explicitly rather than assuming success.
>
> ### 0. Instructions and orientation
> 1. Confirm the server advertised **authoring instructions** (the doctrine you were
>    given before your first call). Expect them to cover ownership/branching and
>    "rerun to fix, branch to progress". If you never received any, that is a FAIL.
> 2. Read the resource `improve://authoring-guide` — expect the same doctrine text.
> 3. `improve_get_server_info` — expect a base URL and a version.
> 4. `improve_get_current_user` — expect `loggedIn: true` and a username.
> 5. `improve_list_children` on `/_MCP_Integration` — expect it to succeed.
>
> ### 1. Scaffolding
> 6. `improve_create_folder` parentPath `/_MCP_Integration`, name `e2e-run` — expect a Folder.
> 7. `improve_create_tree` parentPath `…/e2e-run`, name `wf` — expect an Analysis Tree.
> 8. `improve_create_step` parentPath `…/e2e-run/wf`, with `rationale` = "baseline
>    1-compartment fit" and `description` = "NONMEM base run". Expect a Step whose
>    **name was assigned by the server** (`Step N`), and both fields stored. Note it
>    as **StepA**.
> 9. `improve_create_step` again, this time passing `name: "my base model"` — expect
>    a **failure** telling you steps are named by the server and that wording belongs
>    in rationale/description. This is a PASS for the guard. Verify no step was created.
> 10. `improve_upload_file` parentPath `…/e2e-run`, name `note.txt`, content `hello\n` — expect a committed File.
>
> ### 2. Read
> 11. `improve_read_resource` on `…/e2e-run/note.txt` — expect `text` = `hello\n`.
> 12. `improve_get_revisions` on the same — expect at least one revision.
> 13. `improve_get_metadata` on the same — expect it to succeed (may be empty).
> 14. `improve_search_resources` query `note` — expect the hits to be usable paths.
>
> ### 3. Content patch (checkout → edit → commit)
> 15. `improve_checkout` on `…/e2e-run/note.txt`.
> 16. `improve_edit_content` find `hello`, replace `hello world` — expect `replacements: 1`.
> 17. `improve_edit_content` find `zzz`, replace `q` — expect a **failure** ("not found"); PASS for the guard.
> 18. `improve_read_resource` workingCopy `true` — expect `hello world\n`.
> 19. `improve_commit` — expect committed and unlocked.
>
> ### 4. Documentation and ownership
> 20. `improve_describe_step` on StepA — expect `rationale`, `description`,
>     `ownedByName` and `isOwnedByYou: true` (you created it). Expect **no**
>     ownership `note`, since you own it.
> 21. `improve_set_documentation` on StepA with only `rationale` = "revised: baseline
>     before testing 2-compartment" — expect it stored, and expect the **description
>     to be unchanged** (a partial update must not wipe the other field).
> 22. `improve_set_documentation` on StepA with neither field — expect a **failure**
>     ("nothing to set"); PASS for the guard.
>
> ### 5. Step configuration — command-file, copy vs. link
> 23. `improve_set_step_tool` path StepA, tool `nonmem_7.4-lsf`, runserver
>     `runserver1-docker-lsf` — expect `toolChanged: true` and two inputs seeded
>     (`command-file`, `dataset`).
> 24. `improve_set_step_input` on StepA with `asCommandFile: true`, `asCopy: true`,
>     file `/robert/lib/base.ctl`. Expect `copied: true`, and the **command-file to
>     point at a copy INSIDE StepA**, not at `/robert/lib/base.ctl`.
> 25. `improve_get_copy_ancestry` on that copy — expect it to trace back to
>     `/robert/lib/base.ctl`. This proves the copy is tracked.
> 26. `improve_set_step_input` name `dataset`, file `/robert/lib/concentrations.dat`
>     (no `asCopy`) — expect a **LINK**: `copied` absent/false, and the input
>     pointing at `/robert/lib/concentrations.dat` itself.
> 27. `improve_set_step_input` with neither `name` nor `asCommandFile` — expect a
>     **failure**; PASS for the guard.
> 28. `improve_describe_step` StepA — expect both fileRef inputs resolved to paths.
> 29. `improve_clear_step_input` name `dataset`, then set it back — expect the clear
>     to empty it and the set to restore it.
>
> ### 6. Run
> 30. `improve_run_step_and_wait` StepA, timeoutSec 300 — expect `status: FINISHED`,
>     `succeeded: true` (~60 s).
> 31. `improve_list_step_outputs` StepA — expect ≥ 1 output including a `STEP*.lst`.
> 32. `improve_get_run_output` StepA — expect a command line and a terminal run status.
> 33. `improve_read_resource` on the `STEP*.lst` — expect it to contain
>     `MINIMIZATION SUCCESSFUL`. **A terminal status alone is not success**: this is
>     what proves the tool actually computed.
>
> ### 7. Branch — the decision tree
> 34. `improve_create_step` with parentPath = **StepA** (branching a child), and
>     `rationale` = "testing whether a two-compartment model improves fit". Expect
>     `inheritedTool: true`, a `note` about the tracked copy, and a server-assigned
>     name. Note it as **StepB**.
> 35. `improve_describe_step` StepB — expect the **parent's tool and BOTH inputs to
>     have been inherited**, with the inputs now pointing at StepB's *own* copies
>     (not at StepA's files).
> 36. `improve_get_step_tree` StepA — expect `children` to include StepB, and the
>     `tree` to list the steps with their parent links.
>
> ### 8. Clean rerun
> 37. `improve_run_step_and_wait` on **StepB** with `resetInventory: true`,
>     timeoutSec 300 — expect `status: FINISHED`, `succeeded: true`, and a
>     `STEP*.lst` containing `MINIMIZATION SUCCESSFUL`. (This is the clean-rerun
>     path; the incremental default was already exercised in step 30.)
>
> ### 9. Provenance — data flow
> 38. Link an output of StepA into a new step: create **StepC** under the tree
>     (parentPath = `…/e2e-run/wf`), then `improve_call_endpoint` POST
>     `/resources/<StepA's STEP*.lst resourceId>/references` with body
>     `{ "name": "STEP.lst", "targetId": "<StepC resourceId>" }` — expect a Link.
> 39. `improve_get_dependencies` StepC — expect exactly StepA (upstream).
> 40. `improve_get_usages` StepA — expect StepC among the results (downstream).
> 41. `improve_get_dependencies` on a **file** path (e.g. `…/e2e-run/note.txt`) —
>     expect a **failure** ("not a Step"); PASS for the Steps-only guard.
>
> ### 10. Provenance — copy origin
> 42. `improve_call_endpoint` POST `/resources/<note.txt id>/copy?targetId=<wf tree id>`
>     — copy note.txt into the tree (note: `targetId` is a **query** parameter).
> 43. `improve_get_copy_descendants` on the original `note.txt` — expect the copy.
> 44. `improve_get_copy_ancestry` on the copy — expect the original, **exactly once**
>     (duplicates would be a FAIL).
>
> ### 11. Generic endpoint + safety
> 45. `improve_search_endpoints` query `usages` — expect the `/resources/{id}/usages` endpoint.
> 46. `improve_describe_endpoint` GET `/resources/{resourceId}/dependencies` — expect a signature.
> 47. `improve_call_endpoint` GET on any resource — expect 200 and confirm the
>     response headers show `authorization: <redacted>` (no token leak).
>
> ### 12. Cleanup
> 48. `improve_delete_resource` path `/_MCP_Integration/e2e-run`, `confirm: true` —
>     expect `deleted: true`. Verify the folder is gone. Deleting the container
>     removes everything the test created, so a re-run starts clean.
>
> ### Report
> Print a table: step | tool | expected | observed | PASS/FAIL. End with a count of
> passes and fails. If any of the guard steps (9, 17, 22, 27, 41, 47) did **not**
> refuse as required, call that out prominently — a tool that succeeds where it must
> refuse is worse than one that errors.

---

## What each family proves

| Family | Tools | What a pass means |
|---|---|---|
| Instructions | server `instructions`, `improve://authoring-guide` | the doctrine reaches the model before its first call |
| Scaffolding | create_folder/tree/step, upload_file | the agent can build structure; the server names steps |
| Read | read_resource, get_revisions, get_metadata, search_resources | search hits are usable paths |
| Patch | checkout, edit_content, commit | find/replace works; an absent match is refused |
| Documentation | describe_step, set_documentation | WHY and WHAT are stored and readable; partial updates merge |
| Ownership | describe_step | `isOwnedByYou` is decidable; a foreign step tells you to branch |
| Step config | set_step_tool, set/clear_step_input | tool binds on the process; command-file targetable by flag |
| Copy vs. link | set_step_input `asCopy`, get_copy_ancestry | a model is copied and stays traceable; data is linked |
| Run | run_step_and_wait, list_step_outputs, get_run_output | the loop closes; NONMEM converges |
| Branch | create_step under a Step, get_step_tree | the child inherits the parent's config as a tracked copy |
| Clean rerun | run_step_and_wait `resetInventory` | the fix path reproduces from a clean state |
| Provenance | get_dependencies/usages, get_copy_ancestry/descendants | data flow and copy origin are distinct, both resolvable |
| Safety | the guard steps | the token is redacted; guards refuse rather than silently proceed |
| Cleanup | delete_resource | a container delete removes everything below it |

The guard rows are the important ones. A tool that *succeeds* where it must refuse
is worse than one that errors: it teaches the agent a wrong habit and hides the
damage.

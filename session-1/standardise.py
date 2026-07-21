"""Step 2 — standardise: z-score the four numeric columns.

Input:  session-1/clean.csv    (333 rows)
Output: session-1/std.csv      (333 rows, 4 columns: bill_length_mm_std, bill_depth_mm_std,
                                 flipper_length_mm_std, body_mass_g_std)
        session-1/std_params.json  (mean and std per column, for verification)

Determinism:
  - LF line endings
  - Population std (ddof=0) to avoid numpy default ambiguity
  - Float formatting: 10 decimal places, fixed
  - Row order: same as clean.csv (sorted by species/island/bill_length_mm/bill_depth_mm)
  - JSON: sort_keys=True, no trailing spaces, one trailing newline
  - No seeds / no timestamps / no absolute paths
"""
import csv
import json
import sys
import numpy as np

NUM_COLS = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
OUT_COLS = [c + "_std" for c in NUM_COLS]


def main():
    with open("session-1/clean.csv", "r", newline="") as fh:
        rows = list(csv.DictReader(fh))

    matrix = np.array([[float(r[c]) for c in NUM_COLS] for r in rows])

    means = matrix.mean(axis=0)
    stds  = matrix.std(axis=0, ddof=0)   # population std

    std_matrix = (matrix - means) / stds

    # Write standardised CSV
    with open("session-1/std.csv", "w", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(OUT_COLS)
        for row in std_matrix:
            writer.writerow([f"{v:.10f}" for v in row])

    # Write params JSON (for reproducibility verification)
    params = {
        "columns": NUM_COLS,
        "mean": [round(float(v), 10) for v in means],
        "std":  [round(float(v), 10) for v in stds],
    }
    with open("session-1/std_params.json", "w") as fh:
        fh.write(json.dumps(params, sort_keys=True, separators=(",", ":")) + "\n")

    print(f"standardise: {len(rows)} rows, {len(NUM_COLS)} columns → session-1/std.csv",
          file=sys.stderr)


if __name__ == "__main__":
    main()

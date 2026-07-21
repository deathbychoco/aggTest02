"""Step 3 — summarise: per-cluster statistics CSV.

Input:  session-1/penguins_clustered.csv    (333 rows, 8 columns)
Output: session-1/penguins_summary.csv      (3 rows — one per cluster)

Contract (matches prior producer sha256:d9d3fbadf2cd1bbf...):
  - Columns: cluster, count, then for each of the 4 numeric cols:
      <col>_mean, <col>_std, <col>_min, <col>_max
  - std uses ddof=1 (sample std, numpy default)
  - Floats rounded to 4 decimal places
  - Rows sorted by cluster id ascending
  - LF line endings; no timestamps / no locale / no absolute paths
"""
import csv
import sys
import numpy as np

NUM_COLS = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]


def fmt(v):
    """Round to 4 dp, strip trailing zeros after decimal point."""
    rounded = round(float(v), 4)
    # Use Python g-style: strip trailing zeros but keep at least one decimal
    s = f"{rounded:.4f}".rstrip("0").rstrip(".")
    return s


def main():
    with open("session-1/penguins_clustered.csv", "r", newline="") as fh:
        rows = list(csv.DictReader(fh))

    # Group by cluster
    clusters = sorted(set(int(r["cluster"]) for r in rows))
    groups = {k: [r for r in rows if int(r["cluster"]) == k] for k in clusters}

    stat_cols = []
    for c in NUM_COLS:
        stat_cols += [f"{c}_mean", f"{c}_std", f"{c}_min", f"{c}_max"]

    out_cols = ["cluster", "count"] + stat_cols

    with open("session-1/penguins_summary.csv", "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=out_cols, lineterminator="\n")
        writer.writeheader()
        for k in clusters:
            grp = groups[k]
            row = {"cluster": str(k), "count": str(len(grp))}
            for c in NUM_COLS:
                vals = np.array([float(r[c]) for r in grp])
                row[f"{c}_mean"] = fmt(vals.mean())
                row[f"{c}_std"]  = fmt(vals.std(ddof=1))
                row[f"{c}_min"]  = fmt(vals.min())
                row[f"{c}_max"]  = fmt(vals.max())
            writer.writerow(row)

    print(f"summarise: {len(clusters)} clusters → session-1/penguins_summary.csv",
          file=sys.stderr)


if __name__ == "__main__":
    main()

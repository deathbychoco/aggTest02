"""Step 2 — cluster: k-means (k=3) on 4 numeric columns with canonical label assignment.

Input:  session-1/penguins_clean.csv        (333 rows, 7 columns)
Output: session-1/penguins_clustered.csv    (333 rows, 8 columns — adds 'cluster')

Contract (matches prior producer sha256:4e4c6f20acb70e95...):
  - Feature columns (standardised internally): bill_length_mm, bill_depth_mm,
    flipper_length_mm, body_mass_g
  - KMeans k=3, random_state=42, n_init=10; StandardScaler (mean=0, std ddof=0)
  - Canonical labels: sort cluster indices by ascending centroid bill_length_mm_std
  - Output: all 7 input columns + 'cluster' (integer, 0/1/2); same row order as input
  - Numeric values written as str(float(v)) (same as input)
  - LF line endings; no timestamps / no locale / no absolute paths
"""
import csv
import sys
import numpy as np
from sklearn.cluster import KMeans

N_CLUSTERS = 3
NUM_COLS   = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
ALL_COLS   = ["species", "island", "sex",
              "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]


def main():
    with open("session-1/penguins_clean.csv", "r", newline="") as fh:
        rows = list(csv.DictReader(fh))

    matrix = np.array([[float(r[c]) for c in NUM_COLS] for r in rows])

    # Standardise (z-score, ddof=0 — same as StandardScaler)
    means = matrix.mean(axis=0)
    stds  = matrix.std(axis=0, ddof=0)
    std_matrix = (matrix - means) / stds

    km = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    km.fit(std_matrix)

    # Canonical labelling: sort cluster indices by ascending centroid bill_length_mm_std (dim 0)
    order     = np.argsort(km.cluster_centers_[:, 0])
    label_map = {int(old): int(new) for new, old in enumerate(order)}
    labels    = [label_map[int(l)] for l in km.labels_]

    out_cols = ALL_COLS + ["cluster"]
    with open("session-1/penguins_clustered.csv", "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=out_cols, lineterminator="\n")
        writer.writeheader()
        for row, label in zip(rows, labels):
            out = {c: row[c] for c in ALL_COLS}
            out["cluster"] = str(label)
            writer.writerow(out)

    counts = {i: labels.count(i) for i in range(N_CLUSTERS)}
    print(f"cluster: k={N_CLUSTERS} counts={counts} → session-1/penguins_clustered.csv",
          file=sys.stderr)


if __name__ == "__main__":
    main()

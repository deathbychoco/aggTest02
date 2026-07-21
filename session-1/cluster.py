import csv, sys
import numpy as np

in_path  = sys.argv[1]   # session-1/standardized.csv
out_path = sys.argv[2]   # session-1/clustered.csv

with open(in_path, newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    body   = list(reader)

X = np.array([[float(v) for v in row] for row in body])

# Deterministic k-means: fixed init (rows 0, 111, 222), 25 Lloyd iterations
C = X[[0, 111, 222]].copy()
for _ in range(25):
    dists = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
    labels = dists.argmin(axis=1)
    for k in range(3):
        mask = labels == k
        if mask.any():
            C[k] = X[mask].mean(axis=0)

# Canonicalise labels by ascending centroid sum (permutation-invariant)
order  = np.argsort(C.sum(axis=1))
remap  = {int(old): int(new) for new, old in enumerate(order)}
labels = np.array([remap[int(l)] for l in labels])

with open(out_path, 'w', newline='') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(header + ['cluster'])
    for row, label in zip(body, labels):
        writer.writerow(row + [str(int(label))])

import csv, sys
import numpy as np

NUM_COLS = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']

in_path  = sys.argv[1]   # session-1/clean.csv
out_path = sys.argv[2]   # session-1/standardized.csv

with open(in_path, newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    body   = list(reader)

col_idx = [header.index(c) for c in NUM_COLS]
X = np.array([[float(row[i]) for i in col_idx] for row in body])

# z-score, population std (ddof=0)
Z = (X - X.mean(axis=0)) / X.std(axis=0, ddof=0)

with open(out_path, 'w', newline='') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(NUM_COLS)
    for z in Z:
        writer.writerow([f'{v:.6f}' for v in z])

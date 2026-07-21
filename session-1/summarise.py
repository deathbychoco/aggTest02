import csv, sys, json
import numpy as np

in_path  = sys.argv[1]   # session-1/clustered.csv
out_path = sys.argv[2]   # session-1/summary.json

with open(in_path, newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    body   = list(reader)

cluster_idx = header.index('cluster')
num_cols    = header[:cluster_idx]

clusters_data: dict = {}
for row in body:
    k = int(row[cluster_idx])
    vals = [float(x) for x in row[:cluster_idx]]
    clusters_data.setdefault(k, []).append(vals)

out = {
    'clusters': [
        {
            'label': k,
            'mean':  [round(float(m), 6) for m in np.array(v).mean(axis=0)],
            'size':  len(v),
        }
        for k, v in sorted(clusters_data.items())
    ],
    'features':   num_cols,
    'n_clusters': len(clusters_data),
    'n_rows':     len(body),
}

with open(out_path, 'w') as f:
    json.dump(out, f, sort_keys=True, separators=(',', ':'))
    f.write('\n')

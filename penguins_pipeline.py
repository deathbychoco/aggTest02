#!/usr/bin/env python3
"""
penguins pipeline: clean -> standardise -> cluster -> summarise
Deterministic: same inputs produce byte-identical outputs.
Determinism checklist:
  - random_state=42 fixed for KMeans
  - n_init=10, max_iter=300 fixed
  - StandardScaler(copy=True) on NUMERIC_COLS
  - cluster labels remapped by ascending mean(bill_length_mm)
  - NAs dropped (reproducible policy)
  - categoricals lowercased, numerics rounded to 4dp
  - sort: species, island, sex, bill_length_mm (mergesort, stable)
  - CSV: LF line endings, no BOM, no index
"""
import sys, pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

NUMERIC_COLS = ['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g']
CAT_COLS     = ['species','island','sex']
SORT_BY      = ['species','island','sex','bill_length_mm']
KMEANS_K, KMEANS_SEED, KMEANS_NINIT, KMEANS_MAXITER = 3, 42, 10, 300

def standardise(df):
    df = df.copy()
    for c in CAT_COLS:   df[c] = df[c].str.strip().str.lower()
    df = df.dropna(subset=NUMERIC_COLS+CAT_COLS).reset_index(drop=True)
    for c in NUMERIC_COLS: df[c] = df[c].round(4)
    df = df[CAT_COLS+NUMERIC_COLS]
    return df.sort_values(SORT_BY, kind='mergesort').reset_index(drop=True)

def cluster(df):
    X  = df[NUMERIC_COLS].values
    Xs = StandardScaler(copy=True).fit_transform(X)
    km = KMeans(n_clusters=KMEANS_K, random_state=KMEANS_SEED,
                n_init=KMEANS_NINIT, max_iter=KMEANS_MAXITER)
    rl = km.fit_predict(Xs)
    cm = {c: df.loc[rl==c, 'bill_length_mm'].mean() for c in range(KMEANS_K)}
    rm = {old:new for new,old in enumerate(sorted(cm, key=cm.get))}
    df = df.copy()
    df['cluster'] = [rm[l] for l in rl]
    return df.sort_values(SORT_BY+['cluster'], kind='mergesort').reset_index(drop=True)

def summarise(df):
    rows = []
    for c in sorted(df['cluster'].unique()):
        sub  = df[df['cluster']==c][NUMERIC_COLS]
        row  = {'cluster': int(c), 'count': int(len(sub))}
        for col in NUMERIC_COLS:
            row[f'{col}_mean'] = round(float(sub[col].mean()), 4)
            row[f'{col}_std']  = round(float(sub[col].std(ddof=1)), 4)
            row[f'{col}_min']  = round(float(sub[col].min()), 4)
            row[f'{col}_max']  = round(float(sub[col].max()), 4)
        rows.append(row)
    return pd.DataFrame(rows)

def save(df, path):
    with open(path, 'w', newline='') as f:
        f.write(df.to_csv(index=False, lineterminator='\n'))

if __name__ == '__main__':
    raw      = pd.read_csv('data/penguins.csv')
    clean    = standardise(raw);    save(clean,    'data/penguins_clean.csv')
    clustered= cluster(clean);      save(clustered,'data/penguins_clustered.csv')
    summary  = summarise(clustered);save(summary,  'data/penguins_summary.csv')
    print("Done. Output hashes:")
    import hashlib
    for p in ['data/penguins_clean.csv','data/penguins_clustered.csv','data/penguins_summary.csv']:
        print(f"  {p}: sha256:{hashlib.sha256(open(p,'rb').read()).hexdigest()}")

"""Step 1 — clean: drop rows with any missing field, lowercase strings, float-format numerics.

Input:  data/penguins.csv                (344 rows, 7 columns)
Output: session-1/penguins_clean.csv     (333 rows, 7 columns)

Contract (matches prior producer sha256:6217e82c75acc88b...):
  - Drop rows where ANY of the 7 columns is empty
  - Lowercase all string values (species, island, sex)
  - Numeric columns written as Python str(float(v)) — gives "187.0" not "187"
  - Column order: species, island, sex, bill_length_mm, bill_depth_mm,
                  flipper_length_mm, body_mass_g
  - Sort by (species, island, sex, bill_length_mm) ascending
  - LF line endings; no timestamps / no locale / no absolute paths in body
"""
import csv
import sys

ALL_COLS  = ["species", "island", "sex",
             "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
STR_COLS  = ["species", "island", "sex"]
NUM_COLS  = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]


def main():
    with open("data/penguins.csv", "r", newline="") as fh:
        rows = list(csv.DictReader(fh))

    # Drop rows with any missing field
    clean = [r for r in rows if all(r[c].strip() != "" for c in ALL_COLS)]

    # Normalise: lowercase strings, float-format numerics
    out = []
    for r in clean:
        row = {}
        for c in STR_COLS:
            row[c] = r[c].strip().lower()
        for c in NUM_COLS:
            row[c] = str(float(r[c].strip()))
        out.append(row)

    # Sort for determinism
    out.sort(key=lambda r: (
        r["species"], r["island"], r["sex"], float(r["bill_length_mm"])
    ))

    with open("session-1/penguins_clean.csv", "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=ALL_COLS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(out)

    print(f"clean: {len(rows)} → {len(out)} rows → session-1/penguins_clean.csv",
          file=sys.stderr)


if __name__ == "__main__":
    main()

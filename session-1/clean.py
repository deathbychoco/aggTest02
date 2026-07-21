import csv, sys

# DETERMINISM: LF endings, drop rows with any empty or NA field, preserve column order
in_path = sys.argv[1]   # data/penguins.csv
out_path = sys.argv[2]  # session-1/clean.csv

with open(in_path, newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = [row for row in reader
            if all(cell.strip() != '' and cell.strip().upper() != 'NA'
                   for cell in row)]

with open(out_path, 'w', newline='') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)

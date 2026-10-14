"""csv_cleaner.py — clean up messy CSV files.

Usage:
    python3 csv_cleaner.py INPUT.csv --out OUTPUT.csv [--dedupe] [--lower-headers]

What it does:
  - strips leading/trailing whitespace from every cell
  - drops fully-empty rows
  - optionally lowercases/snake_cases headers (--lower-headers)
  - optionally removes duplicate rows (--dedupe)
"""

import argparse
import csv
import re
import sys


def normalize_header(h: str, lower: bool) -> str:
    h = h.strip()
    if lower:
        h = re.sub(r"[^0-9a-zA-Z]+", "_", h).strip("_").lower()
    return h


def clean(input_path: str, output_path: str, dedupe: bool, lower_headers: bool) -> int:
    with open(input_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            print("error: no header row found", file=sys.stderr)
            return 1
        fieldnames = [normalize_header(h, lower_headers) for h in reader.fieldnames]
        rows = []
        seen = set()
        for row in reader:
            cleaned = {fn: (row[orig] or "").strip()
                       for fn, orig in zip(fieldnames, reader.fieldnames)}
            if not any(cleaned.values()):
                continue  # skip empty rows
            key = tuple(sorted(cleaned.items()))
            if dedupe and key in seen:
                continue
            seen.add(key)
            rows.append(cleaned)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows -> {output_path}")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="Clean up a messy CSV file.")
    p.add_argument("input", help="input CSV path")
    p.add_argument("--out", required=True, help="output CSV path")
    p.add_argument("--dedupe", action="store_true", help="drop duplicate rows")
    p.add_argument("--lower-headers", action="store_true",
                   help="normalize headers to snake_case")
    args = p.parse_args()
    sys.exit(clean(args.input, args.out, args.dedupe, args.lower_headers))


if __name__ == "__main__":
    main()

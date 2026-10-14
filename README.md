# Python Automation Toolkit

Small, practical Python utilities I wrote to kill repetitive manual work — the same kind of scripts I build for freelance clients (data entry helpers, file/report automation). No client data or credentials here; everything runs on sample inputs.

## What's inside

| Script | What it does |
|---|---|
| `csv_cleaner.py` | Deduplicates rows, trims whitespace, normalizes headers, and writes a clean CSV. |
| `file_organizer.py` | Sorts a messy folder into subfolders by file type (documents, images, archives, …). |

## Quick start

```bash
python3 csv_cleaner.py messy.csv --out clean.csv --dedupe
python3 file_organizer.py ~/Downloads --dry-run   # preview first, then run without --dry-run
```

## Why it exists

Repetitive data cleanup is where I consistently save clients 5+ hours a week. These two scripts are the sanitized core of that work — boring, reliable, and honest about what they do.

MIT licensed — use freely.

"""file_organizer.py — sort a messy folder into subfolders by file type.

Usage:
    python3 file_organizer.py ~/Downloads            # actually moves files
    python3 file_organizer.py ~/Downloads --dry-run  # preview only

Files are grouped into: documents, images, videos, audio, archives,
code, spreadsheets, and other. Name collisions get a numeric suffix.
"""

import argparse
import shutil
from pathlib import Path

GROUPS = {
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt"},
    "spreadsheets": {".csv", ".xls", ".xlsx", ".ods"},
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"},
    "videos": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "audio": {".mp3", ".wav", ".flac", ".ogg"},
    "archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "code": {".py", ".js", ".ts", ".html", ".css", ".json", ".java", ".go"},
}


def group_for(suffix: str) -> str:
    for group, exts in GROUPS.items():
        if suffix in exts:
            return group
    return "other"


def unique_dest(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    i = 2
    while (cand := dest.with_name(f"{stem}_{i}{suffix}")).exists():
        i += 1
    return cand


def organize(folder: Path, dry_run: bool) -> int:
    moved = 0
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        target_dir = folder / group_for(item.suffix.lower())
        dest = unique_dest(target_dir / item.name)
        if dry_run:
            print(f"would move: {item.name} -> {target_dir.name}/{dest.name}")
        else:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest))
            print(f"moved: {item.name} -> {target_dir.name}/{dest.name}")
        moved += 1
    print(f"{moved} file(s) {'previewed' if dry_run else 'organized'}")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="Organize a folder by file type.")
    p.add_argument("folder", help="folder to organize")
    p.add_argument("--dry-run", action="store_true", help="preview without moving")
    args = p.parse_args()
    folder = Path(args.folder).expanduser()
    if not folder.is_dir():
        p.error(f"not a directory: {folder}")
    raise SystemExit(organize(folder, args.dry_run))


if __name__ == "__main__":
    main()

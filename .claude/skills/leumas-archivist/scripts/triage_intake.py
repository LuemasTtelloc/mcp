#!/usr/bin/env python3
"""Deterministic triage for the Leumas Archivist.

Read-only. Scans the Out Tray (the single desktop dump folder), classifies each file by type,
clusters duplicates, proposes a route, and reports which files are already in
the Library (the master archive, so re-runs are idempotent). It does NOT move, file, or
write anything — it produces the worklist the archivist then acts on.

Usage:
    python3 triage_intake.py <out-tray> [<library-root>] [--json]

The LLM step (what is it / does it matter / write the Memory Card) happens after
this, using the manifest as its worklist. This script only does the parts that
should be deterministic: typing, dedup clustering, and archive-presence checks.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict

# Extension -> coarse type. The LLM refines (e.g. pdf -> "investor deck").
TYPE_BY_EXT = {
    ".pdf": "document", ".doc": "document", ".docx": "document",
    ".txt": "note", ".md": "note", ".rtf": "note",
    ".ppt": "presentation", ".pptx": "presentation", ".key": "presentation",
    ".xls": "spreadsheet", ".xlsx": "spreadsheet", ".csv": "spreadsheet",
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".gif": "image",
    ".heic": "image", ".webp": "image", ".tiff": "image",
    ".mp3": "audio", ".wav": "audio", ".m4a": "audio", ".aiff": "audio",
    ".mp4": "video", ".mov": "video", ".m4v": "video",
    ".eml": "email", ".msg": "email",
}

# Intake-folder name -> hint about likely route (overridden by content).
FOLDER_ROUTE_HINT = {
    "personal intake": "samuel",
    "ai command intake": "samuel",      # AI systems / command -> founder brain
    "voice notes": "samuel",
    "howa intake": "howa",
    "screenshots": "review",            # decide per image
}

# Filenames/patterns that almost never produce knowledge -> archive only.
ARCHIVE_ONLY_HINTS = [
    "natwest", "uncon", "wagco", "wagoco", "povey", "payroll", "amr ",
    "liquidation", "lease", "auto-reply", "automatic reply", "out of office",
    "read receipt", "delivery status",
]

# Strip a trailing " copy", " copy 2", "-4", "(1)" etc. to cluster duplicates.
DUP_SUFFIX_RE = re.compile(
    r"(?:\s*copy(?:\s*\d+)?|\s*-\s*\d+|\s*\(\d+\)|\s*\d+-\d+)\s*$",
    re.IGNORECASE,
)


@dataclass
class IntakeItem:
    path: str
    name: str
    ext: str
    type: str
    size_mb: float
    intake_folder: str
    route_hint: str
    dup_key: str
    dup_cluster: int = 0
    is_duplicate: bool = False
    in_archive: bool = False
    archive_only_hint: bool = False
    flags: list = field(default_factory=list)


def normalize_stem(name: str) -> str:
    stem, _ = os.path.splitext(name)
    stem = stem.strip()
    # collapse repeated dup suffixes ("X copy 2 copy" -> "X")
    prev = None
    while prev != stem:
        prev = stem
        stem = DUP_SUFFIX_RE.sub("", stem).strip()
    return re.sub(r"\s+", " ", stem).lower()


def top_intake_folder(path: str, intake_root: str) -> str:
    rel = os.path.relpath(path, intake_root)
    parts = rel.split(os.sep)
    return parts[0] if len(parts) > 1 else "(root)"


def archive_stems(archive_root: str | None) -> set[str]:
    """Set of normalized stems already present anywhere in the archive."""
    stems: set[str] = set()
    if not archive_root or not os.path.isdir(archive_root):
        return stems
    for root, _dirs, files in os.walk(archive_root):
        for fn in files:
            stems.add(normalize_stem(fn))
    return stems


def scan(intake_root: str, archive_root: str | None) -> list[IntakeItem]:
    archived = archive_stems(archive_root)
    items: list[IntakeItem] = []

    for root, dirs, files in os.walk(intake_root):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            if fn.startswith("."):
                continue
            full = os.path.join(root, fn)
            ext = os.path.splitext(fn)[1].lower()
            try:
                size_mb = round(os.path.getsize(full) / (1024 * 1024), 2)
            except OSError:
                size_mb = 0.0
            folder = top_intake_folder(full, intake_root)
            stem = normalize_stem(fn)
            low = fn.lower()
            item = IntakeItem(
                path=full,
                name=fn,
                ext=ext,
                type=TYPE_BY_EXT.get(ext, "unknown"),
                size_mb=size_mb,
                intake_folder=folder,
                route_hint=FOLDER_ROUTE_HINT.get(folder.lower(), "review"),
                dup_key=stem,
                in_archive=stem in archived,
                archive_only_hint=any(h in low for h in ARCHIVE_ONLY_HINTS),
            )
            if item.type == "unknown":
                item.flags.append("unknown-type")
            if item.size_mb == 0.0:
                item.flags.append("empty-file")
            items.append(item)

    # Cluster duplicates by normalized stem; first seen is canonical.
    clusters: dict[str, int] = {}
    counts: dict[str, int] = {}
    for it in items:
        counts[it.dup_key] = counts.get(it.dup_key, 0) + 1
    next_id = 1
    seen: set[str] = set()
    for it in sorted(items, key=lambda x: (x.dup_key, x.name)):
        if counts[it.dup_key] > 1:
            if it.dup_key not in clusters:
                clusters[it.dup_key] = next_id
                next_id += 1
            it.dup_cluster = clusters[it.dup_key]
            if it.dup_key in seen:
                it.is_duplicate = True
                it.flags.append("duplicate")
            seen.add(it.dup_key)
    return items


def print_report(items: list[IntakeItem], intake_root: str, archive_root):
    total = len(items)
    dupes = sum(1 for i in items if i.is_duplicate)
    already = sum(1 for i in items if i.in_archive)
    archive_only = sum(1 for i in items if i.archive_only_hint)
    new_canonical = [i for i in items if not i.is_duplicate and not i.in_archive]

    print(f"Intake triage — {intake_root}")
    print(f"archive: {archive_root or '(none given — presence check skipped)'}\n")
    print(f"{total} file(s): {len(new_canonical)} new canonical, "
          f"{dupes} duplicate(s), {already} already archived, "
          f"{archive_only} likely archive-only (no card)\n")

    header = f"{'route?':<7} {'type':<12} {'size':>6}  {'flags':<22} file"
    print(header)
    print("-" * max(len(header), 60))
    for it in sorted(items, key=lambda x: (x.intake_folder, x.name)):
        route = "ARCHIVE" if it.archive_only_hint else it.route_hint
        flags = ",".join(it.flags) or "—"
        tag = " (in-archive)" if it.in_archive else ""
        print(f"{route:<7} {it.type:<12} {it.size_mb:>6}  {flags:<22} "
              f"{it.intake_folder}/{it.name}{tag}")

    print("\nWorklist: archive every NEW canonical file as evidence, then write "
          "Memory Cards only for the ones that matter. Skip 'in-archive' and "
          "'duplicate' rows. 'ARCHIVE' route = store as evidence, no card.")


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    as_json = "--json" in argv
    if not args:
        print("usage: triage_intake.py <out-tray> [<library-root>] [--json]",
              file=sys.stderr)
        return 2
    intake_root = os.path.abspath(args[0])
    archive_root = os.path.abspath(args[1]) if len(args) > 1 else None
    if not os.path.isdir(intake_root):
        print(f"error: not a directory: {intake_root}", file=sys.stderr)
        return 2

    items = scan(intake_root, archive_root)
    if as_json:
        print(json.dumps([asdict(i) for i in items], indent=2))
    else:
        print_report(items, intake_root, archive_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

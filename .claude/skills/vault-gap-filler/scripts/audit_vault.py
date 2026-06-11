#!/usr/bin/env python3
"""Phase 1 vault audit scanner for the vault-gap-filler skill.

Deterministic, read-only, stdlib-only. Walks a markdown vault and reports, for
each top-level folder, a completeness score and a downstream-blocking score so
the skill can rank which folder to fill next.

Usage:
    python3 audit_vault.py <vault-root> [--json] [--config PATH]

Completeness (0-100) penalizes: missing index/MOC note, empty notes, notes
without YAML frontmatter, and very small folders. Blocking score = number of
notes elsewhere in the vault that link INTO this folder (inbound [[wikilinks]]
and markdown links). The fill priority sorts by blocking score first, then by
how incomplete the folder is, so high-leverage folders surface first.

Optional config: a JSON file at the vault root named ".vault-gap-filler.json"
(or passed via --config) may override defaults, e.g.:
    {
      "ignore_dirs": [".obsidian", "_meta", "attachments"],
      "index_names": ["index", "_moc", "readme"],
      "require_frontmatter": true
    }
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict

DEFAULT_IGNORE_DIRS = {
    ".git", ".obsidian", ".trash", "node_modules", ".vscode",
    "attachments", "assets", "_attachments", "files", ".claude",
}
DEFAULT_INDEX_STEMS = {"index", "_moc", "moc", "readme", "_index", "00-index"}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
MDLINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"^﻿?---\s*\n.*?\n---\s*\n", re.DOTALL)


@dataclass
class FolderReport:
    name: str
    note_count: int = 0
    empty_notes: int = 0
    missing_frontmatter: int = 0
    has_index: bool = False
    inbound_links: int = 0
    completeness: int = 0
    blocking: int = 0
    missing_items: list = field(default_factory=list)


def load_config(vault_root: str, config_path: str | None) -> dict:
    path = config_path or os.path.join(vault_root, ".vault-gap-filler.json")
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError) as exc:
            print(f"warning: could not read config {path}: {exc}", file=sys.stderr)
    return {}


def is_md(name: str) -> bool:
    return name.lower().endswith((".md", ".markdown"))


def read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def has_frontmatter(text: str) -> bool:
    return bool(FRONTMATTER_RE.match(text))


def link_targets(text: str) -> list[str]:
    """Extract bare link targets (wikilink note names + local md link paths)."""
    targets = [m.strip() for m in WIKILINK_RE.findall(text)]
    for raw in MDLINK_RE.findall(text):
        raw = raw.strip()
        if raw.startswith(("http://", "https://", "mailto:", "#")):
            continue
        targets.append(raw.split("#")[0])
    return [t for t in targets if t]


def collect(vault_root: str, ignore_dirs: set[str]):
    """Return (top_folders -> [md paths], note_basename -> top_folder map, all md paths)."""
    top_folders: dict[str, list[str]] = {}
    note_owner: dict[str, str] = {}
    all_paths: list[str] = []

    for entry in sorted(os.listdir(vault_root)):
        full = os.path.join(vault_root, entry)
        if not os.path.isdir(full) or entry in ignore_dirs or entry.startswith("."):
            continue
        paths: list[str] = []
        for root, dirs, files in os.walk(full):
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith(".")]
            for fn in files:
                if is_md(fn):
                    p = os.path.join(root, fn)
                    paths.append(p)
                    all_paths.append(p)
                    stem = os.path.splitext(fn)[0].lower()
                    note_owner.setdefault(stem, entry)
        top_folders[entry] = paths
    return top_folders, note_owner, all_paths


def folder_of_path(path: str, vault_root: str) -> str | None:
    rel = os.path.relpath(path, vault_root)
    parts = rel.split(os.sep)
    return parts[0] if len(parts) > 1 else None


def audit(vault_root: str, config: dict) -> list[FolderReport]:
    ignore_dirs = set(config.get("ignore_dirs", [])) | DEFAULT_IGNORE_DIRS
    index_stems = {s.lower() for s in config.get("index_names", [])} | DEFAULT_INDEX_STEMS
    require_fm = config.get("require_frontmatter", True)

    top_folders, note_owner, all_paths = collect(vault_root, ignore_dirs)

    # First pass: per-folder structural metrics.
    reports: dict[str, FolderReport] = {}
    for folder, paths in top_folders.items():
        rep = FolderReport(name=folder, note_count=len(paths))
        for p in paths:
            text = read_text(p)
            stem = os.path.splitext(os.path.basename(p))[0].lower()
            if stem in index_stems or stem == folder.lower():
                rep.has_index = True
            if not text.strip():
                rep.empty_notes += 1
            elif require_fm and not has_frontmatter(text):
                rep.missing_frontmatter += 1
        reports[folder] = rep

    # Second pass: inbound links (blocking). A link in folder A pointing at a
    # note owned by folder B counts as one inbound link for B.
    for p in all_paths:
        src_folder = folder_of_path(p, vault_root)
        text = read_text(p)
        for tgt in link_targets(text):
            tgt_stem = os.path.splitext(os.path.basename(tgt))[0].lower()
            owner = note_owner.get(tgt_stem)
            if owner and owner != src_folder and owner in reports:
                reports[owner].inbound_links += 1

    # Scoring.
    for rep in reports.values():
        score = 100
        if not rep.has_index:
            score -= 30
            rep.missing_items.append("index/MOC note")
        if rep.note_count == 0:
            score -= 40
            rep.missing_items.append("folder is empty")
        if rep.note_count and rep.note_count < 3:
            score -= 10
            rep.missing_items.append("sparse (fewer than 3 notes)")
        if rep.empty_notes:
            score -= min(20, rep.empty_notes * 5)
            rep.missing_items.append(f"{rep.empty_notes} empty note(s)")
        if rep.missing_frontmatter:
            score -= min(20, rep.missing_frontmatter * 3)
            rep.missing_items.append(f"{rep.missing_frontmatter} note(s) missing frontmatter")
        rep.completeness = max(0, score)
        # Blocking: inbound demand weighted by how incomplete the folder is.
        incompleteness = (100 - rep.completeness) / 100.0
        rep.blocking = round(rep.inbound_links * (0.5 + incompleteness), 1)

    # Rank: most-blocking first, then least complete.
    return sorted(
        reports.values(),
        key=lambda r: (-r.blocking, r.completeness, r.name),
    )


def print_table(reports: list[FolderReport]) -> None:
    matches = all(r.completeness == 100 for r in reports) if reports else True
    print(f"Vault audit — {len(reports)} top-level folder(s)")
    print(f"Structure matches standard: {'YES' if matches else 'NO'}\n")
    header = f"{'#':>2}  {'folder':<28} {'compl':>5} {'inbound':>7} {'block':>6}  missing"
    print(header)
    print("-" * len(header))
    for i, r in enumerate(reports, 1):
        missing = "; ".join(r.missing_items) or "—"
        print(f"{i:>2}  {r.name[:28]:<28} {r.completeness:>5} "
              f"{r.inbound_links:>7} {r.blocking:>6}  {missing}")
    if reports:
        print(f"\nFill next: {reports[0].name} "
              f"(blocking={reports[0].blocking}, completeness={reports[0].completeness})")


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    as_json = "--json" in argv
    config_path = None
    if "--config" in argv:
        idx = argv.index("--config")
        if idx + 1 < len(argv):
            config_path = argv[idx + 1]
            args = [a for a in args if a != config_path]

    vault_root = os.path.abspath(args[0]) if args else os.getcwd()
    if not os.path.isdir(vault_root):
        print(f"error: not a directory: {vault_root}", file=sys.stderr)
        return 2

    config = load_config(vault_root, config_path)
    reports = audit(vault_root, config)

    if as_json:
        print(json.dumps([asdict(r) for r in reports], indent=2))
    else:
        print_table(reports)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

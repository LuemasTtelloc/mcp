#!/usr/bin/env python3
"""Phase 1 thin-spot scanner for the memory-interviewer skill.

Deterministic, read-only, stdlib-only. Walks the Samuel Command vault and
surfaces where the founder's story is thin, so the skill can choose the one
gap worth a question this session.

Usage:
    python3 find_thin_spots.py <vault-root> [--json] [--config PATH] [--stub-chars N]

It reports three kinds of thin spot, each ranked by leverage (how many other
notes depend on the gap):

  1. NAMED-BUT-MISSING — a name/entity referenced in [[wikilinks]] across the
     vault that has no note of its own. The story keeps pointing at someone the
     vault can't describe. Ranked by reference count (inbound demand).
  2. STUB NOTES — notes that exist but are nearly empty (body under --stub-chars,
     default 200). Ranked by inbound links: a heavily-referenced stub blocks the
     most downstream notes.
  3. DANGLING THREADS — open `> [!todo]` callouts and `status: unrouted` cards;
     a single answer often closes these.

Per top-level folder it also prints note count, stub/empty count, and todo count
so the judgement layer (see references/interview-method.md) can weigh what
*matters* to the founder's story on top of the raw numbers.

Optional config: a JSON file at the vault root named ".memory-interviewer.json"
(or --config PATH) may override defaults, e.g.:
    {
      "ignore_dirs": [".obsidian", "_meta", "04 Memory Candidates"],
      "stub_chars": 200
    }
The candidate shelf is ignored by default so proposals aren't mistaken for canon.
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
    "04 Memory Candidates", "10 Candidate Shelves", "_inbox",
}
DEFAULT_STUB_CHARS = 200

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
FRONTMATTER_RE = re.compile(r"^﻿?---\s*\n.*?\n---\s*\n", re.DOTALL)
TODO_RE = re.compile(r">\s*\[!todo\]", re.IGNORECASE)
UNROUTED_RE = re.compile(r"^status:\s*unrouted\s*$", re.IGNORECASE | re.MULTILINE)


@dataclass
class FolderReport:
    name: str
    note_count: int = 0
    stub_notes: int = 0
    empty_notes: int = 0
    todo_count: int = 0


@dataclass
class ThinSpot:
    kind: str          # "named-missing" | "stub" | "dangling"
    label: str         # the entity name or note path
    folder: str = ""   # owning top-level folder, if any
    demand: int = 0    # inbound references / leverage
    detail: str = ""


def load_config(vault_root: str, config_path: str | None) -> dict:
    path = config_path or os.path.join(vault_root, ".memory-interviewer.json")
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


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def wikilink_targets(text: str) -> list[str]:
    return [m.strip() for m in WIKILINK_RE.findall(text) if m.strip()]


def folder_of_path(path: str, vault_root: str) -> str | None:
    rel = os.path.relpath(path, vault_root)
    parts = rel.split(os.sep)
    return parts[0] if len(parts) > 1 else None


def collect(vault_root: str, ignore_dirs: set[str]):
    """Return (md paths, note_stem -> owning folder)."""
    all_paths: list[str] = []
    note_owner: dict[str, str] = {}
    for entry in sorted(os.listdir(vault_root)):
        full = os.path.join(vault_root, entry)
        if not os.path.isdir(full) or entry in ignore_dirs or entry.startswith("."):
            continue
        for root, dirs, files in os.walk(full):
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith(".")]
            for fn in files:
                if is_md(fn):
                    p = os.path.join(root, fn)
                    all_paths.append(p)
                    stem = os.path.splitext(fn)[0].lower()
                    note_owner.setdefault(stem, entry)
    return all_paths, note_owner


def scan(vault_root: str, config: dict):
    ignore_dirs = set(config.get("ignore_dirs", [])) | DEFAULT_IGNORE_DIRS
    stub_chars = int(config.get("stub_chars", DEFAULT_STUB_CHARS))

    all_paths, note_owner = collect(vault_root, ignore_dirs)

    folders: dict[str, FolderReport] = {}
    stub_inbound: dict[str, int] = {}      # note stem -> inbound link count
    stub_meta: dict[str, tuple[str, str]] = {}  # stem -> (rel path, folder)
    missing_demand: dict[str, int] = {}    # referenced name with no note -> count
    dangling: list[ThinSpot] = []

    # Pass 1: per-note structural metrics + record stubs.
    for p in all_paths:
        folder = folder_of_path(p, vault_root) or "(root)"
        rep = folders.setdefault(folder, FolderReport(name=folder))
        rep.note_count += 1

        text = read_text(p)
        body = strip_frontmatter(text).strip()
        stem = os.path.splitext(os.path.basename(p))[0].lower()

        if not body:
            rep.empty_notes += 1
            stub_meta[stem] = (os.path.relpath(p, vault_root), folder)
        elif len(body) < stub_chars:
            rep.stub_notes += 1
            stub_meta[stem] = (os.path.relpath(p, vault_root), folder)

        todos = len(TODO_RE.findall(text))
        rep.todo_count += todos
        if todos:
            dangling.append(ThinSpot(
                kind="dangling", label=os.path.relpath(p, vault_root),
                folder=folder, demand=todos, detail=f"{todos} open [!todo]"))
        if UNROUTED_RE.search(text):
            dangling.append(ThinSpot(
                kind="dangling", label=os.path.relpath(p, vault_root),
                folder=folder, demand=1, detail="status: unrouted"))

    # Pass 2: inbound link demand — for missing entities and for stubs.
    for p in all_paths:
        for tgt in wikilink_targets(read_text(p)):
            tgt_stem = os.path.splitext(os.path.basename(tgt))[0].lower()
            if tgt_stem in note_owner:
                if tgt_stem in stub_meta:
                    stub_inbound[tgt_stem] = stub_inbound.get(tgt_stem, 0) + 1
            else:
                # referenced but no note exists anywhere — named-but-missing
                missing_demand[tgt] = missing_demand.get(tgt, 0) + 1

    named_missing = [
        ThinSpot(kind="named-missing", label=name, demand=count,
                 detail=f"referenced {count}× , no note")
        for name, count in missing_demand.items()
    ]
    stubs = [
        ThinSpot(kind="stub", label=stub_meta[stem][0], folder=stub_meta[stem][1],
                 demand=stub_inbound.get(stem, 0),
                 detail=f"{stub_inbound.get(stem, 0)} inbound link(s)")
        for stem in stub_meta
    ]

    named_missing.sort(key=lambda s: (-s.demand, s.label.lower()))
    stubs.sort(key=lambda s: (-s.demand, s.label.lower()))
    dangling.sort(key=lambda s: (-s.demand, s.label.lower()))

    ranked_folders = sorted(
        folders.values(),
        key=lambda r: (-(r.empty_notes + r.stub_notes + r.todo_count), r.name),
    )
    return ranked_folders, named_missing, stubs, dangling


def print_report(folders, named_missing, stubs, dangling) -> None:
    def top(items, n=10):
        return items[:n]

    print("Memory Interviewer — thin-spot scan\n")

    print("NAMED-BUT-MISSING (referenced people/entities with no note) — highest leverage")
    if named_missing:
        for i, s in enumerate(top(named_missing), 1):
            print(f"  {i:>2}. {s.label:<32} {s.detail}")
    else:
        print("  — none found")

    print("\nSTUB / EMPTY NOTES (exist but near-empty), ranked by inbound demand")
    if stubs:
        for i, s in enumerate(top(stubs), 1):
            print(f"  {i:>2}. {s.label:<40} [{s.folder}]  {s.detail}")
    else:
        print("  — none found")

    print("\nDANGLING THREADS (open todos / unrouted)")
    if dangling:
        for i, s in enumerate(top(dangling), 1):
            print(f"  {i:>2}. {s.label:<40} [{s.folder}]  {s.detail}")
    else:
        print("  — none found")

    print("\nPER-FOLDER SUMMARY")
    header = f"  {'folder':<28} {'notes':>5} {'stub':>5} {'empty':>5} {'todo':>5}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for r in folders:
        print(f"  {r.name[:28]:<28} {r.note_count:>5} {r.stub_notes:>5} "
              f"{r.empty_notes:>5} {r.todo_count:>5}")

    # Single recommendation: the highest-leverage thin spot overall.
    best = None
    if named_missing:
        best = ("named-but-missing person/entity", named_missing[0].label,
                named_missing[0].detail)
    elif stubs and stubs[0].demand > 0:
        best = ("heavily-referenced stub", stubs[0].label, stubs[0].detail)
    elif dangling:
        best = ("dangling thread", dangling[0].label, dangling[0].detail)
    if best:
        print(f"\nAsk-about-next: {best[0]} — {best[1]} ({best[2]})")
    else:
        print("\nAsk-about-next: vault looks well-covered; pick a depth question by judgement.")


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    as_json = "--json" in argv
    config_path = None
    if "--config" in argv:
        idx = argv.index("--config")
        if idx + 1 < len(argv):
            config_path = argv[idx + 1]
            args = [a for a in args if a != config_path]
    cli_stub = None
    if "--stub-chars" in argv:
        idx = argv.index("--stub-chars")
        if idx + 1 < len(argv):
            try:
                cli_stub = int(argv[idx + 1])
            except ValueError:
                print("warning: --stub-chars expects an integer", file=sys.stderr)
            args = [a for a in args if a != argv[idx + 1]]

    vault_root = os.path.abspath(args[0]) if args else os.getcwd()
    if not os.path.isdir(vault_root):
        print(f"error: not a directory: {vault_root}", file=sys.stderr)
        return 2

    config = load_config(vault_root, config_path)
    if cli_stub is not None:
        config["stub_chars"] = cli_stub

    folders, named_missing, stubs, dangling = scan(vault_root, config)

    if as_json:
        print(json.dumps({
            "folders": [asdict(f) for f in folders],
            "named_missing": [asdict(s) for s in named_missing],
            "stubs": [asdict(s) for s in stubs],
            "dangling": [asdict(s) for s in dangling],
        }, indent=2))
    else:
        print_report(folders, named_missing, stubs, dangling)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

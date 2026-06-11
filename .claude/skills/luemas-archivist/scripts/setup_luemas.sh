#!/bin/zsh
# Luemas one-time migration — sets up the Desk / Out Tray / Library model.
# See .claude/LUEMAS-ARCHITECTURE.md ("One-time migration").
#
# SAFE BY DEFAULT: running with no arguments is a DRY RUN that only prints what
# it would do. Run with --apply to actually make changes. Never deletes a file;
# only creates folders and moves files (collisions get a numeric suffix).
#
# Usage (on the Mac Studio):
#   ./setup_luemas.sh             # dry run — review the plan
#   ./setup_luemas.sh --apply     # do it
#
# Optional environment overrides:
#   LUEMAS_HOME      default: $HOME/Luemas
#   OLD_ARCHIVE      default: auto-detect "HoWA Index"/"HoWA Index Intake" on Desktop/Documents
#   OUT_TRAY         default: $HOME/Desktop/Out Tray

set -euo pipefail

APPLY=false
[[ "${1:-}" == "--apply" ]] && APPLY=true

LUEMAS_HOME="${LUEMAS_HOME:-$HOME/Luemas}"
LIBRARY="$LUEMAS_HOME/Library"
OUT_TRAY="${OUT_TRAY:-$HOME/Desktop/Out Tray}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$(cd "$SCRIPT_DIR/../.." && pwd)"   # .claude/skills
SKILLS_DST="$HOME/.claude/skills"

note()  { print -- "  $1"; }
plan()  { print -- "PLAN  $1"; }
did()   { print -- "DONE  $1"; }

run() {  # run "description" cmd args...
  local desc="$1"; shift
  if $APPLY; then "$@" && did "$desc"; else plan "$desc"; fi
}

# Move a file/folder into a destination dir, suffixing on collision. Never overwrites.
move_into() {
  local src="$1" dstdir="$2"
  local base="${src:t}" target="$dstdir/${src:t}" n=1
  local stem="${base%.*}" ext=""
  [[ "$base" == *.* && "$base" != .* ]] && ext=".${base##*.}"
  while [[ -e "$target" ]]; do
    target="$dstdir/$stem ($n)$ext"
    (( n++ ))
  done
  run "move '$src' -> '$target'" mv -n "$src" "$target"
}

print "Luemas migration — $($APPLY && echo 'APPLYING' || echo 'DRY RUN (pass --apply to execute)')"
print "  LUEMAS_HOME: $LUEMAS_HOME"
print "  Library:     $LIBRARY"
print "  Out Tray:    $OUT_TRAY"
print ""

# ── 1. The Library (rename the old "HoWA Index" archive) ────────────────────
print "── Step 1: Library"
if [[ -d "$LIBRARY" ]]; then
  note "Library already exists — leaving it alone."
else
  OLD_ARCHIVE="${OLD_ARCHIVE:-}"
  if [[ -z "$OLD_ARCHIVE" ]]; then
    for cand in "$HOME/Desktop/HoWA Index Intake" "$HOME/Desktop/HoWA Index" \
                "$HOME/Documents/HoWA Index Intake" "$HOME/Documents/HoWA Index"; do
      [[ -d "$cand" ]] && OLD_ARCHIVE="$cand" && break
    done
  fi
  run "create $LUEMAS_HOME" mkdir -p "$LUEMAS_HOME"
  if [[ -n "$OLD_ARCHIVE" && -d "$OLD_ARCHIVE" ]]; then
    note "found old archive: $OLD_ARCHIVE"
    run "rename old archive -> $LIBRARY" mv -n "$OLD_ARCHIVE" "$LIBRARY"
  else
    note "no 'HoWA Index' folder auto-detected (set OLD_ARCHIVE=/path to point at it)"
    run "create empty Library at $LIBRARY" mkdir -p "$LIBRARY"
  fi
fi

# ── 2. The Out Tray ──────────────────────────────────────────────────────────
print "\n── Step 2: Out Tray"
if [[ -d "$OUT_TRAY" ]]; then
  note "Out Tray already exists."
else
  run "create '$OUT_TRAY'" mkdir -p "$OUT_TRAY"
fi

# ── 3. Retire the five intake folders into the Out Tray ─────────────────────
print "\n── Step 3: retire old intake folders"
for name in "Personal Intake" "AI Command Intake" "HoWA Intake" "Voice Notes" "Screenshots"; do
  src="$HOME/Desktop/$name"
  if [[ -d "$src" ]]; then
    # move contents (incl. dotfile-free), then remove the empty folder
    found=false
    for item in "$src"/*(N) "$src"/.*(N); do
      [[ "${item:t}" == "." || "${item:t}" == ".." || "${item:t}" == ".DS_Store" ]] && continue
      move_into "$item" "$OUT_TRAY"; found=true
    done
    $found || note "'$name' is empty"
    run "remove empty folder '$src'" rmdir "$src" 2>/dev/null || note "'$name' not empty after move — left in place"
  else
    note "'$name' not found — skipping"
  fi
done

# ── 4. Skills install ────────────────────────────────────────────────────────
print "\n── Step 4: install skills"
run "create $SKILLS_DST" mkdir -p "$SKILLS_DST"
for skill in luemas-archivist vault-gap-filler; do
  if [[ -d "$SKILLS_SRC/$skill" ]]; then
    run "install skill '$skill'" cp -R "$SKILLS_SRC/$skill" "$SKILLS_DST/"
  else
    note "skill source not found: $SKILLS_SRC/$skill (run this script from the repo checkout)"
  fi
done

# ── Done ─────────────────────────────────────────────────────────────────────
print ""
if $APPLY; then
  print "Migration applied. Next:"
else
  print "Dry run complete — nothing changed. Re-run with --apply to execute. Then:"
fi
print "  1. Drag any finished work into '$OUT_TRAY'"
print "  2. Run:  claude -p \"empty my Out Tray\""
print "  3. Check the routing; when happy, enable the schedule:"
print "     see ~/.claude/skills/luemas-archivist/references/autonomy.md"

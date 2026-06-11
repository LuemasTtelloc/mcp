# TONIGHT — Autopilot + back up the whole brain to the private repo

**For:** Claude Code on the Mac Studio. Run interactively
(`cd ~/luemas-setup && git pull && claude "read .claude/CONSOLIDATE-AND-AUTOPILOT-BRIEF.md and carry it out"`).
**Posture:** back up before changing; one step at a time; ask before anything
destructive; nothing deleted. Report into `~/Leumas/Command Centre.md` at the end.

---

## PHASE 0 — Privacy gate (HARD STOP)

Confirm the git remote of this repo is **private**:
`git remote -v` → then the user confirms in GitHub Desktop that the repo shows
**Private**. **If it is public, do PHASE 1 only and skip PHASE 2/3 entirely** —
never push personal/operational config to a public repo. Report the block.

---

## PHASE 1 — Switch on the Archivist schedule (autopilot)

The scheduled run must write Memory Cards into the Samuel Command Vault, which
currently lives under `~/Documents` — TCC-blocked for launchd. Fix with the
**least-broad** Full Disk Access grant, NOT a vault move tonight.

1. Install the schedule: copy the launchd plist from
   `.claude/skills/leumas-archivist/references/autonomy.md` to
   `~/Library/LaunchAgents/com.leumas.archivist.plist` (08:00 + 18:00), edit
   paths, and merge the scoped `permissions.allow` rules from that same file
   into `~/.claude/settings.json` (add, don't replace).
2. **Full Disk Access:** grant it to the *specific* binary the schedule runs
   (the `claude` executable, or a tiny dedicated wrapper script the plist
   calls) via System Settings → Privacy & Security → Full Disk Access.
   **Do NOT grant FDA to `/usr/bin/python3` or `/bin/zsh`** — too broad. If only
   a broad target is possible, stop and ask the user first.
3. `launchctl load` the plist, then `launchctl kickstart -k gui/$(id -u)/com.leumas.archivist`.
   Verify: a clean run in `~/Library/Logs/leumas-archivist.log`, a test file in
   the Out Tray gets filed, a card lands on the candidate shelf, and the
   Command Centre updates. If the vault write still fails, report and fall back
   to manual-only (do not widen FDA without asking).
4. Optional now that TCC is solved for this runner: restore the HoWA canon root
   to the FTS index job (re-add `~/Documents/HoWA`) IF that job runs under the
   same FDA'd runner; otherwise leave it on the Leumas-only corpus.

---

## PHASE 2 — Back up the live brain to the repo (private only)

Goal: every prompt, skill, agent script, and direction in ONE versioned place.
Create `mac-config/` at the repo root and copy in (do not move — leave originals
running):

- `~/.openclaw/workspace/scripts/`  → `mac-config/openclaw-scripts/`
- `~/Library/LaunchAgents/com.samuel.*.plist` and `_retired/` → `mac-config/launch-agents/`
- `~/.agents/skills/` (e.g. `samuel-spiritual-guru`) → `mac-config/agents-skills/`
- the morning-questions / daily-reflection prompt + any email templates → `mac-config/prompts/`
- `crontab -l` output → `mac-config/crontab.txt`
- a generated `mac-config/INVENTORY.md` listing every agent, its trigger, and source path

### SECRET SCRUB (mandatory, before any commit)
1. Scan everything staged for secrets:
   `grep -rniE 'token|secret|api[_-]?key|password|bearer|OPENCLAW_GATEWAY_TOKEN|sk-[a-z0-9]' mac-config/`
2. For every hit: replace the value with `<REDACTED — see Mac keychain/env>`.
   Known example: `OPENCLAW_GATEWAY_TOKEN`. Also strip anything resembling the
   `Victoria80` password incident.
3. Harden `.gitignore` (append) so these can never be committed:
   ```
   # Leumas: never commit secrets, vault content, or evidence
   mac-config/**/*.env
   mac-config/**/*.key
   mac-config/**/*token*
   mac-config/**/secrets*
   **/Library/**            # the evidence Library
   **/*_INDEX_LANCE/**
   **/*.db
   ```
4. Re-run the grep. Only commit when it returns nothing sensitive.
5. `git add mac-config .gitignore && git commit && git push`.

If unsure whether a file is safe, EXCLUDE it and list it in INVENTORY.md as
"held back — review", rather than risk committing a secret.

---

## PHASE 3 — Report
Update `~/Leumas/Command Centre.md`: autopilot status (schedule live?), what was
backed up, what was held back for security, and the one deferred task (full
vault relocation out of ~/Documents). Tell the user plainly what is now done.

---

## DEFERRED (future session, not tonight)
Move the two vaults from `~/Documents` into `~/Leumas`, repointing Obsidian, the
two vault MCP servers, the Claude Desktop config, and any launchd paths. FDA
makes this optional, so do it fresh — not at the end of a long day.

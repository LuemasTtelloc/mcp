# Making the Archivist Autonomous (Mac Studio)

The brief wants the Archivist to run on its own (Layer 2). Don't build a bespoke
file-watcher daemon — schedule a headless Claude Code run. Start **on-demand**,
trust the routing for a week, then turn on the schedule.

## Step 1 — Permissions (required, or scheduled runs will stall)

The first live run confirmed it: headless `claude -p` cannot answer permission
prompts, so file moves get blocked unless pre-approved. Scope the approval
tightly — allow moving/writing in the tray, Library, and vaults; deny everything
else — with `--permission-mode dontAsk` plus explicit allow rules.

Add to `~/.claude/settings.json` on the Mac Studio (edit the vault path):

```json
{
  "permissions": {
    "allow": [
      "Bash(mv *)",
      "Bash(python3 *)",
      "Read",
      "Write(~/Leumas/**)",
      "Write(~/Desktop/Out Tray/**)",
      "Write(~/<path-to-vaults>/**)"
    ],
    "additionalDirectories": [
      "~/Desktop",
      "~/Leumas",
      "~/<path-to-vaults>"
    ]
  }
}
```

Notes: rule syntax is `Bash(mv *)` (the space before `*` is a word boundary —
matches `mv x y`, not `mvedit`); `additionalDirectories` grants file access to
paths outside the working directory. With `dontAsk`, anything not on the allow
list is silently denied rather than prompting — the safe failure mode for cron.

## Option A — `launchd` (recommended on macOS)

Save as `~/Library/LaunchAgents/com.leumas.archivist.plist`, edit the paths,
then `launchctl load ~/Library/LaunchAgents/com.leumas.archivist.plist`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>              <string>com.leumas.archivist</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>-lc</string>
    <!-- runs headless; -p is print/non-interactive mode -->
    <string>cd /Users/luemasttelloc/Leumas && claude -p "empty my Out Tray" --permission-mode dontAsk --add-dir ~/Desktop --add-dir ~/Leumas >> ~/Library/Logs/leumas-archivist.log 2>&1</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>
    <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
    <dict><key>Hour</key><integer>18</integer><key>Minute</key><integer>0</integer></dict>
  </array>
  <key>StandardErrorPath</key>   <string>/Users/luemasttelloc/Library/Logs/leumas-archivist.err</string>
  <key>StandardOutPath</key>     <string>/Users/luemasttelloc/Library/Logs/leumas-archivist.log</string>
</dict>
</plist>
```

Runs the archivist at 08:00 and 18:00 daily. Adjust the times/cadence freely.

## Option B — cron

```cron
0 8,18 * * *  cd /Users/luemasttelloc/Leumas && /usr/local/bin/claude -p "empty my Out Tray" --permission-mode dontAsk --add-dir ~/Desktop --add-dir ~/Leumas >> ~/Library/Logs/leumas-archivist.log 2>&1
```

## Engine Room reporting

Each run should append one status line the AI Engine Room can read (agent name,
last run, counts, errors). Point the log path above at wherever the Engine Room
tails agent activity, or have the archivist write a `_meta/agent-status.json`
entry on each run:

```json
{"agent": "archivist", "last_run": "<iso8601>", "archived": 0, "cards": {"samuel": 0, "howa": 0}, "held": 0, "errors": 0}
```

## Guardrails for unattended runs

- Idempotent: re-running over already-archived files must not duplicate them
  (the triage script reports what's already in the archive).
- Never delete; archive is immutable.
- Anything it can't confidently route goes to `Samuel/_inbox` (`status:
  unrouted`) for your review — autonomy must never guess into a vault.
- Keep a per-run log so a bad batch can be traced and reverted at the card
  level (cards are reversible; the archive is not touched destructively).

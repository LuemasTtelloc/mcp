# Making the Memory Interviewer Autonomous (Mac Studio)

Like the Archivist, don't build a bespoke daemon — schedule a headless Claude
Code run. **Start on-demand.** Per the architecture's "no agent before the last
is trusted" rule, review a week of questions and the cards they produce before
turning the schedule on.

## Step 1 — Permissions (or scheduled runs stall)

Headless `claude -p` cannot answer permission prompts. Scope tightly: the
Interviewer only needs to **read** the Samuel vault and **write** to its
candidate shelf (plus send the questions). Deny everything else with
`--permission-mode dontAsk` plus explicit allow rules.

Add to `~/.claude/settings.json` on the Mac Studio (edit the vault path; note the
double-slash `//` prefix for absolute paths in file-tool rules):

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(python3 *)",
      "Write(//Users/luemasttelloc/Documents/Samuel Command Vault/04 Memory Candidates/**)"
    ],
    "additionalDirectories": [
      "//Users/luemasttelloc/Documents/Samuel Command Vault"
    ]
  }
}
```

It must **not** be allowed to write into vault canon — only the
`04 Memory Candidates/` shelf. That is the review gate; keep it narrow.

## Option A — `launchd` (recommended on macOS)

Save as `~/Library/LaunchAgents/com.leumas.memory-interviewer.plist`, edit the
paths, then `launchctl load ~/Library/LaunchAgents/com.leumas.memory-interviewer.plist`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>              <string>com.leumas.memory-interviewer</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>-lc</string>
    <string>cd "/Users/luemasttelloc/Documents/Samuel Command Vault" && claude -p "run the memory interview" --permission-mode dontAsk --add-dir "/Users/luemasttelloc/Documents/Samuel Command Vault" >> ~/Library/Logs/leumas-memory-interviewer.log 2>&1</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>
    <dict><key>Hour</key><integer>6</integer><key>Minute</key><integer>30</integer></dict>
  </array>
  <key>StandardErrorPath</key>   <string>/Users/luemasttelloc/Library/Logs/leumas-memory-interviewer.err</string>
  <key>StandardOutPath</key>     <string>/Users/luemasttelloc/Library/Logs/leumas-memory-interviewer.log</string>
</dict>
</plist>
```

Runs at 06:30 daily — alongside the existing `morning-questions` reflection
email. Once trusted, the Interviewer should *supply* `morning-questions` its
questions (vault-derived) rather than the fixed list, then replace it. Until
then, stagger them or pick one so Samuel isn't asked twice.

## Option B — cron

```cron
30 6 * * *  cd "/Users/luemasttelloc/Documents/Samuel Command Vault" && /usr/local/bin/claude -p "run the memory interview" --permission-mode dontAsk --add-dir "/Users/luemasttelloc/Documents/Samuel Command Vault" >> ~/Library/Logs/leumas-memory-interviewer.log 2>&1
```

## Engine Room reporting

Append one status line per run wherever the Engine Room tails agent activity
(mirrors the Archivist's `_meta/agent-status.json` shape):

```json
{"agent": "memory-interviewer", "last_run": "<iso8601>", "thin_spot": "<what>", "questions": 0, "answered": 0, "cards": 0, "errors": 0}
```

## Guardrails for unattended runs

- **One thin spot per run.** Never interview the whole vault at once.
- **Never write canon.** Cards land only on the `04 Memory Candidates/` shelf.
- **Never re-ask.** Read the ledger first; skip answered/declined threads.
- **No answer, no card.** If Samuel doesn't reply, the run logs the open
  question and stops — it never fabricates an answer.
- **Don't double-ask.** Coordinate with `morning-questions` so the founder gets
  one set of questions a day, not two.

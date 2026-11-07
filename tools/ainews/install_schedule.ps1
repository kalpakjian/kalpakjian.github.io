<#
  install_schedule.ps1 - register the 10-minute AINews poll with Task Scheduler.

  What gets scheduled: detect.py against the most recent payload.json that an
  agent session wrote. The Gmail fetch itself is NOT schedulable from a plain
  batch file (it needs the Composio MCP tool), so the split is:

      agent session (every 10 min, or on demand)
          -> GMAIL_FETCH_EMAILS -> tools/ainews/out/payload.json
      scheduled task (every 10 min, independent of the agent)
          -> run_ainews_poll.ps1 -PayloadFile out/payload.json

  If the payload is stale, the poll simply reports "nothing new", so the two
  halves can run at different cadences without coordinating.

  Usage:
    pwsh -File tools/ainews/install_schedule.ps1              # install/update (2h)
    pwsh -File tools/ainews/install_schedule.ps1 -EveryMinutes 60
    pwsh -File tools/ainews/install_schedule.ps1 -Remove      # uninstall
    pwsh -File tools/ainews/install_schedule.ps1 -WhatIfOnly  # print, do nothing

  Why 2 hours and not 10 minutes:
    AINews publishes at most once a day. At a 10-minute cadence that is ~143
    runs per issue, ~142 of them pure no-ops. Two hours cuts that to ~12 while
    the worst-case lag stays under a digest's writing time (and the idempotent
    ledger means a run that finds nothing costs one IMAP SEARCH).

    The cadence is a latency/effort trade-off, not a correctness one: the ledger
    keys on messageId, so any cadence is safe -- only how long you wait changes.

  Runs as the current user, in the current user's session, so a toast is visible.
  No admin rights required (-RunLevel Limited); registering for all users would
  need elevation and is deliberately not attempted.
#>
[CmdletBinding()]
param(
    [int]$EveryMinutes = 120,
    [switch]$Remove,
    [switch]$WhatIfOnly,
    [string]$TaskName = 'AINews Poll'
)

$ErrorActionPreference = 'Stop'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent (Split-Path -Parent $here)
$poll = Join-Path $here 'run_ainews_poll.ps1'

if ($Remove) {
    if ($WhatIfOnly) { Write-Host "would unregister: $TaskName"; exit 0 }
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "removed task: $TaskName"
    } else {
        Write-Host "not installed: $TaskName"
    }
    exit 0
}

$pwsh = (Get-Command pwsh -ErrorAction SilentlyContinue).Source
if (-not $pwsh) { $pwsh = (Get-Command powershell).Source }

# NO -PayloadFile: that switch selects the stage-1-only replay mode. Without it
# the script runs the full chain (detect -> IMAP fetch -> extract -> brief ->
# figures), which is what a scheduled job is for. An earlier version pinned
# -PayloadFile here and silently reduced every scheduled run to detection only.
$argLine = '-NoProfile -ExecutionPolicy Bypass -File "{0}" -Quiet' -f $poll

$action = New-ScheduledTaskAction -Execute $pwsh -Argument $argLine -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes $EveryMinutes)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew `
    -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive -RunLevel Limited

Write-Host "task      : $TaskName"
Write-Host "every     : $EveryMinutes min"
Write-Host "exec      : $pwsh"
Write-Host "args      : $argLine"
Write-Host "workdir   : $root"

if ($WhatIfOnly) { Write-Host '(what-if: nothing registered)'; exit 0 }

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal -Force | Out-Null

$t = Get-ScheduledTask -TaskName $TaskName
Write-Host ("installed : state=" + $t.State)
Write-Host ("next run  : " + (Get-ScheduledTaskInfo -TaskName $TaskName).NextRunTime)
Write-Host "log       : $(Join-Path $here 'out\poll.log')"

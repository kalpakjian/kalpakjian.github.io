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
    pwsh -File tools/ainews/install_schedule.ps1              # install/update
    pwsh -File tools/ainews/install_schedule.ps1 -EveryMinutes 5
    pwsh -File tools/ainews/install_schedule.ps1 -Remove      # uninstall
    pwsh -File tools/ainews/install_schedule.ps1 -WhatIfOnly  # print, do nothing

  Runs as the current user, in the current user's session, so a toast is visible.
  No admin rights required (-RunLevel Limited); registering for all users would
  need elevation and is deliberately not attempted.
#>
[CmdletBinding()]
param(
    [int]$EveryMinutes = 10,
    [switch]$Remove,
    [switch]$WhatIfOnly,
    [string]$TaskName = 'AINews Poll'
)

$ErrorActionPreference = 'Stop'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent (Split-Path -Parent $here)
$poll = Join-Path $here 'run_ainews_poll.ps1'
$payload = Join-Path $here 'out\payload.json'

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

$argLine = '-NoProfile -ExecutionPolicy Bypass -File "{0}" -PayloadFile "{1}" -Quiet' -f $poll, $payload

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

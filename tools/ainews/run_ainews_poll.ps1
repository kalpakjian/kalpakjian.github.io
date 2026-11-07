<#
  run_ainews_poll.ps1 - poll Gmail for a new AINews issue and shout about it.

  Scope (deliberately narrow): DETECT + RECORD + NOTIFY. This script does not
  draft, does not call a model, and does not publish. It exists so the writing
  pipeline can be added later without re-deciding any of this.

  Why a 10-minute timer instead of "once a day":
    Observed arrival times (UTC) are 05:35, 19:18, 06:24, 10:36, 03:05 -- there
    is no daily hour that is "soon after". Detection is cheap and, more
    importantly, idempotent: detect.py keys the write on Gmail messageId, so
    running this every 10 minutes can never produce a second alert or a second
    ledger row for the same issue. Frequency therefore costs nothing but buys
    up to 10 minutes of latency instead of up to 24 hours.

  Two ways to run:

    1) Scheduled (recommended) -- the fetch step needs the Composio MCP tool,
       which lives inside an agent session. Schedule the *agent* to run this
       prompt every 10 minutes; it fetches, saves payload.json, then runs:
           pwsh -File tools/ainews/run_ainews_poll.ps1 -PayloadFile out\payload.json

    2) Standalone (no fetch) -- replay an already-saved payload:
           pwsh -File tools/ainews/run_ainews_poll.ps1 -PayloadFile fixtures\sample-payload.json -DryRun

  Exit codes:
    0 = nothing new (the usual, quiet case)
    2 = new issue(s) found; `-Once`-style callers should raise a toast/beep
    1 = error

  The notifier is intentionally dumb: toast via BurntToast if installed, else a
  MessageBox-free console banner + beep, plus a JSONL file the future writer
  stage can pick up. No network, no credentials.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PayloadFile,

    # Report but never touch the ledger.
    [switch]$DryRun,

    # Where new-issues.jsonl is written (default: tools/ainews/out).
    [string]$NotifyDir,

    # Suppress the Windows toast/beep (useful under Task Scheduler).
    [switch]$Quiet
)

$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent (Split-Path -Parent $here)
if (-not $NotifyDir) { $NotifyDir = Join-Path $here 'out' }

function Write-Step([string]$msg) { Write-Host ("[ainews] " + $msg) }

# --- 1. detect ---------------------------------------------------------------
$args = @((Join-Path $here 'detect.py'), '--input', $PayloadFile, '--notify-dir', $NotifyDir)
if ($DryRun) { $args += '--dry-run' }

Write-Step ("payload = " + $PayloadFile)
$output = & python @args 2>&1
$code = $LASTEXITCODE
$output | ForEach-Object { Write-Host $_ }

# detect.py: 0 = nothing new, 2 = new, 1 = error
if ($code -eq 1) {
    Write-Step 'FAILED (detector error)'
    exit 1
}
if ($code -eq 0) {
    Write-Step 'nothing new'
    $log0 = Join-Path $NotifyDir 'poll.log'
    $stamp0 = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    Add-Content -LiteralPath $log0 -Encoding UTF8 -Value ("$stamp0  new=0  payload=" + (Split-Path -Leaf $PayloadFile))
    exit 0
}

# --- 2. notify ---------------------------------------------------------------
$alertFile = Join-Path $NotifyDir 'new-issues.jsonl'
$new = @()
if (Test-Path -LiteralPath $alertFile) {
    $new = Get-Content -LiteralPath $alertFile -Encoding UTF8 | Where-Object { $_.Trim() }
}
$count = $new.Count
if ($count -eq 0) { $count = 1 }   # detector said "new" but the file is missing
$alertStamp = (Get-Item -LiteralPath $alertFile -ErrorAction SilentlyContinue).LastWriteTimeUtc

$summary = "AINews: $count new issue(s)"
Write-Step $summary
foreach ($line in $new) { Write-Step ("  " + $line) }

if (-not $Quiet) {
    # BurntToast is optional; fall back to a console banner + beep so the script
    # has no hard dependency on a PowerShell Gallery module.
    $toasted = $false
    if (Get-Module -ListAvailable -Name BurntToast) {
        try {
            Import-Module BurntToast -ErrorAction Stop
            New-BurntToastNotification -Text 'New AINews issue', $summary | Out-Null
            $toasted = $true
        } catch { $toasted = $false }
    }
    if (-not $toasted) {
        for ($i = 0; $i -lt 3; $i++) { [Console]::Beep(880, 180); Start-Sleep -Milliseconds 120 }
        Write-Host ''
        Write-Host ('=' * 68) -ForegroundColor Yellow
        Write-Host '  NEW AINEWS ISSUE -- 導讀待撰寫' -ForegroundColor Yellow
        Write-Host ('  alert: ' + $alertFile) -ForegroundColor Yellow
        Write-Host ('=' * 68) -ForegroundColor Yellow
    }
}

# --- 3. refresh the log ------------------------------------------------------
$log = Join-Path $NotifyDir 'poll.log'
$stamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
Add-Content -LiteralPath $log -Encoding UTF8 -Value ("$stamp  new=$count  payload=" + (Split-Path -Leaf $PayloadFile))

exit 2

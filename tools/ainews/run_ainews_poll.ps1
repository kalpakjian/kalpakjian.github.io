<#
  run_ainews_poll.ps1 - scheduled AINews job (detect -> fetch -> materials).

  Two modes, because the cheap half and the expensive half have different needs:

    -PayloadFile given   : stage 1 only (ledger + notify), replaying a saved
                           GMAIL_FETCH_EMAILS payload. No credentials needed.
    (no -PayloadFile)    : full chain -- detect, then pipeline.py which IMAP-fetches
                           any issue missing a message.json and produces
                           source.txt / extract.json / brief / figures.

  The full chain needs GMAIL_USER and GMAIL_APP_PASSWORD in the environment.
  Without them it degrades to "nothing new" instead of failing the task, because a
  missing credential must not look like a broken pipeline in the log.

  Exit codes: 0 = nothing new, 2 = new issue(s) / materials produced, 1 = error.
#>
[CmdletBinding()]
param(
    [string]$PayloadFile,
    [switch]$DryRun,
    [string]$NotifyDir,
    [switch]$Quiet
)

$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent (Split-Path -Parent $here)
if (-not $NotifyDir) { $NotifyDir = Join-Path $here 'out' }

function Write-Step([string]$msg) { Write-Host ("[ainews] " + $msg) }

function Write-PollLog([string]$line) {
    $log = Join-Path $NotifyDir 'poll.log'
    $stamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    Add-Content -LiteralPath $log -Encoding UTF8 -Value ("$stamp  " + $line)
}

if (-not $PayloadFile) {
    # ---- full chain: everything except writing and publishing ----------------
    $hasCreds = $env:GMAIL_USER -and $env:GMAIL_APP_PASSWORD
    Write-Step ("full chain (credentials: " + $(if ($hasCreds) { "present" } else { "MISSING" }) + ")")

    # Missing credentials are a CONFIG state, not a fault: exit 0 with a clear
    # log line so Task Scheduler does not show a red run every 10 minutes for a
    # condition the user has not acted on yet. The real error still surfaces the
    # moment the chain runs with credentials present.
    if (-not $hasCreds) {
        Write-Step 'no GMAIL_USER / GMAIL_APP_PASSWORD -> skipping fetch (stage 1 only)'
        Write-PollLog 'chain=skipped (no credentials)'
        exit 0
    }

    $args = @((Join-Path $here 'pipeline.py'), '--qa')
    if ($DryRun) { $args += '--dry-run' }
    $out = & python @args 2>&1
    $code = $LASTEXITCODE
    $out | ForEach-Object { Write-Host $_ }

    if ($code -eq 1) {
        Write-PollLog 'chain=error'
        Write-Step 'FAILED'
        exit 1
    }
    Write-PollLog ("chain=ok code=$code")
    if ($code -eq 2) {
        if (-not $Quiet) {
            for ($i = 0; $i -lt 3; $i++) { [Console]::Beep(880, 180); Start-Sleep -Milliseconds 120 }
            Write-Host ''
            Write-Host ('=' * 68) -ForegroundColor Yellow
            Write-Host '  NEW AINEWS MATERIALS -- 導讀待撰寫' -ForegroundColor Yellow
            Write-Host ('  ' + (Join-Path $here 'out')) -ForegroundColor Yellow
            Write-Host ('=' * 68) -ForegroundColor Yellow
        }
        exit 2
    }
    Write-Step 'nothing new'
    exit 0
}

# ---- stage 1 only: replay a saved payload -----------------------------------
$args = @((Join-Path $here 'detect.py'), '--input', $PayloadFile, '--notify-dir', $NotifyDir)
if ($DryRun) { $args += '--dry-run' }

Write-Step ("payload = " + $PayloadFile)
$output = & python @args 2>&1
$code = $LASTEXITCODE
$output | ForEach-Object { Write-Host $_ }

if ($code -eq 1) {
    Write-PollLog 'detect=error'
    Write-Step 'FAILED (detector error)'
    exit 1
}
if ($code -eq 0) {
    Write-Step 'nothing new'
    Write-PollLog 'detect=0'
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

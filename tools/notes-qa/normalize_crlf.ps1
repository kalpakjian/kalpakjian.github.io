# Normalize lone LF line endings to CRLF in every study-note file.
#
# A "note" is a folder under <repo>\source that has index.html plus a paired
# *_Study_Notes.md -- the same definition qa_notes.ps1 uses, so both tools always
# look at the same set of folders.
#
# Lone LF is only a warning in the gate (it does not block a deploy), but it shows
# up as diff noise and can break md tables, so this tool cleans it up.
#
# Portable: <repo>\source is located by walking up from this script's own location,
# so the tool behaves the same wherever it is invoked from.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\normalize_crlf.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\normalize_crlf.ps1 -DryRun
#   powershell -NoProfile -ExecutionPolicy Bypass -File tools\notes-qa\normalize_crlf.ps1 -Root <dir>
param(
  [string]$Root = '',
  [switch]$DryRun,
  [switch]$Quiet
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Root)) {
  $dir = $PSScriptRoot
  while (-not [string]::IsNullOrWhiteSpace($dir) -and
         -not (Test-Path (Join-Path $dir 'source'))) {
    $parent = Split-Path -Parent $dir
    if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $dir) { break }
    $dir = $parent
  }
  $Root = Join-Path $dir 'source'
  if (-not (Test-Path $Root)) {
    throw "cannot find <repo>\source above $PSScriptRoot - pass -Root explicitly"
  }
}

$utf8 = New-Object System.Text.UTF8Encoding($false)
$loneLf = "(?<!\r)\n"
$fixed = 0
$clean = 0
$notes = 0

foreach ($cand in Get-ChildItem -Path $Root -Directory) {
  if (-not (Test-Path (Join-Path $cand.FullName 'index.html'))) { continue }
  $hasMd = @(Get-ChildItem -Path $cand.FullName -Filter '*_Study_Notes.md' -File).Count -gt 0
  if (-not $hasMd) { continue }
  $notes++

  foreach ($f in @(Get-ChildItem -Path $cand.FullName -File |
                   Where-Object { $_.Extension -eq '.md' -or $_.Extension -eq '.html' })) {
    $t = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $n = [regex]::Replace($t, $loneLf, "`r`n")
    if ($n -eq $t) { $clean++; continue }
    $count = ([regex]::Matches($t, $loneLf)).Count
    if (-not $DryRun) { [System.IO.File]::WriteAllText($f.FullName, $n, $utf8) }
    $fixed++
    if (-not $Quiet) {
      Write-Output ("{0} : {1} : {2} lone LF -> CRLF" -f $cand.Name, $f.Name, $count)
    }
  }
}

$label = 'fixed'
if ($DryRun) { $label = 'to fix' }
Write-Output ("notes = {0}   files {1} = {2}   already clean = {3}" -f $notes, $label, $fixed, $clean)
if ($DryRun -and $fixed -gt 0) { Write-Output 'dry run: nothing was written' }

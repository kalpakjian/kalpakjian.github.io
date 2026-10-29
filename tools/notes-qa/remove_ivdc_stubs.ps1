# remove_ivdc_stubs.ps1 - delete the transitional "<slug>-ivdc" redirect folders.
#
# The site renamed its note posts away from the "-ivdc" suffix twice:
#   2026-10-16  13 posts renamed, old URLs kept as meta-refresh stubs
#   2026-10-29  the two CNN posts renamed (cnn-notes, cnn2-notes), stubs added
# Those stubs keep old bookmarks and search results working, but they also keep
# the suffix alive in the URL space, so they are meant to be dropped after a
# 30-day grace period: 2026-11-28.
#
# Usage:
#   pwsh -File tools/notes-qa/remove_ivdc_stubs.ps1 -DryRun   # list only
#   pwsh -File tools/notes-qa/remove_ivdc_stubs.ps1           # delete
#
# Every target is checked first (folder + index.html + meta refresh); anything
# that does not look like a redirect stub aborts the run untouched.

param([switch]$DryRun)

$ErrorActionPreference = 'Stop'

$dir = $PSScriptRoot
while (-not [string]::IsNullOrWhiteSpace($dir) -and
       -not (Test-Path (Join-Path $dir 'source'))) {
  $parent = Split-Path -Parent $dir
  if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $dir) { break }
  $dir = $parent
}
$source = Join-Path $dir 'source'
if (-not (Test-Path $source)) { throw "cannot find <repo>\source above $PSScriptRoot" }

$targets = @(
  '2026/10/07/opencv-notes-ivdc',
  '2026/10/10/ai-intro-notes-ivdc',
  '2026/10/10/cv-intro-notes-ivdc',
  '2026/10/10/local-gpu-ml-notes-ivdc',
  '2026/10/12/neural-network-notes-ivdc',
  '2026/10/12/responsible-ai-notes-ivdc',
  '2026/10/13/huggingface-notes-ivdc',
  '2026/10/13/litellm-notes-ivdc',
  '2026/10/13/llm-intro-notes-ivdc',
  '2026/10/13/local-llm-notes-ivdc',
  '2026/10/13/popular-llm-notes-ivdc',
  '2026/10/13/prompt-engineering-notes-ivdc',
  '2026/10/13/streamlit-flask-notes-ivdc',
  '2026/10/26/cnn-notes-ivdc',
  '2026/10/29/cnn2-notes-ivdc'
)

$stubs = @()
foreach ($t in $targets) {
  $path = Join-Path $source ($t -replace '/', '\')
  if (-not (Test-Path $path)) { continue }
  $index = Join-Path $path 'index.html'
  if (-not (Test-Path $index)) { throw "not a stub (no index.html): $t" }
  $html = [System.IO.File]::ReadAllText($index, [System.Text.Encoding]::UTF8)
  if ($html -notmatch 'http-equiv="refresh"') { throw "not a redirect stub: $t" }
  $stubs += $path
}

if ($stubs.Count -eq 0) { Write-Output 'no stubs left - nothing to do'; exit 0 }

if ($DryRun) {
  $stubs | ForEach-Object { Write-Output ('WOULD REMOVE  ' + $_) }
  Write-Output ('dry run: {0} stub folder(s); nothing was deleted' -f $stubs.Count)
  exit 0
}

$stubs | ForEach-Object { Remove-Item -LiteralPath $_ -Recurse -Force }
Write-Output ('removed {0} stub folder(s); run ''npx hexo clean && npx hexo generate'' and commit' -f $stubs.Count)

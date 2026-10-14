# Second polish pass (ASCII-only script, rules read as UTF-8).
param(
  [Parameter(Mandatory = $true)][string]$ruleFile,
  [string]$filter = '*',
  [string]$Root = ''
)
$ErrorActionPreference = 'Stop'
# Portable: <repo>\source, derived from this script's own location (tools/notes-qa).
if ([string]::IsNullOrWhiteSpace($Root)) {
  $Root = Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) 'source'
}
$root     = $Root
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$rules = @()
foreach ($line in [System.IO.File]::ReadAllLines($ruleFile, [System.Text.Encoding]::UTF8)) {
    if ($line.Trim().Length -eq 0) { continue }
    $p = $line -split '@@@'
    if ($p.Count -lt 2) { throw "bad rule line: $line" }
    $rep = $p[1].TrimEnd([char]0x0D, [char]0x0A)
    $rep = $rep.Replace([string]'~NL~', [string]([char]0x0D + [char]0x0A))
    $rep = $rep.Replace([string]'~LF~', [string][char]0x0A)
    $rules += ,@($p[0].Trim(), $rep)
}
Write-Output ("rules loaded: " + $rules.Count)

$bad = @()
foreach ($r in $rules) { try { $null = [regex]::new($r[0]) } catch { $bad += $r[0] } }
if ($bad.Count -gt 0) { Write-Output 'INVALID PATTERNS:'; $bad | ForEach-Object { Write-Output $_ }; exit 1 }
# drop patterns that can match an empty string (they would insert the replacement everywhere)
$safe = @()
foreach ($r in $rules) {
    if ([regex]::IsMatch('', $r[0])) { Write-Output ('SKIP empty-match pattern: ' + $r[0]) } else { $safe += ,$r }
}
$rules = $safe
Write-Output ('usable rules: ' + $rules.Count)
$files = Get-ChildItem -Path $root -Recurse -File | Where-Object { ($_.Extension -eq '.md' -or $_.Extension -eq '.html') -and $_.Directory.Name -like $filter }
$total = 0
foreach ($f in $files) {
    $text = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $new = $text
    foreach ($r in $rules) {
        $c = ([regex]::Matches($new, $r[0])).Count
        if ($c -gt 0) {
            $new = [regex]::Replace($new, $r[0], $r[1])
            $total += $c
            Write-Output ("{0} : {1} hits : {2}" -f $f.Name, $c, $r[0])
        }
    }
    if ($new -ne $text) { [System.IO.File]::WriteAllText($f.FullName, $new, $utf8NoBom) }
}
Write-Output ("total hits: " + $total)

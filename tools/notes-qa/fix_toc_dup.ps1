$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding($false)
# Portable: <repo>\source is located by walking up from this script's own location,
# so the tool behaves the same wherever it is invoked from.
$dir = $PSScriptRoot
while (-not [string]::IsNullOrWhiteSpace($dir) -and
       -not (Test-Path (Join-Path $dir 'source'))) {
  $parent = Split-Path -Parent $dir
  if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $dir) { break }
  $dir = $parent
}
$root = Join-Path $dir 'source'
if (-not (Test-Path $root)) { throw "cannot find <repo>\source above $PSScriptRoot" }

function Fix-Html([string]$t) {
  $script:hits = 0
  $rx = [regex]'(?s)<td>(\d+)</td>(\s*<td><a href="#[^"]*">)\s*(\d+)\.\s+'
  $out = $rx.Replace($t, {
    param($m)
    if ($m.Groups[1].Value -eq $m.Groups[3].Value) {
      $script:hits++
      return $m.Groups[1].Value + '</td>' + $m.Groups[2].Value
    }
    return $m.Value
  })
  return $out
}

function Fix-Md([string]$t) {
  $script:mhits = 0
  $rx = [regex]'(?m)^\| (\d+) \| \[(\d+)\. '
  $out = $rx.Replace($t, {
    param($m)
    if ($m.Groups[1].Value -eq $m.Groups[2].Value) {
      $script:mhits++
      return '| ' + $m.Groups[1].Value + ' | ['
    }
    return $m.Value
  })
  return $out
}

Get-ChildItem -Path $root -Recurse -Include index.html | ForEach-Object {
  $t = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
  $n = Fix-Html $t
  if ($script:hits -gt 0) {
    [System.IO.File]::WriteAllText($_.FullName, $n, $utf8)
    Write-Output ("html {0} : {1} rows fixed" -f $_.Directory.Name, $script:hits)
  }
}

Get-ChildItem -Path $root -Recurse -Include *_Study_Notes.md | ForEach-Object {
  $t = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
  $n = Fix-Md $t
  if ($script:mhits -gt 0) {
    [System.IO.File]::WriteAllText($_.FullName, $n, $utf8)
    Write-Output ("md   {0} : {1} rows fixed" -f $_.Name, $script:mhits)
  }
}
Write-Output 'done'

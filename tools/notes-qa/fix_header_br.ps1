$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding($false)
# Portable: <repo>\source, derived from this script's own location (tools/notes-qa).
$root = Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) 'source'
# end-of-line chars: 。！？）」 (U+3002 U+FF01 U+FF1F U+FF09 U+300D)
$endChars = @([char]0x3002, [char]0xFF01, [char]0xFF1F, [char]0xFF09, [char]0x300D)
# prefix "課程：" = U+8AB2 U+7A0B U+FF1A
$keCheng = [string]([char]0x8AB2) + [string]([char]0x7A0B) + [string]([char]0xFF1A)
$br = '<' + 'br />'
$total = 0
Get-ChildItem -Path $root -Recurse -Include index.html | ForEach-Object {
  $path = $_.FullName
  $t = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
  $h1 = $t.IndexOf('</h1>')
  if ($h1 -lt 0) { return }
  $s = $t.IndexOf('<blockquote>', $h1)
  if ($s -lt 0) { return }
  $e = $t.IndexOf('</blockquote>', $s)
  if ($e -lt 0) { return }
  $seg = $t.Substring($s, $e - $s)
  $lines = $seg -split "`r`n"
  $hits = 0
  for ($i = 0; $i -lt $lines.Count; $i++) {
    $cur = $lines[$i].Trim()
    if ($cur -eq '' -or $cur -eq '<blockquote>') { continue }
    if ($cur -match ('<' + 'br\s*/?>$')) { continue }
    $next = ''
    for ($j = $i + 1; $j -lt $lines.Count; $j++) {
      if ($lines[$j].Trim() -ne '') { $next = $lines[$j].Trim(); break }
    }
    if ($next -eq '' -or $next -eq '</blockquote>') { continue }
    $last = $cur.Substring($cur.Length - 1, 1)
    $isLabel = $cur.StartsWith('<p>' + $keCheng)
    if (($endChars -contains $last) -or $isLabel) {
      $lines[$i] = $lines[$i].TrimEnd() + $br
      $hits++
    }
  }
  if ($hits -gt 0) {
    $newSeg = ($lines -join "`r`n")
    $t = $t.Substring(0, $s) + $newSeg + $t.Substring($e)
    [System.IO.File]::WriteAllText($path, $t, $utf8)
    Write-Output ("{0} : {1} breaks added" -f $_.Directory.Name, $hits)
    $total += $hits
  }
}
Write-Output ("total = " + $total)

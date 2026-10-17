<#
  build-cards.ps1 -- regenerate the AutoML cheat-sheet deck (cards.html / cards-large.html)
  from the condensed page source/automl-notes/summary.html.

  Pipeline (2 passes, see README.md):
    1) pass 1:  powershell -File build-cards.ps1 -Mode compact
                powershell -File measure-cards.ps1 -Mode compact
    2) pass 2:  powershell -File build-cards.ps1 -Mode compact     # now packs by real heights
                powershell -File measure-cards.ps1 -Mode compact   # verify

  Inputs  (tools/notes-cards/): template.html, splits.txt, groups.txt, labels.txt, heights-<mode>.txt
  Output  (source/automl-notes/): -Out (default cards.html for compact, cards-large.html for large)

  This script is pure ASCII on purpose: Windows PowerShell 5.1 reads .ps1 files with the ANSI
  code page, so all CJK text lives in the UTF-8 data files instead.
#>
param(
  [string]$Root = '',
  [ValidateSet('mobile', 'compact', 'large')][string]$Mode = 'mobile',
  [ValidateSet('masonry', 'pairs')][string]$Pack = 'masonry',
  [string]$Out = '',
  [string]$Template = '',
  [double]$ColMax = 194.0,
  [double]$ColGap = 3.0
)
$ErrorActionPreference = 'Stop'
$nl = [string][char]10
$utf8 = [System.Text.Encoding]::UTF8

if ([string]::IsNullOrWhiteSpace($Root)) {
  $dir = $PSScriptRoot
  while (-not [string]::IsNullOrWhiteSpace($dir) -and -not (Test-Path (Join-Path $dir 'source'))) {
    $parent = Split-Path -Parent $dir
    if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $dir) { break }
    $dir = $parent
  }
  if (-not (Test-Path (Join-Path $dir 'source'))) { throw 'cannot find <repo>\source above the script' }
  $Root = $dir
}
$srcDir = Join-Path $Root 'source\automl-notes'
$toolsDir = Join-Path $Root 'tools\notes-cards'
if ([string]::IsNullOrWhiteSpace($Out)) {
  if ($Mode -eq 'mobile') { $Out = 'cards.html' }
  elseif ($Mode -eq 'compact') { $Out = 'cards-print.html' }
  else { $Out = 'cards-large.html' }
}
if ([string]::IsNullOrWhiteSpace($Template)) {
  if ($Mode -eq 'mobile') { $Template = 'template-mobile.html' } else { $Template = 'template.html' }
}

function ReplaceFirst([string]$text, [string]$find, [string]$repl) {
  $i = $text.IndexOf($find)
  if ($i -lt 0) { return $text }
  return $text.Substring(0, $i) + $repl + $text.Substring($i + $find.Length)
}
# rename the text inside the first <h1 ...>...</h1> span, keeping attributes (e.g. id)
function RenameFirstH1([string]$text, [string]$title) {
  $i = $text.IndexOf('<h1')
  if ($i -lt 0) { return $text }
  $gt = $text.IndexOf('>', $i)
  if ($gt -lt 0) { return $text }
  $j = $text.IndexOf('</h1>', $gt)
  if ($j -lt 0) { return $text }
  return $text.Substring(0, $gt + 1) + $title + $text.Substring($j)
}
function ReadLines([string]$p) { [System.IO.File]::ReadAllLines($p, [System.Text.Encoding]::UTF8) }

$summary = [System.IO.File]::ReadAllText((Join-Path $srcDir 'summary.html'), $utf8)
$template = [System.IO.File]::ReadAllText((Join-Path $toolsDir $Template), $utf8)
$splits = ReadLines (Join-Path $toolsDir 'splits.txt')
$groups = ReadLines (Join-Path $toolsDir 'groups.txt')

$labels = @{}
foreach ($l in (ReadLines (Join-Path $toolsDir 'labels.txt'))) {
  if ([string]::IsNullOrWhiteSpace($l)) { continue }
  $eq = $l.IndexOf('=')
  if ($eq -lt 1) { continue }
  $labels[$l.Substring(0, $eq).Trim()] = $l.Substring($eq + 1).Trim()
}
$needKeys = @('body', 'title', 'alt')
if ($Mode -ne 'mobile') { $needKeys += @('print', 'pagehint', 'pagemargin') }
foreach ($k in $needKeys) {
  if (-not $labels.ContainsKey($Mode + '.' + $k)) { throw ('labels.txt is missing ' + $Mode + '.' + $k) }
}

# 1) condensed content of summary.html
$wrapTag = '<div class="wrap">'
$ws = $summary.IndexOf($wrapTag)
if ($ws -lt 0) { throw 'wrap not found in summary.html' }
$inner = $summary.Substring($ws + $wrapTag.Length)
$we = $inner.LastIndexOf('</div>')
$inner = $inner.Substring(0, $we)
$firstH2 = $inner.IndexOf('<h2 ')
$inner = $inner.Substring($firstH2)
$lastHr = $inner.LastIndexOf('<hr />')
if ($lastHr -ge 0) { $inner = $inner.Substring(0, $lastHr) }

# 2) one section per <h2 ...>, its title becomes the card title
$parts = @()
foreach ($p in [regex]::Split($inner, '(?=<h2 )')) {
  $t = $p.Trim()
  if ($t -ne '') { $parts += $t }
}
for ($k = 0; $k -lt $parts.Count; $k++) {
  $t = $parts[$k] -replace '<h2 ', '<h1 '
  $t = $t -replace '</h2>', '</h1>'
  $t = [regex]::Replace($t, '(?m)^\s*<hr\s*/?>\s*$', '')
  $parts[$k] = $t.Trim()
}

# 3) apply split / rename rules (section id | anchor h3 | new card title | rename first card)
foreach ($line in $splits) {
  if ([string]::IsNullOrWhiteSpace($line)) { continue }
  $f = $line.Split('|')
  if ($f.Count -lt 2) { continue }
  $sect = $f[0].Trim()
  $anchor = $f[1].Trim()
  $newTitle = ''
  if ($f.Count -ge 3) { $newTitle = $f[2].Trim() }
  $rename = ''
  if ($f.Count -ge 4) { $rename = $f[3].Trim() }
  $hit = $false
  for ($k = 0; $k -lt $parts.Count; $k++) {
    if ($parts[$k] -notmatch ('id="' + [regex]::Escape($sect) + '"')) { continue }
    $hit = $true
    if ($rename -ne '') { $parts[$k] = RenameFirstH1 $parts[$k] $rename }
    if ($anchor -ne '') {
      $old = '<h3>' + $anchor + '</h3>'
      if ($parts[$k].IndexOf($old) -lt 0) { throw ('anchor not found: ' + $anchor) }
      $new = '</section>' + $nl + '<section class="card">' + $nl + '<h1>' + $newTitle + '</h1>'
      $parts[$k] = ReplaceFirst $parts[$k] $old $new
    }
  }
  if (-not $hit) { throw ('section not found for rule: ' + $sect) }
}

# 4) wrap as cards, then re-split so every split rule yields its own card
$all = ''
foreach ($p in $parts) { $all += '<section class="card">' + $nl + $p + $nl + '</section>' + $nl }
$cardList = @([regex]::Split($all, '(?=<section class="card">)') | Where-Object { $_.Trim() -ne '' })

# 5) numbered badge + unit colour band + unit chip (chapter order first)
$unitCls = @()
$unitLabel = @()
for ($i = 0; $i -lt $cardList.Count; $i++) {
  $n = $i + 1
  $cls = 'u6'
  $label = ''
  foreach ($g in $groups) {
    if ([string]::IsNullOrWhiteSpace($g)) { continue }
    $gf = $g.Split('|')
    if ($gf.Count -lt 4) { continue }
    if ($n -ge [int]$gf[0] -and $n -le [int]$gf[1]) { $cls = $gf[2].Trim(); $label = $gf[3].Trim(); break }
  }
  $unitCls += $cls
  $unitLabel += $label
  $c = $cardList[$i]
  $c = ReplaceFirst $c '<section class="card">' ('<section class="card ' + $cls + '" data-ch="' + $n + '">')
  $i1 = $c.IndexOf('<h1')
  if ($i1 -lt 0) { throw ('card ' + $n + ' has no h1') }
  $gt = $c.IndexOf('>', $i1)
  $inject = '<span class="badge">' + $n + '</span><span class="chip">' + $label + '</span>'
  $cardList[$i] = $c.Substring(0, $gt + 1) + $inject + $c.Substring($gt + 1)
}

# 5b) importance order (order.txt): reorder, add tier chip, renumber the badge
$orderPath = Join-Path $toolsDir 'order.txt'
if (Test-Path $orderPath) {
  $perm = @()
  $tierOf = @{}
  foreach ($l in (ReadLines $orderPath)) {
    if ([string]::IsNullOrWhiteSpace($l)) { continue }
    if ($l.TrimStart().StartsWith('#')) { continue }
    $f = $l.Split('|')
    if ($f.Count -lt 3) { continue }
    $old = [int]$f[0].Trim()
    $perm += $old
    $tierOf[$old] = @{ cls = $f[1].Trim(); label = $f[2].Trim() }
  }
  if ($perm.Count -eq $cardList.Count) {
    $ordered = @()
    for ($k = 0; $k -lt $perm.Count; $k++) {
      $old = $perm[$k]
      if ($old -lt 1 -or $old -gt $cardList.Count) { throw ('order.txt refers to a non-existent card: ' + $old) }
      $c = $cardList[$old - 1]
      $ti = $tierOf[$old]
      $c = ReplaceFirst $c ('class="card ' + $unitCls[$old - 1] + '"') ('class="card ' + $unitCls[$old - 1] + ' ' + $ti.cls + '"')
      $c = ReplaceFirst $c ('<span class="chip">' + $unitLabel[$old - 1] + '</span>') ('<span class="chip">' + $unitLabel[$old - 1] + '</span><span class="tier">' + $ti.label + '</span>')
      $c = ReplaceFirst $c ('<span class="badge">' + $old + '</span>') ('<span class="badge">' + ($k + 1) + '</span>')
      $ordered += $c
    }
    $cardList = $ordered
    Write-Output ('order.txt applied: ' + $perm.Count + ' cards ordered by exam importance')
  } else {
    Write-Output ('note: order.txt has ' + $perm.Count + ' entries but there are ' + $cardList.Count + ' cards -> chapter order kept')
  }
}

# 5c) mobile: move badge/chip/tier out of <h1> into a header row
if ($Mode -eq 'mobile') {
  for ($k = 0; $k -lt $cardList.Count; $k++) {
    $c = $cardList[$k]
    $m = [regex]::Match($c, '(?s)<h1[^>]*>(\s*<span class="badge">\d+</span>\s*<span class="chip">[^<]*</span>\s*<span class="tier">[^<]*</span>)(.*?)</h1>')
    if (-not $m.Success) { throw ('card ' + ($k + 1) + ': could not split the header spans') }
    $head = $m.Groups[1].Value.Trim()
    $title = $m.Groups[2].Value.Trim()
    $cardList[$k] = $c.Replace($m.Value, '<div class="chead">' + $head + '</div>' + $nl + '<h1>' + $title + '</h1>')
  }
  Write-Output 'mobile: badge/chip/tier moved into a .chead header row'
}

# 6) packing: mobile = one card per panel; pairs = 2 per page; masonry = fill columns to ColMax
$hmap = @{}
$hp = Join-Path $toolsDir ('heights-' + $Mode + '.txt')
if (Test-Path $hp) {
  foreach ($l in (ReadLines $hp)) {
    if ([string]::IsNullOrWhiteSpace($l)) { continue }
    $hf = $l.Split('|')
    if ($hf.Count -ge 2) { $hmap[[int]$hf[0].Trim()] = [double]$hf[1].Trim() }
  }
}
$heights = @()
$stale = $false
for ($k = 0; $k -lt $cardList.Count; $k++) {
  $m = [regex]::Match($cardList[$k], 'data-ch="(\d+)"')
  if (-not $m.Success) { $stale = $true; break }
  $ch = [int]$m.Groups[1].Value
  if (-not $hmap.ContainsKey($ch)) { $stale = $true; break }
  $heights += $hmap[$ch]
}
if ($stale -or $heights.Count -ne $cardList.Count) {
  Write-Output ('note: heights missing or stale (' + $hmap.Count + ' measured) -> one card per column')
  $heights = @()
  foreach ($c in $cardList) { $heights += 999.0 }
}

$sheets = ''
if ($Mode -eq 'mobile') {
  $sheets = ($cardList -join ($nl + $nl))
} elseif ($Pack -eq 'pairs') {
  for ($k = 0; $k -lt $cardList.Count; $k += 2) {
    $sheets += '<div class="sheet">' + $nl + '<div class="col">' + $nl + $cardList[$k] + $nl + '</div>' + $nl
    if (($k + 1) -lt $cardList.Count) { $sheets += '<div class="col">' + $nl + $cardList[$k + 1] + $nl + '</div>' + $nl }
    else { $sheets += '<div class="col"></div>' + $nl }
    $sheets += '</div>' + $nl
  }
} else {
  $columns = @()
  $buf = ''
  $h = 0.0
  for ($k = 0; $k -lt $cardList.Count; $k++) {
    $need = $heights[$k]
    if ($buf -ne '') { $need = $heights[$k] + $ColGap }
    if (($buf -ne '') -and (($h + $need) -gt $ColMax)) {
      $columns += $buf
      $buf = ''
      $h = 0.0
      $need = $heights[$k]
    }
    if ($buf -ne '') { $buf += $nl }
    $buf += $cardList[$k]
    $h += $need
  }
  if ($buf -ne '') { $columns += $buf }
  for ($c = 0; $c -lt $columns.Count; $c += 2) {
    $sheets += '<div class="sheet">' + $nl + '<div class="col">' + $nl + $columns[$c] + $nl + '</div>' + $nl
    if (($c + 1) -lt $columns.Count) { $sheets += '<div class="col">' + $nl + $columns[$c + 1] + $nl + '</div>' + $nl }
    else { $sheets += '<div class="col"></div>' + $nl }
    $sheets += '</div>' + $nl
  }
}

# 7) fill template placeholders and write the deck
$body = $template
$body = $body.Replace('@@BODYCLASS@@', $labels[$Mode + '.body'])
$body = $body.Replace('@@TITLE@@', $labels[$Mode + '.title'])
$body = $body.Replace('@@ALT_CARDS@@', $labels[$Mode + '.alt'])
$body = $body.Replace('@@COUNT@@', [string]$cardList.Count)
$ph = @{ 'print' = '@@PRINTLABEL@@'; 'pagehint' = '@@PAGEHINT@@'; 'pagemargin' = '@@PAGEMARGIN@@'; 'footnote' = '@@FOOTNOTE@@' }
foreach ($k in $ph.Keys) {
  $key = $Mode + '.' + $k
  if ($labels.ContainsKey($key)) { $body = $body.Replace($ph[$k], $labels[$key]) }
}
if ($body.Contains('@@CARDS@@')) {
  $deck = $body.Replace('@@CARDS@@', $sheets)
} else {
  $deck = $body + $nl + $sheets + '</body>' + $nl + '</html>' + $nl
}
$outPath = Join-Path $srcDir $Out
[System.IO.File]::WriteAllText($outPath, $deck, (New-Object System.Text.UTF8Encoding($false)))

Write-Output ('mode=' + $Mode + ' pack=' + $Pack + ' cards=' + $cardList.Count +
              ' sheets=' + ([regex]::Matches($deck, 'class="sheet"')).Count +
              ' -> ' + $Out + ' (' + (Get-Item $outPath).Length + ' B)')

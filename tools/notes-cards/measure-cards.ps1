<#
  measure-cards.ps1 -- measure every card height in the printed layout and (optionally)
  count the pages of the real print output.

  Pass 1 (after build-cards.ps1 with no/stale heights): writes tools/notes-cards/heights-<mode>.txt
  Pass 2 (after re-running build-cards.ps1): re-measure to confirm the packing still fits.

  Requires Microsoft Edge (headless). Pure ASCII on purpose (PS 5.1 reads .ps1 as ANSI).
#>
param(
  [string]$Root = '',
  [ValidateSet('mobile', 'compact', 'large')][string]$Mode = 'mobile',
  [string]$File = '',
  [switch]$SkipPdf
)
$ErrorActionPreference = 'Stop'
$nl = [string][char]10

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
if ([string]::IsNullOrWhiteSpace($File)) {
  if ($Mode -eq 'mobile') { $File = 'cards.html' }
  elseif ($Mode -eq 'compact') { $File = 'cards-print.html' }
  else { $File = 'cards-large.html' }
}
$srcDir = Join-Path $Root 'source\automl-notes'
$toolsDir = Join-Path $Root 'tools\notes-cards'
$target = Join-Path $srcDir $File
if (-not (Test-Path $target)) { throw ('deck not found: ' + $target) }

$edge = ''
foreach ($c in @(
    'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    'C:\Program Files\Google\Chrome\Application\chrome.exe',
    'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')) {
  if (Test-Path $c) { $edge = $c; break }
}
if ($edge -eq '') { throw 'no Edge/Chrome found for headless measurement' }

$html = [System.IO.File]::ReadAllText($target, [System.Text.Encoding]::UTF8)
$m = [regex]::Match($html, '(?s)/\* @print-css-start \*/(.*?)/\* @print-css-end \*/')
if (-not $m.Success) { throw 'print css markers not found in ' + $File }
$printCss = $m.Groups[1].Value

$js = @'
<script>
window.addEventListener('load', function () {
  var px2mm = 1 / (96 / 25.4);
  var out = [], max = 0, maxch = 0;
  var cards = document.querySelectorAll('.card');
  for (var i = 0; i < cards.length; i++) {
    var mm = cards[i].getBoundingClientRect().height * px2mm;
    var ch = cards[i].getAttribute('data-ch') || (i + 1);
    if (mm > max) { max = mm; maxch = ch; }
    out.push(ch + ':' + mm.toFixed(1));
  }
  var pre = document.createElement('pre');
  pre.id = 'measure';
  pre.textContent = out.join(' ') + '||MAX=ch' + maxch + ':' + max.toFixed(1) + 'mm||N=' + cards.length;
  document.body.appendChild(pre);
});
</script>
'@

$mg = [regex]::Match($printCss, '@page\s*\{[^}]*margin:\s*([0-9.]+)mm')
$marginMm = 8.0
if ($mg.Success) { $marginMm = [double]$mg.Groups[1].Value }
$contentW = [math]::Round(297.0 - 2 * $marginMm, 1)
$contentH = [math]::Round(210.0 - 2 * $marginMm, 1)

$sim = '<style id="printsim">' + $printCss + $nl +
       '.sheet{width:' + $contentW + 'mm!important;min-height:0!important;margin:0 0 6mm 0!important;page-break-after:auto!important}' + $nl +
       '</style>' + $nl + $js
$tmp = Join-Path $env:TEMP ('deck-' + $Mode + '.html')
[System.IO.File]::WriteAllText($tmp, $html.Replace('</body>', $sim + '</body>'), (New-Object System.Text.UTF8Encoding($false)))
$dom = Join-Path $env:TEMP ('deck-' + $Mode + '-dom.txt')
$url = 'file:///' + ($tmp -replace '\\', '/')
$edgeCommon = @(
  '--headless=new', '--disable-gpu', '--disable-sync', '--no-first-run',
  '--no-default-browser-check', '--disable-extensions',
  ('--user-data-dir=' + (Join-Path $env:TEMP 'edge-headless-profile'))
)
$ErrorActionPreference = 'Continue'
& $edge @edgeCommon --virtual-time-budget=6000 --dump-dom $url 2>$null |
  Out-File -FilePath $dom -Encoding UTF8
$ErrorActionPreference = 'Stop'
$d = [System.IO.File]::ReadAllText($dom)
$mm = [regex]::Match($d, '<pre id="measure">(.*?)</pre>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
if (-not $mm.Success) { throw 'measure node not found - did the page script run?' }
$payload = $mm.Groups[1].Value
$parts = $payload.Split('||')
$pairs = @()
foreach ($p in $parts[0].Trim().Split(' ')) {
  if ([string]::IsNullOrWhiteSpace($p)) { continue }
  $kv = $p.Split(':')
  if ($kv.Count -ge 2) { $pairs += [pscustomobject]@{ ch = [int]$kv[0]; h = [double]$kv[1] } }
}
$pairs = $pairs | Sort-Object ch
$lines = @()
foreach ($x in $pairs) { $lines += ('' + $x.ch + '|' + $x.h) }
$heightsPath = Join-Path $toolsDir ('heights-' + $Mode + '.txt')
[System.IO.File]::WriteAllLines($heightsPath, $lines, (New-Object System.Text.UTF8Encoding($false)))
Write-Output ('heights written: ' + $heightsPath)
Write-Output ('cards=' + $lines.Count + '  ' + $parts[1] + '  (column limit ' + $contentH + 'mm, margin ' + $marginMm + 'mm)')
Write-Output ('heights(ch|mm): ' + ($lines -join ' '))

if (-not $SkipPdf) {
  $pdf = Join-Path $env:TEMP ('deck-' + $Mode + '.pdf')
  Remove-Item $pdf -ErrorAction SilentlyContinue
  $tmp2 = Join-Path $env:TEMP ('deck-' + $Mode + '-print.html')
  Copy-Item $target $tmp2 -Force
  $url2 = 'file:///' + ($tmp2 -replace '\\', '/')
  $ErrorActionPreference = 'Continue'
  $null = & $edge @edgeCommon --no-pdf-header-footer --print-to-pdf="$pdf" $url2 2>&1
  $ErrorActionPreference = 'Stop'
  Start-Sleep -Seconds 5
  if (Test-Path $pdf) {
    $b = [System.IO.File]::ReadAllBytes($pdf)
    $t = [System.Text.Encoding]::ASCII.GetString($b)
    $pages = ([regex]::Matches($t, '/Type\s*/Page[^s]')).Count
    Write-Output ('printed pages = ' + $pages + '   (pdf bytes ' + $b.Length + ')')
  } else { Write-Output 'PDF not created' }
}

# Regenerate clean anchor ids for every heading (and keep id / href / md links in sync).
$ErrorActionPreference = 'Stop'
# Portable: <repo>\source, derived from this script's own location (tools/notes-qa).
$root = Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) 'source'
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Slug([string]$t) {
    $s = ($t -replace '<[^>]+>', '')
    $s = $s.ToLower() -replace '&[a-z]+;', ''
    $sb = New-Object System.Text.StringBuilder
    foreach ($ch in $s.ToCharArray()) {
        if ([char]::IsLetterOrDigit($ch)) { [void]$sb.Append($ch) }
        elseif ($ch -eq ' ' -or $ch -eq '-' -or $ch -eq '_') { [void]$sb.Append('-') }
    }
    $out = ($sb.ToString() -replace '-{2,}', '-').Trim('-')
    if ($out.Length -gt 60) { $out = $out.Substring(0, 60).Trim('-') }
    return $out
}

$files = Get-ChildItem -Path $root -Recurse -Include *.md -File | Where-Object { $_.Name -notmatch 'ivdc' }
$grand = 0
foreach ($mdFile in $files) {
    $htmlPath = Join-Path $mdFile.Directory.FullName 'index.html'
    if (-not (Test-Path $htmlPath)) { continue }
    $html = [System.IO.File]::ReadAllText($htmlPath, [System.Text.Encoding]::UTF8)
    $md = [System.IO.File]::ReadAllText($mdFile.FullName, [System.Text.Encoding]::UTF8)
    $hM = [regex]::Matches($html, '<h([234])([^>]*)id="([^"]*)"([^>]*)>(.*?)</h\1>')
    $map = @{}; $used = @{}
    foreach ($m in $hM) {
        $oldId = $m.Groups[3].Value
        $text = ($m.Groups[5].Value -replace '<[^>]+>', '').Trim()
        if ($oldId -eq '' -or $text -eq '') { continue }
        $base = Slug $text
        if ($base -eq '') { continue }
        $cand = $base; $k = 2
        while ($used.ContainsKey($cand)) { $cand = $base + '-' + $k; $k++ }
        $used[$cand] = $true
        if ($cand -ne $oldId) { $map[$oldId] = $cand }
    }
    if ($map.Count -eq 0) { continue }
    foreach ($old in @($map.Keys)) {
        $new = $map[$old]
        $html = $html.Replace('id="' + $old + '"', 'id="' + $new + '"').Replace('href="#' + $old + '"', 'href="#' + $new + '"')
        $md = $md.Replace('](#' + $old + ')', '](#' + $new + ')')
    }
    [System.IO.File]::WriteAllText($htmlPath, $html, $utf8)
    [System.IO.File]::WriteAllText($mdFile.FullName, $md, $utf8)
    Write-Output ("{0} : ids regenerated = {1}" -f $mdFile.Name, $map.Count)
    $grand += $map.Count
}
Write-Output ("total ids = " + $grand)

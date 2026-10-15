<#
  qa_notes.ps1 - quality gate for the IVDC study notes (index.html + *_Study_Notes.md + mc-quiz.html)

  Usage:
    powershell -NoProfile -ExecutionPolicy Bypass -File qa_notes.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File qa_notes.ps1 -Root <dir>
    powershell -NoProfile -ExecutionPolicy Bypass -File qa_notes.ps1 -Quiet

  Exit code: 0 = every hard check passed, 1 = at least one hard check failed.

  Hard checks (must be zero):
    1. banned wording   : yuan-gao / jiao-cai / jiang-yi / ben-jie
    2. page references  : standalone pN tokens (p3, p12, p24 ...)
    3. anchors          : every href="#id" resolves inside the same page
    4. md links         : every md link "](#id)" resolves in the paired html
    5. TOC numbering    : no duplicated number in the "#" column
    6. list tags        : <li> / </li> balanced
    7. literal \r\n     : table corruption marker inside md
    8. heading parity   : h2/h3 set identical between md and html
    9. header blockquote: rendered line by line (<br /> present)
                          -- only checked when a header block is actually there,
                             i.e. a <blockquote> immediately after </h1>
   10. quiz            : QUESTIONS JSON parses, count matches the nav label
   11. quiz options    : a quiz that builds <li class="opt"> rows must also
                          reference the option array (q.o[k]); otherwise every
                          choice renders as an empty <li> and the reader sees
                          no options at all (this shipped broken in 12 quizzes)


  Warnings (advisory, never fail the run):
    - lone LF line endings
    - "di N ye" style phrasing (may be a legitimate example)
#>
param(
  [string]$Root = '',
  [switch]$Quiet
)

$ErrorActionPreference = 'Stop'

# Portable default: locate <repo>\source by walking up from this script's own
# location, so the gate behaves identically whether it is run from
# tools/notes-qa/ (canonical, tracked) or from a scratch copy elsewhere.
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

function Ch([int[]]$c) { -join ($c | ForEach-Object { [char]$_ }) }

# Banned wording. Built from code points so this script stays pure ASCII
# (Windows PowerShell 5.1 reads .ps1 files with the ANSI code page).
$BAN = @(
  @{ n = 'yuan-gao'; s = (Ch 0x539F,0x7A3F) },
  @{ n = 'jiao-cai'; s = (Ch 0x6559,0x6750) },
  @{ n = 'jiang-yi'; s = (Ch 0x8B1B,0x7FA9) },
  @{ n = 'ben-jie';  s = (Ch 0x672C,0x7BC0) }
)
$W_YE = Ch 0x9801            # ye (page)
$W_DI = Ch 0x7B2C            # di (ordinal prefix)

$pageRef = '(?<![A-Za-z0-9+/=])p\d{1,2}(?![A-Za-z0-9+/=])'
$diYeRef = [regex]::Escape($W_DI) + '\s*\d+\s*' + [regex]::Escape($W_YE)
$tocDup = '(?s)<td>(\d+)</td>\s*<td><a href="#[^"]*">\s*\1\. '
$liOpen = '<li[ >]'
$liClose = '</li>'
$brRx = '<' + 'br\s*/?>'

function Get-Text([string]$p) { [System.IO.File]::ReadAllText($p, [System.Text.Encoding]::UTF8) }

function NormMd([string]$t) {
  # markdown heading text: backticks/asterisks are markup, "<...>" is literal text
  $s = $t -replace '[`*]', ''
  return ($s -replace '\s+', ' ').Trim()
}

function NormHtml([string]$t) {
  # html heading text: strip real tags first, then unescape entities
  $s = $t -replace '<[^>]+>', ''
  $s = $s.Replace('&lt;', '<').Replace('&gt;', '>').Replace('&amp;', '&')
  $s = $s.Replace('&#39;', "'").Replace('&quot;', '"')
  $s = $s -replace '[`*]', ''
  return ($s -replace '\s+', ' ').Trim()
}

$fail = 0
$warnList = @()
$rows = @()

# A "note" = a folder that has BOTH index.html and a paired *_Study_Notes.md.
# Other page folders (coding-agent, dhh-rails-world-2026, ...) are not notes and are skipped.
$dirs = @()
$skipped = @()
foreach ($cand in Get-ChildItem -Path $Root -Directory) {
  if (-not (Test-Path (Join-Path $cand.FullName 'index.html'))) { continue }
  $hasMd = @(Get-ChildItem -Path $cand.FullName -Filter '*_Study_Notes.md' -File |
    Where-Object { $_.Name -notmatch '-ivdc\.md$' }).Count -gt 0
  if ($hasMd) { $dirs += $cand } else { $skipped += $cand.Name }
}

foreach ($d in $dirs) {
  $name = $d.Name
  $htmlPath = Join-Path $d.FullName 'index.html'
  $quizPath = Join-Path $d.FullName 'mc-quiz.html'
  $mdFile = Get-ChildItem -Path $d.FullName -Filter '*_Study_Notes.md' -File |
    Where-Object { $_.Name -notmatch '-ivdc\.md$' } | Select-Object -First 1
  $problems = @()

  $html = Get-Text $htmlPath
  $md = ''
  if ($mdFile) { $md = Get-Text $mdFile.FullName } else { $problems += 'missing *_Study_Notes.md' }

  # 1) banned wording
  foreach ($b in $BAN) {
    $c1 = ([regex]::Matches($html, [regex]::Escape($b.s))).Count
    $c2 = 0
    if ($md -ne '') { $c2 = ([regex]::Matches($md, [regex]::Escape($b.s))).Count }
    if (($c1 + $c2) -gt 0) { $problems += ("banned word [{0}] html={1} md={2}" -f $b.n, $c1, $c2) }
  }

  # 2) page references
  $p1 = ([regex]::Matches($html, $pageRef)).Count
  $p2 = 0
  if ($md -ne '') { $p2 = ([regex]::Matches($md, $pageRef)).Count }
  if (($p1 + $p2) -gt 0) { $problems += ("page ref pN html={0} md={1}" -f $p1, $p2) }

  # 3) anchors inside the page
  $ids = @{}
  foreach ($m in [regex]::Matches($html, 'id="([^"]+)"')) { $ids[$m.Groups[1].Value] = 1 }
  $badA = 0
  foreach ($m in [regex]::Matches($html, 'href="#([^"]+)"')) {
    if (-not $ids.ContainsKey($m.Groups[1].Value)) { $badA++ }
  }
  if ($badA -gt 0) { $problems += ("broken anchors = {0}" -f $badA) }

  # 4) md links resolve in the paired html
  if ($md -ne '') {
    $badM = 0
    foreach ($m in [regex]::Matches($md, '\]\(#([^)]+)\)')) {
      if (-not $ids.ContainsKey($m.Groups[1].Value)) { $badM++ }
    }
    if ($badM -gt 0) { $problems += ("md links missing in html = {0}" -f $badM) }
  }

  # 5) TOC duplicated numbering
  $dup = ([regex]::Matches($html, $tocDup)).Count
  if ($dup -gt 0) { $problems += ("TOC rows with duplicated number = {0}" -f $dup) }

  # 6) list tag balance
  $o = ([regex]::Matches($html, $liOpen)).Count
  $c = ([regex]::Matches($html, $liClose)).Count
  if ($o -ne $c) { $problems += ("li imbalance open={0} close={1}" -f $o, $c) }

  # 7) literal \r\n inside md
  if ($md -ne '') {
    $lit = ([regex]::Matches($md, '\\r\\n')).Count
    if ($lit -gt 0) { $problems += ("literal \r\n in md = {0}" -f $lit) }
  }

  # 8) heading parity
  if ($md -ne '') {
    $mdNoCode = [regex]::Replace($md, '(?s)```.*?```', '')
    $hb = @()
    foreach ($m in [regex]::Matches($mdNoCode, '(?m)^#{2,3} (.*)$')) { $hb += (NormMd $m.Groups[1].Value) }
    $ha = @()
    foreach ($m in [regex]::Matches($html, '(?s)<h([23])[^>]*>(.*?)</h\1>')) { $ha += (NormHtml $m.Groups[2].Value) }
    $diff = 0
    foreach ($x in $hb) { if ($ha -notcontains $x) { $diff++ } }
    foreach ($x in $ha) { if ($hb -notcontains $x) { $diff++ } }
    if ($diff -gt 0) { $problems += ("heading mismatch md<->html = {0}" -f $diff) }
  }

  # 9) header blockquote rendered line by line (only when a header block is present)
  $main = $html.IndexOf('<main>')
  if ($main -ge 0) { $h1 = $html.IndexOf('</h1>', $main) } else { $h1 = $html.IndexOf('</h1>') }
  if ($h1 -ge 0) {
    $after = $h1 + 5
    $s = $html.IndexOf('<blockquote>', $after)
    if ($s -ge 0) {
      $between = $html.Substring($after, $s - $after)
      if ($between -match '^\s*$') {
        $e = $html.IndexOf('</blockquote>', $s)
        $seg = $html.Substring($s, $e - $s)
        $nbr = ([regex]::Matches($seg, $brRx)).Count
        if ($nbr -lt 3) { $problems += ("header blockquote line breaks = {0} (expect >= 3)" -f $nbr) }
      }
    }
  }

  # 10) quiz JSON + nav count
  if (Test-Path $quizPath) {
    $quiz = Get-Text $quizPath
    $i = $quiz.IndexOf('const QUESTIONS')
    if ($i -lt 0) { $problems += 'quiz: const QUESTIONS not found' }
    else {
      $s = $quiz.IndexOf('[', $i)
      $e = $quiz.IndexOf('];', $s)
      try {
        $arr = $quiz.Substring($s, $e - $s + 1) | ConvertFrom-Json
        $qc = @($arr).Count
        $nav = [regex]::Match($html, 'class="quiz"[^>]*>([^<]*)<')
        if ($nav.Success) {
          $nm = [regex]::Match($nav.Groups[1].Value, '\d+')
          if ($nm.Success -and [int]$nm.Value -ne $qc) {
            $problems += ("quiz count nav={0} actual={1}" -f $nm.Value, $qc)
          }
        }
        if ($qc -lt 20) { $problems += ("quiz has only {0} questions" -f $qc) }
      } catch { $problems += 'quiz JSON parse failed' }
    }

    # 11) a quiz that renders option rows must also render the option TEXT.
    #     The shared shell builds each row with  html += '<li class="' + cls +
    #     '" data-q="' ... '">';  and then appends the letter + text + '</li>'.
    #     When that second line is lost, every choice renders as an empty <li>
    #     and the reader sees no options at all (12 quizzes shipped like this).
    $rendersOptRows = ([regex]::Matches($quiz, "'<li class=")).Count -gt 0
    if ($rendersOptRows) {
      $hasOptText = ([regex]::Matches($quiz, 'q\.o\[')).Count -gt 0
      if (-not $hasOptText) {
        $problems += 'quiz options render without text (no q.o[k] reference)'
      }
    }
  }

  # warnings
  $loneLF = ([regex]::Matches($html, "(?<!\r)\n")).Count
  if ($md -ne '') { $loneLF += ([regex]::Matches($md, "(?<!\r)\n")).Count }
  if ($loneLF -gt 0) { $warnList += ("{0}: lone LF line endings = {1}" -f $name, $loneLF) }

  $dy = ([regex]::Matches($html, $diYeRef)).Count
  if ($md -ne '') { $dy += ([regex]::Matches($md, $diYeRef)).Count }
  if ($dy -gt 0) { $warnList += ("{0}: 'di N ye' phrasing x{1} - review (page ref or legitimate example?)" -f $name, $dy) }

  if ($problems.Count -gt 0) {
    $fail++
    $rows += ("FAIL  {0}" -f $name)
    foreach ($p in $problems) { $rows += ("        - " + $p) }
  } else {
    $rows += ("PASS  {0}" -f $name)
  }
}

if ($dirs.Count -eq 0) {
  Write-Output ("no note folders found under {0} - refusing to report a pass" -f $Root)
  exit 1
}

if (-not $Quiet) {
  $rows | ForEach-Object { Write-Output $_ }
  if ($warnList.Count -gt 0) {
    Write-Output ''
    Write-Output 'WARNINGS (advisory):'
    $warnList | ForEach-Object { Write-Output ('  ' + $_) }
  }
  Write-Output ''
}
Write-Output ("notes checked = {0}   failures = {1}   warnings = {2}" -f $dirs.Count, $fail, $warnList.Count)
if ($skipped.Count -gt 0) { Write-Output ("skipped (not a note folder) = " + ($skipped -join ', ')) }

if ($fail -gt 0) { exit 1 } else { exit 0 }


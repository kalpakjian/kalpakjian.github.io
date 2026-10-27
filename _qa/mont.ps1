param()
Add-Type -AssemblyName System.Drawing

function Mont {
  param($src,$dst,$regions,$cols,$cellw,$cellh,$z,$q)
  $img = [System.Drawing.Image]::FromFile($src)
  $rows = [math]::Ceiling($regions.Count/$cols)
  $bmp = New-Object System.Drawing.Bitmap([int]($cols*$cellw*$z)),([int]($rows*$cellh*$z))
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.Clear([System.Drawing.Color]::FromArgb(60,60,60))
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::Red), 2
  for($i=0;$i -lt $regions.Count;$i++){
    $r = $regions[$i]
    $cx = [int](($i % $cols) * $cellw * $z)
    $cy = [int]([math]::Floor($i/$cols) * $cellh * $z)
    $dest = New-Object System.Drawing.Rectangle($cx,$cy,[int]($cellw*$z),[int]($cellh*$z))
    $srcR = New-Object System.Drawing.Rectangle([int]$r[0],[int]$r[1],[int]$r[2],[int]$r[3])
    $g.DrawImage($img,$dest,$srcR,[System.Drawing.GraphicsUnit]::Pixel)
    $g.DrawRectangle($pen,$dest)
  }
  $enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
  $ep = New-Object System.Drawing.Imaging.EncoderParameters(1)
  $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality,[long]$q)
  $bmp.Save($dst,$enc,$ep)
  $g.Dispose(); $bmp.Dispose(); $img.Dispose()
  Write-Host "saved $dst $((Get-Item $dst).Length)"
}

$A = 'C:\Users\princ\blog\_covergen\cnn_lab_chapters\ch09-confusion.png'
$B = 'C:\Users\princ\blog\_covergen\cnn_lab_chapters\ch10-counterfactual.png'

$regions = New-Object System.Collections.ArrayList
[void]$regions.Add(@(390,460,150,150))
[void]$regions.Add(@(530,460,150,150))
[void]$regions.Add(@(670,460,150,150))
[void]$regions.Add(@(790,460,150,150))
Mont $A 'C:\Users\princ\blog\_qa\LEG.jpg' $regions 2 150 150 3.4 72

$regions2 = New-Object System.Collections.ArrayList
[void]$regions2.Add(@(605,230,70,190))
[void]$regions2.Add(@(480,215,200,150))
[void]$regions2.Add(@(700,255,180,180))
[void]$regions2.Add(@(860,300,180,180))
Mont $A 'C:\Users\princ\blog\_qa\HEAD.jpg' $regions2 2 180 190 3.2 72

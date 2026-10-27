param()
Add-Type -AssemblyName System.Drawing

function CJ {
  param($src,$dst,$x,$y,$w,$h,$z,$q,$mul)
  $img = [System.Drawing.Image]::FromFile($src)
  $ow = [int]($w*$z); $oh = [int]($h*$z)
  $bmp = New-Object System.Drawing.Bitmap($ow,$oh)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $dest = New-Object System.Drawing.Rectangle(0,0,$ow,$oh)
  $srcR = New-Object System.Drawing.Rectangle($x,$y,$w,$h)
  $g.DrawImage($img,$dest,$srcR,[System.Drawing.GraphicsUnit]::Pixel)
  $g.Dispose(); $img.Dispose()
  if($mul -ne $null){
    for($py=0;$py -lt $oh;$py++){
      for($px=0;$px -lt $ow;$px++){
        $c = $bmp.GetPixel($px,$py)
        $r = [Math]::Min(255,[int]($c.R*$mul)); $gg = [Math]::Min(255,[int]($c.G*$mul)); $bb = [Math]::Min(255,[int]($c.B*$mul))
        $bmp.SetPixel($px,$py,(New-Object System.Drawing.Color($r,$gg,$bb)))
      }
    }
  }
  $enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
  $ep = New-Object System.Drawing.Imaging.EncoderParameters(1)
  $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality,[long]$q)
  $bmp.Save($dst,$enc,$ep)
  $bmp.Dispose()
  Write-Host "saved $dst $((Get-Item $dst).Length)"
}

$A = 'C:\Users\princ\blog\_covergen\cnn_lab_chapters\ch09-confusion.png'
$B = 'C:\Users\princ\blog\_covergen\cnn_lab_chapters\ch10-counterfactual.png'
CJ $A 'C:\Users\princ\blog\_qa\M1.jpg' 395 480 175 160 2.4 70 3.0
CJ $A 'C:\Users\princ\blog\_qa\M2.jpg' 555 480 175 160 2.4 70 3.0
CJ $A 'C:\Users\princ\blog\_qa\M3.jpg' 700 480 175 160 2.4 70 3.0
CJ $A 'C:\Users\princ\blog\_qa\M4.jpg' 790 455 175 190 2.4 70 3.0
CJ $A 'C:\Users\princ\blog\_qa\M5.jpg' 370 460 190 190 2.2 70 2.6

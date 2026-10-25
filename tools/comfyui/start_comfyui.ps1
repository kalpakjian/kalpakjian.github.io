# 啟動 ComfyUI（D:\AI\ComfyUI），並修掉兩個已知的 Windows 陷阱。
#
# 用法：
#   powershell -NoProfile -ExecutionPolicy Bypass -File tools\comfyui\start_comfyui.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File tools\comfyui\start_comfyui.ps1 -Wait
#
# 注意：本檔必須存成 UTF-8 with BOM，否則 Windows PowerShell 5.1 會用 ANSI
# 解碼，中文註解變亂碼後可能讓字串終止符失效、整支腳本語法崩壞。
# 用同目錄的 write_ps1.py 轉換。
#
$ErrorActionPreference = 'Continue'

$ComfyRoot = 'D:\AI\ComfyUI'
$Python    = Join-Path $ComfyRoot 'python_embeded\python.exe'
$LogDir    = Join-Path $ComfyRoot 'logs'
$Port      = 8188

if (-not (Test-Path $Python)) {
    throw "找不到 ComfyUI 的 python：$Python"
}

# --- 陷阱 1：編碼 -------------------------------------------------------------
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8       = '1'
# 同時寫進 User 層，讓之後手動啟動也一致
[Environment]::SetEnvironmentVariable('PYTHONIOENCODING', 'utf-8', 'User')
[Environment]::SetEnvironmentVariable('PYTHONUTF8',       '1',       'User')

# --- 陷阱 2：comfy-kitchen 版本 ---------------------------------------------
$required = '0.2.39'
$current = (& $Python -m pip show comfy-kitchen 2>$null |
             Select-String -Pattern '^Version:\s*(\S+)' |
             ForEach-Object { $_.Matches[0].Groups[1].Value })

if ($current -ne $required) {
    Write-Host "[start_comfyui] comfy-kitchen 版本 $current -> 升級到 $required"
    & $Python -m pip install --no-input --disable-pip-version-check "comfy-kitchen==$required"
    if ($LASTEXITCODE -ne 0) {
        throw "comfy-kitchen 升級失敗"
    }
}

# --- 啟動 --------------------------------------------------------------------
# 注意：整支腳本用 Continue，不要用 Stop。
#   否則 Invoke-WebRequest 連線失敗會直接中斷腳本，catch 接不到，
#   變成「等不到就整個死掉」而不是「繼續等」。
$ErrorActionPreference = 'Continue'

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$stamp   = Get-Date -Format 'yyyyMMdd-HHmmss'
$outLog  = Join-Path $LogDir "comfy-$stamp.out.log"
$errLog  = Join-Path $LogDir "comfy-$stamp.err.log"

# 注意：工作目錄要設在 ComfyUI 根目錄，main.py 以相對路徑載入 assets。
$p = Start-Process -FilePath $Python `
        -ArgumentList '-s', 'main.py', '--windows-standalone-build' `
        -WorkingDirectory $ComfyRoot `
        -RedirectStandardOutput $outLog `
        -RedirectStandardError  $errLog `
        -PassThru -WindowStyle Hidden

Write-Host "[start_comfyui] PID = $($p.Id)"
Write-Host "[start_comfyui] out = $outLog"
Write-Host "[start_comfyui] err = $errLog"

# 等待 HTTP 就緒
$ready = $false
for ($i = 0; $i -lt 120; $i++) {
    Start-Sleep -Seconds 2
    if ($p.HasExited) {
        Write-Host "[start_comfyui] 行程已結束，最後 20 行："
        Get-Content $errLog -Tail 20 -ErrorAction SilentlyContinue
        throw "ComfyUI 啟動失敗（exit=$($p.ExitCode)）"
    }
    # 用 TCP 連線測試取代 Invoke-WebRequest：
    #   在 powershell -File 模式，Invoke-WebRequest 的連線失敗會被當成
    #   terminating error，catch 接不住，整支腳本直接死掉。
    $client = New-Object System.Net.Sockets.TcpClient
    $up = $false
    try {
        $iar = $client.BeginConnect('127.0.0.1', $Port, $null, $null)
        if ($iar.AsyncWaitHandle.WaitOne(1500, $false) -and $client.Connected) {
            $client.EndConnect($iar)
            $up = $true
        }
    } catch {
    } finally {
        $client.Close()
    }
    if ($up) {
        # TCP 通了只是 port 有 listen，HTTP 服務可能還在初始化。
        # 探測方式刻意用最底層的 System.Net.WebRequest：
        #   Invoke-WebRequest / .NET HttpClient / curl.exe 在 powershell -File
        #   模式下，連線失敗都會被升級成 terminating error 讓整支腳本死掉；
        #   WebRequest 搭配 try/catch 則不會。
        try {
            $req = [System.Net.WebRequest]::Create("http://127.0.0.1:$Port/system_stats")
            $req.Timeout = 5000
            $resp = $req.GetResponse()
            $code = [int]$resp.StatusCode
            $resp.Close()
            if ($code -eq 200) { $ready = $true; break }
        } catch {
        }
    }
}
if (-not $ready) {
    Write-Host "[start_comfyui] 等待逾時，最後 20 行："
    Get-Content $errLog -Tail 20 -ErrorAction SilentlyContinue
    throw "ComfyUI 未在 240 秒內就緒"
}

Write-Host "[start_comfyui] 就緒 → http://127.0.0.1:$Port"
$p.Id | Out-File -FilePath 'C:\Users\princ\blog\_work\comfy.pid' -Encoding ascii

if ($args -contains '-Wait') {
    Write-Host "[start_comfyui] -Wait：前景等待，按 Ctrl+C 結束"
    $p.WaitForExit()
}

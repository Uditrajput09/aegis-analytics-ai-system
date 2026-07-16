$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

function Stop-Port($port) {
    $lines = netstat -ano | Select-String ":$port\s+.*LISTENING"
    foreach ($line in $lines) {
        $parts = ($line -split "\s+") | Where-Object { $_ -ne "" }
        $procId = $parts[-1]
        if ($procId -match "^\d+$" -and [int]$procId -gt 0) {
            Write-Host "Stopping PID $procId on port $port..."
            taskkill /PID $procId /F 2>$null | Out-Null
        }
    }
    Start-Sleep -Seconds 1
}

Write-Host "=== Restarting Aegis (API + dashboard) ==="
Stop-Port 8000
Stop-Port 8501
Stop-Port 8502

& (Join-Path $PSScriptRoot "deploy.ps1")

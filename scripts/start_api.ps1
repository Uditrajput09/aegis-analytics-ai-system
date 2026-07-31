$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

$line = netstat -ano | Select-String "127.0.0.1:8000.*LISTENING"
if ($line) {
    Write-Host "API is already running at http://127.0.0.1:8000"
    Write-Host "Health check: http://127.0.0.1:8000/health"
    Write-Host "If the app is broken or outdated, run: .\scripts\restart.ps1"
    exit 0
}

Write-Host "Starting API on http://127.0.0.1:8000 ..."
& .\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

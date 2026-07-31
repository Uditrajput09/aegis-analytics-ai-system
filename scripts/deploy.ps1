$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "=== Deploy Aegis Analytics ==="

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Host "Creating venv..."
    python -m venv venv
    & .\venv\Scripts\pip.exe install -r requirements.txt
}

function Start-IfDown($port, $name, $command) {
    $listening = netstat -ano | Select-String ":$port\s+.*LISTENING"
    if ($listening) {
        Write-Host "$name already on port $port"
        return
    }
    Write-Host "Starting $name on port $port..."
    Start-Process powershell -ArgumentList @(
        "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
        "Set-Location '$PWD'; $command"
    ) -WindowStyle Minimized
}

Start-IfDown 8000 "API" ".\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"
Start-Sleep -Seconds 3

$env:API_BASE_URL = "http://127.0.0.1:8000"
Start-IfDown 8501 "Dashboard" "`$env:API_BASE_URL='http://127.0.0.1:8000'; .\venv\Scripts\python.exe -m streamlit run dashboard/app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false"
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "  Dashboard: http://localhost:8501"
Write-Host "  API:       http://127.0.0.1:8000"
Write-Host ""
Write-Host "If the site looks broken or stale, run: .\scripts\restart.ps1"
Write-Host ""

& (Join-Path $PSScriptRoot "health_check.ps1")

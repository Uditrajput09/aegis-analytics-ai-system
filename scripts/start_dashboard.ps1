$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

$api = netstat -ano | Select-String "127.0.0.1:8000.*LISTENING"
if (-not $api) {
    Write-Host "WARNING: API is not running on port 8000. Start it first:"
    Write-Host "  .\scripts\start_api.ps1"
}

$line = netstat -ano | Select-String ":8501.*LISTENING"
if ($line) {
    Write-Host "Dashboard already running at http://localhost:8501"
    Write-Host "If the app is broken or outdated, run: .\scripts\restart.ps1"
    exit 0
}

$env:API_BASE_URL = "http://127.0.0.1:8000"
Write-Host "Starting dashboard at http://localhost:8501 ..."
& .\venv\Scripts\python.exe -m streamlit run dashboard/app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false

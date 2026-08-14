$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "=== Deploy Aegis Analytics AI ==="

# 1. Verify Python Virtual Environment
if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Host "Creating Python venv..."
    python -m venv venv
    & .\venv\Scripts\pip.exe install -r requirements.txt
}

# 2. Build React Frontend Production Bundle
if (Test-Path ".\frontend") {
    Write-Host "Building React/TypeScript Frontend..."
    Push-Location ".\frontend"
    if (-not (Test-Path ".\node_modules")) {
        Write-Host "Installing frontend node dependencies..."
        npm install
    }
    npm run build
    Pop-Location
}

# 3. Helper Function to Start Service if Down
function Start-IfDown($port, $name, $command) {
    $listening = netstat -ano | Select-String ":$port\s+.*LISTENING"
    if ($listening) {
        Write-Host "$name already listening on port $port"
        return
    }
    Write-Host "Starting $name on port $port..."
    Start-Process powershell -ArgumentList @(
        "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
        "Set-Location '$PWD'; $command"
    ) -WindowStyle Minimized
}

# 4. Start FastAPI Backend Service (Port 8000)
Start-IfDown 8000 "FastAPI Backend" ".\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"
Start-Sleep -Seconds 3

# 5. Start New React Frontend Application (Port 3000)
Start-IfDown 3000 "React SPA Frontend" "Set-Location 'frontend'; npm run dev -- --host 127.0.0.1 --port 3000"
Start-Sleep -Seconds 2

# 6. Start Streamlit Dashboard (Backup Frontend - Port 8501)
$env:API_BASE_URL = "http://127.0.0.1:8000"
Start-IfDown 8501 "Streamlit Dashboard (Backup)" "`$env:API_BASE_URL='http://127.0.0.1:8000'; .\venv\Scripts\python.exe -m streamlit run dashboard/app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "=========================================================="
Write-Host "  AEGIS ANALYTICS AI SYSTEM SERVICES ONLINE"
Write-Host "=========================================================="
Write-Host "  React SPA Frontend:    http://localhost:3000"
Write-Host "  FastAPI REST API:      http://127.0.0.1:8000"
Write-Host "  Streamlit Dashboard:   http://localhost:8501"
Write-Host "=========================================================="
Write-Host ""
Write-Host "If any service looks stale or unresponsive, run: .\scripts\restart.ps1"
Write-Host ""

& (Join-Path $PSScriptRoot "health_check.ps1")

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..\frontend")

Write-Host "=== Starting Aegis React/TS Frontend ==="

if (-not (Test-Path ".\node_modules")) {
    Write-Host "Installing node dependencies..."
    npm install
}

Write-Host "Starting Vite development server on http://localhost:3000..."
npm run dev -- --host 127.0.0.1 --port 3000

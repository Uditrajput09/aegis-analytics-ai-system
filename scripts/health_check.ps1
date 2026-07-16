$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")



$apiBase = if ($env:API_BASE_URL) { $env:API_BASE_URL } else { "http://127.0.0.1:8000" }

$failed = 0



function Test-Url($name, $url) {

    try {

        $r = Invoke-WebRequest -Uri $url -TimeoutSec 60 -UseBasicParsing

        Write-Host "[OK] $name"

        return $true

    }

    catch {

        Write-Host "[FAIL] $name — $($_.Exception.Message)"

        $script:failed++

        return $false

    }

}



Write-Host "=== Health check ==="

if (-not (Test-Path ".\venv\Scripts\python.exe")) {

    Write-Host "[FAIL] venv missing"

    exit 1

}

$mc = (Get-ChildItem ".\models\*.joblib" -ErrorAction SilentlyContinue).Count

if ($mc -eq 0) { Write-Host "[WARN] No models"; $failed++ } else { Write-Host "[OK] $mc model artifacts" }



Test-Url "API /health" "$apiBase/health" | Out-Null

Test-Url "API predictions" "$apiBase/predictions/latest?symbol=AAPL&horizon=5m" | Out-Null

Test-Url "API bars" "$apiBase/bars/recent?symbol=AAPL&timeframe=1m&limit=10" | Out-Null

Test-Url "Dashboard" "http://localhost:8501" | Out-Null



& .\venv\Scripts\python.exe -c @"

import requests

base = '$apiBase'

for sym in ['AAPL','MSFT','GOOGL']:

    for h in ['5m','15m','60m','1d']:

        tf = '1m' if h.endswith('m') else '1d'

        for path in ['predictions/latest','risk/latest']:

            r = requests.get(f'{base}/{path}', params={'symbol':sym,'horizon':h,'timeframe':tf}, timeout=90)

            if r.status_code != 200:

                raise SystemExit(f'FAIL {path} {sym}/{h}: {r.status_code}')

print('[OK] All symbols x horizons')

"@

if ($LASTEXITCODE -ne 0) { $failed++ }



if ($failed -gt 0) { exit 1 }

Write-Host "All checks passed."


param(
    [Parameter(Position = 0)]
    [string]$Message = "Update repository changes",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path "$PSScriptRoot\.."
Push-Location $repoRoot
try {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Error "Git is not available in PATH. Install Git or update your PATH."
        exit 1
    }

    $status = git status --porcelain
    if (-not $status) {
        Write-Host "No changes to commit."
        exit 0
    }

    git add -A

    if (-not $Force) {
        Write-Host "Changes detected. Preparing to commit with message:`n$Message"
    }

    git commit -m $Message

    $branch = git branch --show-current
    if (-not $branch) {
        Write-Error "Unable to detect current branch."
        exit 1
    }

    git push origin $branch
    Write-Host "Changes pushed to origin/$branch."
}
finally {
    Pop-Location
}

param(
    [switch]$Install
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root '.venv\Scripts\python.exe'
$backendDir = Join-Path $root 'backend'
$frontendDir = Join-Path $root 'frontend'

if (-not (Test-Path $python)) {
    throw "Python virtual environment not found at $python"
}

if ($Install) {
    & $python -m pip install -r (Join-Path $backendDir 'requirements.txt')
    Push-Location $frontendDir
    npm install
    Pop-Location
}

$backendCommand = "Set-Location '$backendDir'; & '$python' -m uvicorn app.main:app --reload --port 8000"
$frontendCommand = "Set-Location '$frontendDir'; npm run dev"

Start-Process pwsh -ArgumentList '-NoExit', '-Command', $backendCommand | Out-Null
Start-Process pwsh -ArgumentList '-NoExit', '-Command', $frontendCommand | Out-Null

Write-Host 'Started backend on http://localhost:8000 and frontend on http://localhost:5173'
Write-Host 'Configure backend/.env to point MODEL_SERVER_URL at an already-running Qwen-compatible endpoint.'
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendRoot = Join-Path $projectRoot "frontend"
$venvPython = Join-Path $projectRoot ".venv\\Scripts\\python.exe"

if (-not (Test-Path $venvPython)) {
    throw "Python interpreter not found: $venvPython"
}

if (-not (Test-Path (Join-Path $projectRoot "manage.py"))) {
    throw "manage.py not found in project root: $projectRoot"
}

if (-not (Test-Path (Join-Path $frontendRoot "package.json"))) {
    throw "frontend/package.json not found: $frontendRoot"
}

$backendCommand = "Set-Location '$projectRoot'; & '$venvPython' manage.py runserver"
$frontendCommand = "Set-Location '$frontendRoot'; npm.cmd run dev -- --host 127.0.0.1 --port 5173"

Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command", $backendCommand
)

Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command", $frontendCommand
)

Write-Host "Backend started in a new PowerShell window: http://127.0.0.1:8000"
Write-Host "Frontend started in a new PowerShell window: http://127.0.0.1:5173"

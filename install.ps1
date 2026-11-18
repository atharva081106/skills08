<#
.SYNOPSIS
    Skills08 One-Line Windows Installer
.DESCRIPTION
    Installs Skills08 directly into the user profile and configures the environment.
.EXAMPLE
    irm https://raw.githubusercontent.com/atharva081106/skills08/main/install.ps1 | iex
#>

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host "     ⚡ Skills08 — The Package Manager for AI Agent Skills         " -ForegroundColor Yellow
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Locate Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "[FAIL] Python 3 (>= 3.8) is required, but python was not found in your PATH."
    Write-Host "Please install Python from https://www.python.org/ or the Microsoft Store and try again." -ForegroundColor Red
    exit 1
}

$pyVer = & $pythonCmd.Source -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Host "[OK] Detected Python $pyVer ($($pythonCmd.Source))" -ForegroundColor Green

# 2. Install or Upgrade via Pip
Write-Host "-> Installing Skills08 from GitHub..." -ForegroundColor Cyan
try {
    & $pythonCmd.Source -m pip install --upgrade --quiet "git+https://github.com/atharva081106/skills08.git"
    Write-Host "[OK] Skills08 installed successfully via pip." -ForegroundColor Green
} catch {
    Write-Host "[WARN] Direct git pip install failed. Falling back to local clone..." -ForegroundColor Yellow
    $installDir = Join-Path $HOME ".skills08\skills08-cli"
    if (Test-Path $installDir) {
        git -C $installDir pull --quiet
    } else {
        git clone --quiet https://github.com/atharva081106/skills08.git $installDir
    }
    & $pythonCmd.Source -m pip install -e $installDir --quiet
    Write-Host "[OK] Skills08 installed from local mirror." -ForegroundColor Green
}

# 3. Verify Installation
Write-Host "-> Verifying installation..." -ForegroundColor Cyan
try {
    skills08 --version
    Write-Host ""
    Write-Host "🎉 Skills08 is ready to use!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Quick commands to get started:" -ForegroundColor Yellow
    Write-Host "  skills08 doctor                     # Verify your environment" -ForegroundColor White
    Write-Host "  skills08 list                       # Browse 12 production skills" -ForegroundColor White
    Write-Host "  skills08 install security-audit -s  # Install & sync across Cursor, Claude, Antigravity" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "[WARN] 'skills08' command not found in current session PATH." -ForegroundColor Yellow
    Write-Host "Please restart your terminal or run: python -m skills08.cli" -ForegroundColor Yellow
}

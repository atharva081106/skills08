<#
.SYNOPSIS
    Skills08: Native PowerShell Entrypoint for Windows
.DESCRIPTION
    Local-first AI Agent Skill Distribution & Lifecycle Manager for Google Antigravity.
.EXAMPLE
    .\skills08.ps1 list
    .\skills08.ps1 inspect security-audit
    .\skills08.ps1 install security-audit --scope project
    .\skills08.ps1 status
    .\skills08.ps1 verify
#>

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ScriptArgs
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "skills08.py"

# Locate Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "Python 3 is required to run Skills08, but python was not found in PATH."
    exit 1
}

& $pythonCmd.Source $pythonScript @ScriptArgs
exit $LASTEXITCODE


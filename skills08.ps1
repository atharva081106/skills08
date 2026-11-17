<#
.SYNOPSIS
    Skills08: Native PowerShell Entrypoint for Windows
.DESCRIPTION
    Local-first AI Agent Skill Distribution & Lifecycle Manager for Google Antigravity,
    Cursor, Claude Code, and Gemini CLI on Windows 10/11.
.EXAMPLE
    .\skills08.ps1 list
    .\skills08.ps1 search frontend
    .\skills08.ps1 inspect security-audit
    .\skills08.ps1 install security-audit -w "D:\MyProject"
    .\skills08.ps1 status --scope project
    .\skills08.ps1 conflicts
    .\skills08.ps1 verify
    .\skills08.ps1 new my-skill --description "Custom skill"
    .\skills08.ps1 pack .\packages\humanizer
    .\skills08.ps1 doctor
    .\skills08.ps1 agent-init
#>

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ScriptArgs
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "skills08.py"

# Locate Python executable
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "Python 3 (>= 3.8) is required to run Skills08, but python was not found in PATH."
    exit 1
}

& $pythonCmd.Source $pythonScript @ScriptArgs
exit $LASTEXITCODE

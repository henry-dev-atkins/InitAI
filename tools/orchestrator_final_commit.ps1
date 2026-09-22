param(
    [Parameter(Mandatory = $true)][string]$TerminalReview,
    [Parameter(Mandatory = $true)][string]$Message
)

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "orchestrator_final_commit.py"
& python -B $scriptPath --terminal-review $TerminalReview --message $Message
exit $LASTEXITCODE

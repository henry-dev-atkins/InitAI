param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][ValidateSet("create", "overwrite", "append")][string]$Mode,
    [Parameter(Mandatory = $true)][string]$ContentBase64
)

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "write_ai_space_artifact.py"
& python $scriptPath --path $Path --mode $Mode --content-base64 $ContentBase64
exit $LASTEXITCODE

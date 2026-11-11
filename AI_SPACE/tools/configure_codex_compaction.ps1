param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)
py -3 (Join-Path $PSScriptRoot 'configure_codex_compaction.py') @Arguments
exit $LASTEXITCODE

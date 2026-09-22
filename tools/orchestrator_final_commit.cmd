@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0orchestrator_final_commit.ps1" %*
exit /b %ERRORLEVEL%

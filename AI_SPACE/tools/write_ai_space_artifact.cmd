@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0write_ai_space_artifact.ps1" %*
exit /b %ERRORLEVEL%

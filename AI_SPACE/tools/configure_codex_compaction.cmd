@echo off
py -3 "%~dp0configure_codex_compaction.py" %*
exit /b %ERRORLEVEL%

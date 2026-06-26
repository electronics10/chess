@echo off
REM Launch the chess game on Windows.
REM Uses uv if available, otherwise falls back to a system Python.

cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL%==0 (
    uv run main.py
    goto :eof
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py main.py
    goto :eof
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
    python main.py
    goto :eof
)

echo Python was not found. Please install Python 3.12+ from https://www.python.org/downloads/
pause

@echo off
REM Simple helper to start the AI Spiral Simulator on Windows

REM Load environment variables from .env if present
if exist ..\.env (
    for /f "usebackq delims=" %%A in ("..\.env") do set %%A
)

python -m localspiral.main


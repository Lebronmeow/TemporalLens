@echo off
title TemporalLens AI - Grounding Workstation Launcher
echo =====================================================================
echo  TemporalLens AI: Natural Language Video Temporal Grounding System
echo  College Mini Project Demonstration
echo =====================================================================
echo.
cd /d "%~dp0"

echo Activating Python 3.10 CUDA Environment (.venv)...
call .venv\Scripts\activate.bat

echo Starting Demo Web Interface on http://localhost:7860 ...
python demo\app.py %*

pause

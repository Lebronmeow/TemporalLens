@echo off
title TemporalLens AI - College Mini Project Demo
echo =====================================================================
echo  TemporalLens AI: Natural Language Video Temporal Grounding System
echo  College Mini Project Demonstration
echo =====================================================================
echo.
cd /d "%~dp0"

echo Activating Python 3.10 CUDA Environment (.venv)...
call .venv\Scripts\activate.bat

echo Starting Demo Web Interface...
python app.py %*

pause

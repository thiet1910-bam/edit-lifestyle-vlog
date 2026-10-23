@echo off
chcp 65001 >nul
title CAI DAT MOI TRUONG AI VIDEO EDITOR 1-CLICK
cd /d "%~dp0"

echo ============================================================================
echo   DANG TU DONG CAI DAT THU VIEN PYTHON (Pillow + FFmpeg Engine)...
echo ============================================================================
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo [HOAN TAT 100%%] Moi truong da san sang!
pause

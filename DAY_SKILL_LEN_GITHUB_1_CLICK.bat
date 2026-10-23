@echo off
chcp 65001 >nul
title TU DONG DAY SKILL EDIT-LIFESTYLE-VLOG LEN GITHUB
cd /d "%~dp0"

echo ============================================================================
echo   TU DONG HOA DAY SKILL [edit-lifestyle-vlog] LEN GITHUB
echo   (Chuan he sinh thai Agent Skills: Antigravity / Claude Code / Cursor)
echo ============================================================================
echo.
echo Huong dan nhanh:
echo   1. Mo trinh duyet vao: https://github.com/new
echo   2. Dat ten Repository la: edit-lifestyle-vlog (chon Public hoac Private, KHONG tich Add README)
echo   3. Bam "Create repository" va copy duong link https://github.com/.../edit-lifestyle-vlog.git
echo.
set /p REPO_URL="👉 Dan link GitHub Repository cua ban vao day (rồi bấm Enter): "

if "%REPO_URL%"=="" (
    echo [LOI] Ban chua nhap link GitHub Repository!
    pause
    exit /b 1
)

echo.
echo [1/3] Dang cau hinh Git Remote Origin...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [2/3] Dang cap nhat cac thay doi moi nhat...
git add .
git commit -m "chore: update skill package for GitHub release" 2>nul

echo [3/3] Dang day (push) len GitHub (Neu cua so dang nhap GitHub hien ra, hay bam Sign in with Browser)...
git branch -M main
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ============================================================================
    echo   [THANH CONG 100%%] DA DAY SKILL LEN GITHUB!
    echo   Link Repo: %REPO_URL%
    echo   Lenh cai dat tren may bat ky: npx skills add %REPO_URL%
    echo ============================================================================
) else (
    echo [THONG BAO] Neu chua dang nhap GitHub, hay dang nhap tren cua so hien ra va chay lai file nay.
)
pause

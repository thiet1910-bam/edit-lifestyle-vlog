@echo off
chcp 65001 >nul
title TU DONG DAY SKILL LEN GITHUB [thiet1910-bam/edit-lifestyle-vlog]
cd /d "%~dp0"

set REPO_URL=https://github.com/thiet1910-bam/edit-lifestyle-vlog.git

echo ============================================================================
echo   TU DONG DAY SKILL LEN TAI KHOAN: https://github.com/thiet1910-bam
echo   Repository dich: %REPO_URL%
echo ============================================================================
echo.
echo [BUOC 1] Dang mo trang tao Repository (da dien san ten "edit-lifestyle-vlog")...
start "" "https://github.com/new?name=edit-lifestyle-vlog&description=3-Step+AI+Video+Editor+Skill+for+9:16+Lifestyle+Vlogs"
echo   👉 Tren trinh duyet vua mo, ban chi can keo xuong bam nut xanh "Create repository"!
echo.
pause

echo.
echo [BUOC 2] Dang ket noi va day (push) toan bo Skill len %REPO_URL%...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ============================================================================
    echo   [THANH CONG 100%%] DA DAY SKILL LEN GITHUB CUA BAN!
    echo   👉 Xem ngay tai: https://github.com/thiet1910-bam/edit-lifestyle-vlog
    echo   👉 Lenh cai dat Skill (kieu Remotion/Hyperframes):
    echo      npx skills add thiet1910-bam/edit-lifestyle-vlog
    echo ============================================================================
    start "" "https://github.com/thiet1910-bam/edit-lifestyle-vlog"
) else (
    echo [LUU Y] Neu ban chua bam "Create repository" tren web hoac chua dang nhap GitHub,
    echo hay bam "Create repository" tren trinh duyet roi chay lai file nay nhe!
)
pause

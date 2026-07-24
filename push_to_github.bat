@echo off
echo ====================================
echo  Market World - Push to GitHub
echo ====================================

cd /d c:\Users\user\Desktop\pakages\retailplatform\config

:: Stage all changes
git add .

:: Create commit message with timestamp
for /f "tokens=1-5 delims=/ " %%a in ('date /t') do set DATE=%%c-%%b-%%a
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIME=%%a:%%b
set MSG=Auto update - %DATE% %TIME%

:: Check if there are changes to commit
git diff --cached --quiet
if %errorlevel% == 0 (
    echo No changes to commit.
) else (
    git commit -m "%MSG%"
    git push origin main
    echo.
    echo Changes pushed to GitHub successfully!
)

pause

@echo off
setlocal
cd /d "%~dp0"

echo ========================================================
echo   AnemiaScan - Automatic GitHub Repository Sync
echo ========================================================

where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Git is not installed or not in PATH.
    pause
    exit /b 1
)

echo [1/3] Staging all modified and new files...
git add .

git diff --cached --quiet
if %ERRORLEVEL% equ 0 (
    echo [INFO] No new changes detected. Working tree is clean.
    echo Everything is already up to date with GitHub!
    pause
    exit /b 0
)

set "COMMIT_MSG=%*"
if "%COMMIT_MSG%"=="" (
    set "COMMIT_MSG=Update AnemiaScan: %date% %time%"
)

echo [2/3] Committing changes: "%COMMIT_MSG%"...
git commit -m "%COMMIT_MSG%"

echo [3/3] Pushing updates to GitHub (main branch)...
git push origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================================
    echo   [SUCCESS] Successfully pushed all updates to GitHub!
    echo   Repo: https://github.com/28082006gani/anemia-detection-using-conjunctival-images
    echo ========================================================
) else (
    echo.
    echo [ERROR] Git push failed. Please verify your GitHub authentication.
)

echo.
pause

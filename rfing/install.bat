@echo off
:: ════════════════════════════════════════════════════════════════════════════
::  CBA_ODA Production Rebuilder — Windows WSL Installer
::  Double-click this file on Windows to launch the full installation inside
::  Ubuntu WSL.  It will:
::    1. Check that WSL / Ubuntu is installed
::    2. Copy the project into ~/rfing inside WSL
::    3. Run the mega_rebuild.sh script to install every dependency and bot
:: ════════════════════════════════════════════════════════════════════════════
title CBA_ODA Production Rebuilder — WSL Installer

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║   CBA_ODA Production Rebuilder — Windows WSL Installer  ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

:: ── 1. Verify WSL is available ───────────────────────────────────────────────
wsl --status >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] WSL is not installed or not enabled.
    echo.
    echo  Please install WSL by opening PowerShell as Administrator and running:
    echo    wsl --install
    echo  Then restart your computer and run this installer again.
    pause
    exit /b 1
)

:: ── 2. Verify Ubuntu distribution is available ───────────────────────────────
wsl -d Ubuntu -e echo OK >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Ubuntu distribution not found in WSL.
    echo.
    echo  Please install Ubuntu from the Microsoft Store:
    echo    https://aka.ms/wslubuntu
    echo  Then run this installer again.
    pause
    exit /b 1
)

echo [OK] WSL + Ubuntu detected.
echo.

:: ── 3. Get the Windows path to this script's folder ─────────────────────────
set "WIN_DIR=%~dp0"
:: Strip trailing backslash
if "%WIN_DIR:~-1%"=="\" set "WIN_DIR=%WIN_DIR:~0,-1%"

:: Convert Windows path to a WSL-accessible /mnt/... path
:: e.g.  C:\Users\rfing\rfing  ->  /mnt/c/Users/rfing/rfing
set "DRIVE=%WIN_DIR:~0,1%"
set "REST=%WIN_DIR:~3%"
set "REST=%REST:\=/%"
set "WSL_SRC=/mnt/%DRIVE%/%REST%"
:: Make drive letter lowercase (WSL uses lowercase)
for %%i in (a b c d e f g h i j k l m n o p q r s t u v w x y z) do (
    if /i "%DRIVE%"=="%%i" set "DRIVE=%%i"
)
set "WSL_SRC=/mnt/%DRIVE%/%REST%"

echo [INFO] Project source (WSL path): %WSL_SRC%
echo.

:: ── 4. Run the mega_rebuild.sh inside Ubuntu WSL ─────────────────────────────
echo [INFO] Launching Ubuntu WSL — this window will stay open until complete.
echo        You may be prompted for your WSL sudo password.
echo.

wsl -d Ubuntu -e bash -c "bash '%WSL_SRC%/mega_rebuild.sh' '%WSL_SRC%' 2>&1"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation encountered errors. Review the output above.
    pause
    exit /b 1
)

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║   Installation Complete!                                 ║
echo  ║                                                          ║
echo  ║   Open a new Ubuntu WSL terminal and run:               ║
echo  ║     cd ~/rfing                                           ║
echo  ║     bash scripts/start_all.sh                           ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.
pause

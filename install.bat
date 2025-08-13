@echo off
REM Windows installation script for hvym_press
REM Run this as administrator for system-wide installation

echo Installing hvym_press for Windows...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install dependencies
echo Installing Python dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Build the executable
echo Building executable...
python build.py
if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

REM Create installation directory
set INSTALL_DIR=%LOCALAPPDATA%\heavymeta-cli
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
echo Installing to %INSTALL_DIR%...
copy "release\hvym_press.exe" "%INSTALL_DIR%\" >nul
if errorlevel 1 (
    echo Error: Failed to copy executable
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo Application installed to: %INSTALL_DIR%
echo.
echo To run the application, you can:
echo 1. Navigate to %INSTALL_DIR% and double-click hvym_press.exe
echo 2. Add %INSTALL_DIR% to your PATH environment variable
echo.
pause

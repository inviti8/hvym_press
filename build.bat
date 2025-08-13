@echo off
REM Windows batch file for cross-platform build script
REM Provides easy access to common build options

echo.
echo ========================================
echo    HVYM Press Build System (Windows)
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if build script exists
if not exist "build_cross_platform.py" (
    echo ERROR: build_cross_platform.py not found
    echo Please ensure you're in the correct directory
    echo.
    pause
    exit /b 1
)

echo Available build options:
echo.
echo 1. Build for Windows (default)
echo 2. Build and install to test directory
echo 3. Check dependencies only
echo 4. Clean build artifacts
echo 5. Custom build with options
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Building for Windows...
    python build_cross_platform.py
) else if "%choice%"=="2" (
    echo.
    echo Building and installing to test directory...
    python build_cross_platform.py --test
) else if "%choice%"=="3" (
    echo.
    echo Checking dependencies...
    python build_cross_platform.py --check-deps
) else if "%choice%"=="4" (
    echo.
    echo Cleaning build artifacts...
    python build_cross_platform.py --clean
) else if "%choice%"=="5" (
    echo.
    echo Custom build options:
    echo Available flags: --test, --verbose, --clean, --check-deps
    echo.
    set /p custom_opts="Enter custom options: "
    echo.
    echo Running: python build_cross_platform.py %custom_opts%
    python build_cross_platform.py %custom_opts%
) else (
    echo.
    echo Invalid choice. Using default build...
    python build_cross_platform.py
)

echo.
echo Build process completed.
echo.
pause

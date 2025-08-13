#!/bin/bash

# Unix shell script for cross-platform build script
# Provides easy access to common build options

echo
echo "========================================"
echo "    HVYM Press Build System (Unix)"
echo "========================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.8+"
        echo
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if build script exists
if [ ! -f "build_cross_platform.py" ]; then
    echo "ERROR: build_cross_platform.py not found"
    echo "Please ensure you're in the correct directory"
    echo
    exit 1
fi

# Make build script executable
chmod +x build_cross_platform.py

echo "Available build options:"
echo
echo "1. Build for current platform (default)"
echo "2. Build and install to test directory"
echo "3. Check dependencies only"
echo "4. Clean build artifacts"
echo "5. Custom build with options"
echo "6. Show help"
echo

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo
        echo "Building for current platform..."
        $PYTHON_CMD build_cross_platform.py
        ;;
    2)
        echo
        echo "Building and installing to test directory..."
        $PYTHON_CMD build_cross_platform.py --test
        ;;
    3)
        echo
        echo "Checking dependencies..."
        $PYTHON_CMD build_cross_platform.py --check-deps
        ;;
    4)
        echo
        echo "Cleaning build artifacts..."
        $PYTHON_CMD build_cross_platform.py --clean
        ;;
    5)
        echo
        echo "Custom build options:"
        echo "Available flags: --test, --verbose, --clean, --check-deps"
        echo
        read -p "Enter custom options: " custom_opts
        echo
        echo "Running: $PYTHON_CMD build_cross_platform.py $custom_opts"
        $PYTHON_CMD build_cross_platform.py $custom_opts
        ;;
    6)
        echo
        echo "Showing help..."
        $PYTHON_CMD build_cross_platform.py --help
        ;;
    *)
        echo
        echo "Invalid choice. Using default build..."
        $PYTHON_CMD build_cross_platform.py
        ;;
esac

echo
echo "Build process completed."
echo

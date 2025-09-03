#!/bin/bash
set -e

# Create necessary directories
mkdir -p build release

# Install dependencies
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller==5.13.0

# Build the executable
echo "Building executable..."
python build_cross_platform.py --exclude _tkinter --exclude _ssl

# Verify the executable was created
if [ ! -f "release/hvym_press" ]; then
    echo "ERROR: Build failed - executable not found in release/"
    exit 1
fi

# Set executable permissions
chmod +x release/hvym_press

# Verify the executable works
if ! ./release/hvym_press --version; then
    echo "ERROR: Built executable failed to run"
    exit 1
fi

echo "Build completed successfully!"
echo "Executable is available at: $(pwd)/release/hvym_press"
exit 0

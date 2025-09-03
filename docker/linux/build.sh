#!/bin/bash
set -e

# Print environment info
echo "=== Build Environment ==="
uname -a
python --version
pip --version

# Ensure directories exist with correct permissions
echo "\n=== Setting up directories ==="
mkdir -p /app/build /app/release
chmod -R 755 /app/build /app/release

# Ensure we have write permissions in the build directories
chmod -R u+w /app/build /app/release

# Install dependencies
echo "\n=== Installing dependencies ==="
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller==5.13.0

# Verify PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "ERROR: PyInstaller not found after installation"
    exit 1
fi

# Build the executable
echo "\n=== Building executable ==="
cd /app
python build_cross_platform.py --exclude _tkinter --exclude _ssl

# Verify the executable was created
if [ ! -f "release/hvym_press" ]; then
    echo "ERROR: Build failed - executable not found in release/"
    ls -la release/ 2>/dev/null || echo "release/ directory not found"
    exit 1
fi

# Set executable permissions
chmod +x release/hvym_press

# Verify the executable works
echo "\n=== Verifying executable ==="
if ! ./release/hvym_press --version; then
    echo "ERROR: Built executable failed to run"
    ldd release/hvym_press 2>/dev/null || echo "ldd not available"
    exit 1
fi

echo "\n=== Build completed successfully! ==="
ls -lh release/hvym_press
echo "Executable is available at: $(pwd)/release/hvym_press"
exit 0

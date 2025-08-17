#!/usr/bin/env python3
"""
Icon conversion script for hvym_press
Converts PNG logo to various icon formats for different platforms
"""

from PIL import Image
import os
import platform

def convert_to_ico():
    """Convert PNG logo to ICO format with multiple sizes for Windows"""
    try:
        img = Image.open("images/logo.png")
        sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
        
        # Create ICO file with multiple sizes
        img.save("images/logo.ico", format='ICO', sizes=sizes)
        print("SUCCESS: Created logo.ico with multiple sizes")
        return True
    except Exception as e:
        print(f"ERROR: Failed to create logo.ico: {e}")
        return False

def convert_to_icns():
    """Convert PNG logo to ICNS format for macOS (if possible)"""
    try:
        # For now, we'll use PNG directly as ICNS conversion requires additional tools
        # The PNG can be used directly by PyInstaller on macOS
        print("INFO: Using PNG format for macOS (PyInstaller supports this)")
        return True
    except Exception as e:
        print(f"WARNING: ICNS conversion not available: {e}")
        return False

def main():
    """Main conversion function"""
    print("ICON CONVERSION: hvym_press")
    print("=" * 40)
    
    # Check if images directory exists
    if not os.path.exists("images"):
        print("ERROR: images directory not found")
        return False
    
    if not os.path.exists("images/logo.png"):
        print("ERROR: images/logo.png not found")
        return False
    
    success = True
    
    # Convert to ICO for Windows
    if platform.system() == "Windows" or True:  # Always create ICO for cross-platform builds
        success &= convert_to_ico()
    
    # Handle macOS format
    if platform.system() == "Darwin":
        success &= convert_to_icns()
    
    if success:
        print("\nSUCCESS: Icon conversion completed!")
        print("Available icon files:")
        if os.path.exists("images/logo.ico"):
            print("  - images/logo.ico (Windows)")
        print("  - images/logo.png (Linux/macOS)")
    else:
        print("\nERROR: Some icon conversions failed!")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

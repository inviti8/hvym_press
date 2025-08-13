#!/usr/bin/env python3
"""
Cross-platform installation script for hvym_press
Replaces the Unix-specific install.sh
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def get_install_dir():
    """Get the appropriate installation directory for the current platform"""
    home = Path.home()
    
    if platform.system() == "Windows":
        # Windows: %LOCALAPPDATA%\heavymeta-cli
        return home / "AppData" / "Local" / "heavymeta-cli"
    elif platform.system() == "Darwin":  # macOS
        # macOS: ~/Library/Application Support/heavymeta-cli
        return home / "Library" / "Application Support" / "heavymeta-cli"
    else:
        # Linux and others: ~/.local/share/heavymeta-cli
        return home / ".local" / "share" / "heavymeta-cli"

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False
    return True

def copy_executable():
    """Copy the executable to the installation directory"""
    install_dir = get_install_dir()
    
    # Create installation directory if it doesn't exist
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Find the executable
    if platform.system() == "Windows":
        exe_name = "hvym_press.exe"
    else:
        exe_name = "hvym_press"
    
    # Look for executable in common locations
    possible_locations = [
        Path("release") / exe_name,
        Path("dist") / exe_name,
        Path("build") / "dist" / "linux" / exe_name,
        Path("build") / "dist" / "mac" / exe_name,
        Path("build") / "dist" / "windows" / exe_name,
    ]
    
    exe_path = None
    for location in possible_locations:
        if location.exists():
            exe_path = location
            break
    
    if not exe_path:
        print(f"✗ Could not find {exe_name} executable")
        print("Please build the project first using: python build.py")
        return False
    
    # Copy executable to installation directory
    target_path = install_dir / exe_name
    try:
        shutil.copy2(exe_path, target_path)
        print(f"✓ Executable copied to: {target_path}")
        
        # Make executable on Unix-like systems
        if platform.system() != "Windows":
            os.chmod(target_path, 0o755)
            print("✓ Executable permissions set")
        
        return True
    except Exception as e:
        print(f"✗ Failed to copy executable: {e}")
        return False

def create_symlink():
    """Create a symlink or copy to make the command available system-wide"""
    install_dir = get_install_dir()
    
    if platform.system() == "Windows":
        # On Windows, add to PATH or create a .bat file
        print("Note: On Windows, you may need to add the installation directory to your PATH")
        print(f"Installation directory: {install_dir}")
        return True
    else:
        # On Unix-like systems, try to create a symlink in a directory that's in PATH
        bin_dirs = [
            Path.home() / ".local" / "bin",
            Path("/usr/local/bin"),
            Path("/usr/bin"),
        ]
        
        for bin_dir in bin_dirs:
            if bin_dir.exists() and os.access(bin_dir, os.W_OK):
                try:
                    symlink_path = bin_dir / "hvym_press"
                    if symlink_path.exists():
                        symlink_path.unlink()
                    
                    os.symlink(install_dir / "hvym_press", symlink_path)
                    print(f"✓ Symlink created: {symlink_path}")
                    return True
                except Exception as e:
                    continue
        
        print("Note: Could not create system-wide symlink")
        print(f"You can run the application from: {install_dir / 'hvym_press'}")
        return True

def main():
    """Main installation function"""
    print("Installing hvym_press...")
    print(f"Platform: {platform.system()}")
    print(f"Installation directory: {get_install_dir()}")
    print()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Copy executable
    if not copy_executable():
        sys.exit(1)
    
    # Create symlink
    create_symlink()
    
    print()
    print("Installation completed successfully!")
    print(f"Application installed to: {get_install_dir()}")
    
    if platform.system() == "Windows":
        print("You can run the application by navigating to the installation directory")
        print("or by adding it to your PATH environment variable.")
    else:
        print("You can run the application using: hvym_press")

if __name__ == "__main__":
    main()

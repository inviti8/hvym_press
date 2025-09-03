#!/usr/bin/env python3
"""
Cross-platform build script for hvym_press
Replaces the Linux-specific build.py with universal platform support
"""

import os
import sys
import shutil
import subprocess
import platform
import argparse
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class BuildConfig:
    """Configuration class for build settings"""

    def __init__(self):
        self.project_name = "hvym_press"
        self.source_files = [
            "app.py",
            "ColorPicker.py",
            "HVYM.py",
            "IconPicker.py",
            "LoadingWindow.py",
            "MarkdownHandler.py",
            "ServerHandler.py",
            "SiteDataHandler.py",
            "TreeData.py",
            "W3DeployHandler.py",
            "requirements.txt",
        ]

        self.resource_dirs = ["templates", "images", "serve"]

        self.excluded_dirs = {
            ".git",
            ".vscode",
            "__pycache__",
            "node_modules",
            "venv",
            "env",
        }
        self.excluded_files = {".gitignore", ".DS_Store", "Thumbs.db"}


class PlatformManager:
    """Manages platform-specific build configurations"""

    def __init__(self):
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        self.arch = platform.architecture()[0]

    @property
    def is_windows(self) -> bool:
        return self.system == "windows"

    @property
    def is_macos(self) -> bool:
        return self.system == "darwin"

    @property
    def is_linux(self) -> bool:
        return self.system == "linux"

    @property
    def executable_name(self) -> str:
        return (
            f"{BuildConfig().project_name}.exe"
            if self.is_windows
            else BuildConfig().project_name
        )

    @property
    def add_data_separator(self) -> str:
        return ";" if self.is_windows else ":"

    @property
    def platform_name(self) -> str:
        if self.is_windows:
            return "windows"
        elif self.is_macos:
            return "mac"
        else:
            return "linux"

    def get_install_dir(self) -> Path:
        """Get platform-specific installation directory"""
        home = Path.home()

        if self.is_windows:
            return home / "AppData" / "Local" / "heavymeta-cli"
        elif self.is_macos:
            return home / "Library" / "Application Support" / "heavymeta-cli"
        else:
            return home / ".local" / "share" / "heavymeta-cli"


class DependencyChecker:
    """Checks and validates build dependencies"""

    @staticmethod
    def check_python_version() -> bool:
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"ERROR: Python 3.8+ required, found {version.major}.{version.minor}")
            return False
        print(f"SUCCESS: Python {version.major}.{version.minor}.{version.micro}")
        return True

    @staticmethod
    def check_pip() -> bool:
        """Check if pip is available"""
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                capture_output=True,
                check=True,
            )
            print("SUCCESS: pip available")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ERROR: pip not available")
            return False

    @staticmethod
    def check_pyinstaller() -> bool:
        """Check if PyInstaller is available"""
        try:
            subprocess.run(
                ["pyinstaller", "--version"], capture_output=True, check=True
            )
            print("SUCCESS: PyInstaller available")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ERROR: PyInstaller not available")
            return False

    @staticmethod
    def install_pyinstaller() -> bool:
        """Install PyInstaller if not available"""
        print("INFO: Installing PyInstaller...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pyinstaller"], check=True
            )
            print("SUCCESS: PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install PyInstaller: {e}")
            return False


class BuildManager:
    """Manages the build process"""

    def __init__(self, config: BuildConfig, platform_mgr: PlatformManager):
        self.config = config
        self.platform_mgr = platform_mgr
        self.cwd = Path.cwd()
        self.build_dir = self.cwd / "build"
        self.dist_dir = self.build_dir / "dist" / self.platform_mgr.platform_name
        self.release_dir = self.cwd / "release"

    def clean_directory(self, directory: Path, exclude_patterns: set = None) -> None:
        """Clean directory contents, excluding specified patterns"""
        if exclude_patterns is None:
            exclude_patterns = set()

        if not directory.exists():
            return

        for item in directory.iterdir():
            if item.name in exclude_patterns:
                continue

            try:
                if item.is_file():
                    item.unlink()
                else:
                    shutil.rmtree(item)
            except Exception as e:
                print(f"WARNING: Could not remove {item}: {e}")

    def create_directories(self) -> None:
        """Create necessary build directories"""
        print("INFO: Creating build directories...")

        # Clean and recreate build directory
        if self.build_dir.exists():
            self.clean_directory(self.build_dir)
        self.build_dir.mkdir(exist_ok=True)

        # Create dist subdirectory
        self.dist_dir.mkdir(parents=True, exist_ok=True)

        # Clean and recreate release directory
        if self.release_dir.exists():
            self.clean_directory(self.release_dir)
        self.release_dir.mkdir(exist_ok=True)

        print("SUCCESS: Build directories created")

    def copy_source_files(self) -> None:
        """Copy source files to build directory"""
        print("INFO: Copying source files...")

        for file_name in self.config.source_files:
            source_file = self.cwd / file_name
            if source_file.exists():
                shutil.copy2(source_file, self.build_dir)
                print(f"  SUCCESS: {file_name}")
            else:
                print(f"  WARNING: {file_name} not found")

        print("SUCCESS: Source files copied")

    def copy_resource_directories(self) -> None:
        """Copy resource directories to build directory"""
        print("INFO: Copying resource directories...")

        for dir_name in self.config.resource_dirs:
            source_dir = self.cwd / dir_name
            if source_dir.exists() and source_dir.is_dir():
                target_dir = self.build_dir / dir_name
                shutil.copytree(source_dir, target_dir)
                print(f"  SUCCESS: {dir_name}/")
            else:
                print(f"  WARNING: {dir_name}/ not found")

        print("SUCCESS: Resource directories copied")

    def install_dependencies(self) -> bool:
        """Install Python dependencies"""
        print("INFO: Installing Python dependencies...")

        requirements_file = self.build_dir / "requirements.txt"
        if not requirements_file.exists():
            print("ERROR: requirements.txt not found in build directory")
            return False

        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                check=True,
                capture_output=True,
            )
            print("SUCCESS: Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install dependencies: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr.decode()}")
            return False

    def clean_build_directory(self):
        """Clean the build directory before building."""
        import shutil
        
        # Clean PyInstaller build directories
        build_dirs = [
            self.build_dir / "build",
            self.build_dir / "dist",
            self.build_dir / "__pycache__"
        ]
        
        for dir_path in build_dirs:
            if dir_path.exists():
                logger.info(f"Removing directory: {dir_path}")
                shutil.rmtree(dir_path, ignore_errors=True)
    
    def build_executable(self) -> bool:
        """Build executable using PyInstaller"""
        logger.info("Building executable...")
        
        # Clean build directory before starting
        self.clean_build_directory()
        
        # Ensure build directory exists
        self.build_dir.mkdir(parents=True, exist_ok=True)
        
        # Platform-specific icon configuration
        if self.platform_mgr.is_windows:
            icon_param = "--icon=images/logo.ico"
        else:
            icon_param = "--icon=images/logo.png"

        # Prepare PyInstaller command
        # Start with base PyInstaller command
        cmd = [
            "pyinstaller",
            "--onefile",
            f"--name={self.config.project_name}",
            f"--distpath={self.dist_dir}",
            icon_param,
            "--clean",
            "--noconfirm",
            "--log-level", "INFO",  # Reduced from DEBUG to INFO for cleaner logs
        ]
        
        # Add excluded modules
        if hasattr(self, 'exclude_modules') and self.exclude_modules:
            for module in self.exclude_modules:
                cmd.extend(["--exclude", module])
        
        # Add hooks directory if it exists
        hooks_dir = self.cwd / "hooks"
        if hooks_dir.exists():
            cmd.extend(["--additional-hooks-dir", str(hooks_dir)])
            
        # Add hidden imports and collect submodules
        hidden_imports = [
            "cffi",
            "_cffi_backend",
            "nacl",
            "hvym_stellar",
            "ipaddress"
        ]
        
        for imp in hidden_imports:
            cmd.extend(["--hidden-import", imp])
            
        # Explicitly collect all ipaddress modules and data
        cmd.extend(["--collect-all", "ipaddress"])
        cmd.extend(["--collect-submodules", "ipaddress"])

        # Add source files
        for file_name in self.config.source_files:
            if file_name != "requirements.txt":  # Don't include requirements.txt in executable
                source_file = self.build_dir / file_name
                if source_file.exists():
                    cmd.append(str(source_file))

        # Add resource directories
        for dir_name in self.config.resource_dirs:
            source_dir = self.build_dir / dir_name
            if source_dir.exists():
                cmd.extend(
                    [
                        "--add-data",
                        f"{dir_name}{self.platform_mgr.add_data_separator}{dir_name}",
                    ]
                )

        print(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("SUCCESS: Executable built successfully")
            print(f"Build output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Build failed: {e}")
            if e.stdout:
                print(f"Build output: {e.stdout}")
            if e.stderr:
                print(f"Build errors: {e.stderr}")
            return False

    def move_to_release(self) -> bool:
        """Move built executable to release directory"""
        print("INFO: Moving executable to release directory...")

        source_exe = self.dist_dir / self.platform_mgr.executable_name
        target_exe = self.release_dir / self.platform_mgr.executable_name

        if not source_exe.exists():
            print(f"ERROR: Built executable not found: {source_exe}")
            return False

        try:
            shutil.move(str(source_exe), str(target_exe))
            print(f"SUCCESS: Executable moved to: {target_exe}")

            # Set executable permissions on Unix-like systems
            if not self.platform_mgr.is_windows:
                os.chmod(target_exe, 0o755)
                print("SUCCESS: Executable permissions set")

            return True
        except Exception as e:
            print(f"ERROR: Failed to move executable: {e}")
            return False

    def copy_to_install_dir(self, install_dir: Path) -> bool:
        """Copy executable to installation directory for testing"""
        print(f"INFO: Copying executable to install directory: {install_dir}")

        source_exe = self.release_dir / self.platform_mgr.executable_name
        if not source_exe.exists():
            print(f"ERROR: Release executable not found: {source_exe}")
            return False

        try:
            install_dir.mkdir(parents=True, exist_ok=True)
            target_exe = install_dir / self.platform_mgr.executable_name

            shutil.copy2(source_exe, target_exe)
            print(f"SUCCESS: Executable copied to: {target_exe}")

            # Set executable permissions on Unix-like systems
            if not self.platform_mgr.is_windows:
                os.chmod(target_exe, 0o755)
                print("SUCCESS: Install executable permissions set")

            return True
        except Exception as e:
            print(f"ERROR: Failed to copy to install directory: {e}")
            return False

    def build(self, test_install: bool = False) -> bool:
        """Execute the complete build process"""
        print(f"INFO: Starting build for {self.platform_mgr.platform_name}")
        print(f"INFO: Build directory: {self.build_dir}")
        print(f"INFO: Release directory: {self.release_dir}")
        print()

        start_time = time.time()

        try:
            # Step 1: Create directories
            self.create_directories()

            # Step 2: Copy source files
            self.copy_source_files()

            # Step 3: Copy resource directories
            self.copy_resource_directories()

            # Step 4: Install dependencies
            if not self.install_dependencies():
                return False

            # Step 5: Build executable
            if not self.build_executable():
                return False

            # Step 6: Move to release
            if not self.move_to_release():
                return False

            # Step 7: Optional test install
            if test_install:
                install_dir = self.platform_mgr.get_install_dir()
                if not self.copy_to_install_dir(install_dir):
                    print("WARNING: Test install failed, but build succeeded")

            build_time = time.time() - start_time
            print(
                f"\nSUCCESS: Build completed successfully in {build_time:.1f} seconds!"
            )
            print(
                f"INFO: Executable location: {self.release_dir / self.platform_mgr.executable_name}"
            )

            return True

        except Exception as e:
            print(f"\nERROR: Build failed with error: {e}")
            return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Cross-platform build script for hvym_press",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build_cross_platform.py                    # Build for current platform
  python build_cross_platform.py --test            # Build and install to test directory
  python build_cross_platform.py --verbose         # Verbose output
  python build_cross_platform.py --clean           # Clean build artifacts only
        """,
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Copy executable to local install directory after build",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--clean", action="store_true", help="Clean build artifacts only (no build)"
    )
    parser.add_argument(
        "--check-deps", action="store_true", help="Check dependencies only (no build)"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Exclude a specific module from the build (can be used multiple times)"
    )

    args = parser.parse_args()

    # Initialize components
    config = BuildConfig()
    platform_mgr = PlatformManager()
    build_mgr = BuildManager(config, platform_mgr)
    
    # Set build flags from command line
    if args.exclude:
        build_mgr.exclude_modules = args.exclude

    print("BUILD: hvym_press Cross-Platform Build Script")
    print("=" * 50)
    print(f"Platform: {platform_mgr.system.title()} ({platform_mgr.arch})")
    print(f"Python: {sys.version}")
    print(f"Working Directory: {build_mgr.cwd}")
    print()

    # Check dependencies
    print("INFO: Checking dependencies...")
    if not DependencyChecker.check_python_version():
        sys.exit(1)

    if not DependencyChecker.check_pip():
        print("ERROR: pip is required for building")
        sys.exit(1)

    if not DependencyChecker.check_pyinstaller():
        print("INFO: PyInstaller not found, attempting to install...")
        if not DependencyChecker.install_pyinstaller():
            print("ERROR: Failed to install PyInstaller")
            print("Please install manually: pip install pyinstaller")
            sys.exit(1)

    if args.check_deps:
        print("SUCCESS: All dependencies satisfied")
        return

    # Clean only mode
    if args.clean:
        print("INFO: Cleaning build artifacts...")
        build_mgr.clean_directory(build_mgr.build_dir)
        build_mgr.clean_directory(build_mgr.release_dir)
        print("SUCCESS: Cleanup completed")
        return

    # Execute build
    success = build_mgr.build(test_install=args.test)

    if not success:
        print("\nERROR: Build failed! Check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

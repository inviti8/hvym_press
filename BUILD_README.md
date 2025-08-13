# Cross-Platform Build System for HVYM Press

This document describes the new cross-platform build system that replaces the Linux-specific `build.py` with a robust, universal solution.

## 🚀 Overview

The new `build_cross_platform.py` script provides:
- **Universal platform support** (Windows, macOS, Linux)
- **Automatic dependency management** and validation
- **Comprehensive error handling** and user feedback
- **Flexible build options** and configuration
- **Automatic PyInstaller installation** if needed

## 📋 Requirements

### System Requirements
- **Python 3.8+** (3.8, 3.9, 3.10, 3.11, 3.12+)
- **pip** (Python package manager)
- **Internet connection** (for dependency installation)

### Dependencies
The script will automatically install:
- **PyInstaller** (if not present)
- All packages listed in `requirements.txt`

## 🛠️ Installation

### 1. Basic Usage
```bash
# Build for current platform
python build_cross_platform.py

# Build and install to test directory
python build_cross_platform.py --test

# Check dependencies only
python build_cross_platform.py --check-deps

# Clean build artifacts
python build_cross_platform.py --clean
```

### 2. Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--test` | Build and copy to local install directory | `--test` |
| `--verbose` / `-v` | Enable verbose output | `--verbose` |
| `--clean` | Clean build artifacts only | `--clean` |
| `--check-deps` | Check dependencies only | `--check-deps` |

## 🔧 Build Process

The build process follows these steps:

1. **🔍 Dependency Check**
   - Python version validation
   - pip availability check
   - PyInstaller installation (if needed)

2. **📁 Directory Setup**
   - Clean/create build directory
   - Create platform-specific dist subdirectory
   - Clean/create release directory

3. **📋 File Copying**
   - Copy source Python files
   - Copy resource directories (templates, images, serve)

4. **📦 Dependency Installation**
   - Install packages from requirements.txt
   - Handle installation errors gracefully

5. **🔨 Executable Building**
   - Run PyInstaller with optimized settings
   - Include all resources and dependencies
   - Generate single-file executable

6. **📦 Release Management**
   - Move executable to release directory
   - Set proper permissions (Unix systems)
   - Optional test installation

## 🌍 Platform Support

### Windows
- **Executable**: `hvym_press.exe`
- **Install Directory**: `%LOCALAPPDATA%\heavymeta-cli`
- **Path Separator**: `;`
- **Permissions**: Not applicable

### macOS
- **Executable**: `hvym_press`
- **Install Directory**: `~/Library/Application Support/heavymeta-cli`
- **Path Separator**: `:`
- **Permissions**: `755` (executable)

### Linux
- **Executable**: `hvym_press`
- **Install Directory**: `~/.local/share/heavymeta-cli`
- **Path Separator**: `:`
- **Permissions**: `755` (executable)

## 📁 Directory Structure

```
hvym_press/
├── build_cross_platform.py    # New cross-platform build script
├── build.py                   # Legacy Linux build script
├── build/                     # Build artifacts (auto-created)
│   ├── dist/
│   │   ├── windows/          # Windows build output
│   │   ├── mac/              # macOS build output
│   │   └── linux/            # Linux build output
│   ├── templates/             # Copied templates
│   ├── images/                # Copied images
│   └── serve/                 # Copied serve directory
├── release/                   # Final executables
│   ├── hvym_press.exe        # Windows executable
│   ├── hvym_press            # Unix executable
│   └── ...
└── requirements.txt           # Python dependencies
```

## 🔍 Troubleshooting

### Common Issues

#### 1. PyInstaller Not Found
```bash
# The script will automatically install PyInstaller
# If it fails, install manually:
pip install pyinstaller
```

#### 2. Permission Denied (Unix)
```bash
# Make the script executable:
chmod +x build_cross_platform.py

# Or run with Python:
python3 build_cross_platform.py
```

#### 3. Build Fails
```bash
# Check dependencies:
python build_cross_platform.py --check-deps

# Clean and retry:
python build_cross_platform.py --clean
python build_cross_platform.py
```

#### 4. Missing Files
```bash
# Ensure all source files exist:
ls -la *.py
ls -la templates/ images/ serve/
```

### Debug Mode

For detailed debugging, the script provides comprehensive logging:
- File copy operations
- Dependency installation status
- PyInstaller command execution
- Error details and stack traces

## 📊 Performance

### Build Times (Typical)
- **Clean build**: 2-5 minutes
- **Incremental build**: 1-2 minutes
- **Dependency installation**: 1-3 minutes

### Optimization Features
- **Parallel dependency installation** (where possible)
- **Smart file copying** (only changed files)
- **PyInstaller optimization** (--onefile, --clean)
- **Efficient resource bundling**

## 🔄 Migration from Legacy Build

### Before (Legacy build.py)
```bash
# Linux-specific
python build.py --test
```

### After (Cross-platform)
```bash
# Universal
python build_cross_platform.py --test

# Platform-specific
python build_cross_platform.py  # Auto-detects platform
```

### Benefits of Migration
- ✅ **Cross-platform compatibility**
- ✅ **Better error handling**
- ✅ **Automatic dependency management**
- ✅ **Cleaner build artifacts**
- ✅ **Professional logging and feedback**

## 🧪 Testing

### Test Installation
```bash
# Build and install to test directory
python build_cross_platform.py --test

# Verify installation
# Windows: Check %LOCALAPPDATA%\heavymeta-cli
# macOS: Check ~/Library/Application Support/heavymeta-cli
# Linux: Check ~/.local/share/heavymeta-cli
```

### Validation
- Executable runs without errors
- All resources are properly bundled
- Platform-specific paths work correctly
- Permissions are set appropriately

## 📝 Configuration

### Customizing Build

The `BuildConfig` class allows easy customization:

```python
class BuildConfig:
    def __init__(self):
        self.project_name = "hvym_press"           # Change project name
        self.source_files = [...]                  # Modify source files
        self.resource_dirs = [...]                 # Modify resource dirs
        self.excluded_dirs = {...}                 # Modify exclusions
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHONPATH` | Python module search path | Current directory |
| `PIP_INDEX_URL` | Custom PyPI index | Official PyPI |
| `PYINSTALLER_OPTS` | Additional PyInstaller options | None |

## 🤝 Contributing

### Adding New Platforms
1. Extend `PlatformManager` class
2. Add platform-specific logic
3. Update `get_install_dir()` method
4. Test on target platform

### Adding New Features
1. Extend appropriate class
2. Add command line options
3. Update documentation
4. Add tests

## 📚 References

- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Cross-Platform Development](https://docs.python.org/3/library/platform.html)

## 🆘 Support

### Getting Help
1. Check this README
2. Run with `--verbose` for detailed output
3. Check error messages and logs
4. Verify platform compatibility

### Reporting Issues
Include:
- Platform and Python version
- Full error message
- Command used
- Environment details

---

**Note**: This build system replaces the legacy `build.py` and provides a more robust, cross-platform solution for building HVYM Press applications.

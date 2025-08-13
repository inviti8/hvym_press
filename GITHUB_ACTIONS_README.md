# GitHub Actions Automated Release System

This document explains how to use the automated GitHub Actions workflow to build and release HVYM Press across multiple platforms.

## 🚀 Overview

The GitHub Actions workflow automatically:
- **Builds executables** for Windows, Linux, and Intel macOS
- **Creates GitHub releases** with all platform binaries
- **Generates installation scripts** for each platform
- **Triggers on version tags** (e.g., `v0.01`, `v1.00`)

## 📋 Prerequisites

### Repository Setup
- **GitHub repository** with your HVYM Press code
- **GitHub Actions enabled** (should be enabled by default)
- **Proper file structure** with all required files

### Required Files
```
hvym_press/
├── .github/workflows/build-release.yml  # This workflow file
├── build_cross_platform.py              # Cross-platform build script
├── requirements.txt                     # Python dependencies
├── app.py                              # Main application
├── templates/                          # Template files
├── images/                             # Image assets
└── serve/                              # Serve directory
```

## 🔧 Setup

### 1. Enable GitHub Actions
1. Go to your repository on GitHub
2. Click **Actions** tab
3. Ensure GitHub Actions is enabled
4. The workflow will appear automatically

### 2. Verify Workflow File
The workflow file `.github/workflows/build-release.yml` should be in your repository. If not, create the `.github/workflows/` directory and add the file.

### 3. Check Permissions
Ensure the workflow has permission to:
- **Read repository contents**
- **Create releases**
- **Upload artifacts**

## 🏷️ Creating Releases

### Method 1: Using the Helper Script (Recommended)

```bash
# Run the helper script
python create_release.py

# Follow the interactive prompts:
# 1. Choose suggested version or enter custom
# 2. Enter release message
# 3. Script automatically creates and pushes tag
```

### Method 2: Manual Git Commands

```bash
# Create and push a tag
git tag -a v0.01 -m "Release v0.01"
git push origin v0.01

# Or for a different version
git tag -a v1.00 -m "Major release v1.00"
git push origin v1.00
```

### Method 3: GitHub Web Interface

1. Go to **Releases** in your repository
2. Click **Create a new release**
3. Enter tag version (e.g., `v0.01`)
4. Write release notes
5. Click **Publish release**

## 📊 Workflow Process

### 1. Trigger
- **Event**: Push tag matching pattern `v*.*`
- **Examples**: `v0.00`, `v0.01`, `v1.00`, `v2.15`

### 2. Build Jobs (Parallel)
- **Windows**: Builds `hvym_press.exe`
- **Linux**: Builds `hvym_press` (Unix executable)
- **macOS**: Builds `hvym_press` (Intel only)

### 3. Release Creation
- **Downloads** all build artifacts
- **Creates** platform-specific installers
- **Generates** comprehensive release notes
- **Publishes** GitHub release

### 4. Artifacts
Each release includes:
- **Executables** for all supported platforms
- **Installation scripts** for each platform
- **README** with installation instructions
- **Release notes** with changelog

## 🌍 Supported Platforms

| Platform | Executable | Install Script | Notes |
|----------|------------|----------------|-------|
| **Windows** | `hvym_press-windows.exe` | `install-windows.bat` | x64 architecture |
| **Linux** | `hvym_press-linux` | `install-linux.sh` | x64 architecture |
| **macOS** | `hvym_press-macos` | `install-macos.sh` | Intel only (no Apple Silicon) |

## 📁 Release Structure

```
Release v0.01/
├── hvym_press-windows.exe      # Windows executable
├── hvym_press-linux            # Linux executable
├── hvym_press-macos            # macOS executable
├── install-windows.bat         # Windows installer
├── install-linux.sh            # Linux installer
├── install-macos.sh            # macOS installer
└── README.md                   # Installation guide
```

## 🚀 Quick Start

### 1. First Release
```bash
# Ensure all changes are committed
git add .
git commit -m "Initial release preparation"
git push origin main

# Create first release
python create_release.py
# Choose option 1 (suggested version: v0.01)
# Enter release message
# Wait for GitHub Actions to complete
```

### 2. Subsequent Releases
```bash
# Make your changes
git add .
git commit -m "New features and bug fixes"
git push origin main

# Create new release
python create_release.py
# Choose option 1 (suggested version: v0.02)
# Enter release message
```

### 3. Monitor Progress
1. Go to **Actions** tab in your repository
2. Click on the running workflow
3. Monitor build progress for each platform
4. Check for any build failures

## 🔍 Troubleshooting

### Common Issues

#### 1. Workflow Not Triggered
```bash
# Check tag format
git tag -l

# Ensure tag matches pattern v*.*
# Valid: v0.01, v1.00, v2.15
# Invalid: v0.1, v1, 0.01
```

#### 2. Build Failures
- **Check Actions tab** for detailed error logs
- **Verify dependencies** in requirements.txt
- **Ensure all source files** exist
- **Check Python version** compatibility

#### 3. Permission Issues
- **Verify repository permissions**
- **Check GitHub Actions settings**
- **Ensure workflow file** is in correct location

#### 4. Missing Artifacts
- **Check build logs** for each platform
- **Verify PyInstaller** installation
- **Ensure build script** runs successfully

### Debug Mode

For detailed debugging:
1. **Check workflow logs** in Actions tab
2. **Review build steps** for each platform
3. **Examine artifact uploads**
4. **Verify release creation** process

## 📊 Monitoring and Analytics

### GitHub Actions Dashboard
- **Workflow runs** and their status
- **Build times** for each platform
- **Success/failure rates**
- **Artifact sizes** and uploads

### Release Analytics
- **Download counts** per platform
- **Release frequency**
- **User engagement** metrics

## 🔄 Workflow Customization

### Modifying Build Process

Edit `.github/workflows/build-release.yml`:

```yaml
# Change Python version
env:
  PYTHON_VERSION: '3.12'  # Update to newer version

# Add new platforms
build-arm64:
  runs-on: ubuntu-latest
  # Add ARM64 Linux build
```

### Adding New Platforms

1. **Create new job** in workflow
2. **Set appropriate runner** (e.g., `ubuntu-latest`)
3. **Update artifact handling**
4. **Modify release creation**

### Custom Build Options

```yaml
# Add PyInstaller options
- name: Build executable
  run: |
    python build_cross_platform.py --verbose
    # Add custom flags as needed
```

## 📚 Best Practices

### 1. Version Management
- **Use semantic versioning** (vX.YY)
- **Increment consistently** (v0.01 → v0.02 → v0.03)
- **Document changes** in release notes

### 2. Release Process
- **Test locally** before releasing
- **Commit all changes** before tagging
- **Write descriptive** release messages
- **Monitor build progress**

### 3. Quality Assurance
- **Verify executables** work on target platforms
- **Test installation scripts**
- **Check all resources** are bundled
- **Validate cross-platform** compatibility

## 🆘 Support

### Getting Help
1. **Check workflow logs** in Actions tab
2. **Review this documentation**
3. **Examine build scripts** for errors
4. **Verify repository setup**

### Common Commands

```bash
# Check current tags
git tag -l

# Remove local tag (if needed)
git tag -d v0.01

# Remove remote tag (if needed)
git push origin --delete v0.01

# Check workflow status
# Go to Actions tab in GitHub repository
```

### Reporting Issues
Include:
- **Workflow run ID** from Actions tab
- **Platform** where build failed
- **Error messages** from logs
- **Repository setup** details

---

## 🎯 Summary

The GitHub Actions workflow provides:
- ✅ **Automated cross-platform builds**
- ✅ **Professional release management**
- ✅ **Easy version control** with tags
- ✅ **Comprehensive artifact packaging**
- ✅ **User-friendly installation** scripts

**To create a release:**
1. **Commit your changes**
2. **Run `python create_release.py`**
3. **Choose version and message**
4. **Wait for GitHub Actions to complete**
5. **Download from Releases page**

This system eliminates manual build processes and ensures consistent, professional releases across all supported platforms.

# HVYM Press - Cross-Platform Static Site Generator

A modern static site generator with IPFS deployment capabilities using Pintheon.

## 🚀 Cross-Platform Compatibility

This application is now fully compatible with:
- **Windows** (Windows 10/11)
- **macOS** (10.14+)
- **Linux** (Ubuntu 18.04+, CentOS 7+, etc.)

## 📋 Prerequisites

### All Platforms
- **Python 3.8+** - [Download from python.org](https://python.org)
- **Git** - For cloning the repository

### Windows
- **Visual Studio Build Tools** (for some Python packages)
- **Git Bash** or **WSL** (recommended for better Unix-like experience)

### macOS
- **Xcode Command Line Tools** (for some Python packages)
- Run: `xcode-select --install`

### Linux
- **Build essentials** (Ubuntu/Debian: `sudo apt install build-essential`)
- **Python dev packages** (Ubuntu/Debian: `sudo apt install python3-dev`)

## 🛠️ Installation

### Option 1: Automated Installation (Recommended)

#### Windows
```batch
# Run as Administrator
install.bat
```

#### macOS/Linux
```bash
# Make executable and run
chmod +x install.py
python3 install.py
```

### Option 2: Manual Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hvym_press.git
cd hvym_press
```

#### 2. Install Dependencies
```bash
# Windows
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt
```

#### 3. Build the Application
```bash
# Windows
python build.py

# macOS/Linux
python3 build.py
```

#### 4. Install to System
```bash
# Windows
python install.py

# macOS/Linux
python3 install.py
```

## 🏠 Home Page Configuration

HVYM Press supports a special `home.md` file that serves as your site's landing page. This file uses YAML frontmatter for configuration and supports advanced navigation features.

### Basic Home Page Example

```yaml
---
title: Welcome to My Site
hero_title: Build Amazing Static Sites
hero_subtitle: With HVYM Press and Markdown
hero_image: ./_resources/hero.jpg
layout: hero
navigation:
  - text: Get Started
    page: Getting Started
    style: primary
  - text: View Features
    page: Features
    style: secondary
cta_button:
  text: Quick Start
  page: Getting Started
seo:
  description: A modern static site generator with IPFS deployment
  keywords: static site, markdown, IPFS, documentation
---

# Welcome to My Site

[Get Started](Getting Started) | [View Features](Features)
```

### Section-Based Navigation

HVYM Press organizes content into sections (folders), and the navigation system is designed to work with these sections. Here's how it works:

1. **Sections** are folders containing markdown files
2. Each section's first markdown file serves as the landing page for that section
3. Navigation links should reference the section name (folder name)

#### Example Project Structure

```
project/
├── section_a/
│   ├── getting_started.md
│   └── advanced_features.md
├── section_b/
│   ├── examples.md
│   └── tutorials.md
└── home.md
```

#### Navigation in home.md

In your `home.md`, reference sections by their folder name in the navigation:

```yaml
navigation:
  - text: Get Started
    page: section_a        # Points to section_a/getting_started.md
    style: primary
  - text: View Examples
    page: section_b        # Points to section_b/examples.md
    style: secondary
```

#### Internal Links in Markdown

For internal links within your content, you can use either:

1. **Section-based links** (recommended):
   ```markdown
   [Getting Started](section_a)
   ```

2. **Direct file links** (if needed):
   ```markdown
   [Advanced Features](section_a/advanced_features)
   ```

### Navigation Button Styles

Available button styles:
- `primary` - Solid, prominent button
- `secondary` - Secondary action button
- `outline` - Outlined button
- `quiet` - Subtle text button

### Required Frontmatter Fields

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Page title | `title: My Site` |
| `layout` | Page layout | `layout: hero` |
| `navigation` | Array of navigation buttons. Each button should have `text`, `page` (section name), and `style`. | See example above |

### SEO Optimization

Use the `seo` section to add metadata:

```yaml
seo:
  description: A brief description of your site
  keywords: keyword1, keyword2, keyword3
```

## 🏗️ Building from Source

### Build Scripts

The `build.py` script automatically detects your platform and builds accordingly:

```bash
# Build for current platform
python build.py

# Force macOS build
python build.py --mac

# Test build (copy to local install directory)
python build.py --test
```

### Platform-Specific Builds

- **Windows**: Creates `hvym_press.exe` in `build/dist/windows/`
- **macOS**: Creates `hvym_press` in `build/dist/mac/`
- **Linux**: Creates `hvym_press` in `build/dist/linux/`

## 🚀 Running the Application

### After Installation

#### Windows
```batch
# Navigate to installation directory
cd %LOCALAPPDATA%\heavymeta-cli
hvym_press.exe

# Or add to PATH and run from anywhere
hvym_press
```

#### macOS/Linux
```bash
# If symlink was created successfully
hvym_press

# Or run directly from installation directory
~/.local/share/heavymeta-cli/hvym_press
```

### Development Mode
```bash
# Run directly from source
python app.py

# Or
python3 app.py
```

## 🔧 Configuration

### Pintheon Settings

The application is configured to use Pintheon for IPFS deployment:

- **API URL**: `https://localhost:9999/api_upload`
- **Access Token**: Set in the GUI under Deployment Settings
- **Gateway**: `localhost:9999`

### Platform-Specific Paths

The application automatically detects your platform and uses appropriate paths:

- **Windows**: `%LOCALAPPDATA%\heavymeta-cli\`
- **macOS**: `~/Library/Application Support/heavymeta-cli/`
- **Linux**: `~/.local/share/heavymeta-cli/`

## 🐛 Troubleshooting

### Common Issues

#### Windows
- **"python not found"**: Add Python to PATH or use `py` instead of `python`
- **Build errors**: Install Visual Studio Build Tools
- **Permission denied**: Run as Administrator

#### macOS
- **"xcode-select not found"**: Install Xcode Command Line Tools
- **Permission errors**: Check file permissions with `ls -la`

#### Linux
- **"gcc not found"**: Install build essentials
- **"python3-dev not found"**: Install Python development packages

### Build Issues

```bash
# Clean build directory
rm -rf build/ dist/ release/

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Rebuild
python build.py
```

### Installation Issues

```bash
# Check installation directory permissions
ls -la ~/.local/share/heavymeta-cli/

# Reinstall with verbose output
python install.py --verbose
```

## 📁 Project Structure

```
hvym_press/
├── app.py                 # Main application GUI
├── build.py              # Cross-platform build script
├── install.py            # Cross-platform installer
├── install.bat           # Windows installer
├── install.sh            # Unix installer (legacy)
├── requirements.txt      # Python dependencies
├── W3DeployHandler.py   # IPFS deployment logic
├── SiteDataHandler.py   # Site data management
├── templates/            # Site templates
├── images/              # Application images
└── serve/               # Local server files
```

## 🔄 Updates

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt

# Rebuild and reinstall
python build.py
python install.py
```

## 📝 Development

### Adding Platform-Specific Code

```python
import platform

if platform.system() == "Windows":
    # Windows-specific code
    pass
elif platform.system() == "Darwin":
    # macOS-specific code
    pass
else:
    # Linux-specific code
    pass
```

### Testing Cross-Platform Compatibility

```bash
# Test on different platforms
python -m pytest tests/ --platform=windows
python -m pytest tests/ --platform=darwin
python -m pytest tests/ --platform=linux
```

## 🤝 Contributing

When contributing, please ensure:

1. **Cross-platform compatibility** - Test on Windows, macOS, and Linux
2. **Path handling** - Use `pathlib.Path` instead of string concatenation
3. **Shell commands** - Avoid `shell=True`, use platform-specific command arrays
4. **File permissions** - Handle Unix vs Windows permission differences
5. **Line endings** - Use LF for Unix, CRLF for Windows

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with platform information
4. Include error messages and system details

---

**Note**: This application has been refactored to use Pintheon instead of Pinata for IPFS deployment, and all platform-specific issues have been resolved for full cross-platform compatibility.

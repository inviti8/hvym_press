# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for hvym_press
Platform-agnostic configuration with icon support
"""

import os
import platform

# Platform-specific icon configuration
if platform.system() == "Windows":
    icon_file = "images/logo.ico"
else:
    icon_file = "images/logo.png"

# Source files (relative paths)
source_files = [
    'app.py',
    'ColorPicker.py', 
    'HVYM.py',
    'IconPicker.py',
    'LoadingWindow.py',
    'MarkdownHandler.py',
    'ServerHandler.py',
    'SiteDataHandler.py',
    'TreeData.py',
    'W3DeployHandler.py'
]

a = Analysis(
    source_files,
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('images', 'images'), ('serve', 'serve')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='hvym_press',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,  # Platform-specific icon
)

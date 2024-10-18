# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/media/desktop/_dsk/dev/hvym_press/app.py', '/media/desktop/_dsk/dev/hvym_press/ColorPicker.py', '/media/desktop/_dsk/dev/hvym_press/HVYM.py', '/media/desktop/_dsk/dev/hvym_press/IconPicker.py', '/media/desktop/_dsk/dev/hvym_press/LoadingWindow.py', '/media/desktop/_dsk/dev/hvym_press/MarkdownHandler.py', '/media/desktop/_dsk/dev/hvym_press/ServerHandler.py', '/media/desktop/_dsk/dev/hvym_press/SiteDataHandler.py', '/media/desktop/_dsk/dev/hvym_press/TreeData.py', '/media/desktop/_dsk/dev/hvym_press/W3DeployHandler.py'],
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
)

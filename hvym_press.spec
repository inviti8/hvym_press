# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/media/desktop/_dsk/dev/weeeb_3/app.py', '/media/desktop/_dsk/dev/weeeb_3/ColorPicker.py', '/media/desktop/_dsk/dev/weeeb_3/HVYM.py', '/media/desktop/_dsk/dev/weeeb_3/IconPicker.py', '/media/desktop/_dsk/dev/weeeb_3/LoadingWindow.py', '/media/desktop/_dsk/dev/weeeb_3/MarkdownHandler.py', '/media/desktop/_dsk/dev/weeeb_3/ServerHandler.py', '/media/desktop/_dsk/dev/weeeb_3/SiteDataHandler.py', '/media/desktop/_dsk/dev/weeeb_3/TreeData.py', '/media/desktop/_dsk/dev/weeeb_3/W3DeployHandler.py'],
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

# RenewedWorldConverter_debug.spec
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['../renewed_world_converter\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('../LegacyWorldConverter-all.jar', '.'), ('../Conversions.json', '.')],
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
    name='RenewedWorldConverter_debug',
    debug=True,  # Enable debug mode
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX compression for easier debugging
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

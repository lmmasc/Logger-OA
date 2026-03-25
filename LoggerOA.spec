# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('assets', 'assets'), ('src/config', 'src/config'), ('src/domain', 'src/domain'), ('src/infrastructure', 'src/infrastructure'), ('src/interface_adapters', 'src/interface_adapters'), ('src/interface_adapters/ui/themes', 'src/interface_adapters/ui/themes'), ('src/interface_adapters/ui/views', 'src/interface_adapters/ui/views'), ('src/application', 'src/application'), ('src/utils', 'src/utils'), ('src/translation', 'src/translation'), ('src/main.py', 'src/main.py')],
    hiddenimports=['PySide6', 'shiboken6', 'translation.es.all_keys', 'translation.en.all_keys'],
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
    name='LoggerOA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\app_icon.ico'],
)

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('assets', 'assets'), ('src/config', 'src/config'), ('src/domain', 'src/domain'), ('src/infrastructure', 'src/infrastructure'), ('src/interface_adapters', 'src/interface_adapters'), ('src/interface_adapters/ui/themes', 'src/interface_adapters/ui/themes'), ('src/interface_adapters/ui/views', 'src/interface_adapters/ui/views'), ('src/application', 'src/application'), ('src/utils', 'src/utils'), ('src/translation', 'src/translation'), ('src/main.py', 'src/main.py')],
    hiddenimports=['PySide2', 'PySide2.QtCore', 'PySide2.QtGui', 'PySide2.QtWidgets', 'shiboken2', 'qt_compat_bootstrap', 'sitecustomize', 'translation.es.all_keys', 'translation.en.all_keys'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['multiprocessing', '_multiprocessing', 'concurrent.futures.process', 'pkg_resources', 'setuptools'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    exclude_binaries=False,
    name='LoggerOA-win7',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
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

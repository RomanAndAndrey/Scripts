# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file для Anti-AltTab.

Использование:
    pyinstaller Anti-AltTab.spec
"""

import sys
from pathlib import Path

# Пути
project_root = Path(__file__).parent.parent
anti_alttab_dir = Path(__file__).parent

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[str(anti_alttab_dir)],
    binaries=[],
    datas=[
        ('profiles', 'profiles'),  # Включаем папку profiles
    ],
    hiddenimports=[
        'keyboard',
        'psutil',
        'win32api',
        'win32con',
        'win32gui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Anti-AltTab',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console для вывода логов
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

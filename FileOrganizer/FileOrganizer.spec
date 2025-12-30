# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file для FileOrganizer.

Использование:
    pyinstaller FileOrganizer.spec
"""

import sys
from pathlib import Path

# Пути
project_root = Path(__file__).parent.parent
file_organizer_dir = Path(__file__).parent
common_dir = project_root / 'common'

block_cipher = None

a = Analysis(
    ['organizer.py'],
    pathex=[str(file_organizer_dir), str(project_root)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'watchdog',
        'watchdog.observers',
        'watchdog.events',
        'common.logger',
        'common.config',
        'common.file_utils',
        'common.path_utils',
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
    name='FileOrganizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

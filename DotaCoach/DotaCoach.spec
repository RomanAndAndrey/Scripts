# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file для DotaCoach.

Использование:
    pyinstaller DotaCoach.spec
"""

import sys
from pathlib import Path

# Пути
project_root = Path(__file__).parent.parent
dota_coach_dir = Path(__file__).parent

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[str(dota_coach_dir)],
    binaries=[],
    datas=[
        ('tips.json', '.'),  # Включаем tips.json
        ('coach_config.json', '.'),  # Включаем конфиг
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'pyautogui',
        'numpy',
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
    name='DotaCoach',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console - GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

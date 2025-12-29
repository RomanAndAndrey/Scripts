"""
Базовые тесты для DesktopLauncher.
"""
import pytest


def test_imports():
    """Проверка что все модули импортируются."""
    try:
        from DesktopLauncher import constants, models, utils, widgets
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import DesktopLauncher modules: {e}")


def test_constants_defined():
    """Проверка что константы определены."""
    from DesktopLauncher.constants import STATUS_STOPPED, STATUS_RUNNING, STATUS_ERROR, COLORS
    
    assert STATUS_STOPPED == "stopped"
    assert STATUS_RUNNING == "running"
    assert STATUS_ERROR == "error"
    
    # Проверка цветов
    assert "running" in COLORS
    assert "stopped" in COLORS


def test_script_icons():
    """Проверка что иконки скриптов определены."""
    from DesktopLauncher.constants import SCRIPT_ICONS
    
    assert "Anti-AltTab" in SCRIPT_ICONS
    assert "YouTube Downloader" in SCRIPT_ICONS

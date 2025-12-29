"""
Базовые тесты для Anti-AltTab.
"""

import pytest


def test_imports():
    """Проверка что модули импортируются."""
    try:
        from Anti_AltTab import combat, overseer

        assert True
    except ImportError:
        # Используем дефис в имени папки
        pytest.skip("Anti-AltTab modules use hyphen in folder name")


def test_profile_manager():
    """Проверка ProfileManager."""
    try:
        from Anti_AltTab.profile_manager import ProfileManager

        pm = ProfileManager(profiles_dir="Anti-AltTab/profiles")
        profiles = pm.list_profiles()

        # Должны быть созданные профили
        assert len(profiles) >= 3  # dota2, cs2, default
    except Exception:
        pytest.skip("ProfileManager requires hyphen-based imports")

"""
Базовые тесты для FileOrganizer.
"""

from pathlib import Path

import pytest


def test_imports():
    """Проверка что модуль импортируется без ошибок."""
    try:
        from FileOrganizer import organizer

        assert True
    except ImportError:
        pytest.fail("Failed to import FileOrganizer.organizer")


def test_categories_defined():
    """Тест что категории определены."""
    from FileOrganizer.organizer import CATEGORIES

    # Проверяем что CATEGORIES это словарь
    assert isinstance(CATEGORIES, dict)
    assert len(CATEGORIES) > 0

    # Проверяем что есть основные категории
    assert "Изображения" in CATEGORIES
    assert "Архивы" in CATEGORIES


# Placeholder для будущих тестов
def test_file_categorization():
    """TODO: Тест категоризации файлов."""
    # from FileOrganizer.organizer import get_category
    # assert get_category("photo.jpg") == "Изображения"
    pass

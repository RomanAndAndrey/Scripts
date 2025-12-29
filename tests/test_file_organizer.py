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
    """Проверка что категории файлов определены."""
    from FileOrganizer.organizer import CATEGORIES

    assert "Изображения" in CATEGORIES
    assert "Документы" in CATEGORIES
    assert "Архивы" in CATEGORIES

    # Проверка что есть расширения
    assert len(CATEGORIES["Изображения"]) > 0
    assert ".jpg" in CATEGORIES["Изображения"]


# Placeholder для будущих тестов
def test_file_categorization():
    """TODO: Тест категоризации файлов."""
    # from FileOrganizer.organizer import get_category
    # assert get_category("photo.jpg") == "Изображения"
    pass

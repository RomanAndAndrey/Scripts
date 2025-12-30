"""
Тесты для common.path_utils
"""

from pathlib import Path

import pytest

from common.path_utils import (
    get_config_path,
    get_data_folder,
    get_downloads_folder,
    get_log_path,
    get_project_root,
)


def test_get_project_root():
    """Тест получения корневой директории."""
    root = get_project_root()
    assert root.name == "Rutina" or root.name == "Рутина"
    assert root.exists()


def test_get_downloads_folder():
    """Тест получения папки Downloads."""
    downloads = get_downloads_folder()
    assert downloads.name == "Downloads"
    assert downloads.exists()


def test_get_data_folder(tmp_path, monkeypatch):
    """Тест создания папки данных."""
    # Временно меняем home directory
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    data = get_data_folder("TestProject")

    assert data == tmp_path / ".rutina" / "TestProject"
    assert data.exists()


def test_get_data_folder_no_create(tmp_path, monkeypatch):
    """Тест БЕЗ создания папки данных."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    data = get_data_folder("TestProject2", create=False)

    assert data == tmp_path / ".rutina" / "TestProject2"
    assert not data.exists()


def test_get_config_path():
    """Тест получения пути к конфигу."""
    config = get_config_path("FileOrganizer")

    assert "FileOrganizer" in str(config)
    assert config.name == "config.json"


def test_get_log_path():
    """Тест получения пути к логу."""
    log = get_log_path("FileOrganizer")

    assert "FileOrganizer" in str(log)
    assert log.name == "FileOrganizer.log"


def test_get_log_path_custom():
    """Тест получения пути к кастомному логу."""
    log = get_log_path("FileOrganizer", "custom.log")

    assert log.name == "custom.log"

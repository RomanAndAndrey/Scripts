"""
Тесты для модуля auto_update.
"""

from pathlib import Path

import pytest

from common.auto_update import AutoUpdater, Version


class TestVersion:
    """Тесты для класса Version."""

    def test_version_parsing(self):
        """Тест парсинга версий."""
        v1 = Version("1.2.3")
        assert v1.major == 1
        assert v1.minor == 2
        assert v1.patch == 3

    def test_version_with_v_prefix(self):
        """Тест парсинга версий с префиксом v."""
        v1 = Version("v2.5.10")
        assert v1.major == 2
        assert v1.minor == 5
        assert v1.patch == 10

    def test_version_comparison(self):
        """Тест сравнения версий."""
        v1 = Version("1.0.0")
        v2 = Version("1.0.1")
        v3 = Version("1.1.0")
        v4 = Version("2.0.0")

        assert v1 < v2
        assert v2 < v3
        assert v3 < v4
        assert v4 > v1

    def test_version_equality(self):
        """Тест равенства версий."""
        v1 = Version("1.2.3")
        v2 = Version("v1.2.3")

        assert v1 == v2

    def test_version_string(self):
        """Тест строкового представления."""
        v1 = Version("v1.2.3")
        assert str(v1) == "1.2.3"


class TestAutoUpdater:
    """Тесты для класса AutoUpdater."""

    def test_initialization(self):
        """Тест инициализации updater."""
        updater = AutoUpdater(
            repo_owner="RomanAndAndrey",
            repo_name="Scripts",
            current_version="1.0.0",
            app_name="TestApp",
        )

        assert updater.repo_owner == "RomanAndAndrey"
        assert updater.repo_name == "Scripts"
        assert updater.current_version == Version("1.0.0")
        assert updater.app_name == "TestApp"

    def test_latest_release_url(self):
        """Тест формирования URL."""
        updater = AutoUpdater(
            repo_owner="TestOwner",
            repo_name="TestRepo",
            current_version="1.0.0",
            app_name="TestApp",
        )

        expected_url = "https://api.github.com/repos/TestOwner/TestRepo/releases/latest"
        assert updater.latest_release_url == expected_url

    # Note: Тесты check_for_updates, download_update, apply_update
    # требуют mock'ирования сетевых запросов и файловой системы
    # Это можно сделать с помощью pytest-mock или responses library

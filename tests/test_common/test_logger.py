"""
Тесты для common.logger
"""

import logging
from pathlib import Path

import pytest

from common.logger import get_logger, setup_logger


def test_setup_logger_basic():
    """Тест базовой настройки логгера."""
    logger = setup_logger("test_logger")
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO


def test_setup_logger_with_file(tmp_path):
    """Тест логгера с файлом."""
    log_file = tmp_path / "test.log"
    logger = setup_logger("test_file_logger", log_file=log_file)

    logger.info("Test message")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "Test message" in content


def test_setup_logger_no_console(tmp_path):
    """Тест логгера без консольного вывода."""
    log_file = tmp_path / "test.log"
    logger = setup_logger("test_no_console", log_file=log_file, console_output=False)

    assert len(logger.handlers) == 1  # Только файловый handler


def test_get_logger():
    """Тест получения существующего логгера."""
    setup_logger("existing_logger")
    logger = get_logger("existing_logger")
    assert logger.name == "existing_logger"

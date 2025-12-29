"""
Универсальный модуль логирования для всех проектов Рутина.

Предоставляет настраиваемый логгер с:
- Ротацией файлов
- Форматированием сообщений
- Консольным и файловым выводом
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    max_bytes: int = 10_485_760,  # 10MB
    backup_count: int = 5,
    console_output: bool = True,
) -> logging.Logger:
    """
    Настраивает и возвращает логгер с ротацией файлов.

    Args:
        name: Имя логгера (обычно __name__ модуля)
        log_file: Путь к файлу лога (если None - только консоль)
        level: Уровень логирования (logging.DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Кастомный формат сообщений
        max_bytes: Максимальный размер файла лога перед ротацией
        backup_count: Количество бэкап файлов
        console_output: Выводить ли логи в консоль

    Returns:
        Настроенный логгер

    Example:
        >>> from pathlib import Path
        >>> from common.logger import setup_logger
        >>> logger = setup_logger("MyApp", log_file=Path("app.log"))
        >>> logger.info("Application started")
    """
    # Получаем или создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Удаляем существующие handlers чтобы избежать дублирования
    logger.handlers.clear()

    # Формат по умолчанию
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(format_string)

    # Файловый handler с ротацией
    if log_file is not None:
        # Создаем директорию если не существует
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Консольный handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Получает существующий логгер по имени.

    Args:
        name: Имя логгера

    Returns:
        Логгер

    Example:
        >>> logger = get_logger("MyApp")
        >>> logger.info("Using existing logger")
    """
    return logging.getLogger(name)

"""
Вспомогательные функции для Desktop Script Launcher.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("launcher.log", encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def load_scripts_config(config_path: str = "scripts_config.json") -> Dict[str, Any]:
    """
    Загружает конфигурацию скриптов из JSON файла.

    Args:
        config_path: Путь к файлу конфигурации

    Returns:
        Словарь с конфигурацией скриптов
    """
    try:
        script_dir = Path(__file__).parent
        full_path = script_dir / config_path

        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Loaded {len(data.get('scripts', {}))} scripts from config")
            return data.get("scripts", {})
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {config_path}: {e}")
        return {}


def smart_resolve_path(base: str, rel_path: str) -> str:
    """
    Умный поиск пути с fallback вариантами.

    Args:
        base: Базовая директория
        rel_path: Относительный путь

    Returns:
        Абсолютный путь к файлу
    """
    # 1. Пробуем "как есть" (по конфигу)
    path1 = os.path.abspath(os.path.join(base, rel_path))
    if os.path.exists(path1):
        return path1

    # 2. Если путь начинается с ../, пробуем убрать это
    if rel_path.startswith("../") or rel_path.startswith("..\\"):
        path2 = os.path.abspath(os.path.join(base, rel_path[3:]))
        if os.path.exists(path2):
            return path2

    # 3. Возвращаем вариант 1 (чтобы ошибка была стандартной)
    return path1


def get_base_dir() -> str:
    """
    Получает базовую директорию приложения.

    Returns:
        Путь к базовой директории
    """
    if getattr(sys, "frozen", False):
        # Если приложение скомпилировано
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def get_python_exe() -> str:
    """
    Получает путь к интерпретатору Python.

    Returns:
        Путь к python.exe или просто "python"
    """
    if getattr(sys, "frozen", False):
        return "python"  # Предполагаем что в PATH
    else:
        return sys.executable


def resource_path(relative_path: str) -> str:
    """
    Получает абсолютный путь к ресурсу (для PyInstaller).

    Args:
        relative_path: Относительный путь

    Returns:
        Абсолютный путь к ресурсу
    """
    try:
        # PyInstaller создает temp папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

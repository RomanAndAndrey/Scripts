"""
Модуль для работы с конфигурационными файлами.

Поддерживает:
- JSON конфигурации
- Значения по умолчанию
- Валидацию структуры
- Создание конфигурации если отсутствует
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Type, TypeVar

from common.exceptions import ConfigError

T = TypeVar("T")


def load_json_config(
    config_path: Path,
    defaults: Optional[Dict[str, Any]] = None,
    create_if_missing: bool = False,
) -> Dict[str, Any]:
    """
    Загружает JSON конфигурацию.

    Args:
        config_path: Путь к JSON файлу конфигурации
        defaults: Значения по умолчанию
        create_if_missing: Создать файл с defaults если не существует

    Returns:
        Словарь конфигурации

    Raises:
        ConfigError: Если конфигурация не найдена или невалидна

    Example:
        >>> from pathlib import Path
        >>> from common.config import load_json_config
        >>> config = load_json_config(
        ...     Path("config.json"),
        ...     defaults={"debug": False}
        ... )
    """
    if not config_path.exists():
        if create_if_missing and defaults is not None:
            save_json_config(config_path, defaults)
            return defaults.copy()
        raise ConfigError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {config_path}: {e}")
    except Exception as e:
        raise ConfigError(f"Error reading config {config_path}: {e}")

    # Объединяем с defaults если предоставлены
    if defaults is not None:
        # Defaults + config (config имеет приоритет)
        merged = {**defaults, **config}
        return merged

    return config


def save_json_config(config_path: Path, config: Dict[str, Any]) -> None:
    """
    Сохраняет конфигурацию в JSON файл.

    Args:
        config_path: Путь для сохранения
        config: Словарь конфигурации

    Raises:
        ConfigError: Если не удается сохранить

    Example:
        >>> from pathlib import Path
        >>> from common.config import save_json_config
        >>> save_json_config(Path("config.json"), {"debug": True})
    """
    try:
        # Создаем директорию если не существует
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise ConfigError(f"Error saving config to {config_path}: {e}")


def merge_configs(
    base: Dict[str, Any], override: Dict[str, Any], deep: bool = True
) -> Dict[str, Any]:
    """
    Объединяет две конфигурации.

    Args:
        base: Базовая конфигурация
        override: Конфигурация для переопределения
        deep: Глубокое слияние (вложенные словари)

    Returns:
        Объединенная конфигурация

    Example:
        >>> base = {"a": 1, "b": {"c": 2}}
        >>> override = {"b": {"d": 3}}
        >>> merge_configs(base, override)
        {'a': 1, 'b': {'c': 2, 'd': 3}}
    """
    result = base.copy()

    for key, value in override.items():
        if deep and key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value, deep=True)
        else:
            result[key] = value

    return result

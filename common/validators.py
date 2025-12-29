"""
Валидаторы для проверки данных и конфигураций.

Предоставляет функции для:
- Валидации структуры данных
- Проверки путей
- Проверки обязательных полей
"""

from pathlib import Path
from typing import Any, Dict, List, Optional


def validate_config_structure(
    config: Dict[str, Any],
    required_keys: List[str],
    optional_keys: Optional[List[str]] = None,
) -> List[str]:
    """
    Валидирует структуру конфигурации.

    Args:
        config: Словарь конфигурации
        required_keys: Список обязательных ключей
        optional_keys: Список опциональных ключей

    Returns:
        Список ошибок (пустой список если OK)

    Example:
        >>> from common.validators import validate_config_structure
        >>> config = {"name": "app", "version": "1.0"}
        >>> errors = validate_config_structure(
        ...     config,
        ...     required_keys=["name", "version"],
        ...     optional_keys=["debug"]
        ... )
        >>> if not errors:
        ...     print("Config valid!")
    """
    errors = []

    # Проверяем обязательные ключи
    for key in required_keys:
        if key not in config:
            errors.append(f"Missing required key: '{key}'")

    # Проверяем неизвестные ключи
    all_allowed_keys = set(required_keys)
    if optional_keys:
        all_allowed_keys.update(optional_keys)

    for key in config.keys():
        if key not in all_allowed_keys:
            errors.append(f"Unknown key: '{key}'")

    return errors


def validate_path_exists(path: Path, must_be_file: bool = False, must_be_dir: bool = False) -> bool:
    """
    Проверяет существование пути.

    Args:
        path: Путь для проверки
        must_be_file: Путь должен быть файлом
        must_be_dir: Путь должен быть директорией

    Returns:
        True если путь валиден

    Example:
        >>> from pathlib import Path
        >>> from common.validators import validate_path_exists
        >>> if validate_path_exists(Path("data.txt"), must_be_file=True):
        ...     print("File exists!")
    """
    if not path.exists():
        return False

    if must_be_file and not path.is_file():
        return False

    if must_be_dir and not path.is_dir():
        return False

    return True


def validate_required_fields(data: Dict[str, Any], fields: List[str]) -> List[str]:
    """
    Проверяет наличие обязательных полей и что они не пустые.

    Args:
        data: Данные для проверки
        fields: Список обязательных полей

    Returns:
        Список ошибок

    Example:
        >>> from common.validators import validate_required_fields
        >>> data = {"name": "John", "age": 30, "email": ""}
        >>> errors = validate_required_fields(data, ["name", "age", "email"])
        >>> if errors:
        ...     print(errors)  # ['Field email is empty']
    """
    errors = []

    for field in fields:
        if field not in data:
            errors.append(f"Missing field: '{field}'")
        elif not data[field]:  # Проверка на пустое значение
            errors.append(f"Field '{field}' is empty")

    return errors


def validate_file_extension(file_path: Path, allowed_extensions: List[str]) -> bool:
    """
    Проверяет расширение файла.

    Args:
        file_path: Путь к файлу
        allowed_extensions: Список разрешенных расширений (с точкой, например ['.txt', '.json'])

    Returns:
        True если расширение разрешено

    Example:
        >>> from pathlib import Path
        >>> from common.validators import validate_file_extension
        >>> if validate_file_extension(Path("data.json"), ['.json', '.yaml']):
        ...     print("Valid extension!")
    """
    return file_path.suffix.lower() in [ext.lower() for ext in allowed_extensions]

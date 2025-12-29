"""
Утилиты для работы с файлами и директориями.

Безопасные операции:
- Чтение/запись файлов
- Ожидание готовности файла
- Создание директорий
- Поиск файлов
"""

import os
import time
from pathlib import Path
from typing import List, Optional


def wait_for_file_ready(file_path: Path, timeout: int = 10, check_interval: float = 0.5) -> bool:
    """
    Ожидает пока файл перестанет изменяться (полностью загрузится/скопируется).

    Args:
        file_path: Путь к файлу
        timeout: Максимальное время ожидания в секундах
        check_interval: Интервал проверки в секундах

    Returns:
        True если файл готов, False если timeout

    Example:
        >>> from pathlib import Path
        >>> from common.file_utils import wait_for_file_ready
        >>> if wait_for_file_ready(Path("download.zip")):
        ...     print("File ready!")
    """
    if not file_path.exists():
        return False

    start_time = time.time()
    last_size = -1

    while time.time() - start_time < timeout:
        try:
            current_size = file_path.stat().st_size
            if current_size == last_size and current_size > 0:
                # Размер не изменился - файл готов
                return True
            last_size = current_size
            time.sleep(check_interval)
        except (OSError, PermissionError):
            # Файл еще заблокирован
            time.sleep(check_interval)

    return False


def safe_read_file(file_path: Path, encoding: str = "utf-8") -> Optional[str]:
    """
    Безопасное чтение файла с обработкой ошибок.

    Args:
        file_path: Путь к файлу
        encoding: Кодировка файла

    Returns:
        Содержимое файла или None при ошибке

    Example:
        >>> from pathlib import Path
        >>> from common.file_utils import safe_read_file
        >>> content = safe_read_file(Path("data.txt"))
    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def safe_write_file(
    file_path: Path, content: str, encoding: str = "utf-8", create_dirs: bool = True
) -> bool:
    """
    Безопасная запись в файл.

    Args:
        file_path: Путь к файлу
        content: Содержимое для записи
        encoding: Кодировка файла
        create_dirs: Создавать директории если не существуют

    Returns:
        True при успехе, False при ошибке

    Example:
        >>> from pathlib import Path
        >>> from common.file_utils import safe_write_file
        >>> safe_write_file(Path("output/data.txt"), "Hello!")
    """
    try:
        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False


def ensure_directory(directory: Path, parents: bool = True) -> bool:
    """
    Создает директорию если не существует.

    Args:
        directory: Путь к директории
        parents: Создавать родительские директории

    Returns:
        True если директория существует или создана

    Example:
        >>> from pathlib import Path
        >>> from common.file_utils import ensure_directory
        >>> ensure_directory(Path("data/logs"))
    """
    try:
        directory.mkdir(parents=parents, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return False


def find_files(
    directory: Path,
    pattern: str = "*",
    recursive: bool = False,
    exclude_hidden: bool = True,
) -> List[Path]:
    """
    Находит файлы по паттерну.

    Args:
        directory: Директория для поиска
        pattern: Glob паттерн (например: "*.txt", "*.py")
        recursive: Рекурсивный поиск
        exclude_hidden: Исключить скрытые файлы

    Returns:
        Список найденных файлов

    Example:
        >>> from pathlib import Path
        >>> from common.file_utils import find_files
        >>> files = find_files(Path("."), pattern="*.py")
    """
    if not directory.exists():
        return []

    if recursive:
        found = list(directory.rglob(pattern))
    else:
        found = list(directory.glob(pattern))

    # Фильтруем скрытые файлы
    if exclude_hidden:
        found = [f for f in found if not f.name.startswith(".")]

    # Только файлы (не директории)
    return [f for f in found if f.is_file()]

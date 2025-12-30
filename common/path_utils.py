"""
Утилиты для работы с путями.

Кроссплатформенные функции для получения стандартных путей:
- Корень проекта
- Папка загрузок
- Папка данных приложения
"""

from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """
    Получает корневую директорию проекта Rutina.

    Returns:
        Path к корневой директории проекта

    Example:
        >>> from common.path_utils import get_project_root
        >>> root = get_project_root()
        >>> print(root)  # C:/Users/user/Desktop/GitHub/Rutina
    """
    # common находится в project_root/common
    return Path(__file__).parent.parent


def get_downloads_folder() -> Path:
    """
    Получает путь к папке загрузок (кроссплатформенно).

    Returns:
        Path к папке Downloads

    Example:
        >>> from common.path_utils import get_downloads_folder
        >>> downloads = get_downloads_folder()
        >>> print(downloads)  # C:/Users/user/Downloads
    """
    return Path.home() / "Downloads"


def get_data_folder(project_name: str, create: bool = True) -> Path:
    """
    Получает папку данных для конкретного проекта.

    Создает структуру: ~/.rutina/project_name/

    Args:
        project_name: Имя проекта (например "FileOrganizer")
        create: Создать директорию если не существует

    Returns:
        Path к папке данных проекта

    Example:
        >>> from common.path_utils import get_data_folder
        >>> data = get_data_folder("FileOrganizer")
        >>> print(data)  # C:/Users/user/.rutina/FileOrganizer
    """
    data_dir = Path.home() / ".rutina" / project_name

    if create:
        data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir


def get_config_path(project_name: str, config_filename: str = "config.json") -> Path:
    """
    Получает путь к файлу конфигурации проекта.

    Args:
        project_name: Имя проекта
        config_filename: Имя файла конфигурации

    Returns:
        Path к файлу конфигурации

    Example:
        >>> from common.path_utils import get_config_path
        >>> config = get_config_path("Anti-AltTab")
        >>> print(config)  # C:/GitHub/Rutina/Anti-AltTab/config.json
    """
    project_root = get_project_root()
    return project_root / project_name / config_filename


def get_log_path(project_name: str, log_filename: Optional[str] = None) -> Path:
    """
    Получает путь к файлу лога проекта.

    Args:
        project_name: Имя проекта
        log_filename: Имя файла лога (по умолчанию: project_name.log)

    Returns:
        Path к файлу лога

    Example:
        >>> from common.path_utils import get_log_path
        >>> log = get_log_path("FileOrganizer")
        >>> print(log)  # C:/GitHub/Rutina/FileOrganizer/FileOrganizer.log
    """
    if log_filename is None:
        log_filename = f"{project_name}.log"

    project_root = get_project_root()
    return project_root / project_name / log_filename

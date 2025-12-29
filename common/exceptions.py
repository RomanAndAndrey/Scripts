"""
Общие исключения для common библиотеки.
"""


class CommonLibraryError(Exception):
    """Базовое исключение для common библиотеки."""

    pass


class ConfigError(CommonLibraryError):
    """Ошибка конфигурации."""

    pass


class ValidationError(CommonLibraryError):
    """Ошибка валидации данных."""

    pass


class FileOperationError(CommonLibraryError):
    """Ошибка файловой операции."""

    pass

"""
Менеджер профилей конфигурации для Anti-AltTab.
Позволяет загружать и переключать профили для разных игр.
"""

import json
import os
from typing import Any, Dict, List, Optional


class ProfileManager:
    """
    Управление профилями конфигурации.

    Attributes:
        profiles_dir: Путь к папке с профилями
        current_profile: Имя текущего профиля
        current_config: Загруженная конфигурация
    """

    def __init__(self, profiles_dir: str = "profiles"):
        """
        Инициализирует менеджер профилей.

        Args:
            profiles_dir: Путь к папке с профилями
        """
        self.profiles_dir = profiles_dir
        self.current_profile: Optional[str] = None
        self.current_config: Dict[str, Any] = {}

        # Создаем папку profiles если не существует
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)

    def list_profiles(self) -> List[str]:
        """
        Возвращает список доступных профилей.

        Returns:
            Список имен файлов профилей без расширения
        """
        if not os.path.exists(self.profiles_dir):
            return []

        profiles = []
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith(".json"):
                profiles.append(filename[:-5])  # Убираем .json
        return sorted(profiles)

    def load_profile(self, profile_name: str) -> Dict[str, Any]:
        """
        Загружает профиль из файла.

        Args:
            profile_name: Имя профиля (без .json)

        Returns:
            Словарь с конфигурацией

        Raises:
            FileNotFoundError: Если профиль не найден
            json.JSONDecodeError: Если JSON невалидный
        """
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")

        with open(profile_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.current_profile = profile_name
        self.current_config = config

        return config

    def create_profile(self, profile_name: str, config: Dict[str, Any]) -> None:
        """
        Создает новый профиль.

        Args:
            profile_name: Имя профиля
            config: Конфигурация для сохранения
        """
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")

        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def get_config(self) -> Dict[str, Any]:
        """
        Возвращает текущую загруженную конфигурацию.

        Returns:
            Словарь конфигурации
        """
        return self.current_config

    def get_current_profile_name(self) -> Optional[str]:
        """
        Возвращает имя текущего профиля.

        Returns:
            Имя профиля или None
        """
        return self.current_profile

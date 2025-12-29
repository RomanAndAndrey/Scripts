"""
Модуль Overseer для мониторинга активных окон и процессов.
Определяет, какое приложение активно и принадлежит ли оно играм или запрещенным приложениям.
"""

import json
import os
from typing import Any, Dict, List, Optional

import psutil
import win32gui
import win32process


class Overseer:
    """
    Агент для мониторинга активных окон и процессов.

    Attributes:
        config: Словарь конфигурации с списками игр и запрещенных приложений
    """

    def __init__(self, config_path: str = "config.json"):
        """
        Инициализирует Overseer и загружает конфигурацию.

        Args:
            config_path: Путь к файлу конфигурации
        """
        self.config: Dict[str, Any] = {}
        self.load_config(config_path)

    def load_config(self, path: str) -> None:
        """
        Загружает конфигурацию из JSON файла.

        Args:
            path: Путь к файлу конфигурации
        """
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "games": [],
                "forbidden_apps": [],
                "cruelty_mode": "INPUT_BLOCK",
                "safety_key": "ctrl+alt+f12",
            }

    def get_active_window_process_name(self) -> Optional[str]:
        """
        Получает имя процесса активного окна.

        Returns:
            Имя процесса (например, "dota2.exe") или None при ошибке
        """
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None

            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()
        except Exception:
            return None

    def get_active_window_hwnd(self) -> int:
        """
        Получает handle активного окна.

        Returns:
            Handle окна (целое число)
        """
        return win32gui.GetForegroundWindow()

    def is_game_active(self) -> bool:
        """
        Проверяет, активна ли игра из списка.

        Returns:
            True если текущее окно - это игра из конфигурации
        """
        current_process = self.get_active_window_process_name()
        if not current_process:
            return False

        return current_process in self.config.get("games", [])

    def is_forbidden_app_active(self) -> bool:
        """
        Проверяет, активно ли запрещенное приложение.

        Returns:
            True если текущее окно - это запрещенное приложение
        """
        current_process = self.get_active_window_process_name()
        if not current_process:
            return False

        return current_process in self.config.get("forbidden_apps", [])

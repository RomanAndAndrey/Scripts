"""
Модуль проверки зависимостей для DesktopLauncher.
Проверяет наличие установленных пакетов из requirements.txt скриптов.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


def check_script_dependencies(script_path: str) -> List[str]:
    """
    Проверяет зависимости скрипта из его requirements.txt.

    Args:
        script_path: Путь к скрипту

    Returns:
        Список отсутствующих пакетов
    """
    script_dir = os.path.dirname(script_path)
    requirements_file = os.path.join(script_dir, "requirements.txt")

    if not os.path.exists(requirements_file):
        return []  # Нет файла requirements = нет зависимостей

    try:
        # Читаем requirements.txt
        with open(requirements_file, "r", encoding="utf-8") as f:
            required_packages = []
            for line in f:
                line = line.strip()
                # Пропускаем комментарии и пустые строки
                if line and not line.startswith("#"):
                    # Получаем имя пакета (до == или >=)
                    package_name = line.split("==")[0].split(">=")[0].split("[")[0].strip()
                    required_packages.append(package_name)

        # Получаем список установленных пакетов
        installed_packages = get_installed_packages()

        # Находим отсутствующие
        missing = []
        for package in required_packages:
            if package.lower() not in installed_packages:
                missing.append(package)

        return missing

    except Exception as e:
        print(f"Ошибка проверки зависимостей: {e}")
        return []


def get_installed_packages() -> set:
    """
    Получает список установленных Python пакетов.

    Returns:
        Множество имен установленных пакетов (lowercase)
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=freeze"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        installed = set()
        for line in result.stdout.split("\n"):
            if "==" in line:
                package_name = line.split("==")[0].strip().lower()
                installed.add(package_name)

        return installed

    except Exception as e:
        print(f"Ошибка получения списка пакетов: {e}")
        return set()


def install_dependencies(requirements_file: str) -> bool:
    """
    Устанавливает зависимости из requirements.txt.

    Args:
        requirements_file: Путь к requirements.txt

    Returns:
        True если установка успешна
    """
    if not os.path.exists(requirements_file):
        return False

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Ошибка установки зависимостей: {e}")
        return False

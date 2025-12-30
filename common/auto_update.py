"""
Модуль автоматического обновления через GitHub Releases.

Проверяет наличие новых версий, скачивает и устанавливает обновления.
"""

import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


class Version:
    """Класс для работы с semantic versioning."""

    def __init__(self, version_str: str):
        """
        Инициализация версии.

        Args:
            version_str: Строка версии в формате "1.2.3" или "v1.2.3"
        """
        # Убираем 'v' если есть
        version_str = version_str.lstrip("v")
        parts = version_str.split(".")

        self.major = int(parts[0]) if len(parts) > 0 else 0
        self.minor = int(parts[1]) if len(parts) > 1 else 0
        self.patch = int(parts[2]) if len(parts) > 2 else 0

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other: "Version") -> bool:
        """Меньше чем."""
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        return self.patch < other.patch

    def __le__(self, other: "Version") -> bool:
        return self < other or self == other

    def __gt__(self, other: "Version") -> bool:
        return not self <= other

    def __ge__(self, other: "Version") -> bool:
        return not self < other

    def __eq__(self, other: "Version") -> bool:
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch


class AutoUpdater:
    """Класс для автоматического обновления приложений."""

    def __init__(self, repo_owner: str, repo_name: str, current_version: str, app_name: str):
        """
        Инициализация обновлятора.

        Args:
            repo_owner: Владелец репозитория (например "RomanAndAndrey")
            repo_name: Название репозитория (например "Scripts")
            current_version: Текущая версия приложения (например "1.0.0")
            app_name: Название приложения для поиска .exe (например "DesktopLauncher")
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = Version(current_version)
        self.app_name = app_name

        self.api_base = "https://api.github.com"
        self.latest_release_url = f"{self.api_base}/repos/{repo_owner}/{repo_name}/releases/latest"

        logger.info(f"AutoUpdater initialized for {app_name} v{self.current_version}")

    def check_for_updates(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Проверяет наличие обновлений на GitHub Releases.

        Returns:
            Кортеж (есть_обновление, новая_версия, download_url)

        Example:
            >>> updater = AutoUpdater("RomanAndAndrey", "Scripts", "1.0.0", "DesktopLauncher")
            >>> has_update, new_version, url = updater.check_for_updates()
            >>> if has_update:
            ...     print(f"Доступна версия {new_version}")
        """
        try:
            logger.info("Checking for updates...")

            # GitHub API запрос
            req = Request(self.latest_release_url)
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("User-Agent", f"{self.app_name}/{self.current_version}")

            with urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

            # Получаем версию
            tag_name = data.get("tag_name", "")
            new_version = Version(tag_name)

            logger.info(f"Latest version: {new_version}, current: {self.current_version}")

            # Сравниваем версии
            if new_version > self.current_version:
                # Ищем .exe файл в assets
                assets = data.get("assets", [])
                download_url = None

                for asset in assets:
                    asset_name = asset.get("name", "")
                    if self.app_name in asset_name and asset_name.endswith(".exe"):
                        download_url = asset.get("browser_download_url")
                        break

                if download_url:
                    logger.info(f"Update available: {new_version} at {download_url}")
                    return True, str(new_version), download_url
                else:
                    logger.warning(f"New version {new_version} found but no .exe asset")
                    return False, None, None
            else:
                logger.info("No updates available")
                return False, None, None

        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return False, None, None

    def download_update(self, download_url: str, progress_callback=None) -> Optional[Path]:
        """
        Скачивает обновление.

        Args:
            download_url: URL для скачивания
            progress_callback: Опциональный callback для прогресса (bytes_downloaded, total_bytes)

        Returns:
            Path к скачанному файлу или None при ошибке
        """
        try:
            logger.info(f"Downloading update from {download_url}")

            # Временная директория
            temp_dir = Path(tempfile.gettempdir()) / "rutina_updates"
            temp_dir.mkdir(exist_ok=True)

            # Имя файла из URL
            filename = download_url.split("/")[-1]
            temp_file = temp_dir / filename

            # Скачивание с progress
            req = Request(download_url)
            req.add_header("User-Agent", f"{self.app_name}/{self.current_version}")

            with urlopen(req, timeout=30) as response:
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded = 0

                with open(temp_file, "wb") as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback and total_size > 0:
                            progress_callback(downloaded, total_size)

            logger.info(f"Update downloaded to {temp_file}")
            return temp_file

        except Exception as e:
            logger.error(f"Error downloading update: {e}")
            return None

    def apply_update(self, new_exe_path: Path) -> bool:
        """
        Применяет обновление через updater.exe.

        Args:
            new_exe_path: Path к новому .exe файлу

        Returns:
            True если запущен процесс обновления
        """
        try:
            # Текущий .exe файл
            if getattr(sys, "frozen", False):
                current_exe = Path(sys.executable)
            else:
                logger.error("Cannot update - not running from .exe")
                return False

            # Путь к updater.exe (должен быть рядом)
            updater_exe = current_exe.parent / "updater.exe"

            if not updater_exe.exists():
                logger.error(f"Updater not found: {updater_exe}")
                return False

            # Запускаем updater с аргументами
            cmd = [
                str(updater_exe),
                "--source",
                str(new_exe_path),
                "--target",
                str(current_exe),
                "--wait-process",
                str(os.getpid()),
            ]

            logger.info(f"Starting updater: {' '.join(cmd)}")

            # Запускаем updater
            subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )

            # Закрываем текущее приложение
            logger.info("Exiting for update...")
            return True

        except Exception as e:
            logger.error(f"Error applying update: {e}")
            return False

    def check_and_notify(self) -> Tuple[bool, Optional[str]]:
        """
        Удобный метод для быстрой проверки обновлений.

        Returns:
            (есть_обновление, новая_версия)
        """
        has_update, new_version, _ = self.check_for_updates()
        return has_update, new_version

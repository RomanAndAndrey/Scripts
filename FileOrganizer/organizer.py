"""
Автоматический организатор файлов для папки Загрузки.
Сортирует файлы по категориям в реальном времени используя watchdog.
"""

import os
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List

# Добавляем родительскую директорию в sys.path для импорта common
sys.path.insert(0, str(Path(__file__).parent.parent))

from docx import Document
from pypdf import PdfReader
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from common.file_utils import wait_for_file_ready

# Используем common library
from common.logger import setup_logger

# Настройка логирования через common.logger
logger = setup_logger("FileOrganizer", log_file=Path(__file__).parent / "organizer.log")

# --- КОНФИГУРАЦИЯ ---

# Путь к папке Загрузки (кроссплатформенно)
# И папки Telegram Desktop
DOWNLOADS_DIR = Path.home() / "Downloads"
TELEGRAM_DIR = DOWNLOADS_DIR / "Telegram Desktop"

# Список папок для отслеживания
WATCH_DIRS = [DOWNLOADS_DIR, TELEGRAM_DIR]

# Ключевые слова для категории "Учеба"
STUDY_KEYWORDS = [
    "Лабораторная",
    "Курсовая",
    "Лекция",
    "Бадалин",
    "Андрей",
    "Дмитриевич",
    "Трембач",
    "Роман",
    "Федорович",
    "Терпугова",
    "Глушкова",
    "Отчет",
    "Отчёт",
    "Проект",
    "Практика",
    "Курсовая работа",
    "3 курс",
    "2 курс",
    "1 курс",
    "Лабораторная работа",
    "Доклад",
    "Диплом",
    "Дипломная работа",
    "Дипломная",
    "Конспект",
    "Конспекты",
    "Конспекты и ответы",
    "Задание",
    "ОТЧЕТ",
]

# Настройка расширений для категорий
CATEGORIES = {
    "Изображения": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp", ".tiff", ".ico"],
    "Инсталляторы": [".exe", ".msi", ".bat", ".cmd", ".msix"],
    "Архивы": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
    "Видео": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp"],
    "Презентации": [".pptx", ".ppt", ".pps", ".ppsx", ".odp"],
    "Торрент": [".torrent"],
    # "Учеба" заполняется динамически на основе контента или вручную добавленных расширений, если требуется
}

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---


# Функция wait_for_file_ready теперь импортируется из common.file_utils---


# --- ФУНКЦИИ АНАЛИЗА КОНТЕНТА ---


def check_pdf_content(file_path):
    """Сканирует PDF на наличие ключевых слов."""
    try:
        reader = PdfReader(file_path)
        # Проверяем первые 5 страниц, чтобы не тормозить на книгах
        for i, page in enumerate(reader.pages):
            if i > 5:
                break
            text = page.extract_text()
            if text:
                for keyword in STUDY_KEYWORDS:
                    if keyword.lower() in text.lower():
                        logger.info(f"Найдено ключевое слово '{keyword}' в {Path(file_path).name}")
                        return True
    except Exception as e:
        logger.error(f"Ошибка чтения PDF {Path(file_path).name}: {e}")
    return False


def check_docx_content(file_path):
    """Сканирует DOCX на наличие ключевых слов."""
    try:
        doc = Document(file_path)
        # Проверяем все параграфы
        for para in doc.paragraphs:
            for keyword in STUDY_KEYWORDS:
                if keyword.lower() in para.text.lower():
                    logger.info(f"Найдено ключевое слово '{keyword}' в {Path(file_path).name}")
                    return True
    except Exception as e:
        logger.error(f"Ошибка чтения DOCX {Path(file_path).name}: {e}")
    return False


# --- ЛОГИКА ПЕРЕМЕЩЕНИЯ ---


def move_file(file_path: Path, category_name: str) -> None:
    """
    Перемещает файл в папку категории, обрабатывая дубликаты.

    Args:
        file_path: Путь к файлу
        category_name: Название категории
    """
    destination_folder = DOWNLOADS_DIR / category_name

    if not destination_folder.exists():
        destination_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Создана папка: {category_name}")

    filename = file_path.name
    destination_path = destination_folder / filename

    # Если файл уже существует, добавляем счетчик
    counter = 1
    stem = file_path.stem
    ext = file_path.suffix
    while destination_path.exists():
        destination_path = destination_folder / f"{stem}_{counter}{ext}"
        counter += 1

    try:
        # Проверяем готовность файла перед перемещением
        if not wait_for_file_ready(file_path, timeout=5):
            logger.warning(f"Timeout ожидания готовности файла: {filename}")
            return

        shutil.move(str(file_path), str(destination_path))
        logger.info(f"[ПЕРЕМЕЩЕНО] {filename} -> {category_name}")
    except Exception as e:
        logger.error(f"Не удалось переместить {filename}: {e}")


# --- ОБРАБОТЧИК СОБЫТИЙ ---


class OrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_modified(self, event):
        # Часто срабатывает много раз при загрузке, лучше использовать on_created + паузу
        # или отслеживать завершение загрузки (.crdownload и т.д.)
        pass

    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.dest_path)

    def process_file(self, file_path_str: str) -> None:
        """Обрабатывает новый или измененный файл."""
        file_path = Path(file_path_str)
        filename = file_path.name

        # Игнорируем временные файлы и скрытые файлы
        if filename.startswith(".") or file_path.suffix in [".tmp", ".crdownload", ".part"]:
            return

        # Проверяем, что файл находится в одной из отслеживаемых папок
        if file_path.parent not in WATCH_DIRS:
            return

        # Даем системе время записать файл
        time.sleep(2)

        try:
            ext = file_path.suffix.lower()

            # 1. Проверка на Учебу (по контенту)
            is_study = False
            if ext == ".pdf":
                is_study = check_pdf_content(file_path)
            elif ext == ".docx":
                is_study = check_docx_content(file_path)

            if is_study:
                move_file(file_path, "Учеба")
                return

            # 2. Проверка по остальным категориям
            for category, extensions in CATEGORIES.items():
                if ext in extensions:
                    move_file(file_path, category)
                    return

            # Если никуда не попало - остается на месте

        except Exception as e:
            logger.error(f"Ошибка при обработке {filename}: {e}")


if __name__ == "__main__":
    logger.info("Запуск Организатора Файлов...")
    for d in WATCH_DIRS:
        logger.info(f"Отслеживаемая папка: {d}")
        if not d.exists():
            logger.warning(f"Внимание: папка {d} не существует!")
    logger.info("Для выхода нажмите Ctrl+C")

    # Создаем категории заранее (опционально, но удобно)
    for cat in list(CATEGORIES.keys()) + ["Учеба"]:
        path = DOWNLOADS_DIR / cat
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

    event_handler = OrganizerHandler()
    observer = Observer()

    # Обработка существующих файлов при запуске
    logger.info("Сканирование существующих файлов...")
    for d in WATCH_DIRS:
        if d.exists():
            for file_item in d.iterdir():
                if file_item.is_file():
                    event_handler.process_file(str(file_item))

            # Добавляем в наблюдатель
            observer.schedule(event_handler, str(d), recursive=False)

    logger.info("Сканирование завершено. Ожидание новых файлов...")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("\nОстановка скрипта...")

    observer.join()

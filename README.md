# Рутина - Автоматизация Рутинных Задач

![GitHub release (latest by date)](https://img.shields.io/github/v/release/RomanAndAndrey/Scripts?style=for-the-badge&logo=github&color=blue)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/RomanAndAndrey/Scripts/build-desktop-launcher.yml?style=for-the-badge&logo=github-actions&label=Build)
![Python Version](https://img.shields.io/badge/python-3.14-blue?style=for-the-badge&logo=python)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

Коллекция Python утилит для автоматизации повседневных задач.

## 📦 Проекты

### 🎮 [Anti-AltTab](./Anti-AltTab)
Блокировка Alt+Tab во время игры для полной концентрации.

### 📁 [FileOrganizer](./FileOrganizer)
Автоматическая сортировка загруженных файлов по категориям.

### 🖥️ [DesktopLauncher](./DesktopLauncher)
Единый менеджер для запуска и мониторинга всех скриптов с GUI.

### 🎯 [DotaCoach](./DotaCoach)
Прозрачный оверлей с советами для Dota 2.

### 🎤 [Real-time Context Overlay](./Real-time%20Context%20Overlay)
AI-ассистент с распознаванием речи через Whisper.

### 📹 [YouTubeDownloader](./YouTubeDownloader)
Скачивание видео и музыки с YouTube через yt-dlp.

### 📊 [Code to Slides](./Code%20to%20Slides)
Генератор PowerPoint презентаций из Markdown файлов.

### 🚀 [ScriptLauncher](./ScriptLauncher)
Web-интерфейс на Streamlit для запуска Python скриптов.


---

## 📥 Установка

### Для Пользователей (Легко!)

**📦 Скачайте готовые .exe:**
1. Перейдите на [Releases](https://github.com/RomanAndAndrey/Scripts/releases)
2. Скачайте нужный проект (DesktopLauncher, FileOrganizer, Anti-AltTab, DotaCoach)
3. Запустите - готово! ✅

**Никакого Python, никаких зависимостей!**

### 🐳 Docker
```bash
docker pull ghcr.io/romanandandrey/rutina-file-organizer:latest
docker-compose up -d file-organizer
```

### 👨‍💻 Для Разработчиков
```bash
git clone https://github.com/RomanAndAndrey/Scripts.git
cd Scripts
pip install -r requirements.txt
python DesktopLauncher/main.py
```

---

## 📚 Common Library

Переиспользуемая библиотека для всех проектов с компонентами:
- **logger.py** - универсальное логирование с ротацией файлов
- **config.py** - загрузка/сохранение JSON конфигураций
- **file_utils.py** - безопасные файловые операции
- **validators.py** - валидация данных
- **exceptions.py** - кастомные исключения

**Использование:**
```python
from common.logger import setup_logger
from common.config import load_json_config

logger = setup_logger("MyApp", log_file=Path("app.log"))
config = load_json_config(Path("config.json"), create_if_missing=True)
```

См. [common/README.md](./common/README.md) для подробностей.

> [!IMPORTANT]
> Для скриптов, находящихся в подпапках (FileOrganizer, Anti-AltTab и т.д.), необходимо добавить родительскую директорию в `sys.path`:
> ```python
> import sys
> from pathlib import Path
> sys.path.insert(0, str(Path(__file__).parent.parent))
> ```

---

## 📋 Требования

- **Python 3.11+**
- **CustomTkinter** - GUI
- **Code Quality**: Black, isort, MyPy, Pylint
- **CI/CD**: GitHub Actions, Pre-commit hooks
- **Testing**: Pytest


```bash
pip install -r requirements.txt
```

## 🚀 Быстрый Старт

### Вариант 1: Desktop Launcher (рекомендуется)

```bash
cd DesktopLauncher
python main.py
# Или запустите DesktopLauncher.exe из dist/
```

### Вариант 2: Отдельные скрипты

```bash
# FileOrganizer
cd FileOrganizer
python organizer.py

# Anti-AltTab
cd Anti-AltTab
python main.py

# И так далее...
```

## 🧪 Тестирование

```bash
# Запуск тестов
pytest tests/ -v

# С покрытием кода
pytest tests/ -v --cov=. --cov-report=html
```

## 💻 Разработка

### Code Quality Tools

Проект использует автоматическое форматирование и проверки:

```bash
# Форматирование
black .
isort .

# Проверка типов
mypy . --ignore-missing-imports

# Линтинг
pylint **/*.py
```

### Pre-commit Hooks

Автоматические проверки перед коммитом:

```bash
pre-commit install
```

Теперь перед каждым коммитом код автоматически форматируется!

## 📊 Статистика Проекта

- **Проектов:** 8 + common библиотека
- **Строк кода:** ~4000+ (с типизацией)
- **Покрытие тестами:** 48%
- **Документация:** 100% (README для каждого проекта)
- **Модулей в common:** 5
- **Тестов common:** 10/10 прошли

## 🎯 Фазы Разработки

- ✅ **Фаза 1:** Критичные исправления (100%)
- ✅ **Фаза 2:** Структурирование (100%)
- ✅ **Фаза 3:** Типизация и документация (100%)
- ✅ **Фаза 4:** Новые фичи (100%)
- ✅ **Фаза 5:** CI/CD и автоматизация (100%)
- ✅ **Фаза 6:** Общая библиотека (90%)

## 📝 Лицензия

MIT License - свободное использование

## 👤 Автор

Создано для оптимизации рабочего процесса и автоматизации рутинных задач.

---

**⭐ Если проект полезен - поставьте звезду!**

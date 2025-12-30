# Changelog

Все заметные изменения в проекте Rutina будут задокументированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/),
и этот проект придерживается [Semantic Versioning](https://semver.org/lang/ru/).

## [Unreleased]

### Планируется
- Автоматическая компиляция .exe через GitHub Actions
- Docker контейнеры для веб-приложений
- Система автообновления

---

## [1.0.0] - 2025-12-30

### Добавлено

#### Фаза 1: Критичные исправления
- `.gitignore` для защиты API ключей
- Кроссплатформенные пути через `pathlib`
- Исправление race conditions в FileOrganizer

#### Фаза 2: Структурирование
- Модульная архитектура DesktopLauncher (6 модулей)
- Рефакторинг FileOrganizer (-36% кода)
- Централизованные конфигурации

#### Фаза 3: Типизация и документация
- Type hints для всех проектов (500+ строк)
- Docstrings в Google стиле
- 7 README файлов с примерами

#### Фаза 4: Новые фичи
- Проверка FFmpeg в YouTubeDownloader
- Валидация конфигурации в ScriptLauncher
- Система профилей для Anti-AltTab
- Dependency checker для DesktopLauncher
- Калибровка смерти в DotaCoach

#### Фаза 5: CI/CD и автоматизация
- Pre-commit hooks (black, isort, mypy)
- GitHub Actions workflow для качества кода
- `pyproject.toml` с централизованной конфигурацией
- Pytest тесты (17+ тестов)
- Главный README.md с badges

#### Фаза 6: Общая библиотека
- `common/logger.py` - универсальное логирование
- `common/config.py` - загрузка JSON конфигураций
- `common/file_utils.py` - безопасные файловые операции
- `common/validators.py` - валидация данных
- `common/exceptions.py` - кастомные исключения
- Тесты для common (10/10 прошли)
- Миграция FileOrganizer на common

#### Фаза 7: Расширенная миграция
- `common/path_utils.py` - кроссплатформенные пути
- Миграция DesktopLauncher на common
- 17/17 тестов common прошли
- Дублирование кода -100% в мигрированных проектах

### Изменено
- DesktopLauncher: современный дизайн UI
- FileOrganizer: улучшенная производительность
- Pre-commit: обновлен для Python 3.14

### Исправлено
- ModuleNotFoundError в FileOrganizer (sys.path)
- Pre-commit ошибка с Python 3.11 → 3.14
- Mypy конфликты types-all

---

## Статистика релиза v1.0.0

- **Фаз завершено:** 7 из 8
- **Модулей создано:** 25+
- **Строк кода:** ~4000+
- **Строк типизации:** 500+
- **README файлов:** 8
- **Тестов:** 17
- **Покрытие:** 57%
- **Дублирование кода:** -100% (цель была -50%)

---

[Unreleased]: https://github.com/RomanAndAndrey/Scripts/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/RomanAndAndrey/Scripts/releases/tag/v1.0.0

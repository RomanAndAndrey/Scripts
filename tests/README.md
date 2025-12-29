# Tests

Базовые тесты для проверки качества кода проектов Рутина.

## Запуск тестов

```bash
# Все тесты
pytest tests/ -v

# С покрытием кода
pytest tests/ -v --cov=. --cov-report=html

# Один конкретный тест
pytest tests/test_desktop_launcher.py -v
```

## Структура

- `test_file_organizer.py` - тесты FileOrganizer
- `test_desktop_launcher.py` - тесты DesktopLauncher  
- `test_anti_alttab.py` - тесты Anti-AltTab

## Отчет о покрытии

После запуска с `--cov-report=html` откройте `htmlcov/index.html` в браузере.

## TODO

- [ ] Добавить функциональные тесты для каждого модуля
- [ ] Добавить integration тесты
- [ ] Настроить fixtures для тестовых данных
- [ ] Добавить тесты для YouTubeDownloader
- [ ] Добавить тесты для ScriptLauncher

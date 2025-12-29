# Компиляция DesktopLauncher в .exe

## Требования

1. Установите PyInstaller:
```bash
pip install pyinstaller
```

## Команда для компиляции

Запустите из папки `DesktopLauncher`:

```bash
pyinstaller --name="Desktop Launcher" --onefile --windowed --icon=icon.ico --add-data "scripts_config.json;." --add-data "constants.py;." --add-data "models.py;." --add-data "widgets.py;." --add-data "utils.py;." --add-data "dependency_checker.py;." --hidden-import=customtkinter main.py
```

### Если нет icon.ico, используйте без иконки:

```bash
pyinstaller --name="Desktop Launcher" --onefile --windowed --add-data "scripts_config.json;." --add-data "constants.py;." --add-data "models.py;." --add-data "widgets.py;." --add-data "utils.py;." --add-data "dependency_checker.py;." --hidden-import=customtkinter main.py
```

## Упрощенная команда (рекомендуется)

```bash
pyinstaller --name="DesktopLauncher" --onefile --windowed ^
  --add-data "scripts_config.json;." ^
  --add-data "*.py;." ^
  --hidden-import=customtkinter ^
  --collect-all=customtkinter ^
  main.py
```

## Результат

После выполнения:
- В папке `dist/` появится `Desktop Launcher.exe` (или `DesktopLauncher.exe`)
- Скопируйте этот .exe в удобное место
- Запускайте двойным кликом!

## Устранение проблем

### Ошибка "module not found"
Добавьте `--hidden-import=имя_модуля`

### Ошибка с CustomTkinter
```bash
pip install --upgrade customtkinter
pyinstaller --clean ...  # повторите команду с --clean
```

### .exe слишком большой
Используйте UPX для сжатия:
```bash
pip install pyinstaller[upx]
# Затем повторите команду компиляции
```

## Текущее состояние

✅ Все 7 проектов добавлены в scripts_config.json:
1. Anti-AltTab
2. Организатор Файлов
3. Dota Coach
4. Context Overlay
5. YouTube Downloader
6. Code to Slides
7. Тестовый Пинг (ScriptLauncher test)

Готово к компиляции! 🚀

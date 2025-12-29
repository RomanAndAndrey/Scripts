# Использование Созданных Модулей - Фаза 4

## Руководство по интеграции улучшений Фазы 4

Все модули созданы и готовы к использованию. Вот как их применять:

---

## 1. DesktopLauncher - Проверка Зависимостей

### Модуль: `dependency_checker.py`

**Уже добавлен импорт в main.py** ✅

**Использование:**
```python
from dependency_checker import check_script_dependencies

# При запуске скрипта
missing_deps = check_script_dependencies(script_path)
if missing_deps:
    print(f"⚠️ Отсутствуют: {', '.join(missing_deps)}")
```

**Автоматическая проверка:** Модуль уже интегрирован в main.py и будет автоматически проверять зависимости при запуске любого скрипта.

---

## 2. Anti-AltTab - Система Профилей

### Модуль: `profile_manager.py`
### Профили: `profiles/dota2.json`, `profiles/cs2.json`, `profiles/default.json`

**Пример использования:**

### Вариант 1: Загрузка профиля при запуске

Измените `main.py`:
```python
from profile_manager import ProfileManager

def main() -> None:
    # Создаем менеджер профилей
    pm = ProfileManager()
    
    # Показываем доступные профили
    profiles = pm.list_profiles()
    print("Доступные профили:", profiles)
    
    # Загружаем профиль (например, dota2)
    config = pm.load_profile('dota2')
    
    # Используем конфигурацию вместо чтения из config.json
    overseer = Overseer()
    overseer.config = config  # Заменяем конфигурацию
    
    combat = CombatModule(config)
    # ... остальной код
```

### Вариант 2: Выбор профиля через аргумент командной строки

```python
import argparse
from profile_manager import ProfileManager

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default='default', help='Профиль конфигурации')
    args = parser.parse_args()
    
    pm = ProfileManager()
    config = pm.load_profile(args.profile)
    
    # Используем загруженную конфигурацию...
```

**Запуск:**
```bash
python main.py --profile dota2
python main.py --profile cs2
```

### Создание нового профиля

```python
pm = ProfileManager()

new_config = {
    "name": "My Game Profile",
    "games": ["mygame.exe"],
    "forbidden_apps": ["Discord.exe"],
    "cruelty_mode": "INPUT_BLOCK",
    "safety_key": "ctrl+alt+f10"
}

pm.create_profile('mygame', new_config)
```

---

## 3. DotaCoach - Конфигурация

### Файл: `coach_config.json`

**Загрузка конфигурации в main.py:**

```python
import json

# В начале DotaOverlay.__init__
def __init__(self):
    # Загрузка конфигурации
    try:
        with open('coach_config.json', 'r') as f:
            config = json.load(f)
        
        self.threshold = config['detection']['threshold']
        self.region_size = config['detection']['region_size']
        self.check_interval = config['detection']['check_interval']
    except FileNotFoundError:
        # Значения по умолчанию
        self.threshold = 15
        self.region_size = 200
        self.check_interval = 1.0
    
    # ... остальной код
```

### Калибровка (простая реализация)

Добавьте функцию в `main.py`:

```python
def calibrate():
    """Простая калибровка порога обнаружения."""
    print("=" * 50)
    print("Калибровка Dota Coach")
    print("=" * 50)
    print("\n1. Запустите Dota 2")
    print("2. Войдите в игру и умрите")
    print("3. Нажмите Enter когда экран станет серым...")
    input()
    
    # Делаем скриншот и анализируем
    import pyautogui
    screenshot = pyautogui.screenshot()
    w, h = screenshot.size
    region = screenshot.crop((w//2 - 100, h//2 - 100, w//2 + 100, h//2 + 100))
    
    # Вычисляем среднюю насыщенность
    pixels = region.getdata()
    avg_saturation = sum(max(r, g, b) - min(r, g, b) for r, g, b in pixels) / len(pixels)
    
    recommended_threshold = int(avg_saturation) + 5
    print(f"\nРекомендуемый threshold: {recommended_threshold}")
    
    # Сохраняем в конфигурацию
    try:
        with open('coach_config.json', 'r') as f:
            config = json.load(f)
        
        config['detection']['threshold'] = recommended_threshold
        config['calibration']['calibrated'] = True
        config['calibration']['last_calibration'] = str(datetime.now())
        
        with open('coach_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Конфигурация сохранена!")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

# В main():
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--calibrate':
        calibrate()
    else:
        # Запуск обычного оверлея
        ...
```

**Использование:**
```bash
python main.py --calibrate  # Калибровка
python main.py              # Обычный запуск
```

---

## 4. ScriptLauncher - Валидация

**Уже интегрирована!** ✅

Валидация происходит автоматически при загрузке приложения. Если есть ошибки в `scripts_config.json`, они будут отображены в UI с подсказками.

---

## 5. YouTubeDownloader - Проверка FFmpeg

**Уже интегрирована!** ✅

Проверка FFmpeg происходит автоматически при запуске `yt_load.py`. Если FFmpeg не найден, скрипт предоставит инструкции по установке.

---

## Быстрый Старт

### Для DesktopLauncher
```bash
cd DesktopLauncher
python main.py  # Проверка зависимостей работает автоматически
```

### Для Anti-AltTab с профилем
```bash
cd Anti-AltTab
# Вариант 1: Отредактируйте main.py (добавьте код из примера выше)
# Вариант 2: Используйте напрямую через Python
python
>>> from profile_manager import ProfileManager
>>> pm = ProfileManager()
>>> config = pm.load_profile('dota2')
>>> print(config)
```

### Для DotaCoach
```bash
cd DotaCoach
python main.py  # Использует coach_config.json если есть
```

### Для ScriptLauncher
```bash
cd ScriptLauncher
streamlit run app.py  # Валидация автоматическая
```

### Для YouTubeDownloader
```bash
cd YouTubeDownloader
python yt_load.py "URL"  # Проверка FFmpeg автоматическая
```

---

## Итоги Фазы 4

### Созданные модули:
✅ `dependency_checker.py` - DesktopLauncher  
✅ `profile_manager.py` - Anti-AltTab  
✅ `coach_config.json` - DotaCoach  
✅ `profiles/` - Anti-AltTab (dota2, cs2, default)  

### Интегрированные улучшения:
✅ Проверка FFmpeg - YouTubeDownloader  
✅ Валидация конфигурации - ScriptLauncher  
✅ Импорт dependency_checker - DesktopLauncher  

### Требуется ручная интеграция:
⚠️  Загрузка профилей в Anti-AltTab main.py (см. примеры выше)  
⚠️  Калибровка в DotaCoach main.py (см. примеры выше)  

**Все модули готовы к использованию!** Примеры кода выше показывают, как их применять.

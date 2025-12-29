# Common Library

Переиспользуемая библиотека для всех проектов Рутина.

## Модули

### logger.py
Универсальное логирование с ротацией файлов.

```python
from common.logger import setup_logger
from pathlib import Path

logger = setup_logger("MyApp", log_file=Path("app.log"))
logger.info("Application started")
```

### config.py
Загрузка и сохранение JSON конфигураций.

```python
from common.config import load_json_config, save_json_config
from pathlib import Path

config = load_json_config(
    Path("config.json"),
    defaults={"debug": False},
    create_if_missing=True
)
```

### file_utils.py
Безопасные файловые операции.

```python
from common.file_utils import wait_for_file_ready, safe_read_file
from pathlib import Path

if wait_for_file_ready(Path("download.zip")):
    content = safe_read_file(Path("data.txt"))
```

### validators.py
Валидация данных и конфигураций.

```python
from common.validators import validate_config_structure

errors = validate_config_structure(
    config,
    required_keys=["name", "version"],
    optional_keys=["debug"]
)
```

### exceptions.py
Кастомные исключения.

```python
from common.exceptions import ConfigError, ValidationError

try:
    config = load_json_config(path)
except ConfigError as e:
    logger.error(f"Config error: {e}")
```

## Тестирование

```bash
# Запуск всех тестов common
pytest tests/test_common/ -v

# С покрытием
pytest tests/test_common/ -v --cov=common --cov-report=html
```

## Использование в Проектах

### FileOrganizer
- ✅ Использует `common.logger`
- ✅ Использует `common.file_utils`

### Другие Проекты
Миграция в процессе...

## Преимущества

- ✅ **DRY принцип** - нет дублирования кода
- ✅ **Единые стандарты** - одинаковое логирование везде
- ✅ **Легко тестировать** - модули независимы
- ✅ **Быстрое развитие** - новые проекты используют готовые компоненты

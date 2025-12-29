"""
Модели данных для Desktop Script Launcher.
"""

import subprocess
from typing import Any, Dict, List, Optional

from constants import STATUS_STOPPED


class ScriptState:
    """
    Класс для хранения состояния каждого скрипта.

    Attributes:
        name: Название скрипта
        config: Конфигурация скрипта из JSON
        process: Subprocess объект запущенного процесса
        status: Текущий статус (stopped/running/error)
        logs: Список строк лога
        return_code: Код возврата после завершения
        stopped_by_user: Флаг остановки пользователем
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.process: Optional[subprocess.Popen] = None
        self.status: str = STATUS_STOPPED
        self.logs: List[str] = []
        self.return_code: Optional[int] = None
        self.stopped_by_user: bool = False

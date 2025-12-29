"""
Streamlit Web Interface для запуска Python скриптов с параметрами и мониторингом логов.
"""

import json
import os
import queue
import subprocess
import sys
import threading
import time
from typing import Any, Dict, List, Optional

import streamlit as st

# Настройка страницы
st.set_page_config(page_title="Script Launcher", page_icon="🚀", layout="wide")

# Путь к конфигурации
CONFIG_FILE: str = "scripts_config.json"
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


def load_config() -> List[Dict[str, Any]]:
    """
    Загружает список скриптов из JSON файла.

    Returns:
        Список словарей с конфигурацией скриптов
    """
    config_path = os.path.join(BASE_DIR, CONFIG_FILE)
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Файл конфигурации не найден: {config_path}")
        return []
    except json.JSONDecodeError:
        st.error(f"Ошибка чтения JSON файла: {config_path}")
        return []


def validate_config(scripts: List[Dict[str, Any]]) -> List[str]:
    """
    Валидирует конфигурацию скриптов.

    Args:
        scripts: Список конфигураций скриптов

    Returns:
        Список ошибок (пустой если все ОК)
    """
    errors = []

    if not scripts:
        errors.append("Конфигурация пуста или не загружена")
        return errors

    for i, script in enumerate(scripts):
        script_id = script.get("name", f"Script #{i+1}")

        # Проверка обязательных полей
        if "name" not in script:
            errors.append(f"[{i+1}] Отсутствует поле 'name'")

        if "path" not in script:
            errors.append(f"[{script_id}] Отсутствует поле 'path'")
        else:
            # Проверка существования скрипта
            script_path = os.path.join(BASE_DIR, script["path"])
            if not os.path.exists(script_path):
                errors.append(f"[{script_id}] Скрипт не найден: {script['path']}")

        # Проверка структуры аргументов
        if "args" in script:
            args = script["args"]
            if not isinstance(args, list):
                errors.append(f"[{script_id}] Поле 'args' должно быть списком")
            else:
                for j, arg in enumerate(args):
                    if not isinstance(arg, dict):
                        errors.append(f"[{script_id}] Аргумент #{j+1} должен быть объектом")
                    elif "name" not in arg:
                        errors.append(f"[{script_id}] Аргумент #{j+1} без поля 'name'")

    return errors


def run_script(script_path: str, args_list: List[str]) -> Optional[subprocess.Popen]:
    """
    Запускает скрипт в подпроцессе.

    Args:
        script_path: Относительный путь к скрипту
        args_list: Список аргументов командной строки

    Returns:
        Объект Popen или None при ошибке
    """
    full_path = os.path.join(BASE_DIR, script_path)
    if not os.path.exists(full_path):
        st.error(f"Скрипт не найден: {full_path}")
        return None

    cmd = [sys.executable, "-u", full_path] + args_list

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding="utf-8",
            cwd=os.path.dirname(full_path),
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        return process
    except Exception as e:
        st.error(f"Ошибка запуска: {e}")
        return None


def enqueue_output(process: subprocess.Popen, log_queue: queue.Queue) -> None:
    """
    Читает вывод процесса и помещает в очередь.

    Args:
        process: Объект Popen
        log_queue: Очередь для логов
    """
    for line in iter(process.stdout.readline, ""):
        log_queue.put(line)
    process.stdout.close()


# --- Состояние сессии ---

if "running_process" not in st.session_state:
    st.session_state.running_process = None
if "log_queue" not in st.session_state:
    st.session_state.log_queue = None
if "logs" not in st.session_state:
    st.session_state.logs = []
if "script_finished" not in st.session_state:
    st.session_state.script_finished = False

# --- Интерфейс ---

st.title("🚀 Script Launcher")

# Сайдбар - Выбор скрипта
scripts = load_config()

# Валидация конфигурации
validation_errors = validate_config(scripts)
if validation_errors:
    st.error("🚨 Ошибки в конфигурации scripts_config.json:")
    for error in validation_errors:
        st.warning(f"• {error}")

    with st.expander("ℹ️ Как исправить"):
        st.info(
            """
        1. Откройте `scripts_config.json`
        2. Проверьте, что у каждого скрипта есть поля `name` и `path`
        3. Убедитесь, что файлы скриптов существуют
        4. Проверьте правильность структуры JSON
        5. Перезагрузите страницу после исправления
        """
        )
    st.stop()

script_names = [s["name"] for s in scripts]
selected_script_name = st.sidebar.selectbox("Выберите скрипт", script_names)

# Поиск выбранного конфига
selected_script_config = next((s for s in scripts if s["name"] == selected_script_name), None)

if selected_script_config:
    st.header(selected_script_config["name"])
    st.write(selected_script_config.get("description", ""))

    st.divider()

    # Генерация аргументов
    arg_values: Dict[str, Any] = {}
    if "args" in selected_script_config:
        st.subheader("Параметры")
        col1, col2 = st.columns(2)

        for i, arg in enumerate(selected_script_config["args"]):
            key = f"arg_{arg['name']}"
            label = arg.get("label", arg["name"])
            default = arg.get("default", "")
            arg_type = arg.get("type", "text")

            place = col1 if i % 2 == 0 else col2

            if arg_type == "int":
                arg_values[arg["name"]] = place.number_input(
                    label, value=int(default) if default else 0, step=1, key=key
                )
            elif arg_type == "float":
                arg_values[arg["name"]] = place.number_input(
                    label, value=float(default) if default else 0.0, key=key
                )
            elif arg_type == "bool":
                arg_values[arg["name"]] = place.checkbox(label, value=bool(default), key=key)
            else:
                arg_values[arg["name"]] = place.text_input(label, value=str(default), key=key)

    st.divider()

    # Управление запуском
    col_run, col_stop, _ = st.columns([1, 1, 4])

    # Кнопка Run
    if col_run.button(
        "Запустить", type="primary", disabled=st.session_state.running_process is not None
    ):
        st.session_state.logs = []
        st.session_state.script_finished = False

        # Сбор аргументов для командной строки
        cmd_args: List[str] = []
        for arg in selected_script_config.get("args", []):
            name = arg["name"]
            val = arg_values[name]

            if arg.get("type") == "bool":
                if val:
                    cmd_args.append(f"--{name}")
            else:
                cmd_args.append(f"--{name}")
                cmd_args.append(str(val))

        # Запуск
        process = run_script(selected_script_config["path"], cmd_args)
        if process:
            st.session_state.running_process = process
            st.session_state.log_queue = queue.Queue()

            t = threading.Thread(target=enqueue_output, args=(process, st.session_state.log_queue))
            t.daemon = True
            t.start()
            st.rerun()

    # Кнопка Stop
    if col_stop.button(
        "Остановить", type="secondary", disabled=st.session_state.running_process is None
    ):
        if st.session_state.running_process:
            st.session_state.running_process.terminate()
            st.session_state.logs.append("\n[STOP] Процесс был остановлен пользователем.\n")
            st.session_state.running_process = None
            st.session_state.script_finished = True
            st.rerun()

    # --- Отображение логов ---

    st.subheader("Логи выполнения")
    log_container = st.container(height=400, border=True)

    if st.session_state.running_process:
        try:
            while True:
                line = st.session_state.log_queue.get_nowait()
                st.session_state.logs.append(line)
        except queue.Empty:
            pass

        if st.session_state.running_process.poll() is not None:
            st.session_state.running_process = None
            st.session_state.script_finished = True
            st.session_state.logs.append("\n[DONE] Процесс завершился\n")

    with log_container:
        if st.session_state.logs:
            st.code("".join(st.session_state.logs), language="text", line_numbers=False)
        else:
            st.info("Здесь будет вывод скрипта...")

    # Авто-обновление
    if st.session_state.running_process is not None:
        time.sleep(0.5)
        st.rerun()

"""
Desktop Script Launcher v2.1 - Refactored
Менеджер для запуска и мониторинга Python скриптов с GUI интерфейсом.
"""

import os
import queue
import subprocess
import sys
import threading
from typing import Dict, Optional

import customtkinter as ctk
from dependency_checker import check_script_dependencies

# Локальные модули
from constants import (
    APPEARANCE_MODE,
    COLOR_THEME,
    MAX_LOG_LINES,
    STATUS_ERROR,
    STATUS_RUNNING,
    STATUS_STOPPED,
)
from models import ScriptState
from utils import get_base_dir, get_python_exe, load_scripts_config, logger, smart_resolve_path
from widgets import ContextMenu, InputFrame, SidebarItem

# Настройка темы
ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(COLOR_THEME)


class App(ctk.CTk):
    """
    Главное приложение Desktop Script Launcher.

    Attributes:
        scripts_config: Конфигурация скриптов из JSON
        scripts_state: Словарь состояний скриптов
        sidebar_items: Словарь виджетов сайдбара
        current_script_name: Имя текущего выбранного скрипта
        event_queue: Очередь событий из потоков
    """

    def __init__(self):
        super().__init__()

        self.title("Desktop Script Launcher v2.1")
        self.geometry("1000x700")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Загрузка конфигурации
        self.scripts_config = load_scripts_config()
        if not self.scripts_config:
            logger.error("No scripts loaded! Check scripts_config.json")

        # Очередь событий
        self.event_queue: queue.Queue = queue.Queue()

        # Состояние приложения
        self.scripts_state: Dict[str, ScriptState] = {
            name: ScriptState(name, cfg) for name, cfg in self.scripts_config.items()
        }
        self.sidebar_items: Dict[str, SidebarItem] = {}
        self.current_script_name: Optional[str] = None

        # Построение UI
        self._build_ui()

        # Запуск цикла обработки событий
        self.check_queue()

        # Выбираем первый скрипт по умолчанию
        if self.scripts_config:
            first_script = list(self.scripts_config.keys())[0]
            self.select_script(first_script)

        logger.info("Application started successfully")

    def _build_ui(self) -> None:
        """Строит пользовательский интерфейс."""
        # 1. Sidebar
        self._build_sidebar()

        # 2. Main Area
        self._build_main_area()

    def _build_sidebar(self) -> None:
        """Строит боковую панель со списком скриптов."""
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo = ctk.CTkLabel(
            self.sidebar, text="Launcher", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo.pack(padx=20, pady=(20, 10))

        self.scroll_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        for name in self.scripts_config.keys():
            item = SidebarItem(self.scroll_frame, name, self.select_script)
            item.pack(fill="x", pady=2)
            self.sidebar_items[name] = item

    def _build_main_area(self) -> None:
        """Строит основную область с описанием, вводом и консолью."""
        self.main_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(3, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        # 2.1 Header с кнопками управления
        self.header_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Выберите скрипт",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.title_label.pack(side="left", padx=5)

        self.controls_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.controls_frame.pack(side="right")

        self.btn_start = ctk.CTkButton(
            self.controls_frame,
            text="Запустить",
            fg_color="green",
            width=100,
            command=self.on_start_click,
        )
        self.btn_start.pack(side="left", padx=5)

        self.btn_stop = ctk.CTkButton(
            self.controls_frame,
            text="Остановить",
            fg_color="red",
            width=100,
            command=self.on_stop_click,
        )
        self.btn_stop.pack(side="left", padx=5)

        # 2.2 Description
        self.desc_label = ctk.CTkLabel(
            self.main_area,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w",
            wraplength=700,
        )
        self.desc_label.grid(row=1, column=0, sticky="ew", pady=(5, 10), padx=5)

        # 2.3 Inputs Area
        self.input_frame = InputFrame(self.main_area)
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # 2.4 Console
        self.console = ctk.CTkTextbox(self.main_area, font=("Consolas", 12))
        self.console.grid(row=3, column=0, sticky="nsew")
        self.console.insert("0.0", "Выберите скрипт для начала работы...")
        self.console.configure(state="disabled")

        # Контекстное меню для консоли
        ContextMenu(self.console)

    def check_queue(self) -> None:
        """Обработка событий из потоков."""
        while not self.event_queue.empty():
            try:
                event_type, name, data = self.event_queue.get_nowait()

                state = self.scripts_state[name]

                if event_type == "log":
                    state.logs.append(data)
                    # Оптимизация памяти
                    if len(state.logs) > MAX_LOG_LINES:
                        state.logs.pop(0)

                    if self.current_script_name == name:
                        self.console.configure(state="normal")
                        self.console.insert("end", data)
                        self.console.see("end")
                        self.console.configure(state="disabled")

                elif event_type == "status":
                    state.status = data
                    self.sidebar_items[name].set_status(data)
                    if self.current_script_name == name:
                        self.update_buttons_state(state.status)

            except queue.Empty:
                pass

        self.after(100, self.check_queue)

    def select_script(self, name: str) -> None:
        """
        Выбирает скрипт для отображения.

        Args:
            name: Название скрипта
        """
        self.current_script_name = name

        for item_name, item in self.sidebar_items.items():
            item.set_selected(item_name == name)

        state = self.scripts_state[name]

        self.title_label.configure(text=name)
        self.desc_label.configure(text=state.config.get("description", ""))

        self.console.configure(state="normal")
        self.console.delete("0.0", "end")
        self.console.insert("0.0", "".join(state.logs))
        self.console.see("end")
        self.console.configure(state="disabled")

        # Строим поля ввода
        self.input_frame.build_inputs(state.config.get("inputs", []))

        self.update_buttons_state(state.status)

    def update_buttons_state(self, status: str) -> None:
        """Обновляет состояние кнопок в зависимости от статуса."""
        if status == STATUS_RUNNING:
            self.btn_start.configure(state="disabled", fg_color="gray")
            self.btn_stop.configure(state="normal", fg_color="red")
        else:
            self.btn_start.configure(state="normal", fg_color="green")
            self.btn_stop.configure(state="disabled", fg_color="gray")

    def on_start_click(self) -> None:
        """Обработчик кнопки запуска."""
        name = self.current_script_name
        if not name:
            return

        state = self.scripts_state[name]
        if state.status == STATUS_RUNNING:
            return

        # Собираем аргументы из GUI
        dynamic_args = self.input_frame.get_args()

        self.start_script_thread(name, dynamic_args)

    def on_stop_click(self) -> None:
        """Обработчик кнопки остановки."""
        name = self.current_script_name
        if not name:
            return

        state = self.scripts_state[name]
        if state.process:
            state.stopped_by_user = True
            state.process.terminate()
            logger.info(f"User stopped script: {name}")

    def start_script_thread(self, name: str, dynamic_args: list = None) -> None:
        """
        Запускает скрипт в отдельном потоке.

        Args:
            name: Название скрипта
            dynamic_args: Динамические аргументы из полей ввода
        """
        state = self.scripts_state[name]
        state.logs = []
        state.stopped_by_user = False

        if self.current_script_name == name:
            self.console.configure(state="normal")
            self.console.delete("0.0", "end")
            self.console.configure(state="disabled")

        threading.Thread(
            target=self._run_process_logic, args=(name, dynamic_args), daemon=True
        ).start()

    def _run_process_logic(self, name: str, dynamic_args: Optional[list] = None) -> None:
        """
        Логика запуска процесса в отдельном потоке.

        Args:
            name: Название скрипта
            dynamic_args: Динамические аргументы
        """
        state = self.scripts_state[name]
        config = state.config

        self.event_queue.put(("status", name, STATUS_RUNNING))
        self.event_queue.put(("log", name, f"[STARTING] {name}...\n"))
        logger.info(f"Starting script: {name}")

        try:
            base_dir = get_base_dir()
            python_exe = get_python_exe()

            script_path = smart_resolve_path(base_dir, config["path"])
            raw_cwd = config.get("cwd", ".")
            cwd_path = smart_resolve_path(base_dir, raw_cwd)

            # Валидация
            if not os.path.exists(script_path):
                self.event_queue.put(
                    ("log", name, f"[ERROR] Файл скрипта не найден:\n{script_path}\n")
                )
                self.event_queue.put(("log", name, f"[DEBUG] Искали относительно: {base_dir}\n"))
                self.event_queue.put(("status", name, STATUS_ERROR))
                logger.error(f"Script not found: {script_path}")
                return

            if not os.path.exists(cwd_path):
                self.event_queue.put(
                    ("log", name, f"[ERROR] Рабочая папка не найдена:\n{cwd_path}\n")
                )
                self.event_queue.put(("status", name, STATUS_ERROR))
                logger.error(f"CWD not found: {cwd_path}")
                return

            full_args = config.get("args", [])
            if dynamic_args:
                full_args = full_args + dynamic_args

            cmd = [python_exe, "-u", script_path] + full_args

            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # UTF-8 encoding
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=cwd_path,
                startupinfo=startupinfo,
                encoding="utf-8",
                errors="replace",
                env=env,
            )

            state.process = process

            for line in iter(process.stdout.readline, ""):
                self.event_queue.put(("log", name, line))

            process.stdout.close()
            return_code = process.wait()
            state.return_code = return_code

            state.process = None

            # Определение финального статуса
            if state.stopped_by_user or return_code == 0:
                final_status = STATUS_STOPPED
            else:
                final_status = STATUS_ERROR

            msg = f"\n[DONE] Exit Code: {return_code}\n"

            self.event_queue.put(("log", name, msg))
            self.event_queue.put(("status", name, final_status))
            logger.info(f"Script finished: {name}, exit code: {return_code}")

        except Exception as e:
            self.event_queue.put(("log", name, f"\n[EXCEPTION] {e}\n"))
            self.event_queue.put(("status", name, STATUS_ERROR))
            logger.error(f"Exception in script {name}: {e}", exc_info=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()

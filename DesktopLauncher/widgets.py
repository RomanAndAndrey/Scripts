"""
Виджеты GUI для Desktop Script Launcher.
Обновлено для премиального дизайна.
"""

import tkinter as tk
from typing import Any, Callable, Dict, List, Optional

import customtkinter as ctk

from DesktopLauncher.constants import COLORS, SCRIPT_ICONS, SIZES, STATUS_STOPPED


class SidebarItem(ctk.CTkFrame):
    """
    Современный элемент сайдбара с иконкой, статусным индикатором и hover эффектами.

    Attributes:
        name: Название скрипта
        command: Callback функция при клике
        indicator: Цветной индикатор статуса (круг)
        btn: Кнопка с названием и иконкой
    """

    def __init__(self, master: ctk.CTkFrame, name: str, command: Callable[[str], None], **kwargs):
        super().__init__(
            master, fg_color="transparent", corner_radius=SIZES["corner_radius"], **kwargs
        )
        self.command = command
        self.name = name

        # Лайаут
        self.grid_columnconfigure(1, weight=1)

        # Статусный индикатор (крутой неоновый кружок)
        indicator_size = SIZES["indicator_size"]
        self.indicator = ctk.CTkFrame(
            self,
            width=indicator_size,
            height=indicator_size,
            corner_radius=indicator_size // 2,
            fg_color=COLORS[STATUS_STOPPED],
            border_width=0,
        )
        self.indicator.grid(row=0, column=0, padx=(12, 8), pady=12)

        # Получаем иконку для этого скрипта
        icon = SCRIPT_ICONS.get(name, "•")
        button_text = f"{icon}  {name}" if icon != "•" else name

        # Кнопка с градиентным hover эффектом
        self.btn = ctk.CTkButton(
            self,
            text=button_text,
            anchor="w",
            fg_color="transparent",
            text_color=COLORS["text_secondary"],
            hover_color=COLORS["bg_card"],
            font=("Segoe UI", 13),
            corner_radius=SIZES["corner_radius"] - 2,
            border_width=0,
            command=lambda: self.command(name),
        )
        self.btn.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=6)

    def set_status(self, status: str) -> None:
        """Устанавливает цвет индикатора с эффектом свечения."""
        self.indicator.configure(fg_color=COLORS.get(status, COLORS["text_muted"]))

    def set_selected(self, is_selected: bool) -> None:
        """Выделяет элемент современным способом."""
        if is_selected:
            self.btn.configure(
                fg_color=COLORS["bg_card"],
                text_color=COLORS["text_primary"],
                font=("Segoe UI Semibold", 13),
            )
        else:
            self.btn.configure(
                fg_color="transparent", text_color=COLORS["text_secondary"], font=("Segoe UI", 13)
            )


class ContextMenu:
    """
    Класс для добавления контекстного меню и шорткатов (Копировать/Вставить) к виджетам ctk.

    Attributes:
        widget: Tkinter виджет (внутренний)
        menu: Контекстное меню
    """

    def __init__(self, widget: Any):
        # Пытаемся добраться до реального tkinter виджета внутри ctk
        if hasattr(widget, "_entry"):
            self.widget = widget._entry
        elif hasattr(widget, "_textbox"):
            self.widget = widget._textbox
        else:
            self.widget = widget

        self.menu = tk.Menu(self.widget, tearoff=0)
        self.menu.add_command(label="Копировать (Ctrl+C)", command=self.copy)
        self.menu.add_command(label="Вставить (Ctrl+V)", command=self.paste)
        self.menu.add_command(label="Вырезать (Ctrl+X)", command=self.cut)
        self.menu.add_separator()
        self.menu.add_command(label="Выделить всё (Ctrl+A)", command=self.select_all)

        # Бинд на правую кнопку мыши
        self.widget.bind("<Button-3>", self.show_menu)

        # Явные бинды клавиатуры
        self.widget.bind("<Control-c>", lambda e: self.copy())
        self.widget.bind("<Control-v>", lambda e: self.paste())
        self.widget.bind("<Control-x>", lambda e: self.cut())
        self.widget.bind("<Control-a>", lambda e: self.select_all())

    def show_menu(self, event: tk.Event) -> None:
        """Отображает контекстное меню."""
        self.widget.focus_set()
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def copy(self, event: Optional[tk.Event] = None) -> None:
        """Копирует выделенный текст."""
        try:
            self.widget.event_generate("<<Copy>>")
        except:
            pass

    def paste(self, event: Optional[tk.Event] = None) -> None:
        """Вставляет текст из буфера."""
        try:
            self.widget.event_generate("<<Paste>>")
        except:
            pass

    def cut(self, event: Optional[tk.Event] = None) -> None:
        """Вырезает выделенный текст."""
        try:
            self.widget.event_generate("<<Cut>>")
        except:
            pass

    def select_all(self, event: Optional[tk.Event] = None) -> Optional[str]:
        """Выделяет весь текст."""
        try:
            self.widget.event_generate("<<SelectAll>>")
            return "break"
        except:
            pass


class InputFrame(ctk.CTkFrame):
    """
    Фрейм для динамического отображения полей ввода.

    Attributes:
        entries: Словарь {name: {widget, config}}
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.entries: Dict[str, Dict[str, Any]] = {}

    def clear(self) -> None:
        """Очищает все виджеты ввода."""
        for widget in self.winfo_children():
            widget.destroy()
        self.entries = {}

    def build_inputs(self, inputs_config: Optional[List[Dict[str, Any]]]) -> None:
        """
        Строит виджеты ввода на основе конфигурации.

        Args:
            inputs_config: Список конфигураций полей ввода
        """
        self.clear()
        if not inputs_config:
            return

        for i, conf in enumerate(inputs_config):
            self._create_input_widget(i, conf)

    def _create_input_widget(self, row: int, conf: Dict[str, Any]) -> None:
        """Создает виджет ввода (Entry или ComboBox)."""
        label = ctk.CTkLabel(self, text=conf["label"] + ":", anchor="w")
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        widget = None
        if conf["type"] == "entry":
            widget = ctk.CTkEntry(self, placeholder_text=conf.get("placeholder", ""), width=300)
            if conf.get("default"):
                widget.insert(0, conf["default"])

        elif conf["type"] == "combo":
            widget = ctk.CTkComboBox(
                self, values=conf.get("values", []), state="readonly", width=150
            )
            if conf.get("default"):
                widget.set(conf["default"])

        if widget:
            widget.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            self.entries[conf["name"]] = {"widget": widget, "config": conf}

            # Добавляем контекстное меню
            ContextMenu(widget)

    def get_args(self) -> List[str]:
        """
        Собирает аргументы командной строки на основе введенных значений.

        Returns:
            Список аргументов для передачи скрипту
        """
        dynamic_args = []
        for name, data in self.entries.items():
            widget = data["widget"]
            conf = data["config"]

            value = widget.get()
            if not value:
                continue

            # Форматирование аргумента
            fmt = conf.get("arg_format", "{value}")
            formatted = fmt.format(value=value)

            # Разбираем строку аргументов в список
            parts = formatted.split(" ")
            dynamic_args.extend(parts)

        return dynamic_args

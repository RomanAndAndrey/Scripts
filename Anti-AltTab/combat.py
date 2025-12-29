"""
Модуль Combat для блокировки Alt+Tab и управления оверлеем.
Предоставляет три режима "жестокости": блокировка ввода, черный экран,refocus игры.
"""

import threading
import time
import tkinter as tk
from typing import Any, Dict, Optional

import keyboard
import win32gui


class CombatModule:
    """
    Модуль боевого режима для предотвращения переключения из игры.

    Поддерживает три режима:
    - INPUT_BLOCK: Блокирует Alt+Tab
    - BLACK_SCREEN: Показывает черный экран поверх всех окон
    - REFOCUS: Возвращает фокус на игру

    Attributes:
        config: Конфигурация режима
        blocked: Флаг блокировки ввода
        overlay_window: Окно черного экрана (Tkinter)
        game_hwnd: Handle окна игры
        hook_handler: Handler hotkey для разблокировки
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Инициализирует модуль боя.

        Args:
            config: Словарь конфигурации с параметром cruelty_mode
        """
        self.config = config
        self.blocked: bool = False
        self.overlay_window: Optional[tk.Tk] = None
        self.game_hwnd: Optional[int] = None
        self.hook_handler: Optional[Any] = None

    def set_game_hwnd(self, hwnd: int) -> None:
        """
        Устанавливает handle окна игры.

        Args:
            hwnd: Windows handle окна игры
        """
        self.game_hwnd = hwnd

    def activate_combat_mode(self) -> None:
        """Активирует боевой режим согласно конфигурации."""
        mode = self.config.get("cruelty_mode", "INPUT_BLOCK")

        if mode == "INPUT_BLOCK":
            self._block_input()
        elif mode == "BLACK_SCREEN":
            self._show_black_screen()
        elif mode == "REFOCUS":
            self._refocus_game()

    def deactivate_combat_mode(self) -> None:
        """Деактивирует все режимы блокировки."""
        self._unblock_input()
        self._hide_black_screen()

    def _block_input(self) -> None:
        """Блокирует комбинацию Alt+Tab, оставляя клавиши активными по отдельности."""
        if not self.blocked:
            try:
                self.hook_handler = keyboard.add_hotkey("alt+tab", lambda: None, suppress=True)
                print("Combat Mode: Alt+Tab Blocked (Keys Active)")
                self.blocked = True
            except Exception as e:
                print(f"Failed to block input: {e}")

    def _unblock_input(self) -> None:
        """Разблокирует Alt+Tab."""
        if self.blocked and self.hook_handler:
            try:
                keyboard.remove_hotkey(self.hook_handler)
                print("Combat Mode: Alt+Tab Unblocked")
            except Exception as e:
                print(f"Error unblocking: {e}")
            self.blocked = False
            self.hook_handler = None

    def _refocus_game(self) -> None:
        """Возвращает фокус на окно игры."""
        if self.game_hwnd:
            try:
                win32gui.SetForegroundWindow(self.game_hwnd)
                print("Combat Mode: Refocused Game")
            except Exception as e:
                print(f"Refocus failed: {e}")

    def _show_black_screen(self) -> None:
        """Показывает полноэкранный черный оверлей."""
        if not self.overlay_window:

            def create_overlay():
                self.overlay_window = tk.Tk()
                self.overlay_window.attributes("-fullscreen", True)
                self.overlay_window.attributes("-topmost", True)
                self.overlay_window.configure(bg="black")

                label = tk.Label(
                    self.overlay_window,
                    text="ФОКУС НА ИГРЕ!",
                    font=("Arial", 48, "bold"),
                    fg="red",
                    bg="black",
                )
                label.pack(expand=True)

                self.overlay_window.mainloop()

            threading.Thread(target=create_overlay, daemon=True).start()
            time.sleep(0.1)
            print("Combat Mode: Black Screen Active")

    def _hide_black_screen(self) -> None:
        """Скрывает черный оверлей."""
        if self.overlay_window:
            try:
                self.overlay_window.destroy()
                self.overlay_window = None
                print("Combat Mode: Black Screen Removed")
            except:
                pass

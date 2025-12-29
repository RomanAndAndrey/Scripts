"""
Anti-AltTab Helper - Утилита для блокировки отвлечений во время игры.
Предотвращает случайное переключение на другие приложения через Alt+Tab.
"""

import threading
import time

import keyboard
from combat import CombatModule
from overseer import Overseer


def main() -> None:
    """
    Главная функция приложения.
    Запускает мониторинг активных окон и применяет блокировку согласно конфигурации.
    """
    # Инициализация компонентов
    overseer = Overseer()
    combat = CombatModule(overseer.config)

    # Состояние
    running: bool = True
    enabled: bool = True

    print("Anti-AltTab Helper Started.")
    print(
        f"Loaded {len(overseer.config['games'])} games and {len(overseer.config['forbidden_apps'])} forbidden apps."
    )
    print(f"Safety Key: {overseer.config['safety_key']}")
    print("Use Safety Key to toggle protection ON/OFF.")

    def toggle_safety() -> None:
        """Переключает защиту вкл/выкл по нажатию safety key."""
        nonlocal enabled
        enabled = not enabled
        status = "ENABLED" if enabled else "DISABLED"
        print(f"\n[SAFETY KEY PRESSED] Protection is now: {status}")
        if not enabled:
            combat.deactivate_combat_mode()
            combat._hide_black_screen()

    # Регистрация safety key
    try:
        keyboard.add_hotkey(overseer.config["safety_key"], toggle_safety)
    except Exception as e:
        print(f"Error registering hotkey: {e}. Try running as Admin.")

    print("Monitoring started...")

    try:
        while running:
            if enabled:
                game_active = overseer.is_game_active()
                forbidden_active = overseer.is_forbidden_app_active()
                current_hwnd = overseer.get_active_window_hwnd()

                if game_active:
                    # Мы в игре
                    combat.set_game_hwnd(current_hwnd)
                    # Активируем блокировку согласно режиму
                    if combat.config["cruelty_mode"] == "INPUT_BLOCK":
                        combat._block_input()
                    elif combat.config["cruelty_mode"] == "BLACK_SCREEN":
                        # Черный экран остается до выхода из игры
                        pass
                    elif combat.config["cruelty_mode"] == "REFOCUS":
                        # REFOCUS работает только при обнаружении запрещенного приложения
                        pass
                else:
                    # Не в игре - снимаем блокировку
                    combat.deactivate_combat_mode()

                if forbidden_active and game_active:
                    # Запрещенное приложение активно, но игра должна быть в фокусе
                    combat.activate_combat_mode()

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nShutting down...")
        combat.deactivate_combat_mode()


if __name__ == "__main__":
    main()

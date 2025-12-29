import ctypes
import json
import random
import threading
import time
import tkinter as tk
from ctypes import windll, wintypes

import pyautogui

# Константы для Windows API
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
LWA_ALPHA = 0x00000002


class DotaOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dota Coach Overlay")

        # Настройка окна: без рамок, всегда сверху, на весь экран
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")

        # Прозрачный фон
        self.bg_color = "black"  # Используем черный для прозрачности
        self.root.config(bg=self.bg_color)
        self.root.attributes("-transparentcolor", self.bg_color)
        self.root.attributes("-alpha", 0.8)  # Общая прозрачность элементов

        # Элементы интерфейса
        self.frame = tk.Frame(self.root, bg=self.bg_color)
        self.frame.pack(expand=True, fill="both")

        self.title_label = tk.Label(
            self.frame,
            text="АНАЛИЗИРУЙ ОШИБКИ",
            font=("Arial", 32, "bold"),
            fg="red",
            bg=self.bg_color,
        )
        self.title_label.pack(pady=(200, 20))

        self.tip_label = tk.Label(
            self.frame,
            text="Загрузка советов...",
            font=("Arial", 24),
            fg="white",
            bg=self.bg_color,
            wraplength=800,
        )
        self.tip_label.pack(pady=20)

        self.tips = self.load_tips()

        # Сначала скрываем оверлей
        self.is_visible = False
        self.hide_overlay()

        # Настройка click-through (пропуск кликов)
        self.set_click_through()

        # Запуск потока мониторинга
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_game, daemon=True)
        self.monitor_thread.start()

    def set_click_through(self):
        """Делает окно 'прозрачным' для кликов мыши."""
        hwnd = windll.user32.GetParent(self.root.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style | WS_EX_LAYERED | WS_EX_TRANSPARENT
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def load_tips(self):
        try:
            with open("tips.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return ["Ошибка загрузки советов: " + str(e)]

    def show_overlay(self):
        if not self.is_visible:
            self.root.deiconify()
            self.update_tip()
            self.is_visible = True
            # При показе нужно убедиться, что click-through работает, но обычно один раз достаточно
            # self.set_click_through()

    def hide_overlay(self):
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False

    def update_tip(self):
        self.tip_label.config(text=random.choice(self.tips))

    def monitor_game(self):
        """
        Фоновый процесс проверки состояния игры.
        Здесь будет логика определения 'смерти' (серый экран).
        """
        print("Monitoring started...")
        while self.running:
            try:
                # Эмуляция проверки (заглушка)
                # TODO: Реализовать проверку пикселей экрана
                is_dead = self.check_death_condition()

                if is_dead:
                    self.root.after(0, self.show_overlay)
                else:
                    self.root.after(0, self.hide_overlay)

                time.sleep(1)  # Проверка раз в секунду
            except Exception as e:
                print(f"Error in monitor: {e}")

    def check_death_condition(self):
        """
        Проверяет, мертв ли персонаж, анализируя насыщенность цветов в центре экрана.
        """
        try:
            # Захват области в центре экрана (200x200 пикселей)
            screen_width, screen_height = pyautogui.size()
            region = (screen_width // 2 - 100, screen_height // 2 - 100, 200, 200)
            # grab() возвращает PIL Image
            screenshot = pyautogui.screenshot(region=region)

            # Анализ: проверяем, является ли изображение черно-белым (серая пелена смерти)
            # Для оптимизации берем уменьшенную копию
            small_img = screenshot.resize((20, 20))
            pixels = list(small_img.getdata())

            total_saturation = 0
            for r, g, b in pixels:
                # Простая эвристика насыщенности: разница между макс и мин каналом
                # Если серый, то r ~= g ~= b, разница мала
                saturation = max(r, g, b) - min(r, g, b)
                total_saturation += saturation

            avg_saturation = total_saturation / len(pixels)

            # Порог "серости". Если средняя разница каналов меньше X, считаем что экран серый.
            # В обычной игре цвета яркие, saturation будет высоким (например > 40-50).
            # При смерти все становится серым, saturation падает (например < 15-20).
            # Нужно калибровать. Начнем с 15.
            threshold = 15

            # print(f"Current Saturation: {avg_saturation}") # Debug

            return avg_saturation < threshold

        except Exception as e:
            print(f"Error checking death: {e}")
            return False

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DotaOverlay()
    app.run()

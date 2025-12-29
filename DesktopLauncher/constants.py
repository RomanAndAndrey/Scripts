"""
Константы и настройки для Desktop Script Launcher.
Обновлено для современного premium дизайна.
"""

# Статусы скриптов
STATUS_STOPPED = "stopped"
STATUS_RUNNING = "running"
STATUS_ERROR = "error"

# Настройки лога
MAX_LOG_LINES = 1000

# Тема приложения
APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"

# Современная цветовая палитра (Premium Dark Theme)
COLORS = {
    # Основные фоны
    "bg_primary": "#0d1117",  # Главный фон
    "bg_secondary": "#161b22",  # Сайдбар
    "bg_card": "#1c2128",  # Карточки/элементы
    "bg_header": "linear-gradient",  # Градиент для header
    # Статусы (яркие неоновые)
    "running": "#10b981",  # Зеленый - запущен
    "stopped": "#6b7280",  # Серый - остановлен
    "error": "#ef4444",  # Красный - ошибка
    # Акцентные цвета (градиентные)
    "accent_blue": "#3b82f6",  # Bright Blue
    "accent_purple": "#8b5cf6",  # Purple
    "accent_cyan": "#06b6d4",  # Cyan
    # Кнопки
    "button_success": "#10b981",  # Зеленая (Запустить)
    "button_success_hover": "#059669",
    "button_danger": "#ef4444",  # Красная (Остановить)
    "button_danger_hover": "#dc2626",
    # Текст
    "text_primary": "#f0f6fc",  # Основной
    "text_secondary": "#8b949e",  # Вторичный
    "text_muted": "#6e7681",  # Приглушенный
    # Границы
    "border": "#30363d",
    "border_hover": "#484f58",
    "border_active": "#3b82f6",  # Синяя при фокусе
}

# Шрифты (современные)
FONTS = {
    "title": ("Segoe UI", 22, "bold"),
    "header": ("Segoe UI Semibold", 16),
    "body": ("Segoe UI", 12),
    "code": ("Cascadia Code", 11),  # Моноширинный шрифт
    "small": ("Segoe UI", 10),
}

# Размеры и отступы
SIZES = {
    "sidebar_width": 260,
    "header_height": 90,
    "button_height": 44,
    "corner_radius": 14,  # Увеличенные скругления
    "border_width": 2,
    "indicator_size": 14,  # Размер статусного индикатора
}

# Emoji иконки для скриптов (опционально)
SCRIPT_ICONS = {
    "Anti-AltTab": "🎮",
    "Организатор Файлов": "📁",
    "Dota Coach": "🎯",
    "Context Overlay": "🎤",
    "YouTube Downloader": "📹",
    "Code to Slides": "📊",
    "Тестовый Пинг": "🔧",
}

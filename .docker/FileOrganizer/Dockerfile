FROM python:3.14-slim

LABEL maintainer="RomanAndAndrey"
LABEL description="FileOrganizer - автоматическая сортировка файлов"

WORKDIR /app

# Установка зависимостей
COPY FileOrganizer/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY common/ ./common/
COPY FileOrganizer/ ./FileOrganizer/

# Переменные окружения
ENV DOWNLOADS_PATH=/downloads \
    LOG_LEVEL=INFO \
    PYTHONUNBUFFERED=1

# Volume для папки Downloads
VOLUME ["/downloads"]

# Рабочая директория для запуска
WORKDIR /app/FileOrganizer

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Запуск
CMD ["python", "-u", "organizer.py"]

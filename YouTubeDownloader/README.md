# YouTube Downloader

Консольная утилита для скачивания видео и аудио с YouTube с использованием yt-dlp. Поддерживает выбор качества, плейлисты и обход ограничений через cookies браузера.

## Возможности

- ✅ **Скачивание видео** - выбор качества от 480p до 4K
- ✅ **Скачивание аудио** - автоконвертация в MP3
- ✅ **Поддержка плейлистов** - загрузка всех видео из плейлиста
- ✅ **Cookies из браузера** - обход возрастных ограничений и региональных блокировок
- ✅ **Прогресс в реальном времени** - отображение скорости и ETA
- ✅ **Автослияние потоков** - видео + аудио = готовый MP4

## Требования

### Обязательные зависимости:
```bash
pip install -r requirements.txt
```
- yt-dlp
- colorama

### FFmpeg (обязательно!):
FFmpeg необходим для слияния видео/аудио и конвертации.

**Windows:**
1. Скачайте FFmpeg: https://ffmpeg.org/download.html
2. Распакуйте в `C:\ffmpeg`
3. Добавьте `C:\ffmpeg\bin` в PATH

**Linux/macOS:**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS (Homebrew)
brew install ffmpeg
```

## Установка

```bash
# Клонируйте или скачайте проект
cd YouTubeDownloader

# Установите зависимости
pip install -r requirements.txt

# Проверьте ffmpeg
ffmpeg -version
```

## Использование

### Базовые примеры

**Скачать видео (1080p):**
```bash
python yt_load.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Скачать видео в 720p:**
```bash
python yt_load.py "https://www.youtube.com/watch?v=VIDEO_ID" --type video --quality 720p
```

**Скачать только аудио (MP3):**
```bash
python yt_load.py "https://www.youtube.com/watch?v=VIDEO_ID" --type audio
```

**Скачать плейлист:**
```bash
python yt_load.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" --type video
```

**Использовать cookies из Chrome (для ограниченного контента):**
```bash
python yt_load.py "https://www.youtube.com/watch?v=VIDEO_ID" --browser chrome
```

### Параметры

```bash
python yt_load.py <URL> [опции]
```

**Позиционные аргументы:**
- `url` - URL видео или плейлиста YouTube

**Опциональные аргументы:**
- `--type {video,audio}` - Тип загрузки (по умолчанию: video)
- `--quality {2160p,1440p,1080p,720p,480p}` - Качество видео (по умолчанию: 1080p)
- `--output FOLDER` - Папка для сохранения (по умолчанию: ./Downloads)
- `--browser {none,chrome,firefox,opera,edge,vivaldi}` - Браузер для cookies (по умолчанию: none)

## Примеры сценариев

### 1. Скачать музыкальный альбом в MP3

```bash
python yt_load.py "https://www.youtube.com/playlist?list=PLxxx" \
    --type audio \
    --output "./Music/MyAlbum"
```

### 2. Скачать 4K видео

```bash
python yt_load.py "https://www.youtube.com/watch?v=xxx" \
    --quality 2160p \
    --output "./Videos/4K"
```

### 3. Скачать возрастно-ограниченное видео

```bash
# Сначала войдите в YouTube в Chrome
python yt_load.py "https://www.youtube.com/watch?v=xxx" \
    --browser chrome
```

### 4. Массовая загрузка курса

```bash
python yt_load.py "https://www.youtube.com/playlist?list=COURSE_ID" \
    --quality 720p \
    --output "./Courses/Python101"
```

## Структура проекта

```
YouTubeDownloader/
├── yt_load.py          # Главный скрипт
├── requirements.txt    # Зависимости
├── Downloads/          # Папка загрузок (создается автоматически)
└── README.md
```

## Классы и функции

### `class Downloader`
Основной класс для загрузки.

**Методы:**
- `download_video(url, quality, browser)` - Скачивает видео
- `download_audio(url, browser)` - Скачивает аудио в MP3
- `progress_hook(d)` - Callback для отображения прогресса

### `main()`
Парсит аргументы командной строки и запускает загрузку.

## Форматы и качество

### Видео:
- **2160p (4K)** - Максимальное качество
- **1440p (2K)** - Высокое качество
- **1080p (Full HD)** - По умолчанию, оптимальный баланс
- **720p (HD)** - Среднее качество
- **480p (SD)** - Низкое качество

### Аудио:
- Формат: MP3
- Битрейт: 192 kbps
- Берется лучший доступный аудиопоток

## Cookies из браузера

Cookies помогают обойти:
- Возрастные ограничения (18+)
- Региональные блокировки
- Ограничения для незарегистрированных пользователей

**Поддерживаемые браузеры:**
- Chrome
- Firefox
- Opera
- Edge
- Vivaldi

**Примечание:** Вы должны быть авторизованы в YouTube в выбранном браузере.

## Устранение проблем

### "ffmpeg не найден"
**Решение:**
1. Установите FFmpeg (см. раздел Требования)
2. Добавьте FFmpeg в PATH
3. Перезапустите терминал

### "HTTP Error 429: Too Many Requests"
**Решение:**
- Подождите несколько минут
- Используйте `--browser chrome` для авторизации

### "This video is not available"
**Решение:**
- Проверьте доступность видео в браузере
- Используйте cookies через `--browser`
- Видео может быть удалено или заблокировано в вашей стране

### Медленная загрузка
**Решение:**
- Попробуйте другое время суток
- Используйте более низкое качество
- Проверьте скорость интернета

### Для плейлиста скачивается только одно видео
**Решение:**
- Убедитесь, что URL содержит `?list=` часть
- Проверьте, что плейлист публичный

## Продвинутое использование

### Скачать субтитры
Нужно модифицировать опции yt-dlp:
```python
opts.update({
    'writesubtitles': True,
    'subtitleslangs': ['ru', 'en'],
})
```

### Ограничить скорость загрузки
```python
opts.update({
    'ratelimit': 1000000,  # 1 MB/s
})
```

### Пропустить уже скачанные видео
```python
opts.update({
    'download_archive': 'downloaded.txt',
})
```

## Ограничения

- Не поддерживает загрузку платного контента
- Не может обойти DRM защиту
- Требует стабильного интернет-соединения
- FFmpeg обязателен для конвертации

## Лицензия

Используйте ответственно. Соблюдайте авторские права.

## Автор

Создано для личного использования и обучения

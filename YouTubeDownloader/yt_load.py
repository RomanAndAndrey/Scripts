"""
YouTube Downloader - Утилита для загрузки видео и аудио с YouTube через yt-dlp.
"""

import argparse
import os
import shutil
import sys
from typing import Any, Dict, Optional

import yt_dlp
from colorama import Fore, Style, init

# Инициализация colorama для красивого вывода в Windows
init(autoreset=True)


def check_ffmpeg() -> bool:
    """
    Проверяет наличие FFmpeg в системе.

    Returns:
        True если FFmpeg найден, False в противном случае
    """
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        print(f"{Fore.RED}╔════════════════════════════════════════════════════════╗")
        print(f"{Fore.RED}║  [ERROR] FFmpeg не найден в системе!                   ║")
        print(f"{Fore.RED}╚════════════════════════════════════════════════════════╝")
        print(f"\n{Fore.YELLOW}FFmpeg требуется для объединения видео/аудио и конвертации.")
        print(f"\n{Fore.CYAN}Установите FFmpeg:")
        print(f"{Fore.GREEN}  → Windows: https://ffmpeg.org/download.html")
        print(f"{Fore.GREEN}  → Linux:   sudo apt install ffmpeg")
        print(f"{Fore.GREEN}  → macOS:   brew install ffmpeg")
        print(f"\n{Fore.YELLOW}После установки добавьте FFmpeg в PATH и перезапустите скрипт.\n")
        return False

    print(f"{Fore.GREEN}✓ FFmpeg найден: {ffmpeg_path}")
    return True


class Downloader:
    """
    Класс для скачивания видео и аудио с YouTube.

    Attributes:
        download_folder: Папка для сохранения загрузок
    """

    def __init__(self, download_folder: str = "./Downloads"):
        """
        Инициализирует загрузчик.

        Args:
            download_folder: Путь к папке для загрузок
        """
        self.download_folder = download_folder
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

    def _get_common_opts(self, browser: Optional[str] = None) -> Dict[str, Any]:
        """
        Возвращает общие настройки для yt-dlp.

        Args:
            browser: Имя браузера для извлечения cookies (chrome, firefox, etc.)

        Returns:
            Словарь опций для yt-dlp
        """
        opts: Dict[str, Any] = {
            "outtmpl": os.path.join(self.download_folder, "%(title)s.%(ext)s"),
            "ignoreerrors": True,
            "no_warnings": True,
            "progress_hooks": [self.progress_hook],
            "quiet": False,
            "ffmpeg_location": None,
            "nocheckcertificate": True,
        }

        if browser and browser.lower() != "none":
            opts["cookiesfrombrowser"] = (browser,)

        return opts

    def progress_hook(self, d: Dict[str, Any]) -> None:
        """
        Callback для отображения прогресса загрузки.

        Args:
            d: Словарь с информацией о прогрессе от yt-dlp
        """
        if d["status"] == "downloading":
            p = d.get("_percent_str", "N/A")
            s = d.get("_speed_str", "N/A")
            eta = d.get("_eta_str", "N/A")
            sys.stdout.write(f"\r{Fore.CYAN}[download] {p} at {s} ETA {eta}    ")
            sys.stdout.flush()
        elif d["status"] == "finished":
            sys.stdout.write(f"\n{Fore.GREEN}[done] Загрузка завершена: {d['filename']}\n")
            sys.stdout.flush()

    def download_video(
        self, url: str, quality: str = "1080p", browser: Optional[str] = None
    ) -> None:
        """
        Скачивает видео с объединением видео и аудио потоков.

        Args:
            url: URL видео или плейлиста
            quality: Качество видео (например, "1080p", "720p")
            browser: Браузер для cookies
        """
        print(f"{Fore.YELLOW}[Info] Загрузка видео: {url} (Качество: {quality})")

        if quality.endswith("p"):
            height = quality[:-1]
        else:
            height = quality

        format_str = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"

        opts = self._get_common_opts(browser)
        opts.update(
            {
                "format": format_str,
                "merge_output_format": "mp4",
            }
        )

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"{Fore.RED}[Error] Ошибка при скачивании видео: {e}")

    def download_audio(self, url: str, browser: Optional[str] = None) -> None:
        """
        Скачивает только аудио и конвертирует в MP3.

        Args:
            url: URL видео или плейлиста
            browser: Браузер для cookies
        """
        print(f"{Fore.YELLOW}[Info] Загрузка аудио: {url}")

        opts = self._get_common_opts(browser)
        opts.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"{Fore.RED}[Error] Ошибка при скачивании аудио: {e}")


def main() -> None:
    """Главная функция с парсингом аргументов."""
    # Проверка наличия FFmpeg
    if not check_ffmpeg():
        print(f"{Fore.RED}Скрипт не может работать без FFmpeg. Выход.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="YouTube Downloader (yt-dlp)")
    parser.add_argument("url", type=str, help="URL видео или плейлиста YouTube")
    parser.add_argument(
        "--type",
        type=str,
        choices=["video", "audio"],
        default="video",
        help="Тип загрузки: video или audio",
    )
    parser.add_argument(
        "--quality",
        type=str,
        default="1080p",
        help="Качество видео (только для video): 2160p, 1440p, 1080p, 720p, 480p",
    )
    parser.add_argument("--output", type=str, default="./Downloads", help="Папка для сохранения")
    parser.add_argument(
        "--browser",
        type=str,
        default="none",
        choices=["none", "chrome", "firefox", "opera", "edge", "vivaldi"],
        help="Браузер для извлечения cookies (для обхода ограничений)",
    )

    args = parser.parse_args()

    downloader = Downloader(download_folder=args.output)

    browser_arg: Optional[str] = None if args.browser == "none" else args.browser

    if args.type == "video":
        downloader.download_video(args.url, quality=args.quality, browser=browser_arg)
    else:
        downloader.download_audio(args.url, browser=browser_arg)

    print(f"{Fore.GREEN}\n✓ Готово!")


if __name__ == "__main__":
    main()

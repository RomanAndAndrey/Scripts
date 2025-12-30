"""
Updater - автономная утилита для замены .exe файлов.

Запускается основным приложением для обновления самого себя.
"""

import argparse
import os
import shutil
import sys
import time
from pathlib import Path


def wait_for_process(pid: int, timeout: int = 30):
    """
    Ждет завершения процесса.

    Args:
        pid: ID процесса
        timeout: Максимальное время ожидания в секундах
    """
    print(f"Waiting for process {pid} to exit...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # Проверяем существование процесса
            if sys.platform == "win32":
                import ctypes

                kernel32 = ctypes.windll.kernel32
                PROCESS_QUERY_INFORMATION = 0x0400
                handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)

                if handle == 0:
                    # Процесс не существует
                    print(f"Process {pid} has exited")
                    return True

                kernel32.CloseHandle(handle)
            else:
                os.kill(pid, 0)  # На Unix это просто проверка

        except (OSError, Exception):
            # Процесс завершился
            print(f"Process {pid} has exited")
            return True

        time.sleep(0.5)

    print(f"Timeout waiting for process {pid}")
    return False


def replace_file(source: Path, target: Path) -> bool:
    """
    Заменяет целевой файл на новый.

    Args:
        source: Путь к новому файлу
        target: Путь к файлу для замены

    Returns:
        True если успешно
    """
    try:
        print(f"Replacing {target} with {source}")

        # Создаем бэкап
        backup = target.with_suffix(target.suffix + ".bak")
        if target.exists():
            print(f"Creating backup: {backup}")
            shutil.copy2(target, backup)

        # Заменяем файл
        print(f"Copying {source} to {target}")
        shutil.copy2(source, target)

        print("✅ File replaced successfully")
        return True

    except Exception as e:
        print(f"❌ Error replacing file: {e}")

        # Восстанавливаем из бэкапа
        if backup.exists():
            print(f"Restoring from backup...")
            try:
                shutil.copy2(backup, target)
                print("Backup restored")
            except Exception as restore_error:
                print(f"Failed to restore backup: {restore_error}")

        return False


def launch_application(app_path: Path) -> bool:
    """
    Запускает обновленное приложение.

    Args:
        app_path: Путь к приложению

    Returns:
        True если успешно запущено
    """
    try:
        print(f"Launching {app_path}")

        if sys.platform == "win32":
            import subprocess

            subprocess.Popen(
                [str(app_path)],
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
            )
        else:
            os.execv(str(app_path), [str(app_path)])

        return True

    except Exception as e:
        print(f"❌ Error launching app: {e}")
        return False


def cleanup(source: Path, backup: Path):
    """
    Очистка временных файлов.

    Args:
        source: Временный файл источника
        backup: Файл бэкапа
    """
    try:
        if source.exists():
            print(f"Removing temporary file: {source}")
            source.unlink()

        if backup.exists():
            print(f"Removing backup: {backup}")
            backup.unlink()

    except Exception as e:
        print(f"Warning: cleanup error: {e}")


def main():
    """Главная функция updater."""
    parser = argparse.ArgumentParser(description="Rutina Application Updater")
    parser.add_argument("--source", required=True, type=str, help="Path to new .exe file")
    parser.add_argument("--target", required=True, type=str, help="Path to file to replace")
    parser.add_argument(
        "--wait-process",
        type=int,
        help="Wait for this process ID to exit before updating",
    )
    parser.add_argument("--no-launch", action="store_true", help="Don't launch app after update")

    args = parser.parse_args()

    source = Path(args.source)
    target = Path(args.target)

    print("=" * 60)
    print("Rutina Application Updater")
    print("=" * 60)
    print(f"Source: {source}")
    print(f"Target: {target}")
    print("")

    # Проверяем файлы
    if not source.exists():
        print(f"❌ Source file not found: {source}")
        sys.exit(1)

    if not target.exists():
        print(f"❌ Target file not found: {target}")
        sys.exit(1)

    # Ждем завершения процесса
    if args.wait_process:
        if not wait_for_process(args.wait_process):
            print("⚠️  Process didn't exit, continuing anyway...")
            time.sleep(2)  # Дополнительная пауза

    # Заменяем файл
    backup = target.with_suffix(target.suffix + ".bak")
    success = replace_file(source, target)

    if not success:
        print("❌ Update failed!")
        input("Press Enter to exit...")
        sys.exit(1)

    # Запускаем приложение
    if not args.no_launch:
        if launch_application(target):
            print("✅ Application launched")
        else:
            print("⚠️  Failed to launch application")

    # Очистка
    cleanup(source, backup)

    print("")
    print("✅ Update completed successfully!")
    print("Updater will exit in 3 seconds...")
    time.sleep(3)


if __name__ == "__main__":
    main()

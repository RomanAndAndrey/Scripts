"""
Script для управления версиями проекта (Semantic Versioning).

Использование:
    python scripts/bump_version.py major  # 1.0.0 -> 2.0.0
    python scripts/bump_version.py minor  # 1.0.0 -> 1.1.0
    python scripts/bump_version.py patch  # 1.0.0 -> 1.0.1
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Получает корень проекта."""
    return Path(__file__).parent.parent


def read_version() -> str:
    """Читает текущую версию из VERSION файла."""
    version_file = get_project_root() / "VERSION"
    if not version_file.exists():
        print("❌ VERSION файл не найден!")
        sys.exit(1)
    return version_file.read_text().strip()


def write_version(version: str) -> None:
    """Записывает новую версию в VERSION файл."""
    version_file = get_project_root() / "VERSION"
    version_file.write_text(version)
    print(f"✅ VERSION обновлен: {version}")


def parse_version(version: str) -> tuple[int, int, int]:
    """Парсит версию в формате major.minor.patch."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version)
    if not match:
        print(f"❌ Неверный формат версии: {version}")
        sys.exit(1)
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def bump_version(current: str, bump_type: str) -> str:
    """
    Увеличивает версию согласно типу.

    Args:
        current: Текущая версия (например "1.2.3")
        bump_type: Тип увеличения (major/minor/patch)

    Returns:
        Новая версия
    """
    major, minor, patch = parse_version(current)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        print(f"❌ Неверный тип: {bump_type}. Используйте major/minor/patch")
        sys.exit(1)


def create_git_tag(version: str, message: str = None) -> None:
    """Создает git tag для версии."""
    tag_name = f"v{version}"

    if message is None:
        message = f"Release {version}"

    try:
        # Проверяем есть ли несохраненные изменения
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        )

        if result.stdout.strip():
            print("⚠️  Есть несохраненные изменения. Сначала закоммитьте их:")
            print(result.stdout)
            sys.exit(1)

        # Создаем тег
        subprocess.run(["git", "tag", "-a", tag_name, "-m", message], check=True)
        print(f"✅ Git tag создан: {tag_name}")
        print(f"\n💡 Для публикации выполните: git push origin {tag_name}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка создания git tag: {e}")
        sys.exit(1)


def main():
    """Главная функция."""
    parser = argparse.ArgumentParser(
        description="Управление версиями проекта (Semantic Versioning)"
    )
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Тип увеличения версии",
    )
    parser.add_argument(
        "--no-tag",
        action="store_true",
        help="Не создавать git tag",
    )
    parser.add_argument(
        "--message",
        "-m",
        help="Сообщение для git tag",
    )

    args = parser.parse_args()

    # Читаем текущую версию
    current_version = read_version()
    print(f"📌 Текущая версия: {current_version}")

    # Увеличиваем версию
    new_version = bump_version(current_version, args.bump_type)
    print(f"🚀 Новая версия: {new_version}")

    # Записываем новую версию
    write_version(new_version)

    # Создаем git tag если нужно
    if not args.no_tag:
        create_git_tag(new_version, args.message)
    else:
        print("⚠️  Git tag не создан (--no-tag)")

    print("\n✨ Готово!")
    print(f"\nСледующие шаги:")
    print(f"1. Обновите CHANGELOG.md")
    print(f"2. git add VERSION CHANGELOG.md")
    print(f"3. git commit -m 'chore: bump version to {new_version}'")
    if not args.no_tag:
        print(f"4. git push origin v{new_version}")


if __name__ == "__main__":
    main()

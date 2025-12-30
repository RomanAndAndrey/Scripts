"""
Генератор changelog из git commits.

Автоматически создает секции changelog на основе conventional commits.

Использование:
    python scripts/generate_changelog.py --from v1.0.0 --to HEAD
    python scripts/generate_changelog.py --latest  # Последний тег
"""

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def get_project_root() -> Path:
    """Получает корень проекта."""
    return Path(__file__).parent.parent


def run_git_command(cmd: List[str]) -> str:
    """Выполняет git команду и возвращает результат."""
    try:
        result = subprocess.run(
            ["git"] + cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=get_project_root(),
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка git: {e}")
        sys.exit(1)


def get_latest_tag() -> str:
    """Получает последний git tag."""
    tags = run_git_command(["tag", "--sort=-v:refname"])
    if not tags:
        print("⚠️  Теги не найдены!")
        return None
    return tags.split("\n")[0]


def get_commits(from_ref: str, to_ref: str = "HEAD") -> List[Dict[str, str]]:
    """
    Получает список коммитов между двумя ссылками.

    Args:
        from_ref: Начальная ссылка (тег/коммит)
        to_ref: Конечная ссылка (по умолчанию HEAD)

    Returns:
        Список словарей с информацией о коммитах
    """
    # Формат: hash|subject|author|date
    git_log = run_git_command(["log", f"{from_ref}..{to_ref}", "--pretty=format:%H|%s|%an|%aI"])

    if not git_log:
        print("⚠️  Новых коммитов не найдено")
        return []

    commits = []
    for line in git_log.split("\n"):
        hash_val, subject, author, date = line.split("|", 3)
        commits.append({"hash": hash_val[:7], "subject": subject, "author": author, "date": date})

    return commits


def parse_commit_type(subject: str) -> tuple[str, str]:
    """
    Парсит тип коммита из conventional commit.

    Примеры:
        feat: Add new feature -> ("feat", "Add new feature")
        fix(api): Fix bug -> ("fix", "Fix bug")
        docs: Update README -> ("docs", "Update README")

    Args:
        subject: Строка subject коммита

    Returns:
        Кортеж (тип, описание)
    """
    # Паттерн: type(scope?): description
    pattern = r"^(\w+)(?:\([^)]+\))?: (.+)$"
    match = re.match(pattern, subject)

    if match:
        return match.group(1), match.group(2)
    else:
        return "other", subject


def group_commits_by_type(commits: List[Dict]) -> Dict[str, List[Dict]]:
    """Группирует коммиты по типам."""
    grouped = defaultdict(list)

    for commit in commits:
        commit_type, description = parse_commit_type(commit["subject"])
        commit["type"] = commit_type
        commit["description"] = description
        grouped[commit_type].append(commit)

    return dict(grouped)


def format_changelog_section(
    version: str, date: str, grouped_commits: Dict[str, List[Dict]]
) -> str:
    """
    Форматирует секцию changelog.

    Args:
        version: Версия релиза
        date: Дата релиза
        grouped_commits: Коммиты сгруппированные по типам

    Returns:
        Отформатированная секция changelog
    """
    # Маппинг типов на секции
    type_mapping = {
        "feat": "Added",
        "fix": "Fixed",
        "docs": "Documentation",
        "style": "Changed",
        "refactor": "Changed",
        "perf": "Performance",
        "test": "Tests",
        "chore": "Maintenance",
        "ci": "CI/CD",
        "build": "Build",
    }

    lines = [f"## [{version}] - {date}", ""]

    # Сортируем типы по важности
    priority_order = ["feat", "fix", "perf", "docs", "refactor", "test", "chore", "ci"]

    for commit_type in priority_order:
        if commit_type not in grouped_commits:
            continue

        section_name = type_mapping.get(commit_type, "Other")
        lines.append(f"### {section_name}")
        lines.append("")

        for commit in grouped_commits[commit_type]:
            # Формат: - Description (hash)
            lines.append(f"- {commit['description']} (`{commit['hash']}`)")

        lines.append("")

    # Добавляем остальные типы
    for commit_type, commits_list in grouped_commits.items():
        if commit_type in priority_order:
            continue

        section_name = type_mapping.get(commit_type, "Other")
        lines.append(f"### {section_name}")
        lines.append("")

        for commit in commits_list:
            lines.append(f"- {commit['description']} (`{commit['hash']}`)")

        lines.append("")

    return "\n".join(lines)


def update_changelog(new_section: str) -> None:
    """Обновляет CHANGELOG.md, добавляя новую секцию."""
    changelog_path = get_project_root() / "CHANGELOG.md"

    if not changelog_path.exists():
        print("⚠️  CHANGELOG.md не найден, создаю новый...")
        content = "# Changelog\n\n" + new_section
    else:
        with open(changelog_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Вставляем новую секцию после заголовка и [Unreleased]
        # Ищем первую секцию версии (## [x.x.x])
        pattern = r"(## \[[Uu]nreleased\].*?\n\n)"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            # Вставляем после [Unreleased]
            insert_pos = match.end()
            content = content[:insert_pos] + new_section + "\n\n" + content[insert_pos:]
        else:
            # Если нет [Unreleased], вставляем после # Changelog
            content = content.replace("# Changelog\n\n", f"# Changelog\n\n{new_section}\n\n")

    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ CHANGELOG.md обновлен!")


def main():
    """Главная функция."""
    parser = argparse.ArgumentParser(description="Генератор changelog из git commits")
    parser.add_argument("--from", dest="from_ref", help="Начальная ссылка (тег/коммит)")
    parser.add_argument(
        "--to", dest="to_ref", default="HEAD", help="Конечная ссылка (по умолчанию HEAD)"
    )
    parser.add_argument("--latest", action="store_true", help="Использовать последний тег как from")
    parser.add_argument("--version", help="Версия для секции (по умолчанию из VERSION)")
    parser.add_argument("--dry-run", action="store_true", help="Только вывести, не сохранять")

    args = parser.parse_args()

    # Определяем from_ref
    if args.latest:
        from_ref = get_latest_tag()
        if not from_ref:
            print("❌ Последний тег не найден!")
            sys.exit(1)
        print(f"📌 Использую последний тег: {from_ref}")
    elif args.from_ref:
        from_ref = args.from_ref
    else:
        print("❌ Укажите --from или --latest")
        parser.print_help()
        sys.exit(1)

    # Получаем коммиты
    print(f"🔍 Получаю коммиты {from_ref}..{args.to_ref}")
    commits = get_commits(from_ref, args.to_ref)

    if not commits:
        print("⚠️  Нечего добавлять в changelog")
        sys.exit(0)

    print(f"📝 Найдено коммитов: {len(commits)}")

    # Группируем по типам
    grouped = group_commits_by_type(commits)

    # Определяем версию
    if args.version:
        version = args.version
    else:
        version_file = get_project_root() / "VERSION"
        version = version_file.read_text().strip() if version_file.exists() else "Unreleased"

    # Формат даты
    date = datetime.now().strftime("%Y-%m-%d")

    # Генерируем секцию
    changelog_section = format_changelog_section(version, date, grouped)

    # Выводим результат
    print("\n" + "=" * 60)
    print(changelog_section)
    print("=" * 60)

    # Сохраняем или dry-run
    if args.dry_run:
        print("\n🔍 Dry-run mode - изменения не сохранены")
    else:
        update_changelog(changelog_section)
        print("\n✨ Готово!")
        print("\nСледующие шаги:")
        print("1. Проверьте CHANGELOG.md")
        print("2. git add CHANGELOG.md")
        print(f"3. git commit -m 'docs: update changelog for {version}'")


if __name__ == "__main__":
    main()

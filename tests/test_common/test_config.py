"""
Тесты для common.config
"""

from pathlib import Path

import pytest

from common.config import load_json_config, merge_configs, save_json_config
from common.exceptions import ConfigError


def test_load_json_config(tmp_path):
    """Тест загрузки JSON конфигурации."""
    config_path = tmp_path / "config.json"
    config_path.write_text('{"name": "test", "value": 42}', encoding="utf-8")

    config = load_json_config(config_path)

    assert config["name"] == "test"
    assert config["value"] == 42


def test_load_json_config_with_defaults(tmp_path):
    """Тест загрузки с defaults."""
    config_path = tmp_path / "config.json"
    config_path.write_text('{"name": "test"}', encoding="utf-8")

    defaults = {"name": "default", "value": 0}
    config = load_json_config(config_path, defaults=defaults)

    assert config["name"] == "test"  # Из файла
    assert config["value"] == 0  # Из defaults


def test_load_json_config_create_if_missing(tmp_path):
    """Тест создания конфигурации если отсутствует."""
    config_path = tmp_path / "config.json"
    defaults = {"debug": False}

    config = load_json_config(config_path, defaults=defaults, create_if_missing=True)

    assert config_path.exists()
    assert config["debug"] == False


def test_load_json_config_missing_raises_error(tmp_path):
    """Тест что выбрасывается ошибка если файл отсутствует."""
    config_path = tmp_path / "missing.json"

    with pytest.raises(ConfigError):
        load_json_config(config_path)


def test_save_json_config(tmp_path):
    """Тест сохранения конфигурации."""
    config_path = tmp_path / "save_test.json"
    config = {"key": "value", "number": 123}

    save_json_config(config_path, config)

    assert config_path.exists()
    loaded = load_json_config(config_path)
    assert loaded == config


def test_merge_configs():
    """Тест слияния конфигураций."""
    base = {"a": 1, "b": {"c": 2, "d": 3}}
    override = {"b": {"d": 4, "e": 5}, "f": 6}

    result = merge_configs(base, override)

    assert result["a"] == 1
    assert result["b"]["c"] == 2  # Из base
    assert result["b"]["d"] == 4  # Из override
    assert result["b"]["e"] == 5  # Из override
    assert result["f"] == 6

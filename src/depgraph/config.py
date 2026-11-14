"""Чтение и проверка конфигурации из CSV-файла (этап 1).

Формат файла: каждая строка — ``ключ,значение``. Пустые строки
и строки, начинающиеся с `#`, пропускаются. Обязательные ключи:
package, repo, test_mode, image.
"""

import csv
import os

REQUIRED_KEYS = ("package", "repo", "test_mode", "image")


class ConfigError(Exception):
    """Ошибка в параметрах запуска."""


def parse_flag(value):
    """Превратить строку в логическое значение флага."""
    text = value.strip().lower()
    if text in ("1", "true", "on", "yes"):
        return True
    if text in ("0", "false", "off", "no"):
        return False
    raise ConfigError("флаг должен быть on/off, true/false или 1/0")


def load_csv_config(path):
    """Прочитать CSV-файл настроек в словарь строк."""
    if not os.path.isfile(path):
        raise ConfigError("файл конфигурации не найден: %s" % path)
    settings = {}
    with open(path, encoding="utf-8", newline="") as handle:
        for row in csv.reader(handle):
            if not row:
                continue
            key = row[0].strip()
            if not key or key.startswith("#"):
                continue
            if len(row) < 2:
                raise ConfigError("строка без значения: %s" % key)
            if key not in REQUIRED_KEYS and key not in settings:
                raise ConfigError("неизвестный параметр: %s" % key)
            settings[key] = row[1].strip()
    return settings


def check_package(value):
    """Проверить имя пакета: не должно быть пустым."""
    if not value or not value.strip():
        raise ConfigError("имя пакета не должно быть пустым")
    return value.strip()


def check_repo(value):
    """Проверить адрес репозитория: URL или существующий файл."""
    text = (value or "").strip()
    if text.startswith("http://") or text.startswith("https://"):
        return text
    if text and os.path.isfile(text):
        return text
    raise ConfigError("repo должен быть URL или существующим файлом")


def check_image(value):
    """Проверить имя файла изображения: не должно быть пустым."""
    if not value or not value.strip():
        raise ConfigError("имя файла изображения не должно быть пустым")
    return value.strip()


def validate(raw):
    """Проверить все параметры, вернуть словарь настроек."""
    for key in REQUIRED_KEYS:
        if key not in raw:
            raise ConfigError("нет обязательного параметра: %s" % key)
    return {
        "package": check_package(raw["package"]),
        "repo": check_repo(raw["repo"]),
        "test_mode": parse_flag(raw["test_mode"]),
        "image": check_image(raw["image"]),
    }


def format_params(settings):
    """Отформатировать настройки строками ключ-значение."""
    lines = []
    for key in REQUIRED_KEYS:
        lines.append("%s=%s" % (key, settings[key]))
    return "\n".join(lines)


def load_settings(config_path):
    """Прочитать и проверить конфигурацию из CSV-файла."""
    return validate(load_csv_config(config_path))

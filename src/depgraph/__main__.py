"""Запуск пакета из командной строки."""

import argparse

from depgraph.cargo import direct_dependencies
from depgraph.config import ConfigError, format_params, load_settings


def build_parser():
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализация графа зависимостей Cargo")
    parser.add_argument("--config", required=True,
                        help="путь к CSV-файлу настроек")
    return parser


def main(argv=None):
    """Точка входа: настройки, затем прямые зависимости (этап 2)."""
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings(args.config)
    except ConfigError as err:
        print("ошибка: %s" % err)
        return 2
    print(format_params(settings))
    try:
        deps = direct_dependencies(settings["package"],
                                   settings["repo"])
    except Exception as err:  # сеть недоступна: честно сообщаем
        print("ошибка: %s" % err)
        return 1
    print("dependencies:")
    for name in deps:
        print("  " + name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

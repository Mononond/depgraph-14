"""Запуск пакета из командной строки."""

import argparse

from depgraph.config import ConfigError, format_params, load_settings


def build_parser():
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализация графа зависимостей Cargo")
    parser.add_argument("--config", required=True,
                        help="путь к CSV-файлу настроек")
    return parser


def main(argv=None):
    """Точка входа: прочитать CSV и вывести параметры (этап 1)."""
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings(args.config)
    except ConfigError as err:
        print("ошибка: %s" % err)
        return 2
    print(format_params(settings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

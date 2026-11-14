"""Запуск пакета из командной строки."""

import argparse
import os

from depgraph.cargo import direct_dependencies
from depgraph.config import ConfigError, format_params, load_settings
from depgraph.graph import dfs_iterative, load_test_repo


def build_parser():
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализация графа зависимостей Cargo")
    parser.add_argument("--config", required=True,
                        help="путь к CSV-файлу настроек")
    return parser


def print_test_graph(settings):
    """Построить и вывести граф из тестового файла (этапы 3-5)."""
    from depgraph.order import load_order
    if not settings["test_mode"] or not os.path.isfile(
            settings["repo"]):
        return None
    graph = load_test_repo(settings["repo"])
    get_deps = graph.get
    order, cycles = dfs_iterative(settings["package"], get_deps)
    print("graph order:")
    for name in order:
        print("  " + name)
    if cycles:
        print("cycles:")
        for found in cycles:
            print("  " + " -> ".join(found))
    print("load order:")
    for name in load_order(settings["package"], get_deps):
        print("  " + name)
    return 0


def main(argv=None):
    """Точка входа: настройки, затем зависимости (этапы 2-3)."""
    args = build_parser().parse_args(argv)
    try:
        settings = load_settings(args.config)
    except ConfigError as err:
        print("ошибка: %s" % err)
        return 2
    print(format_params(settings))
    if print_test_graph(settings) == 0:
        return 0
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

"""Тесты конфигурации из CSV (этап 1)."""

import os
import unittest

from depgraph.config import (
    ConfigError,
    check_image,
    check_package,
    check_repo,
    format_params,
    load_csv_config,
    load_settings,
    validate,
)

HERE = os.path.dirname(os.path.abspath(__file__))


def data(name):
    """Путь к файлу-приспособлению."""
    return os.path.join(HERE, "fixtures", name)


class TestConfig(unittest.TestCase):
    """Проверка чтения и валидации CSV-настроек."""

    def test_load_good(self):
        """Корректный файл читается в словарь."""
        raw = load_csv_config(data("good.csv"))
        self.assertEqual(raw["package"], "serde")
        self.assertEqual(raw["test_mode"], "off")

    def test_missing_file(self):
        """Отсутствие файла даёт ошибку настроек."""
        with self.assertRaises(ConfigError):
            load_csv_config(data("нет-такого.csv"))

    def test_unknown_key(self):
        """Неизвестный параметр отклоняется."""
        with self.assertRaises(ConfigError):
            load_csv_config(data("unknown.csv"))

    def test_no_value(self):
        """Строка без значения отклоняется."""
        with self.assertRaises(ConfigError):
            load_csv_config(data("noval.csv"))

    def test_missing_key(self):
        """Отсутствие обязательного ключа замечается."""
        with self.assertRaises(ConfigError):
            validate({"package": "A"})

    def test_bad_flag(self):
        """Мусор во флаге даёт ошибку настроек."""
        raw = {"package": "A", "repo": "https://x/y",
               "test_mode": "maybe", "image": "g.png"}
        with self.assertRaises(ConfigError):
            validate(raw)

    def test_empty_package(self):
        """Пустое имя пакета запрещено."""
        with self.assertRaises(ConfigError):
            check_package("   ")

    def test_bad_repo(self):
        """Несуществующий путь отклоняется."""
        with self.assertRaises(ConfigError):
            check_repo("/нет/такого/файла.txt")

    def test_empty_image(self):
        """Пустое имя файла запрещено."""
        with self.assertRaises(ConfigError):
            check_image("  ")

    def test_format(self):
        """Вывод настроек идёт строками ключ-значение."""
        text = format_params(load_settings(data("good.csv")))
        self.assertIn("package=serde", text)
        self.assertIn("image=graph.png", text)


if __name__ == "__main__":
    unittest.main()

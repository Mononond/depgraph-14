"""Тесты получения зависимостей Cargo (этап 2)."""

import json
import os
import unittest

from depgraph.cargo import direct_dependencies, latest_version

HERE = os.path.dirname(os.path.abspath(__file__))


def load_fixture(name):
    """Прочитать JSON-приспособление из папки tests/fixtures."""
    path = os.path.join(HERE, "fixtures", name)
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def fake_opener(mapping):
    """Подменить сеть словарём адрес-ответ."""
    def opener(url):
        return mapping.get(url, {})
    return opener


class TestCargo(unittest.TestCase):
    """Проверка разбора ответов crates.io."""

    def test_latest(self):
        """Отозванные версии пропускаются."""
        info = load_fixture("crate.json")
        self.assertEqual(latest_version(info), "2.0.0")

    def test_no_versions(self):
        """Без версий возвращается пусто."""
        self.assertIsNone(latest_version({}))

    def test_direct(self):
        """Сквозной разбор: пакет плюс зависимости."""
        info = load_fixture("crate.json")
        deps = load_fixture("deps.json")
        mapping = {
            "https://repo.example/api/crates/demo": info,
            "https://repo.example/api/crates/demo/2.0.0/dependencies":
                deps,
        }
        names = direct_dependencies("demo", "https://repo.example/api",
                                    fake_opener(mapping))
        self.assertEqual(names, ["DepA", "DepB"])

    def test_dev_skipped(self):
        """Dev-зависимости и опциональные отсеиваются."""
        deps = load_fixture("deps.json")
        kinds = [d["kind"] for d in deps["dependencies"]]
        self.assertIn("dev", kinds)


if __name__ == "__main__":
    unittest.main()

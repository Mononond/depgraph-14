"""Тесты Mermaid-описания и PNG-картинки (этап 5)."""

import os
import unittest

from depgraph.graph import load_test_repo
from depgraph.mermaid import describe
from depgraph.pngimg import write_png

HERE = os.path.dirname(os.path.abspath(__file__))


def data(name):
    """Путь к файлу тестового репозитория."""
    return os.path.join(HERE, "testdata", name)


class TestMermaid(unittest.TestCase):
    """Проверка текстового описания графа."""

    def test_frame(self):
        """Описание начинается с graph TD."""
        graph = load_test_repo(data("chain.txt"))
        self.assertTrue(describe(graph).startswith("graph TD"))

    def test_edges(self):
        """Все рёбра присутствуют в виде стрелок."""
        graph = load_test_repo(data("branch.txt"))
        text = describe(graph)
        self.assertIn("A-->B", text)
        self.assertIn("A-->C", text)
        self.assertIn("B-->D", text)
        self.assertIn("C-->D", text)


class TestPng(unittest.TestCase):
    """Проверка PNG-изображения графа."""

    def test_signature(self):
        """Файл начинается с сигнатуры PNG."""
        path = os.path.join(HERE, "tmp_graph.png")
        try:
            write_png(load_test_repo(data("branch.txt")), "A", path)
            with open(path, "rb") as handle:
                head = handle.read(8)
            self.assertEqual(head, b"\x89PNG\r\n\x1a\n")
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_size(self):
        """Картинка не пустая и имеет разумный размер."""
        path = os.path.join(HERE, "tmp_graph.png")
        try:
            write_png(load_test_repo(data("chain.txt")), "A", path)
            size = os.path.getsize(path)
            self.assertTrue(size > 500)
        finally:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()

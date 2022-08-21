import unittest
import scraper
from pathlib import Path


class ToPathTestCase(unittest.TestCase):
    def test_to_path(self):
        self.assertEqual(scraper.to_path("/hello"), Path.cwd() / "hello")
        self.assertEqual(
            scraper.to_path("https://example.org/hello", base="test"),
            Path.cwd() / "test" / "example.org" / "hello",
        )

        self.assertEqual(scraper.to_path(""), Path.cwd() / "index.html")

import unittest
from scraper import Scraper
import asyncio

class ScraperTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.s = Scraper(base_url="https://example.com")

    def test_same_origin_relative(self):
        self.assertTrue(self.s.same_origin("/aoeuaoeu#dhtnhd"))

    def test_same_origin_absolute(self):
        self.assertTrue(self.s.same_origin("https://example.com/snthsnht#jkxjkx"))
        self.assertFalse(self.s.same_origin("https://foo.bar/snthsnht#jkxjkx"))



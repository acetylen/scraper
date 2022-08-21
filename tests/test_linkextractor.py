import unittest
from scraper import LinkExtractor


class LinkExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.x = LinkExtractor(baseurl="https://example.url")

    def tearDown(self):
        self.x.clear()

    def test_normalise_url_absolute(self):
        result = self.x.normalise_url("https://foo.bar/baz#quux")
        self.assertEqual(result, "https://foo.bar/baz")

    def test_normalise_url_relative(self):
        result = self.x.normalise_url("/baz#quux")
        self.assertEqual(result, "https://example.url/baz")

    def test_parse_html(self):

        text = """
        <p>
         This is a <a href="/foo/bar">link</a> to another page.
         <span>
          Check out this <a href="https://foo.bar/article/hello">
           other page
          </a>
         </span>
         Also see <a href="/foo/bar#further_down">here</a>.
        </p>"""

        self.x.feed(text)

        result = self.x.extract()
        self.assertEqual(
            sorted(result),
            sorted([
                "https://example.url/foo/bar",
                "https://foo.bar/article/hello",
            ]),
        )

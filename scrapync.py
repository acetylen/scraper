#!/usr/bin/env python3

"""ScraPyNc is a website scraper.

Steps:
    1. Find out base URL and create a directory.
    2. Fetch url.
    3. Parse downloaded file.
    4. For each unique url found, go to 2.
    5. When no new urls have been found, we're done.
"""

from html.parser import HTMLParser
from urllib.parse import urlparse


class LinkExtractor(HTMLParser):
    """Parses a HTML document and pulls all href attributes."""

    def __init__(self, baseurl: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.found_links = set()
        self.baseurl = baseurl

    def normalise_url(self, url: str) -> str:
        """
        Remove fragment part of {url} so that links to the same page are identical.
        If url is relative, copy scheme and location from baseurl.
        """

        # note: _replace looks like a private interface, but it's not. It's a
        # consequence of urlparse's return type being a subclass of namedtuple.
        link = urlparse(url)._replace(fragment="")
        if not link.netloc:
            base = urlparse(self.baseurl)
            link._replace(scheme=base.scheme)
            link._replace(netloc=base.netloc)

        return link.geturl()

    def handle_starttag(self, tagname: str, attrs: list[tuple[str, str]]):
        """Search every tag for any of the attributes in self.attrs, adding
        it to found links if it's non-empty."""

        attrdict = dict(attrs)
        if "href" not in attrdict:
            return

        link = attrdict["href"]

        self.found_links.add(normalise_url(link))

    def extract(self) -> list[str]:
        """Returns a list of unique links found so far."""

        return list(self.found_links)


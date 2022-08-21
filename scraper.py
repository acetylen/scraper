#!/usr/bin/env python3

"""Scraper is a website scraper and downloader.

Steps:
    1. Fetch resource at url.
    2. Save resource to disk.
    2. Parse downloaded file.
    3. Check if file contains any new urls.
        3a, if yes, go to 1.
        3b, if no, we're done.
"""
__version__ = "0.0.1"

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
        Clean up {url} to remove duplicate entries.
        Removes fragment and trailing /..
        If {url} is relative, copy scheme and location from {self.baseurl}.
        """

        # note: _replace looks like a private interface in order for it to not
        # look like a namedtuple field (ParseResult is a subclass)
        link = urlparse(url)._replace(fragment="")
        if link.path.endswith("/"):
            link = link._replace(path=link.path[:-1])
        if not link.netloc:
            base = urlparse(self.baseurl)
            link = link._replace(scheme=base.scheme, netloc=base.netloc)

        return link.geturl()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        """Search tag for a href, adding it to found links if it exists."""
        if attrs is None:
            return
        href = dict(attrs).get("href")
        if href is None:
            return

        self.found_links.add(self.normalise_url(href))



    def extract(self) -> set[str]:
        """Returns unique links found so far."""

        return self.found_links


async def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cross-origin",
        action="store_true",
        help="also fetch resources from different domains",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        help="base directory for storing fetched resources",
    )
    parser.add_argument("url", help="URL to fetch")

    args = parser.parse_args()

    raise NotImplementedError()


def entrypoint():
    # Can't use async functions as entrypoints
    asyncio.run(main())


if __name__ == "__main__":
    entrypoint()

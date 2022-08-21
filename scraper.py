#!/usr/bin/env python3

"""Scraper is a website scraper and downloader.
It parses the resource at the provided link for urls, then concurrently downloads
the target resources and repeats the process until it finds no more links.
"""
__version__ = "1.0.0"

import asyncio
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, URLError, HTTPError


def to_path(url: str, base: str = None) -> Path:
    """Given a {url}, convert it to a file system path.
    If {base} is given, prepend it to the url path."""

    here = Path.cwd()
    if base:
        # appending as-is allows us to append an absolute path
        here /= base

    parts = urlparse(url)

    # special case for index pages
    if parts.path in ("", "/"):
        parts = parts._replace(path="/index.html")

    return here / parts.netloc / parts.path[1:]


def fetch(url: str) -> bytes:
    """Given a url, fetch the resource and return it."""

    try:
        with urlopen(url) as r:
            html = r.read()
    except (HTTPError, URLError) as err:
        print(f"Error fetching {url}: {err}")
        return None
    return html


def store(url: str, html: bytes, base: str = None):
    """Save a web resource to a file, optionally under the {base} directory"""
    path = to_path(url, base)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_bytes(html)


class LinkExtractor(HTMLParser):
    """Parses a HTML document and pulls all href attributes."""

    def __init__(self, baseurl: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.found_links: set[str] = set()
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

        href = dict(attrs).get("href")
        if href is None:
            return

        self.found_links.add(self.normalise_url(href))

    def extract(self) -> set[str]:
        """Returns unique links found so far."""

        return self.found_links


class Scraper:
    """Scrapes all urls it finds"""

    def __init__(
        self,
        base_url: str,
        cross_origin: bool = False,
        base_dir: str = None,
    ):
        self.seen_links: set[str] = set()
        self.extractor = LinkExtractor(base_url)
        self.base_url = base_url
        self.loop = asyncio.get_running_loop()
        self.cross_origin = cross_origin
        self.base_dir = base_dir

    @cache
    def same_origin(self, url: str) -> bool:
        """True if url is relative or has same domain"""
        domain = urlparse(url).netloc
        return domain == "" or domain == urlparse(self.base_url).netloc

    async def scrape(self):
        await self.scrape_all([self.base_url])

    def fetch_and_store(self, url: str) -> bytes:

        print(f"fetching {url}...")
        html = fetch(url)

        if html:
            store(url, html, self.base_dir)

        return html

    async def scrape_all(self, urls: list[str]):
        """Given a list of urls, concurrently fetches and scrapes them.
        If this results in new urls being found, these are fetched as well."""
        self.seen_links |= set(urls)

        if not self.cross_origin:
            urls = [url for url in urls if self.same_origin(url)]

        tasks = [asyncio.to_thread(self.fetch_and_store, url) for url in urls]
        for task in asyncio.as_completed(tasks):
            html = await task
            if html:
                try:
                    text = html.decode()
                except ValueError as err:
                    print(err)
                    continue
                self.extractor.feed(text)

        links = self.extractor.extract()

        # filter out already visited links before running the next batch
        new_links = links - self.seen_links
        self.seen_links |= links

        if new_links:
            await self.scrape_all(list(new_links))


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

    scraper = Scraper(
        base_url=args.url,
        cross_origin=args.cross_origin,
        base_dir=args.output_dir,
    )
    await scraper.scrape()


def entrypoint():
    # Can't use async functions as entrypoints
    asyncio.run(main())


if __name__ == "__main__":
    entrypoint()

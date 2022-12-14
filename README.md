# Scraper

This is an asynchronous website scraper built using only the python 3.10
standard library.

## Installation

This tool is distributed as a single file, which means it can be run by
`$ python scraper.py <url>`. Installing using `pip install .` will add the
`scrape` tool to your path, which behaves the same way.

## Usage

```shell
$ scrape -h
usage: scrape [-h] [--cross-origin] [-o OUTPUT_DIR] url

Scraper is a website scraper and downloader. It parses the resource at the provided link for urls, then
concurrently downloads the target resources and repeats the process until it finds no more links.

positional arguments:
  url                   URL to fetch

options:
  -h, --help            show this help message and exit
  --cross-origin        also fetch resources from different domains
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        base directory for storing fetched resources

$ scrape https://example.org --output-dir example
$ tree example
example/
└── example.org
    └── index.html
```

## Rationale

For this project I wanted to build something with modern python tooling, 
without any external dependencies. The pyproject.toml file has been 
standardized and is now supported by `setuptools` and `pip`, so that 
eliminates any question marks about packaging. The tool is housed in a single
file spanning about 200 lines, which is pretty okay for a tool with some 
actual error handling.

The most painful part of this project was probably testing, since the
`unittest` library was never particularly ergonomic and `doctest` just feels
a bit hacky.

Regarding style, the tool is written in a look-before-you-leap style, only
resorting to exceptions when external modules throw them or when the python
style dictates it. I personally prefer to not use exceptions everywhere
as they tend to become less effective and more confusing when reduced to just
another control flow mechanism.

Formatting is done using `black` and `isort`, and linting is done using `flake8`
(using the `pyproject-flake8` wrapper `pflake8` to read `black`-compatible
settings from the pyproject-file) and `mypy`.

Test coverage was done using `coverage.py`, however coverage is about 60% since
testing functionality that relies on an internet connection is too fiddly and
annoying for a quick project such as this.

## Future work

There is currently no validation being done on the input. Breaking the tool by
feeding it bad URLs is very simple.

There are no checks for disk i/o, so overwriting important files is just a
matter of inputting a bad URL.

Handling of paths that are not files (like how foo.bar/ points to foo.bar/index.html)
is currently very simplistic, so some files may be missed.

The tool currently pulls every `href` it can find, no matter the protocol, so
`mailto` links get pulled in as well, and result in error messages.

Speaking of errors, the only error handling done on failed requests is to skip them.
Ideally there should be a retry mechanic and a protocol distinction.

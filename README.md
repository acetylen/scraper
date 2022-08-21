# Scraper

This is an asynchronous website scraper built using only the python 3.10
standard library.

## Installation

This tool is distributed as a single file, which means it can be run by
`$ python scraper.py <url>`. Installing using `pip install .` will add the
`scrape` tool to your path, which behaves the same way.

## Usage

```shell
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
and `mypy`.
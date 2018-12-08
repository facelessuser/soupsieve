"""
Soup Sieve.

A CSS selector filter for BeautifulSoup4.

MIT License

Copyright (c) 2018 Isaac Muse

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from .__meta__ import __version__, __version_info__  # noqa: F401
from . import css_parser as cp
from .util import HTML, HTML5, XHTML, XML

__all__ = (
    'HTML', 'HTML5', 'XHTML', 'XML',
    'SoupSieve', 'compile', 'purge', 'comments', 'select', 'match', 'filter'
)

SoupSieve = cp.SoupSieve


def compile(pattern, namespaces=None, mode=HTML5):  # noqa: A001
    """Compile CSS pattern."""

    if isinstance(pattern, SoupSieve):
        if mode != pattern.mode:
            raise ValueError("Cannot change mode of a pattern")
        elif namespaces != pattern.namespaces:
            raise ValueError("Cannot change namespaces of a pattern")
        return pattern

    if namespaces is None:
        namespaces = cp._Namespaces()
    if not isinstance(namespaces, cp._Namespaces):
        namespaces = cp._Namespaces(**(namespaces))

    return cp._cached_css_compile(pattern, namespaces, mode)


def purge():
    """Purge cached patterns."""

    cp._purge_cache()


def match(node, select, namespaces=None, mode=HTML5):
    """Match node."""

    return compile(select, namespaces, mode).match(node)


def filter(nodes, select, namespaces=None, mode=HTML5):  # noqa: A001
    """Filter list of nodes."""

    return compile(select, namespaces, mode).filter(select)


def comments(node, limit=0, mode=HTML5):
    """Get comments only."""

    yield from compile("", None, mode).comments(node, limit)


def select(node, select, namespaces=None, limit=0, mode=HTML5):
    """Select the specified tags."""

    yield from compile(select, namespaces, mode).select(node, limit)

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
from . import css_match as cm
from . import css_types as ct
from .util import HTML, HTML5, XHTML, XML, deprecated

__all__ = (
    'HTML', 'HTML5', 'XHTML', 'XML',
    'SoupSieve', 'compile', 'purge',
    'comments', 'icomments', 'select', 'iselect', 'match', 'filter'
)

SoupSieve = cm.SoupSieve


def compile(pattern, namespaces=None, mode=HTML5):  # noqa: A001
    """Compile CSS pattern."""

    if namespaces is None:
        namespaces = ct.Namespaces()
    if not isinstance(namespaces, ct.Namespaces):
        namespaces = ct.Namespaces(**(namespaces))

    if isinstance(pattern, SoupSieve):
        if mode != pattern.mode:
            raise ValueError("Cannot change mode of a pattern")
        elif namespaces != pattern.namespaces:
            raise ValueError("Cannot change namespaces of a pattern")
        return pattern

    return cp._cached_css_compile(pattern, namespaces, mode)


def purge():
    """Purge cached patterns."""

    cp._purge_cache()


def match(select, node, namespaces=None, mode=HTML5):
    """Match node."""

    return compile(select, namespaces, mode).match(node)


def filter(select, nodes, namespaces=None, mode=HTML5):  # noqa: A001
    """Filter list of nodes."""

    return compile(select, namespaces, mode).filter(nodes)


def comments(node, limit=0, mode=HTML5):
    """Get comments only."""

    return compile("", None, mode).comments(node, limit)


def icomments(node, limit=0, mode=HTML5):
    """Iterate comments only."""

    yield from compile("", None, mode).icomments(node, limit)


def select(select, node, namespaces=None, limit=0, mode=HTML5):
    """Select the specified tags."""

    return compile(select, namespaces, mode).select(node, limit)


def iselect(select, node, namespaces=None, limit=0, mode=HTML5):
    """Iterate the specified tags."""

    yield from compile(select, namespaces, mode).iselect(node, limit)


# ====== Deprecated ======
@deprecated("Use 'icomments' instead.")
def commentsiter(node, limit=0, mode=HTML5):
    """Iterate comments only."""

    yield from icomments(node, limit, mode)


@deprecated("Use 'iselect' instead.")
def selectiter(select, node, namespaces=None, limit=0, mode=HTML5):
    """Iterate the specified tags."""

    yield from iselect(select, node, namespaces, limit, mode)

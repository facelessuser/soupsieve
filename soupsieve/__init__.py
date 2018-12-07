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
from . import util
from .util import HTML, HTML5, XHTML, XML

__all__ = (
    'HTML', 'HTML5', 'XHTML', 'XML', 'COMMENTS',
    'SoupSieve', 'compile', 'purge', 'comments', 'select',
)

COMMENTS = 0x1


def compile(pattern, namespaces, mode=0):  # noqa: A001
    """Compile CSS pattern."""

    if isinstance(pattern, cp.CSSPattern):
        if mode != pattern.mode:
            raise ValueError("Cannot change mode of a pattern")
        elif namespaces != pattern.namespaces:
            raise ValueError("Cannot change namespaces of a pattern")
        return pattern

    if not all([isinstance(k, str) and isinstance(v, str) for k, v in namespaces.items()]):
        raise TypeError('Namespace keys and values must be Unicode strings')

    return cp._cached_css_compile(
        pattern,
        util.ImmutableDict(**(namespaces if namespaces else {})),
        mode
    )


def purge():
    """Purge cached patterns."""

    cp._purge_cache()


class SoupSieve:
    """Soup sieve CSS selector class."""

    def __init__(self, mode=0):
        """Initialize mode."""

        if mode == 0:
            mode = HTML

        if mode in (HTML, HTML5, XML, XHTML):
            self.mode = mode
        else:
            raise ValueError("Invalid SoupSieve document mode '{}'".format(mode))

    def _select(self, node):
        """Recursively return selected tags."""

        if self.ignores.match(node):
            if self.comments:
                for child in node.descendants:
                    if isinstance(child, util.COMMENT):
                        yield child
        else:
            if self.captures.match(node):
                yield node

            # Walk children
            for child in node.children:
                if isinstance(child, util.TAG):
                    yield from self._select(child)
                elif self.comments and isinstance(child, util.COMMENT):
                    yield child

    def comments(self, node, limit=0):
        """Get comments only."""

        yield from self.select(node, "", "", None, limit, COMMENTS)

    def select(self, node, select="", ignore="", namespaces=None, limit=0, flags=0):
        """Select the specified tags filtering out an tags if 'ignores' is provided."""

        if limit < 1:
            limit = None

        if namespaces is None:
            namespaces = {}

        self.comments = flags & COMMENTS
        self.captures = compile(select, namespaces, self.mode)
        self.ignores = compile(ignore, namespaces, self.mode)

        for child in self._select(node):
            yield child
            if limit is not None:
                limit -= 1
                if limit < 1:
                    break


def comments(node, limit=0, mode=0):
    """Get comments only."""

    yield from SoupSieve(mode).comments(node, limit)


def select(node, select="", ignore="", namespaces=None, limit=0, mode=0, flags=0):
    """Select the specified tags filtering out if a filter pattern is provided."""

    yield from SoupSieve(mode).select(node, select, ignore, namespaces, limit, flags)

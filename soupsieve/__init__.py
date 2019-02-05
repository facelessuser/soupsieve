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
from __future__ import unicode_literals
from .__meta__ import __version__, __version_info__  # noqa: F401
from . import css_parser as cp
from . import css_match as cm
from . import css_types as ct
from . import util
from .util import DEBUG, _QUIRKS, SelectorSyntaxError  # noqa: F401

__all__ = (
    'DEBUG', "_QUIRKS", 'SoupSieve', 'compile', 'purge',
    'comments', 'icomments', 'closest', 'select', 'select_one',
    'iselect', 'match', 'filter', 'SelectorSyntaxError', 'Custom'
)

SoupSieve = cm.SoupSieve


def compile(pattern, namespaces=None, flags=0, **kwargs):  # noqa: A001
    """Compile CSS pattern."""

    ns_none = namespaces is None
    if ns_none:
        namespaces = ct.Namespaces()
    if not isinstance(namespaces, ct.Namespaces):
        namespaces = ct.Namespaces(**namespaces)

    custom = kwargs.get('custom')
    if custom is not None:
        if not isinstance(custom, Custom):
            raise TypeError("Custom selectors must be of type 'Custom'")
        custom = cp._create_custom_selectors(custom, flags)

    if isinstance(pattern, SoupSieve):
        if flags:
            raise ValueError("Cannot process 'flags' argument on a compiled selector list")
        elif not ns_none:
            raise ValueError("Cannot process 'namespaces' argument on a compiled selector list")
        elif custom is not None:
            raise ValueError("Cannot process 'custom' argument on a compiled selector list")
        return pattern

    return cp._cached_css_compile(pattern, namespaces, custom, flags)


def purge():
    """Purge cached patterns."""

    cp._purge_cache()


def closest(select, tag, namespaces=None, flags=0, **kwargs):
    """Match closest ancestor."""

    return compile(select, namespaces, flags, **kwargs).closest(tag)


def match(select, tag, namespaces=None, flags=0, **kwargs):
    """Match node."""

    return compile(select, namespaces, flags, **kwargs).match(tag)


def filter(select, iterable, namespaces=None, flags=0, **kwargs):  # noqa: A001
    """Filter list of nodes."""

    return compile(select, namespaces, flags, **kwargs).filter(iterable)


def comments(tag, limit=0, flags=0, **kwargs):
    """Get comments only."""

    return list(icomments(tag, limit, flags))


def icomments(tag, limit=0, flags=0, **kwargs):
    """Iterate comments only."""

    for comment in cm.CommentsMatch(tag).get_comments(limit):
        yield comment


def select_one(select, tag, namespaces=None, flags=0, **kwargs):
    """Select a single tag."""

    return compile(select, namespaces, flags, **kwargs).select_one(tag)


def select(select, tag, namespaces=None, limit=0, flags=0, **kwargs):
    """Select the specified tags."""

    return compile(select, namespaces, flags, **kwargs).select(tag, limit)


def iselect(select, tag, namespaces=None, limit=0, flags=0, **kwargs):
    """Iterate the specified tags."""

    for el in compile(select, namespaces, flags, **kwargs).iselect(tag, limit):
        yield el


class Custom(object):
    """
    Custom Selectors.

    This object allows us to control order, and possibly extend the complexity of aliases in the future.

    TODO: If desired, we could allow for function custom selectors `:--custom(arg1, arg2)`,
          or even custom logic, though none of these possibilities have been fully evaluated
          for practicality or if they can even be implemented.
    """

    def __init__(self):
        """Initialize."""

        self._custom = util.odict()

    def append(self, alias, selector):
        """Append a new custom selector."""

        name = util.lower(alias)

        if not cp._valid_custom_name(name):
            raise SyntaxError("The name '{}' is not a valid custom pseudo-class name".format(name))
        if name in self._custom:
            raise KeyError("The custom selector '{}' has already been registered".format(name))
        self._custom[name] = selector

    def remove(self, alias):
        """Remove a custom selector by name."""

        del self._custom[alias]

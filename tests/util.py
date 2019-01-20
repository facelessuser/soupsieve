"""Test utilities."""
from __future__ import unicode_literals
import unittest
import bs4
import textwrap
import soupsieve as sv
import sys

PY3 = sys.version_info >= (3, 0)

HTML5 = 0x1
HTML = 0x2
XHTML = 0x4
XML = 0x8
PYHTML = 0x10
LXML_HTML = 0x20


def skip_quirks(func):
    """Decorator that skips when quirks mode is enabled."""

    def skip_if(self, *args, **kwargs):
        """Skip conditional wrapper."""
        if self.quirks is True:
            return
        else:
            return func(self, *args, **kwargs)
    return skip_if


def skip_no_quirks(func):
    """Decorator that skips when no quirks mode is enabled."""

    def skip_if(self, *args, **kwargs):
        """Skip conditional wrapper."""
        if self.quirks is False:
            return
        else:
            return func(self, *args, **kwargs)
    return skip_if


class TestCase(unittest.TestCase):
    """Test case."""

    def setUp(self):
        """Setup."""

        sv.purge()
        self.quirks = False

    def purge(self):
        """Purge cache."""

        sv.purge()

    def compile_pattern(self, selectors, namespaces=None, flags=0):
        """Compile pattern."""

        print('PATTERN: ', selectors)
        flags |= sv.DEBUG
        if self.quirks:
            flags |= sv._QUIRKS
        return sv.compile(selectors, namespaces=namespaces, flags=flags)

    def soup(self, markup, parser):
        """Get soup."""

        print('PARSER: ', parser)
        return bs4.BeautifulSoup(textwrap.dedent(markup.replace('\r\n', '\n')), parser)

    def get_parsers(self, flags):
        """Get parsers."""

        mode = flags & 0x2F
        if mode == HTML:
            parsers = ('html5lib', 'lxml', 'html.parser')
        elif mode == PYHTML:
            parsers = ('html.parser',)
        elif mode == LXML_HTML:
            parsers = ('lxml',)
        elif mode in (HTML5, 0):
            parsers = ('html5lib',)
        elif mode in (XHTML, XML):
            parsers = ('xml',)
        return parsers

    def assert_raises(self, pattern, exception, namespace=None):
        """Assert raises."""

        print('----Running Assert Test----')
        with self.assertRaises(exception):
            self.compile_pattern(pattern)

    def assert_selector(self, markup, selectors, expected_ids, namespaces={}, flags=0):
        """Assert selector."""

        parsers = self.get_parsers(flags)

        print('----Running Selector Test----')
        selector = self.compile_pattern(selectors, namespaces)

        for parser in parsers:
            print('PARSER: ', parser)
            soup = self.soup(markup, parser)

            ids = []
            for el in selector.select(soup):
                print('TAG: ', el.name)
                ids.append(el.attrs['id'])
            self.assertEqual(sorted(ids), sorted(expected_ids))

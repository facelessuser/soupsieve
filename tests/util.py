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

    def assert_raises(self, pattern, exception, namespace=None):
        """Assert raises."""

        with self.assertRaises(exception):
            flags = sv.DEBUG
            if self.quirks:
                flags = sv._QUIRKS

            sv.compile(pattern, flags=flags)

    def assert_selector(self, markup, selectors, expected_ids, namespaces={}, flags=0):
        """Assert selector."""

        mode = flags & 0x2F
        if mode == HTML:
            bs_mode = ('html5lib', 'lxml', 'html.parser')
        elif mode == PYHTML:
            bs_mode = ('html.parser',)
        elif mode == LXML_HTML:
            bs_mode = ('lxml',)
        elif mode in (HTML5, 0):
            bs_mode = ('html5lib',)
        elif mode in (XHTML, XML):
            bs_mode = ('xml',)

        for parser in bs_mode:
            print('PARSER: ', parser)
            soup = bs4.BeautifulSoup(textwrap.dedent(markup.replace('\r\n', '\n')), parser)
            # print(soup)
            flags |= sv.DEBUG
            if self.quirks:
                flags |= sv._QUIRKS

            ids = []
            for el in sv.select(selectors, soup, namespaces=namespaces, flags=flags):
                print('TAG: ', el.name)
                ids.append(el.attrs['id'])
            self.assertEqual(sorted(ids), sorted(expected_ids))

"""Test utilities."""
import unittest
import bs4
import textwrap
import soupsieve as sv


class TestCase(unittest.TestCase):
    """Test case."""

    def assert_selector(self, markup, selectors, expected_ids, namespaces={}, flags=0):
        """Assert selector."""

        mode = flags & sv.util.MODE_MSK
        if mode == sv.HTML:
            bs_mode = 'lxml'
        elif mode in (sv.HTML5, 0):
            bs_mode = 'html5lib'
        elif mode in (sv.XHTML, sv.XML):
            bs_mode = 'xml'
        soup = bs4.BeautifulSoup(textwrap.dedent(markup.replace('\r\n', '\n')), bs_mode)

        ids = []
        for el in sv.select(selectors, soup, namespaces=namespaces, flags=flags):
            ids.append(el.attrs['id'])
        self.assertEqual(sorted(ids), sorted(expected_ids))

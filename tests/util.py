"""Test utilities."""
import unittest
import bs4
import textwrap
import soupsieve as sv


class TestCase(unittest.TestCase):
    """Test case."""

    def assert_selector(self, markup, selectors, expected_ids, namespaces={}, mode=sv.HTML5):
        """Assert selector."""

        if mode == sv.HTML:
            bs_mode = 'lxml'
        elif mode == sv.HTML5:
            bs_mode = 'html5lib'
        elif mode in (sv.XHTML, sv.XML):
            bs_mode = 'xml'
        soup = bs4.BeautifulSoup(textwrap.dedent(markup.replace('\r\n', '\n')), bs_mode)

        ids = []
        for el in sv.select(selectors, soup, namespaces=namespaces, mode=mode):
            ids.append(el.attrs['id'])
        self.assertEqual(sorted(ids), sorted(expected_ids))

"""Test subsequent sibling combinator."""
from .. import util
import soupsieve as sv


class TestSubsequentSibling(util.TestCase):
    """Test subsequent sibling combinator."""

    def test_no_parent_element(self):
        """Test siblings that are at the top level of the document."""

        markup = '<a id="1"></a><b id="2"></b><c id="3"></c>'

        self.assert_selector(markup, "a ~ c", ["3"], flags=util.PYHTML | util.NOCACHE)
        self.assert_selector(markup, "a:has(~ c)", ["1"], flags=util.PYHTML | util.NOCACHE)

    def test_detached_element(self):
        """Test that an element that has been detached has no siblings."""

        for flags in (0, sv.NOCACHE):
            el = self.soup('<a></a><b></b>', 'html.parser').b.extract()
            self.assertFalse(sv.match('a ~ b', el, flags=flags))

    def test_subsequent_sibling(self):
        """Test subsequent sibling."""

        self.assert_selector(
            """
            <div>
            <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
            <a id="2" href="http://google.com">Link</a>
            <span id="3">Direct child</span>
            <pre>
            <span id="4">Child 1</span>
            <span id="5">Child 2</span>
            <span id="6">Child 3</span>
            </pre>
            </div>
            """,
            "p ~ span",
            ["3"],
            flags=util.HTML | util.NOCACHE
        )

    def test_many_siblings(self):
        """Test many siblings case."""

        import soupsieve as sv
        from bs4 import BeautifulSoup

        selector = "b ~ a"
        for n in (1000, 2000, 4000, 8000):
            html = "<div>" + ("<a></a>" * n) + "</div>"
            soup = BeautifulSoup(html, "html.parser")
            self.assertEqual(len(sv.select(selector, soup)), 0)

    def test_many_siblings_late_match(self):
        """Test many siblings case where the first matching sibling is in the middle."""

        import soupsieve as sv
        from bs4 import BeautifulSoup

        selector = "b ~ a"
        for n in (1000, 2000, 4000, 8000):
            html = "<div>" + ("<a></a> " * n) + "<b></b> " + ("<a></a> " * n) + "</div>"
            soup = BeautifulSoup(html, "html.parser")
            self.assertEqual(len(sv.select(selector, soup)), n)

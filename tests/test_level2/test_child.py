"""Test child combinators."""
from .. import util
from soupsieve import SelectorSyntaxError


class TestChild(util.TestCase):
    """Test child combinators."""

    MARKUP = """
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
    """

    def test_direct_child(self):
        """Test direct child."""

        # Spaces
        self.assert_selector(
            self.MARKUP,
            "div > span",
            ["3"],
            flags=util.HTML
        )

    def test_direct_child_no_spaces(self):
        """Test direct child with no spaces."""

        # No spaces
        self.assert_selector(
            self.MARKUP,
            "div>span",
            ["3"],
            flags=util.HTML
        )

    def test_invalid_double_combinator(self):
        """Test that selectors cannot have double combinators."""

        self.assert_raises('div >> p', SelectorSyntaxError)
        self.assert_raises('>> div > p', SelectorSyntaxError)

    def test_invalid_trailing_combinator(self):
        """Test that selectors cannot have a trailing combinator."""

        self.assert_raises('div >', SelectorSyntaxError)
        self.assert_raises('div >, div', SelectorSyntaxError)

    def test_invalid_combinator(self):
        """Test that we do not allow selectors in selector lists to start with combinators."""

        self.assert_raises('> p', SelectorSyntaxError)
        self.assert_raises('div, > a', SelectorSyntaxError)

    def test_document_object_not_parent(self):
        """Test that the `BeautifulSoup` object is not counted as a parent."""

        from bs4 import BeautifulSoup
        soup = BeautifulSoup("<r><c></c></r>", "html.parser")
        self.assertEqual(soup.select("* > r"), [])
        self.assertEqual(soup.select("* > r:root"), [])

    def test_shared_parent(self):
        """Test that the result for a parent does not leak into elements that have other parents."""

        markup = """
        <div id="1"><p id="2"></p><span id="3"></span><span id="4"></span></div>
        <div id="5"><span id="6"></span><span id="7"></span></div>
        <section id="8"><p id="9"></p><span id="10"></span></section>
        """

        for flags in (util.HTML, util.HTML | util.NOCACHE):
            self.assert_selector(markup, "div:has(> p) > span", ["3", "4"], flags=flags)
            self.assert_selector(markup, ":has(> p) > span", ["3", "4", "10"], flags=flags)
            self.assert_selector(markup, "div:not(:has(> p)) > span", ["6", "7"], flags=flags)
            self.assert_selector(markup, "div > span, div:has(> p) > span", ["3", "4", "6", "7"], flags=flags)

    def test_many_children(self):
        """Test that the parent is matched once for all of its children."""

        import soupsieve as sv
        from bs4 import BeautifulSoup
        from unittest import mock

        n = 64
        soup = BeautifulSoup("<div>" + "<span></span>" * n + "</div>", "html.parser")
        match = sv.css_match.CSSMatch._match_selectors
        with mock.patch.object(sv.css_match.CSSMatch, "_match_selectors", autospec=True, side_effect=match) as patched:
            self.assertEqual(len(sv.select("div:has(> p) > span", soup)), 0)
        self.assertLessEqual(patched.call_count, 3 * n)

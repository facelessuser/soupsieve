"""Test descendant combinators."""
from .. import util


class TestDescendants(util.TestCase):
    """Test descendant combinators."""

    def test_descendants(self):
        """Test descendants."""

        self.assert_selector(
            """
            <div>
            <p>Some text <span id="1"> in a paragraph</span>.
            <a id="2" href="http://google.com">Link</a>
            </p>
            </div>
            """,
            "div span",
            ["1"],
            flags=util.HTML
        )

    def test_long_duplicate_tag_case(self):
        """Test long descendant case."""

        import soupsieve as sv

        for n in (1000, 2000, 4000, 8000):
            self.assertEqual(sv.compile("a" + " " * n + "b").selectors.count, 2)

    def test_shared_ancestors(self):
        """Test that the result for an ancestor does not leak into elements that have other ancestors."""

        markup = """
        <section id="1">
          <div id="2"><p id="3"><span id="4"></span></p></div>
          <p id="5"></p>
        </section>
        <div id="6"><p id="7"><span id="8"></span></p></div>
        <div id="9"><section id="10"><p id="11"><span id="12"></span></p></section></div>
        """

        self.assert_selector(markup, "section div p", ["3"], flags=util.HTML | util.NOCACHE)
        self.assert_selector(markup, "section p span", ["4", "12"], flags=util.HTML | util.NOCACHE)
        self.assert_selector(markup, "div p, section span", ["3", "4", "7", "11", "12"], flags=util.HTML | util.NOCACHE)
        self.assert_selector(markup, "div section p span", ["12"], flags=util.HTML | util.NOCACHE)
        self.assert_selector(markup, "section :not(div p)", ["2", "4", "5", "12"], flags=util.HTML | util.NOCACHE)

    def test_many_descendant_combinators(self):
        """Test that every combinator tries each ancestor once in a deeply nested document."""

        import soupsieve as sv
        from bs4 import BeautifulSoup
        from unittest import mock

        n = 32
        soup = BeautifulSoup("<div>" * n, "html.parser")
        match = sv.css_match.CSSMatch._match_selectors
        with mock.patch.object(sv.css_match.CSSMatch, "_match_selectors", autospec=True, side_effect=match) as patched:
            self.assertEqual(len(sv.select("section div div div div", soup)), 0)
        self.assertLessEqual(patched.call_count, 5 * n)

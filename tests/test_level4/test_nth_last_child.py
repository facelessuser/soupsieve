"""Test `nth` last child selectors."""
from .. import util


class TestNthLastChild(util.TestCase):
    """Test `nth` last child selectors."""

    def test_nth_child_of_s_complex(self):
        """Test `nth` child with selector (complex)."""

        markup = """
        <body>
        <p id="0"></p>
        <p id="1"></p>
        <span id="2"></span>
        <span id="3"></span>
        <span id="4"></span>
        <span id="5"></span>
        <span id="6"></span>
        <p id="7"></p>
        <p id="8"></p>
        <p id="9"></p>
        <p id="10"></p>
        <span id="11"></span>
        </body>
        """

        self.assert_selector(
            markup,
            ":nth-last-child(2n + 1 of p[id], span[id])",
            ['1', '3', '5', '7', '9', '11'],
            flags=util.HTML
        )

    def test_nth_child_of_s_first_sibling_not_matching(self):
        """Test `nth` last child with selector when the first sibling does not match the selector."""

        markup = """
        <body>
        <p id="0"></p>
        <p id="1" class="test"></p>
        <p id="2" class="test"></p>
        <p id="3" class="test"></p>
        </body>
        """

        self.assert_selector(
            markup,
            ":nth-last-child(1 of .test)",
            ['3'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            markup,
            ":nth-last-child(2 of .test)",
            ['2'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            markup,
            ":nth-last-child(odd of .test)",
            ['1', '3'],
            flags=util.HTML | util.NOCACHE
        )

    def test_nested_nth_of_s(self):
        """Test `nth` selectors nested in the `of S` of `nth` last child selectors."""

        markup = """
        <body>
        <p id="0" class="a"></p>
        <span id="1"></span>
        <p id="2"></p>
        <p id="3" class="a"></p>
        <span id="4" class="a"></span>
        <p id="5" class="a"></p>
        <span id="6"></span>
        <p id="7"></p>
        <span id="8" class="a"></span>
        <p id="9" class="a"></p>
        </body>
        """

        self.assert_selector(
            markup,
            ":nth-last-child(odd of :nth-last-child(2n of .a))",
            ['0', '8'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            markup,
            ":nth-last-child(-n+2 of :nth-child(odd of p))",
            ['3', '7'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            markup,
            ":nth-child(2 of :nth-last-child(n+2 of .a))",
            ['3'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            markup,
            ":nth-last-child(1 of :nth-last-child(odd of :nth-last-child(n+2 of [id])))",
            ['8'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            markup,
            "[id]:nth-last-child(2n+1 of :nth-last-of-type(odd))",
            ['2', '5', '9'],
            flags=util.HTML | util.NOCACHE
        )

    def test_nested_nth_of_s_evaluates_siblings_once(self):
        """
        Test that nested `nth` selectors with `of S` evaluate each sibling once.

        An `nth` selector's `of S` is evaluated on the siblings in the order the outer selector walks them, which is
        in reverse for `nth` last selectors. The `nth` cache must handle lookups in any order, or each level of
        nesting multiplies the work by the number of siblings.

        Only the cached path is tested as matching without the cache is expected to be slow here.
        """

        import soupsieve as sv
        from bs4 import BeautifulSoup
        from unittest import mock

        n = 50
        markup = '<div>' + '<p class="a"></p><span></span>' * (n // 2) + '</div>'
        soup = BeautifulSoup(markup, 'html.parser')
        match = sv.css_match.CSSMatch._match_selectors
        for selector, matches in (
            (':nth-last-child(n of :nth-last-child(n of :nth-last-child(n of :not(div))))', n),
            (':nth-child(n of :nth-child(n of :nth-child(n of :not(div))))', n),
            (':nth-last-child(n of :nth-child(n of :nth-last-child(n of :not(div))))', n),
            (':nth-child(n of :nth-last-child(n of :nth-child(n of :not(div))))', n),
            (':nth-last-child(odd of :nth-child(2n of :nth-last-child(n+1 of .a)))', 6),
            (':nth-last-child(n of :nth-last-child(n of p:nth-last-of-type(n)))', n // 2)
        ):
            with mock.patch.object(
                sv.css_match.CSSMatch, '_match_selectors', autospec=True, side_effect=match
            ) as patched:
                self.assertEqual(len(sv.select(selector, soup)), matches, selector)
            self.assertLessEqual(patched.call_count, 6 * n, selector)

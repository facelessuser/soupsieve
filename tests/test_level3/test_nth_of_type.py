"""Test `nth` of type selectors."""
from .. import util


class TestNthOfType(util.TestCase):
    """Test `nth` of type selectors."""

    def test_nth_of_type(self):
        """Test `nth` of type."""

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
            "p:nth-of-type(3)",
            ['7'],
            flags=util.HTML
        )

    def test_nth_of_type_complex(self):
        """Test `nth` of type complex."""

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
            "p:nth-of-type(2n + 1)",
            ['0', '7', '9'],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            "span:nth-of-type(2n + 1)",
            ['2', '4', '6'],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            "body :nth-of-type(2n + 1)",
            ['0', '2', '4', '6', '7', '9'],
            flags=util.HTML
        )

    def test_many_types(self):
        """
        Test `of-type` selectors on siblings of many different types.

        The siblings of every type are counted in one scan of the parent's contents. Scanning them again for each type
        takes time quadratic in the number of siblings when they have about as many types, such as custom elements.

        Only the cached path is tested as matching without the cache is expected to be slow here.
        """

        import soupsieve as sv
        from bs4 import BeautifulSoup
        from unittest import mock

        n = 64
        markup = '<div>' + ''.join(f'<x-{i}></x-{i}><p></p>' for i in range(n)) + '</div>'
        soup = BeautifulSoup(markup, 'html.parser')
        get_tag = sv.css_match.CSSMatch.get_tag
        for selector, matches in (
            ('div > :first-of-type', n + 1),
            ('div > :last-of-type', n + 1),
            ('div > :only-of-type', n),
            ('div > :nth-of-type(2)', 1),
            ('div > :nth-last-of-type(2)', 1)
        ):
            with mock.patch.object(
                sv.css_match.CSSMatch, 'get_tag', autospec=True, side_effect=get_tag
            ) as patched:
                self.assertEqual(len(sv.select(selector, soup)), matches, selector)
            self.assertLessEqual(patched.call_count, 6 * n, selector)

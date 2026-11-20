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

    def test_nth_of_type_interleaved_types(self):
        """Test `of-type` selectors on interleaved siblings of several types, which share one scan when cached."""

        markup = """
        <body>
        <p id="0"></p>
        <span id="1"></span>
        <b id="2"></b>
        <p id="3"></p>
        <span id="4"></span>
        <p id="5"></p>
        <i id="6"></i>
        <span id="7"></span>
        <p id="8"></p>
        </body>
        """

        self.assert_selector(markup, "body :first-of-type", ['0', '1', '2', '6'], flags=util.HTML)
        self.assert_selector(markup, "body :last-of-type", ['2', '6', '7', '8'], flags=util.HTML)
        self.assert_selector(markup, "body :only-of-type", ['2', '6'], flags=util.HTML)
        self.assert_selector(markup, "body :nth-of-type(2)", ['3', '4'], flags=util.HTML)
        self.assert_selector(markup, "body :nth-last-of-type(2)", ['4', '5'], flags=util.HTML)
        self.assert_selector(markup, "body :nth-of-type(2n+1)", ['0', '1', '2', '5', '6', '7'], flags=util.HTML)
        # Queried in reverse, so later siblings are scanned before earlier ones are asked about.
        self.assert_selector(
            markup, 'body :is([id="8"], [id="7"], [id="0"]):nth-of-type(n+3)', ['7', '8'], flags=util.HTML
        )

    def test_nth_of_type_namespaces(self):
        """Test that `of-type` selectors count siblings with the same name in different namespaces separately."""

        markup = """
        <root xmlns:a="http://a.com" xmlns:b="http://b.com">
        <a:t id="0"/>
        <b:t id="1"/>
        <a:t id="2"/>
        <b:t id="3"/>
        <t id="4"/>
        </root>
        """

        self.assert_selector(markup, "root > :first-of-type", ['0', '1', '4'], flags=util.XML)
        self.assert_selector(markup, "root > :last-of-type", ['2', '3', '4'], flags=util.XML)

    def test_many_distinct_types(self):
        """Test that siblings with many distinct tag names are scanned once, not once for each tag name."""

        import soupsieve as sv
        from bs4 import BeautifulSoup
        from unittest import mock

        n = 200
        soup = BeautifulSoup('<div>' + ''.join(f'<t{i}></t{i}>' for i in range(n)) + '</div>', 'html.parser')
        get_tag = sv.css_match.CSSMatch.get_tag
        for selector in (':first-of-type', ':last-of-type', ':only-of-type', ':nth-of-type(1)'):
            with mock.patch.object(sv.css_match.CSSMatch, "get_tag", autospec=True, side_effect=get_tag) as patched:
                self.assertEqual(len(sv.select(f'div > {selector}', soup)), n)
            self.assertLessEqual(patched.call_count, 10 * n)

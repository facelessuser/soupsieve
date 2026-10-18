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

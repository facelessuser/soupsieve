"""Test last of type selectors."""
from __future__ import unicode_literals
from .. import util


class TestLastOfType(util.TestCase):
    """Test last of type selectors."""

    def test_last_of_type_at_middle(self):
        """Test last of type that is not the last sibling."""

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
            "p:last-of-type",
            ['10'],
            flags=util.HTML
        )

    def test_last_of_type_at_end(self):
        """Test last of type that is the last sibling."""

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
            "span:last-of-type",
            ['11'],
            flags=util.HTML
        )

    def test_any_last_of_type(self):
        """Test any last of type."""

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
            "body :last-of-type",
            ['10', '11'],
            flags=util.HTML
        )


class TestLastOfTypeQuirks(TestLastOfType):
    """Test last of type selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

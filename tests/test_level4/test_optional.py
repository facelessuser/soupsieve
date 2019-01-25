"""Test optional selectors."""
from __future__ import unicode_literals
from .. import util


class TestOptional(util.TestCase):
    """Test optional selectors."""

    MARKUP = """
    <form>
    <input id="1" type="name" required>
    <input id="2" type="checkbox" required>
    <input id="3" type="email">
    <textarea id="4" name="name" cols="30" rows="10"></textarea>
    <select id="5" name="nm">
        <!-- options -->
    </select>
    </form>
    """

    def test_optional(self):
        """Test optional."""

        self.assert_selector(
            self.MARKUP,
            ":optional",
            ['3', '4', '5'],
            flags=util.HTML
        )

    def test_specific_optional(self):
        """Test specific optional."""

        self.assert_selector(
            self.MARKUP,
            "input:optional",
            ['3'],
            flags=util.HTML
        )


class TestOptionalQuirks(TestOptional):
    """Test optional selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

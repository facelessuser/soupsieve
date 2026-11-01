"""Test required selectors."""
from .. import util


class TestRequired(util.TestCase):
    """Test required selectors."""

    MARKUP = """
    <form>
    <input id="1" type="name" required>
    <input id="2" type="checkbox" required>
    <input id="3" type="email">
    <textarea id="4" name="name" cols="30" rows="10" required></textarea>
    <select id="5" name="nm" required>
        <!-- options -->
    </select>
    </form>
    """

    def test_required(self):
        """Test required."""

        self.assert_selector(
            self.MARKUP,
            ":required",
            ['1', '2', '4', '5'],
            flags=util.HTML
        )

    def test_specific_required(self):
        """Test specific required."""

        self.assert_selector(
            self.MARKUP,
            "input:required",
            ['1', '2'],
            flags=util.HTML
        )

    def test_required_does_not_apply(self):
        """Test that `required` is ignored on input types it does not apply to."""

        markup = """
        <input id="1" type="hidden" required>
        <input id="2" type="range" required>
        <input id="3" type="color" required>
        <input id="4" type="submit" required>
        <input id="5" type="image" required>
        <input id="6" type="reset" required>
        <input id="7" type="BUTTON" required>
        <input id="8" type="text" required>
        <input id="9" type="radio" required>
        <input id="10" type="file" required>
        <input id="11" type="unknown" required>
        """

        self.assert_selector(
            markup,
            ":required",
            ['8', '9', '10', '11'],
            flags=util.HTML
        )

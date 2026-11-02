"""Test optional selectors."""
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

    def test_optional_required_does_not_apply(self):
        """Test that input types `required` does not apply to are optional even with `required`."""

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
            ":optional",
            ['1', '2', '3', '4', '5', '6', '7'],
            flags=util.HTML
        )

    def test_optional_button(self):
        """Test that a `button` is not optional, as `required` does not apply to it (browsers do not agree on this)."""

        markup = """
        <button id="1"></button>
        <button id="2" type="submit"></button>
        <button id="3" required></button>
        """

        self.assert_selector(
            markup,
            ":optional",
            [],
            flags=util.HTML
        )

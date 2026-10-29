"""Test indeterminate selectors."""
from .. import util
from bs4 import BeautifulSoup

IFRAME_TEXT = BeautifulSoup('<iframe><div></div></iframe>', 'html.parser').iframe.text == '<div></div>'


class TestIndeterminate(util.TestCase):
    """Test indeterminate selectors."""

    def test_indeterminate(self):
        """Test indeterminate."""

        markup = """
        <input type="radio" name="" id="radio-no-name1">
        <label>No name 1</label>
        <input type="radio" name="" id="radio-no-name2" checked>
        <label>no name 2</label>
        <div>
          <input type="checkbox" id="checkbox" indeterminate>
          <label for="checkbox">This label starts out lime.</label>
        </div>
        <div>
          <input type="radio" name="test" id="radio1">
          <label for="radio1">This label starts out lime.</label>
          <form>
            <input type="radio" name="test" id="radio2">
            <label for="radio2">This label starts out lime.</label>

            <input type="radio" name="test" id="radio3" checked>
            <label for="radio3">This label starts out lime.</label>

            <input type="radio" name="other" id="radio4">
            <label for="radio4">This label starts out lime.</label>

            <input type="radio" name="other" id="radio5">
            <label for="radio5">This label starts out lime.</label>
          </form>
          <input type="radio" name="test" id="radio6">
          <label for="radio6">This label starts out lime.</label>
        </div>
        """

        self.assert_selector(
            markup,
            ":indeterminate",
            ['checkbox', 'radio1', 'radio6', 'radio4', 'radio5', 'radio-no-name1'],
            flags=util.HTML
        )

    def test_iframe(self):
        """Test indeterminate when `iframe` is involved."""

        markup = """
        <form>
            <input type="radio" name="test" id="radio1">
            <label for="radio1">This label starts out lime.</label>

            <iframe>
            <html>
            <body>
            <input type="radio" name="test" id="radio2" checked>
            <label for="radio2">This label starts out lime.</label>

            <input type="radio" name="other" id="radio3">
            <label for="radio3">This label starts out lime.</label>
            </body>
            </html>
            </iframe></form>"""

        self.assert_selector(
            markup,
            ":indeterminate",
            ['radio1'] if IFRAME_TEXT else ['radio1', 'radio3'],
            flags=util.PYHTML
        )

    def test_indeterminate_many_groups(self):
        """Test indeterminate with several radio button groups in one form, which is only searched once."""

        markup = """
        <form>
            <input type="radio" name="a" id="radio1">
            <input type="radio" name="b" id="radio2">
            <input type="radio" name="b" id="radio3" checked>
            <input type="radio" name="c" id="radio4">
            <input type="checkbox" name="d" id="checkbox1" checked>
            <input type="radio" name="d" id="radio5">
            <input type="radio" name="e" id="radio6">
        </form>
        <form>
            <input type="radio" name="a" id="radio7" checked>
            <input type="radio" name="e" id="radio8">
        </form>
        """

        self.assert_selector(
            markup,
            ":indeterminate",
            ['radio1', 'radio4', 'radio5', 'radio6', 'radio8'],
            flags=util.HTML
        )

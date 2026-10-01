"""Test escapes."""
from .. import util


class TestEscapes(util.TestCase):
    """Test escapes."""

    def test_escapes(self):
        """Test escapes."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo:bar:foobar"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            ".foo\\:bar\\3a foobar",
            ["1"],
            flags=util.HTML
        )

    def test_surrogate_escape_is_replacement(self):
        """A surrogate escape is `U+FFFD`, and so is a code point past Unicode."""

        from soupsieve.css_parser import css_unescape

        self.assertEqual(css_unescape('\\d800'), '\ufffd')
        self.assertEqual(css_unescape('\\DFFF'), '\ufffd')
        self.assertEqual(css_unescape('\\0'), '\ufffd')
        self.assertEqual(css_unescape('\\110000'), '\ufffd')
        self.assertEqual(css_unescape('\\61'), 'a')
        self.assertEqual(css_unescape('\\10FFFF'), '\U0010ffff')
        markup = '<div><p id="1" class="\ufffd">t</p></div>'
        self.assert_selector(markup, '.\\d800', ['1'], flags=util.HTML)

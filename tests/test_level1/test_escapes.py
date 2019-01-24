"""Test escapes."""
from __future__ import unicode_literals
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


class TestEscapesQuirks(TestEscapes):
    """Test escapes with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

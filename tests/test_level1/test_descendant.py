"""Test descendant combinators."""
from __future__ import unicode_literals
from .. import util


class TestDescendants(util.TestCase):
    """Test descendant combinators."""

    def test_descendants(self):
        """Test descendants."""

        self.assert_selector(
            """
            <div>
            <p>Some text <span id="1"> in a paragraph</span>.
            <a id="2" href="http://google.com">Link</a>
            </p>
            </div>
            """,
            "div span",
            ["1"],
            flags=util.HTML
        )


class TestDescendantsQuirks(TestDescendants):
    """Test descendant combinators with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

"""Test descendant combinators."""
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

    def test_long_duplicate_tag_case(self):
        """Test long descendant case."""

        import soupsieve as sv

        for n in (1000, 2000, 4000, 8000):
            self.assertEqual(sv.compile("a" + " " * n + "b").selectors.count, 2)

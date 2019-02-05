"""Test custom selector aliases."""
from __future__ import unicode_literals
from .. import util
import soupsieve as sv


class TestCustomSelectors(util.TestCase):
    """Test custom selector aliases."""

    MARKUP = """
    <body>
    <h1 id="1">Header 1</h1>
    <h2 id="2">Header 2</h2>
    <p id="3"></p>
    <p id="4"><span>child</span></p>
    </body>
    """

    def test_custom_selectors(self):
        """Test custom selectors."""

        custom_selectors = sv.Custom()
        custom_selectors.register(":--headers", "h1, h2, h3, h4, h5, h6")
        custom_selectors.register(":--parent", ":has(> *|*)")

        self.assert_selector(
            self.MARKUP,
            ':--headers',
            ['1', '2'],
            custom=custom_selectors,
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            ':--headers:nth-child(2)',
            ['2'],
            custom=custom_selectors,
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            'p:--parent',
            ['4'],
            custom=custom_selectors,
            flags=util.HTML
        )

    def test_custom_dependency(self):
        """Test custom selector dependency on other custom selectors."""

        custom_selectors = sv.Custom()
        custom_selectors.register(":--parent", ":has(> *|*)")
        custom_selectors.register(":--parent-paragraph", "p:--parent")

        self.assert_selector(
            self.MARKUP,
            ':--parent-paragraph',
            ['4'],
            custom=custom_selectors,
            flags=util.HTML
        )

    def test_bad_custom(self):
        """Test that a bad custom raises a syntax error."""

        custom_selectors = sv.Custom()
        custom_selectors.register(":--parent", ":has(> *|*)")
        custom_selectors.register(":--parent-paragraph", "p:--parent")

        self.assert_raises(':--wrong', SyntaxError, custom=custom_selectors)

    def test_bad_custom_syntax(self):
        """Test that a custom selector with bad syntax in its name fails."""

        custom_selectors = sv.Custom()
        with self.assertRaises(SyntaxError):
            custom_selectors.register(":--parent.", ":has(> *|*)")

    def test_pseudo_class_collision(self):
        """Test that a custom selector cannot match an already existing pseudo-class name."""

        custom_selectors = sv.Custom()

        with self.assertRaises(SyntaxError):
            custom_selectors.register(":hover", ":has(> *|*)")

    def test_custom_collision(self):
        """Test that a custom selector cannot match an already existing custom name."""

        custom_selectors = sv.Custom()
        custom_selectors.register(":--parent", ":has(> *|*)")

        with self.assertRaises(KeyError):
            custom_selectors.register(":--PARENT", "p:--parent")


class TestCustomSelectorsQuirks(TestCustomSelectors):
    """Test custom selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

"""Test custom selector aliases."""
from __future__ import unicode_literals
from .. import util
import soupsieve as sv


class TestAliases(util.TestCase):
    """Test custom selector aliases."""

    MARKUP = """
    <body>
    <h1 id="1">Header 1</h1>
    <h2 id="2">Header 2</h2>
    <p id="3"></p>
    <p id="4"><span>child</span></p>
    </body>
    """

    def test_aliases(self):
        """Test custom selectors."""

        custom_selectors = sv.Aliases()
        custom_selectors.register(":--headers", "h1, h2, h3, h4, h5, h6")
        custom_selectors.register(":--parent", ":has(> *|*)")

        self.assert_selector(
            self.MARKUP,
            ':--headers',
            ['1', '2'],
            aliases=custom_selectors,
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            ':--headers:nth-child(2)',
            ['2'],
            aliases=custom_selectors,
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            'p:--parent',
            ['4'],
            aliases=custom_selectors,
            flags=util.HTML
        )

    def test_alias_dependency(self):
        """Test alias selector dependency on other aliases."""

        custom_selectors = sv.Aliases()
        custom_selectors.register(":--parent", ":has(> *|*)")
        custom_selectors.register(":--parent-paragraph", "p:--parent")

        self.assert_selector(
            self.MARKUP,
            ':--parent-paragraph',
            ['4'],
            aliases=custom_selectors,
            flags=util.HTML
        )

    def test_bad_alias(self):
        """Test that a bad alias raises a syntax error."""

        custom_selectors = sv.Aliases()
        custom_selectors.register(":--parent", ":has(> *|*)")
        custom_selectors.register(":--parent-paragraph", "p:--parent")

        self.assert_raises(':--wrong', SyntaxError, aliases=custom_selectors)

    def test_bad_alias_syntax(self):
        """Test that an alias with bad syntax in its name fails."""

        custom_selectors = sv.Aliases()
        with self.assertRaises(SyntaxError):
            custom_selectors.register(":--parent.", ":has(> *|*)")

    def test_pseudo_class_collision(self):
        """Test that an alias cannot match an already existing pseudo-class name."""

        custom_selectors = sv.Aliases()

        with self.assertRaises(SyntaxError):
            custom_selectors.register(":hover", ":has(> *|*)")

    def test_alias_collision(self):
        """Test that an alias cannot match an already existing alias name."""

        custom_selectors = sv.Aliases()
        custom_selectors.register(":--parent", ":has(> *|*)")

        with self.assertRaises(KeyError):
            custom_selectors.register(":--PARENT", "p:--parent")


class TestAliasesQuirks(TestAliases):
    """Test alias selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

"""Test custom selectors."""
from __future__ import unicode_literals
from . import util
import soupsieve as sv


class TestAliases(util.TestCase):
    """Test custom selectors."""

    def test_aliases(self):
        """Test custom selectors."""

        markup = """
        <body>
        <h1 id="1">Header 1</h1>
        <h2 id="2">Header 2</h2>
        <p id="3"></p>
        <p id="4"><span>child</span></p>
        </body>
        """

        aliases = sv.Aliases()
        aliases.register(":--headers", "h1, h2, h3, h4, h5, h6")
        aliases.register(":--parent", ":has(> *|*)")

        self.assert_selector(
            markup,
            ':--headers',
            ['1', '2'],
            aliases=aliases,
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            ':--headers:nth-child(2)',
            ['2'],
            aliases=aliases,
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            'p:--parent',
            ['4'],
            aliases=aliases,
            flags=util.HTML
        )

    def test_alias_dependency(self):
        """Test alias selector dependency on other aliases."""

        markup = """
        <body>
        <h1 id="1">Header 1</h1>
        <h2 id="2">Header 2</h2>
        <p id="3"></p>
        <p id="4"><span>child</span></p>
        </body>
        """

        aliases = sv.Aliases()
        aliases.register(":--parent", ":has(> *|*)")
        aliases.register(":--parent-paragraph", "p:--parent")

        self.assert_selector(
            markup,
            ':--parent-paragraph',
            ['4'],
            aliases=aliases,
            flags=util.HTML
        )

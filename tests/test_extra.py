"""
Test extra selectors.

Extra patterns that are not in the specification, but may be useful.

```
:contains(text)
```
"""
from . import util


class TestLevel1(util.TestCase):
    """Test level 1 selectors."""

    def test_contains(self):
        """Test tag."""

        markup = """
        <div id="1">
        Testing
        <span id="2"> that </span>
        contains works.
        </div>
        """

        self.assert_selector(
            markup,
            'body span:contains(that)',
            ['2'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            'body span:contains(" that ")',
            ['2'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            'body :contains(" that ")',
            ['1', '2'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            'body :contains( "Testing" )',
            ['1'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            'body :contains(bad)',
            [],
            flags=util.HTML5
        )

    def test_contains_escapes(self):
        """Test tag."""

        markup = """
        <div id="1">Testing<span id="2">
        that</span>contains works.</div>
        """

        self.assert_selector(
            markup,
            'body span:contains("\nthat")',
            ['2'],
            flags=util.HTML5
        )

    def test_contains_cdata(self):
        """Test tag."""

        markup = """
        <div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div>
        """

        self.assert_selector(
            markup,
            'body *:contains("that")',
            ['1'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            '*:contains("that")',
            ['1', '2'],
            flags=util.XML
        )

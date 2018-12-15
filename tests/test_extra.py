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

    def test_attribute_not_equal(self):
        """Test attribute with value that does not equal specified value."""

        markup = """
        <div id="div">
        <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
        <a id="2" href="http://google.com">Link</a>
        <span id="3">Direct child</span>
        <pre id="pre">
        <span id="4">Child 1</span>
        <span id="5">Child 2</span>
        <span id="6">Child 3</span>
        </pre>
        </div>
        """

        # No quotes
        self.assert_selector(
            markup,
            'body [id!=\\35]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

        # Quotes
        self.assert_selector(
            markup,
            "body [id!='5']",
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

        # Double quotes
        self.assert_selector(
            markup,
            'body [id!="5"]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

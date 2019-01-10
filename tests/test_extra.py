"""
Test extra selectors.

Extra patterns that are not in the specification, but may be useful.

```
:contains(text)
[attr!=value]
```
"""
from __future__ import unicode_literals
from . import util


class TestExtra(util.TestCase):
    """Test extra selectors."""

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

    def test_defined(self):
        """Test defined."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
        <div id="0"></div>
        <div-custom id="1"></div-custom>
        <prefix:div id="2"></prefix:div>
        <prefix:div-custom id="3"></prefix:div-custom>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            'body :defined',
            ['0', '2', '3'],
            flags=util.HTML5
        )

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        </head>
        <body>
        <div id="0"></div>
        <div-custom id="1"></div-custom>
        <prefix:div id="2"></prefix:div>
        <!--
        lxml or BeautifulSoup seems to strip away the prefix.
        This is most likely because prefix with no namespace is not really valid.
        XML does allow colons in names, but encourages them to be used for namespaces.
        Do we really care that the prefix is wiped out in XHTML if there is no namespace?
        If we do, we should look into this in the future.
        -->
        <prefix:div-custom id="3"></prefix:div-custom>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            'body :defined',
            ['0', '2'],  # We should get 3, but we don't for reasons stated above.
            flags=util.XHTML
        )

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <html>
        <head>
        </head>
        <body>
        <div id="0"></div>
        <div-custom id="1"></div-custom>
        <prefix:div id="2"></prefix:div>
        <prefix:div-custom id="3"></prefix:div-custom>
        </body>
        </html>
        """

        # Defined is a browser thing.
        # XML doesn't care about defined and this will match nothing in XML.
        self.assert_selector(
            markup,
            'body :defined',
            [],
            flags=util.XML
        )

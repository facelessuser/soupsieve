"""Test root selectors."""
from __future__ import unicode_literals
from .. import util
import soupsieve as sv


class TestRoot(util.TestCase):
    """Test root selectors."""

    MARKUP = """
    <html id="root">
    <head>
    </head>
    <body>
    <div id="div">
    <p id="0" class="somewordshere">Some text <span id="1"> in a paragraph</span>.</p>
    <a id="2" href="http://google.com">Link</a>
    <span id="3" class="herewords">Direct child</span>
    <pre id="pre" class="wordshere">
    <span id="4">Child 1</span>
    <span id="5">Child 2</span>
    <span id="6">Child 3</span>
    </pre>
    </div>
    </body>
    </html>
    """

    MARKUP_IFRAME = """
    <html id="root">
    <head>
    </head>
    <body>
    <div id="div">
    </div>
    <iframe src="https://something.com">
    <html id="root2">
    <head>
    </head>
    <body>
    <div id="div2">
    </div>
    </body>
    </html>
    </iframe>
    <div id="other-div"></div>
    </body>
    </html>
    """

    def test_root(self):
        """Test root."""

        # Root in HTML is `<html>`
        self.assert_selector(
            self.MARKUP,
            ":root",
            ["root"],
            flags=util.HTML
        )

    def test_root_complex(self):
        """Test root within a complex selector."""

        self.assert_selector(
            self.MARKUP,
            ":root > body > div",
            ["div"],
            flags=util.HTML
        )

    def test_no_iframe(self):
        """Test that we don't count `iframe` as root."""

        self.assert_selector(
            self.MARKUP_IFRAME,
            ":root div",
            ["div", "other-div"],
            flags=util.PYHTML
        )

        self.assert_selector(
            self.MARKUP_IFRAME,
            ":root > body > div",
            ["div", "other-div"],
            flags=util.PYHTML
        )

    def test_iframe(self):
        """
        Test that we only count `iframe` as root since the scoped element is the root.

        Not all the parsers treat `iframe` content the same. `html5lib` for instance
        will escape the content in the `iframe`, so we are just going to test the builtin
        Python parser.
        """

        soup = self.soup(self.MARKUP_IFRAME, 'html.parser')

        ids = []
        for el in sv.select(':root div', soup.iframe.html):
            ids.append(el['id'])
        self.assertEqual(sorted(ids), sorted(['div2']))

        ids = []
        for el in sv.select(':root > body > div', soup.iframe.html):
            ids.append(el['id'])
        self.assertEqual(sorted(ids), sorted(['div2']))


class TestRootQuirks(TestRoot):
    """Test root selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

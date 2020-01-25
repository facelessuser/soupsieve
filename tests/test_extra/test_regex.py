"""Test contains selectors."""
from .. import util


class TestRegexContains(util.TestCase):
    """Test regex contains selectors."""

    MARKUP = """
    <body>
    <div id="1">
    Testing
    <span id="2"> that </span>
    contains works.
    </div>
    </body>
    """

    def test_contains_regex(self):
        """Test contains with regex."""

        self.assert_selector(
            self.MARKUP,
            r'body span:contains(/t\w+/)',
            ['2'],
            flags=util.HTML
        )

    def test_contains_regex_no_match(self):
        """Test contains that does not match regex."""

        self.assert_selector(
            self.MARKUP,
            r'body span:contains(/T\w+/)',
            [],
            flags=util.HTML
        )

    def test_contains_regex_flags(self):
        """Test contains using regex flags."""

        self.assert_selector(
            self.MARKUP,
            r'body span:contains(/(?i)T\w+/)',
            ['2'],
            flags=util.HTML
        )


class TestRegexAttribute(util.TestCase):
    """Test regex attribute selectors."""

    MARKUP = """
    <div id="div">
    <p id="0" class="herearesomewords">Some text <span id="1"> in a paragraph</span>.</p>
    <a id="2" href="http://google.com">Link</a>
    <span id="3">Direct child</span>
    <pre id="pre">
    <span id="4">Child 1</span>
    <span id="5">Child 2</span>
    <span id="6">Child 3</span>
    </pre>
    </div>
    """

    MARKUP_LANG = """
    <div id="div">
    <p id="0" lang="en-us">Some text <span id="1"> in a paragraph</span>.</p>
    <a id="2" href="http://google.com">Link</a>
    <span id="3">Direct child</span>
    <pre id="pre">
    <span id="4">Child 1</span>
    <span id="5">Child 2</span>
    <span id="6">Child 3</span>
    </pre>
    </div>
    """

    def test_attribute_begins_regex(self):
        """Test attribute whose value begins with the specified value."""

        self.assert_selector(
            self.MARKUP,
            r"[class^=/h[e]re/]",
            ["0"],
            flags=util.HTML
        )

    def test_attribute_end_regex(self):
        """Test attribute whose value ends with the specified value."""

        self.assert_selector(
            self.MARKUP,
            r"[class$=/w[or]+ds/]",
            ["0"],
            flags=util.HTML
        )

    def test_attribute_contains_regex(self):
        """Test attribute whose value contains the specified value."""

        markup = """
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
        """

        self.assert_selector(
            markup,
            r"[class*=/w[or]+ds/]",
            ["0", "3", "pre"],
            flags=util.HTML
        )

    def test_attribute_equal_regex(self):
        """Test attribute equals a value."""

        self.assert_selector(
            self.MARKUP_LANG,
            r"[lang=/e.*?s/]",
            ["0"],
            flags=util.HTML
        )

    def test_attribute_start_dash_regex(self):
        """Test attribute whose dash separated value starts with the specified value."""

        self.assert_selector(
            self.MARKUP_LANG,
            r"[lang|=/e./]",
            ["0"],
            flags=util.HTML
        )

    def test_attribute_start_dash_regex_fail(self):
        """Test attribute whose dash separated value starts with the specified value."""

        self.assert_selector(
            self.MARKUP_LANG,
            r"[lang|=/E./]",
            [],
            flags=util.HTML
        )

    def test_attribute_start_dash_regex_flags(self):
        """Test attribute whose dash separated value starts with the specified value."""

        self.assert_selector(
            self.MARKUP_LANG,
            r"[lang|=/(?i)E./]",
            ["0"],
            flags=util.HTML
        )

        # Attribute style case selection
        self.assert_selector(
            self.MARKUP_LANG,
            r"[lang|=/E./ i]",
            ["0"],
            flags=util.HTML
        )

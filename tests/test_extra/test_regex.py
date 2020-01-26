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


class TestRegexClass(util.TestCase):
    """Test class selectors."""

    MARKUP = """
    <div>
    <p>Some text <span id="1" class="foo"> in a paragraph</span>.
    <a id="2" class="bar" href="http://google.com">Link</a>
    </p>
    </div>
    """

    def test_class(self):
        """Test class."""

        self.assert_selector(
            self.MARKUP,
            r"./fo{2}/",
            ["1"],
            flags=util.HTML
        )

    def test_multiple_classes(self):
        """Test multiple classes."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        <a id="3" class="foo" href="http://google.com">Link</a>
        <a id="4" class="foo bar" href="http://google.com">Link</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            "a./fo{2}/./b.*/",
            ["4"],
            flags=util.HTML
        )


class TestRegexId(util.TestCase):
    """Test ID selectors."""

    MARKUP = """
    <div>
    <p>Some text <span id="unique"> in a paragraph</span>.
    <a id="2" href="http://google.com">Link</a>
    </p>
    </div>
    """

    def test_id(self):
        """Test ID."""

        self.assert_selector(
            self.MARKUP,
            r"#/u.*/",
            ["unique"],
            flags=util.HTML
        )


class TestRegexType(util.TestCase):
    """Test type selectors with regex."""

    def test_basic_type(self):
        """Test type."""

        self.assert_selector(
            """
            <html>
            <head></head>
            <body>
            <div>
            <p>Some text <span id="1"> in a paragraph</span>.</p>
            <a id="2" href="http://google.com">Link</a>
            </div>
            </body>
            </html>
            """,
            r"body /.*?a.*/",
            ["1", "2"],
            flags=util.HTML
        )


class TestRegexNamespace(util.TestCase):
    """Test namespace selectors."""

    MARKUP = """
    <?xml version="1.0" encoding="UTF-8"?>
    <tag id="root">
      <head id="0"></head>
      <foo:other id="1" xmlns:foo="http://me.com/namespaces/foofoo"
             xmlns:bar="http://me.com/namespaces/foobar">
      <foo:head id="2">
        <foo:title id="3"></foo:title>
        <bar:title id="4"></bar:title>
      </foo:head>
      <body id="5">
        <foo:e1 id="6"></foo:e1>
        <bar:e1 id="7"></bar:e1>
        <e1 id="8"></e1>
        <foo:e2 id="9"></foo:e2>
        <bar:e2 id="10"></bar:e2>
        <e2 id="11"></e2>
        <foo:e3 id="12"></foo:e3>
        <bar:e3 id="13"></bar:e3>
        <e3 id="14"></e3>
      </body>
      </foo:other>
      <other id="15" xmlns="http://me.com/namespaces/other">
        <e4 id="16">Inherit</er>
      </other>
    </tag>
    """

    MARKUP_ATTR = """
    <div>
      <h1>A contrived example</h1>
      <svg viewBox="0 0 20 32" class="icon icon-1">
        <use id="0" xlink:href="images/sprites.svg#icon-undo"></use>
      </svg>
      <svg viewBox="0 0 30 32" class="icon icon-2">
        <use id="1" xlink:href="images/sprites.svg#icon-redo"></use>
      </svg>
      <svg viewBox="0 0 40 32" class="icon icon-3">
        <use id="2" xlink:href="images/sprites.svg#icon-forward"></use>
      </svg>
      <svg viewBox="0 0 50 32" class="icon icon-4">
        <use id="3" xlink:href="other/sprites.svg#icon-reply"></use>
      </svg>
      <svg viewBox="0 0 50 32" class="icon icon-4">
        <use id="4" :href="other/sprites.svg#icon-reply"></use>
      </svg>
      <svg viewBox="0 0 50 32" class="icon icon-4">
        <use id="5" other:href="other/sprites.svg#icon-reply" xlink:other="value doesn't match"></use>
      </svg>
    </div>
    """

    def wrap_xlink(self, content, xhtml=False):
        """Wrap with `xlink`."""

        xhtml_ns = 'xmlns="http://www.w3.org/1999/xhtml"' if xhtml else ''

        return """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html {} xmlns:xlink="http://www.w3.org/1999/xlink">
        <head>
        </head>
        <body>
        {}
        </body>
        </html>
        """.format(xhtml_ns, content)

    def test_namespace_regex(self):
        """Test namespace."""

        self.assert_selector(
            self.MARKUP,
            r"/fo{2}/|title",
            ["3"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

        self.assert_selector(
            self.MARKUP,
            r"/(?:foo|bar)/|title",
            ["3", "4"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

    def test_namespace_case_regex(self):
        """Test that namespaces are always case sensitive."""

        # These won't match
        self.assert_selector(
            self.MARKUP,
            r"/FO{2}/|title",
            [],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

        # These won't match
        self.assert_selector(
            self.MARKUP,
            r"/(?i)FO{2}/|title",
            ["3"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

    def test_attribute_namespace_xml(self):
        """Test attribute namespace in XML."""

        self.assert_selector(
            self.wrap_xlink(self.MARKUP_ATTR),
            r'[/x.*/|href*=forw],[/x.*/|href="images/sprites.svg#icon-redo"]',
            ['1', '2'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.XHTML
        )


class TestRegexAttributeName(util.TestCase):
    """Test attribute selectors."""

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

    def test_attribute_begins(self):
        """Test attribute whose value begins with the specified value."""

        self.assert_selector(
            self.MARKUP,
            r"[/clas{2}/^=here]",
            ["0"],
            flags=util.HTML
        )

    def test_attribute_begins_wild(self):
        """Test attribute whose value begins with the specified value."""

        self.assert_selector(
            self.MARKUP,
            r"[/.*/^=here]",
            ["0"],
            flags=util.HTML
        )

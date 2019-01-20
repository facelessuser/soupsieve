"""
Test selectors level 1.

```
E
E F
E, F
.class
#elementID
:link
:active
:visited
```
"""
from __future__ import unicode_literals
from . import util


class TestLevel1(util.TestCase):
    """Test level 1 selectors."""

    def test_tag(self):
        """Test tag."""

        self.assert_selector(
            """
            <div>
            <p>Some text <span id="1"> in a paragraph</span>.</p>
            <a id="2" href="http://google.com">Link</a>
            </div>
            """,
            "span",
            ["1"],
            flags=util.HTML
        )

    def test_tag_html(self):
        """Test tag for HTML."""

        markup = """
        <Tag id="1">
        <tag id="2"></tag>
        <TAG id="3"></TAG>
        </Tag>
        """

        self.assert_selector(
            markup,
            "tag",
            ["1", "2", "3"],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            "Tag",
            ["1", "2", "3"],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            "TAG",
            ["1", "2", "3"],
            flags=util.HTML
        )

    def test_tag_xhtml(self):
        """Test tag for XHTML."""

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        </head>
        <body>
        <Tag id="1">
        <tag id="2"></tag>
        <TAG id="3"></TAG>
        </Tag>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "tag",
            ["2"],
            flags=util.XHTML
        )

        self.assert_selector(
            markup,
            "Tag",
            ["1"],
            flags=util.XHTML
        )

        self.assert_selector(
            markup,
            "TAG",
            ["3"],
            flags=util.XHTML
        )

    def test_tag_xml(self):
        """Test tag for XML."""

        markup = """
        <Tag id="1">
        <tag id="2"></tag>
        <TAG id="3"></TAG>
        </Tag>
        """

        self.assert_selector(
            markup,
            "tag",
            ["2"],
            flags=util.XML
        )

        self.assert_selector(
            markup,
            "Tag",
            ["1"],
            flags=util.XML
        )

        self.assert_selector(
            markup,
            "TAG",
            ["3"],
            flags=util.XML
        )

    def test_multiple_tags(self):
        """Test multiple selectors."""

        self.assert_selector(
            """
            <div>
            <p>Some text <span id="1"> in a paragraph</span>.
            <a id="2" href="http://google.com">Link</a>
            </p>
            </div>
            """,
            "span, a",
            ["1", "2"],
            flags=util.HTML
        )

    def test_invalid_start_comma(self):
        """Test that selectors cannot start with a comma."""

        self.assert_raises(', p', SyntaxError)

    def test_invalid_end_comma(self):
        """Test that selectors cannot end with a comma."""

        self.assert_raises('p,', SyntaxError)

    def test_invalid_double_comma(self):
        """Test that selectors cannot have double combinators."""

        self.assert_raises('div,, a', SyntaxError)

    def test_child(self):
        """Test child."""

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

    def test_id(self):
        """Test ID."""

        markup = """
        <div>
        <p>Some text <span id="1"> in a paragraph</span>.
        <a id="2" href="http://google.com">Link</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            "#\\31",
            ["1"],
            flags=util.HTML
        )

    def test_tag_and_id(self):
        """Test tag and ID."""

        markup = """
        <div>
        <p>Some text <span id="1"> in a paragraph</span>.
        <a id="2" href="http://google.com">Link</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            "a#\\32",
            ["2"],
            flags=util.HTML
        )

    def test_malformed_id(self):
        """Test malformed ID."""

        # Malformed id
        self.assert_raises('td#.some-class', SyntaxError)

    def test_class(self):
        """Test class."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            ".foo",
            ["1"],
            flags=util.HTML
        )

    def test_tag_and_class(self):
        """Test tag and class."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            "a.bar",
            ["2"],
            flags=util.HTML
        )

    def test_malformed_class(self):
        """Test malformed class."""

        # Malformed class
        self.assert_raises('td.+#some-id', SyntaxError)

    def test_class_xhtml(self):
        """Test tag and class with XHTML since internally classes are stored different for XML."""

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        </head>
        <body>
        <div>
        <p>Some text <span id="1" class="foo"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        </p>
        </div>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            ".foo",
            ["1"],
            flags=util.XHTML
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
            "a.foo.bar",
            ["4"],
            flags=util.HTML
        )

    def test_escapes(self):
        """Test escapes."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo:bar:foobar"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            ".foo\\:bar\\3a foobar",
            ["1"],
            flags=util.HTML
        )

    def test_invalid_syntax(self):
        """Test invalid syntax."""

        self.assert_raises('div?', SyntaxError)

    def test_link(self):
        """Test link (all links are unvisited)."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo:bar:foobar"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        <a id="3">Placeholder text.</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            ":link",
            ["2"],
            flags=util.HTML
        )

    def test_tag_and_link(self):
        """Test link and tag (all links are unvisited)."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo:bar:foobar"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        <a id="3">Placeholder text.</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            "a:link",
            [],
            flags=util.XML
        )

    def test_active(self):
        """Test active."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo:bar:foobar"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        <a id="3">Placeholder text.</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            "a:active",
            [],
            flags=util.HTML
        )

    def test_visited(self):
        """Test visited."""

        markup = """
        <div>
        <p>Some text <span id="1" class="foo:bar:foobar"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        <a id="3">Placeholder text.</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            "a:visited",
            [],
            flags=util.HTML
        )

    def test_malformed_pseudo_class(self):
        """Test malformed class."""

        # Malformed pseudo-class
        self.assert_raises('td:#id', SyntaxError)

    def test_pseudo_class_not_implemented(self):
        """Test pseudo-class that is not implemented."""

        self.assert_raises(':not-implemented', NotImplementedError)


class TestLevel1Quirks(TestLevel1):
    """Test level 1 with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

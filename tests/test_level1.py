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
            flags=util.HTML5
        )

    def test_tags(self):
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
            flags=util.HTML5
        )

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
            flags=util.HTML5
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
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "a#\\32",
            ["2"],
            flags=util.HTML5
        )

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
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "a.bar",
            ["2"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            ".foo",
            ["1"],
            flags=util.XHTML
        )

    def test_classes(self):
        """Test classes."""

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
            flags=util.HTML5
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
            flags=util.HTML5
        )

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
            flags=util.HTML5
        )

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
            flags=util.HTML5
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
            flags=util.HTML5
        )

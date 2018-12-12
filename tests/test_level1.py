"""
Test selectors level 1.

```
E
E F
E, F
.class
#elementID
```
Not supported (with current opinions or plans the matter):

- `:link`: visited or un-visited links have no meaning outside a browser, just search for `:is(a,area,link)[href]` to
  target links. At most, the possibility of supporting the `:link` as an alias for `:link` may be considered in the
  future as technically, all links are un-visited in our scenario.

- `:active`: No elements in our environment can be "active", so this makes no sense in our context.
"""
from . import util
import soupsieve as sv


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
            flags=sv.HTML5
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
            flags=sv.HTML5
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
            flags=sv.HTML5
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
            "#1",
            ["1"],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            "a#2",
            ["2"],
            flags=sv.HTML5
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
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            "a.bar",
            ["2"],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            ".foo",
            ["1"],
            flags=sv.XHTML
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
            flags=sv.HTML5
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
            flags=sv.HTML5
        )

"""
Test selectors level 2.

```
*
:first-child
E > F
E + F
[foo]
[foo='bar']
[foo~='bar']
[foo|='en']
```

Not supported (with current opinions or plans the matter):

- `:lang(en)`: In documents, `:lang()` can take into considerations information in `meta` and other things in the
  header. At this point, there are no plans to implement this. If a reasonable proposal was introduced on how to
  support this, it may be considered.

- `:hover`: Items cannot be hovered in our environment, so this has little meaning and will not be implemented.

- `:focus`: Items cannot be focused in our environment, so this has little meaning and will not be implemented.
"""
from . import util
import soupsieve as sv


class TestLevel2(util.TestCase):
    """Test level 2 selectors."""

    def test_direct_child(self):
        """Test direct child."""

        markup = """
        <div>
        <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
        <a id="2" href="http://google.com">Link</a>
        <span id="3">Direct child</span>
        <pre>
        <span id="4">Child 1</span>
        <span id="5">Child 2</span>
        <span id="6">Child 3</span>
        </pre>
        </div>
        """

        # Spaces
        self.assert_selector(
            markup,
            "div > span",
            ["3"],
            flags=sv.HTML5
        )

        # No spaces
        self.assert_selector(
            markup,
            "div>span",
            ["3"],
            flags=sv.HTML5
        )

    def test_direct_sibling(self):
        """Test direct sibling."""

        markup = """
        <div>
        <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
        <a id="2" href="http://google.com">Link</a>
        <span id="3">Direct child</span>
        <pre>
        <span id="4">Child 1</span>
        <span id="5">Child 2</span>
        <span id="6">Child 3</span>
        </pre>
        </div>
        """

        # Spaces
        self.assert_selector(
            markup,
            "span + span",
            ["5", "6"],
            flags=sv.HTML5
        )

        # No spaces
        self.assert_selector(
            markup,
            "span+span",
            ["5", "6"],
            flags=sv.HTML5
        )

        # Complex
        self.assert_selector(
            markup,
            "span#4 + span#5",
            ["5"],
            flags=sv.HTML5
        )

    def test_wild_tag(self):
        """Test wild tag."""

        self.assert_selector(
            """
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
            """,
            "body *",
            ["0", "1", "2", "3", "4", "5", "6", "div", "pre"],
            flags=sv.HTML5
        )

    def test_attribute(self):
        """Test attribute."""

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

        self.assert_selector(
            markup,
            "[href]",
            ["2"],
            flags=sv.HTML5
        )

        # With spaces
        self.assert_selector(
            markup,
            "[   href   ]",
            ["2"],
            flags=sv.HTML5
        )

    def test_multi_attribute(self):
        """Test multiple attribute."""

        self.assert_selector(
            """
            <div id="div">
            <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
            <a id="2" href="http://google.com">Link</a>
            <span id="3">Direct child</span>
            <pre id="pre">
            <span id="4" class="test">Child 1</span>
            <span id="5" class="test" data-test="test">Child 2</span>
            <span id="6">Child 3</span>
            <span id="6">Child 3</span>
            </pre>
            </div>
            """,
            "span[id].test[data-test=test]",
            ["5"],
            flags=sv.HTML5
        )

    def test_attribute_equal(self):
        """Test attribute with value that equals specified value."""

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
            '[id=5]',
            ["5"],
            flags=sv.HTML5
        )

        # Single quoted
        self.assert_selector(
            markup,
            "[id='5']",
            ["5"],
            flags=sv.HTML5
        )

        # Double quoted
        self.assert_selector(
            markup,
            '[id="5"]',
            ["5"],
            flags=sv.HTML5
        )

        # With spaces
        self.assert_selector(
            markup,
            '[  id  =  "5"  ]',
            ["5"],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            '[ID="5"]',
            ["5"],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            '[  id  =  "5"  ]',
            ["5"],
            flags=sv.HTML
        )

        self.assert_selector(
            markup,
            '[ID="5"]',
            ["5"],
            flags=sv.HTML
        )

        self.assert_selector(
            '<span bad="5"></span>',
            '[  id  =  "5"  ]',
            [],
            flags=sv.HTML
        )

    def test_attribute_type(self):
        """Type is treated as case insensitive in HTML."""

        markup = """
        <html>
        <body>
        <div id="div">
        <p type="TEST" id="0">Some text <span id="1"> in a paragraph</span>.</p>
        <a type="test" id="2" href="http://google.com">Link</a>
        <span id="3">Direct child</span>
        <pre id="pre">
        <span id="4">Child 1</span>
        <span id="5">Child 2</span>
        <span id="6">Child 3</span>
        </pre>
        </div>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            '[type="test"]',
            ["0", '2'],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            '[type="test"]',
            ['2'],
            flags=sv.XML
        )

    def test_attribute_start_dash(self):
        """Test attribute whose dash separated value starts with the specified value."""

        self.assert_selector(
            """
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
            """,
            "[lang|=en]",
            ["0"],
            flags=sv.HTML5
        )

    def test_attribute_contains_space(self):
        """Test attribute whose space separated list contains the specified value."""

        markup = """
        <div id="div">
        <p id="0" class="test1 test2 test3">Some text <span id="1"> in a paragraph</span>.</p>
        <a id="2" href="http://google.com">Link</a>
        <span id="3">Direct child</span>
        <pre id="pre" class="test-a test-b">
        <span id="4">Child 1</span>
        <span id="5">Child 2</span>
        <span id="6">Child 3</span>
        </pre>
        </div>
        """

        # Middle of list
        self.assert_selector(
            markup,
            "[class~=test2]",
            ["0"],
            flags=sv.HTML5
        )

        # Start of list
        self.assert_selector(
            markup,
            "[class~=test-a]",
            ["pre"],
            flags=sv.HTML5
        )

        # End of list
        self.assert_selector(
            markup,
            "[class~=test-b]",
            ["pre"],
            flags=sv.HTML5
        )

    def test_first_child(self):
        """Test first child."""

        self.assert_selector(
            """
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
            """,
            "span:first-child",
            ["1", "4"],
            flags=sv.HTML5
        )

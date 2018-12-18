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
:hover
:focus
:lang(en)
```
"""
from . import util


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
            flags=util.HTML5
        )

        # No spaces
        self.assert_selector(
            markup,
            "div>span",
            ["3"],
            flags=util.HTML5
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
            flags=util.HTML5
        )

        # No spaces
        self.assert_selector(
            markup,
            "span+span",
            ["5", "6"],
            flags=util.HTML5
        )

        # Complex
        self.assert_selector(
            markup,
            "span#\\34 + span#\\35",
            ["5"],
            flags=util.HTML5
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
            flags=util.HTML5
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
            flags=util.HTML5
        )

        # With spaces
        self.assert_selector(
            markup,
            "[   href   ]",
            ["2"],
            flags=util.HTML5
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
            flags=util.HTML5
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
            '[id=\\35]',
            ["5"],
            flags=util.HTML5
        )

        # Single quoted
        self.assert_selector(
            markup,
            "[id='5']",
            ["5"],
            flags=util.HTML5
        )

        # Double quoted
        self.assert_selector(
            markup,
            '[id="5"]',
            ["5"],
            flags=util.HTML5
        )

        # With spaces
        self.assert_selector(
            markup,
            '[  id  =  "5"  ]',
            ["5"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            '[ID="5"]',
            ["5"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            '[  id  =  "5"  ]',
            ["5"],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            '[ID="5"]',
            ["5"],
            flags=util.HTML
        )

        self.assert_selector(
            '<span bad="5"></span>',
            '[  id  =  "5"  ]',
            [],
            flags=util.HTML
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
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            '[type="test"]',
            ['2'],
            flags=util.XML
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
            flags=util.HTML5
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
            flags=util.HTML5
        )

        # Start of list
        self.assert_selector(
            markup,
            "[class~=test-a]",
            ["pre"],
            flags=util.HTML5
        )

        # End of list
        self.assert_selector(
            markup,
            "[class~=test-b]",
            ["pre"],
            flags=util.HTML5
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
            flags=util.HTML5
        )

    def test_hover(self):
        """Test hover."""

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
            "a:hover",
            [],
            flags=util.HTML5
        )

    def test_focus(self):
        """Test focus."""

        markup = """
        <form action="#">
          <fieldset id='a' disabled>
            <legend>
              Simple fieldset <input type="radio" id="1" checked>
              <fieldset id='b' disabled>
                <legend>Simple fieldset <input type="radio" id="2" checked></legend>
                <input type="radio" id="3" checked>
                <label for="radio">radio</label>
              </fieldset>
            </legend>
            <fieldset id='c' disabled>
              <legend>Simple fieldset <input type="radio" id="4" checked></legend>
              <input type="radio" id="5" checked>
              <label for="radio">radio</label>
            </fieldset>
            <input type="radio" id="6" checked>
            <label for="radio">radio</label>
          </fieldset>
          <optgroup id="opt-enable">
            <option id="7" disabled>option</option>
          </optgroup>
          <optgroup id="8" disabled>
            <option id="9">option</option>
          </optgroup>
          <a href="" id="link">text</a>
        </form>
        """

        self.assert_selector(
            markup,
            "input:focus",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "input:not(:focus)",
            ["1", "2", "3", "4", "5", "6"],
            flags=util.HTML5
        )

    def test_lang(self):
        """Test language."""

        markup = """
        <div lang="de-DE">
            <p id="1"></p>
        </div>
        <div lang="de-DE-1996">
            <p id="2"></p>
        </div>
        <div lang="de-Latn-DE">
            <p id="3"></p>
        </div>
        <div lang="de-Latf-DE">
            <p id="4"></p>
        </div>
        <div lang="de-Latn-DE-1996">
            <p id="5"></p>
        </div>
        <p id="6" lang="de-DE"></p>
        """

        self.assert_selector(
            markup,
            "p:lang(de)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

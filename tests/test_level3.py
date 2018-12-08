"""
Test selectors level 3.

```
namespace|*
[foo^='bar']
[foo$='bar']
[foo*='bar']
:not(s)
E ~ F
:root
:empty
:last-child
:only-child
:first-of-type
:last-of-type
:only-of-type
:nth-child(an+b)
:nth-last-child(an+b)
:nth-of-type(an+b)
:nth-of-last-type(an+b)
```

Not supported (with current opinions or plans the matter):

- `:target`: Elements cannot be targeted in our environment, so this will not be implemented.

- `:enabled` / `:disabled`: There are currently no plans to implement this.

- `:checked`: Checked could be complicated to implement. Would you select the first item in a `<select>` tag if no
  option is specified to be selected? Or would you consider this something that occurs when the document is live in the
  browser?  There would need to be some considerations. What if a user has selected multiple radio boxes on accident?
  Is this even useful in the context of how Soup Sieve would be used?
"""
from . import util
import soupsieve as sv


class TestLevel3(util.TestCase):
    """Test level 3 selectors."""

    def test_distant_sibling(self):
        """Test distant sibling."""

        self.assert_selector(
            """
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
            """,
            "p ~ span",
            ["3"],
            mode=sv.HTML5
        )

    def test_not(self):
        """Test not."""

        markup = """
        <div>
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
            'div :not([id="1"])',
            ["0", "2", "3", "4", "5", "6", "pre"],
            mode=sv.HTML5
        )

        self.assert_selector(
            markup,
            'span:not([id="1"])',
            ["3", "4", "5", "6"],
            mode=sv.HTML5
        )

    def test_attribute_begins(self):
        """Test attribute whose value begins with the specified value."""

        self.assert_selector(
            """
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
            """,
            "[class^=here]",
            ["0"],
            mode=sv.HTML5
        )

    def test_attribute_end(self):
        """Test attribute whose value ends with the specified value."""

        self.assert_selector(
            """
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
            """,
            "[class$=words]",
            ["0"],
            mode=sv.HTML5
        )

    def test_attribute_contains(self):
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
            "[class*=words]",
            ["0", "3", "pre"],
            mode=sv.HTML5
        )

    def test_root(self):
        """Test root."""

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

        # Root in HTML is `<html>`
        self.assert_selector(
            markup,
            ":root > body > div",
            ["div"],
            mode=sv.HTML5
        )

    def test_empty(self):
        """Test empty."""

        markup = """
        <div id="div">
        <p id="0" class="somewordshere">Some text <span id="1"> in a paragraph</span>.</p>
        <a id="2" href="http://google.com">Link</a>
        <span id="3" class="herewords">Direct child</span>
        <pre id="pre" class="wordshere">
        <span id="4"> <!-- comment --> </span>
        <span id="5"> </span>
        <span id="6"></span>
        <span id="7"><span id="8"></span></span>
        </pre>
        </div>
        """

        self.assert_selector(
            markup,
            "body :empty",
            ["4", "5", "6", "8"],
            mode=sv.HTML5
        )

    def test_last_child(self):
        """Test last child."""

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
            "span:last-child",
            ["1", "6"],
            mode=sv.HTML5
        )

    def test_only_child(self):
        """Test only child."""

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
            "span:only-child",
            ["1"],
            mode=sv.HTML5
        )

    def test_namespace(self):
        """Test namespace."""

        markup = """
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

        self.assert_selector(
            markup,
            "foo|title",
            ["3"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            mode=sv.XML
        )

        self.assert_selector(
            markup,
            "bar|*",
            ["4", "7", "10", "13"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            mode=sv.XML
        )

        self.assert_selector(
            markup,
            "|head",
            ["0"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            mode=sv.XML
        )

        self.assert_selector(
            markup,
            "*|e2",
            ["9", "10", "11"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            mode=sv.XML
        )

        # Because we employ level 4 selectors
        # E, when no default namespace is defined, will be read as *|E.
        self.assert_selector(
            markup,
            "e3",
            ["12", "13", "14"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            mode=sv.XML
        )

        # Now that we apply a default namespace. Null space.
        self.assert_selector(
            markup,
            "e3",
            ["14"],
            namespaces={
                "": "",
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            mode=sv.XML
        )

        self.assert_selector(
            markup,
            "head",
            ["0"],
            namespaces={
                "": "",
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            mode=sv.XML
        )

        # Because no prefix is specified for "other" in the above document,
        # `e4` inherits the other namespace. The prefix in this case doesn't matter.
        # We specify `other` as prefix in our CSS just so we can use it to target the element.
        self.assert_selector(
            markup,
            "e4",
            [],
            namespaces={
                "": "",
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar",
                "other": "http://me.com/namespaces/other"
            },
            mode=sv.XML
        )

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
:target
:checked
:enabled
:disabled
```
"""
from . import util


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
            flags=util.HTML5
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
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            'div :NOT([id="1"])',
            ["0", "2", "3", "4", "5", "6", "pre"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            'span:not([id="1"])',
            ["3", "4", "5", "6"],
            flags=util.HTML5
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
            flags=util.HTML5
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
            flags=util.HTML5
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
            flags=util.HTML5
        )

    def test_root(self):
        """Test root."""

        markup = """
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

        # Root in HTML is `<html>`
        self.assert_selector(
            markup,
            ":root",
            ["root"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            ":root > body > div",
            ["div"],
            flags=util.HTML5
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
            flags=util.HTML5
        )

    def test_last_child(self):
        """Test last child."""

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
            "span:last-child",
            ["1", "6"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "span:LAST-CHILD",
            ["1", "6"],
            flags=util.HTML5
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
            flags=util.HTML5
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
            flags=util.XML
        )

        self.assert_selector(
            markup,
            "bar|*",
            ["4", "7", "10", "13"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

        self.assert_selector(
            markup,
            "|head",
            ["0"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

        self.assert_selector(
            markup,
            "*|e2",
            ["9", "10", "11"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
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
            flags=util.XML
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
            flags=util.XML
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
            flags=util.XML
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
            flags=util.XML
        )

    def test_attribute_namespace(self):
        """Test attribute namespace."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        </head>
        <body>
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
            <use id="5" other:href="other/sprites.svg#icon-reply"></use>
          </svg>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            '[xlink|href*=forw],[xlink|href="images/sprites.svg#icon-redo"]',
            ['1', '2'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            '[xlink\\:href*=forw],[xlink|href="images/sprites.svg#icon-redo"]',
            ['1', '2'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            '[xlink\\:nomatch*=forw]',
            [],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            '[bad|href*=forw]',
            [],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            '[\\:href]',
            ['4'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

    def test_attribute_namespace_xhtml(self):
        """Test attribute namespace in XHTML."""

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html xmlns:xlink="http://www.w3.org/1999/xlink">
        <head>
        </head>
        <body>
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
            <use id="5" other:href="other/sprites.svg#icon-reply"></use>
          </svg>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            '[xlink|href*=forw],[xlink|href="images/sprites.svg#icon-redo"]',
            ['1', '2'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.XHTML
        )

    def test_first_of_type(self):
        """Test first of type."""

        markup = """
        <p id="0"></p>
        <p id="1"></p>
        <span id="2"></span>
        <span id="3"></span>
        <span id="4"></span>
        <span id="5"></span>
        <span id="6"></span>
        <p id="7"></p>
        <p id="8"></p>
        <p id="9"></p>
        <p id="10"></p>
        <span id="11"></span>
        """

        self.assert_selector(
            markup,
            "p:first-of-type",
            ['0'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "span:first-of-type",
            ['2'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "body :first-of-type",
            ['0', '2'],
            flags=util.HTML5
        )

    def test_last_of_type(self):
        """Test last of type."""

        markup = """
        <p id="0"></p>
        <p id="1"></p>
        <span id="2"></span>
        <span id="3"></span>
        <span id="4"></span>
        <span id="5"></span>
        <span id="6"></span>
        <p id="7"></p>
        <p id="8"></p>
        <p id="9"></p>
        <p id="10"></p>
        <span id="11"></span>
        """

        self.assert_selector(
            markup,
            "p:last-of-type",
            ['10'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "span:last-of-type",
            ['11'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "body :last-of-type",
            ['10', '11'],
            flags=util.HTML5
        )

    def test_only_of_type(self):
        """Test only of type."""

        markup = """
        <div id="0">
            <p id="1"></p>
        </div>
        <span id="2"></span>
        <span id="3"></span>
        <p id="4"></p>
        <span id="5"></span>
        <span id="6"></span>
        <div>
            <p id="7"></p>
            <p id="8"></p>
        </div>
        """

        self.assert_selector(
            markup,
            "p:only-of-type",
            ['1', '4'],
            flags=util.HTML5
        )

    def test_nth_child(self):
        """Test `nth` child."""

        markup = """
        <p id="0"></p>
        <p id="1"></p>
        <span id="2"></span>
        <span id="3"></span>
        <span id="4"></span>
        <span id="5"></span>
        <span id="6"></span>
        <p id="7"></p>
        <p id="8"></p>
        <p id="9"></p>
        <p id="10"></p>
        <span id="11"></span>
        """

        self.assert_selector(
            markup,
            "p:nth-child(2n-5)",
            ['0', '8', '10']
        )

        self.assert_selector(
            markup,
            "p:NTH-CHILD(2n-5)",
            ['0', '8', '10']
        )

        self.assert_selector(
            markup,
            "p:nth-child(-2n+20)",
            ['1', '7', '9']
        )

        self.assert_selector(
            markup,
            "p:nth-child(50n-20)",
            []
        )

        self.assert_selector(
            markup,
            "p:nth-child(-2n-2)",
            []
        )

        self.assert_selector(
            markup,
            "p:nth-child(-2)",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:nth-child(2)",
            ['1'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:nth-child(9n - 1)",
            ['7'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:nth-child(2n + 1)",
            ['0', '8', '10'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:nth-child(-n+3)",
            ['0', '1'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "span:nth-child(-n+3)",
            ['2'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "body *:nth-child(-n+3)",
            ['0', '1', '2'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:nth-child(odd)",
            ['0', '8', '10'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:nth-child(even)",
            ['1', '7', '9'],
            flags=util.HTML5
        )

    def test_nth_last_child(self):
        """Test `nth` last child."""

        markup = """
        <p id="0"></p>
        <p id="1"></p>
        <span id="2"></span>
        <span id="3"></span>
        <span id="4"></span>
        <span id="5"></span>
        <span id="6"></span>
        <p id="7"></p>
        <p id="8"></p>
        <p id="9"></p>
        <p id="10"></p>
        <span id="11"></span>
        """

        self.assert_selector(
            markup,
            "p:nth-last-child(2)",
            ['10'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:nth-last-child(2n + 1)",
            ['1', '7', '9'],
            flags=util.HTML5
        )

    def test_nth_of_type(self):
        """Test `nth` of type."""

        markup = """
        <p id="0"></p>
        <p id="1"></p>
        <span id="2"></span>
        <span id="3"></span>
        <span id="4"></span>
        <span id="5"></span>
        <span id="6"></span>
        <p id="7"></p>
        <p id="8"></p>
        <p id="9"></p>
        <p id="10"></p>
        <span id="11"></span>
        """

        self.assert_selector(
            markup,
            "p:nth-of-type(3)",
            ['7'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:nth-of-type(2n + 1)",
            ['0', '7', '9'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "span:nth-of-type(2n + 1)",
            ['2', '4', '6'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "body :nth-of-type(2n + 1)",
            ['0', '2', '4', '6', '7', '9'],
            flags=util.HTML5
        )

    def test_nth_last_of_type(self):
        """Test `nth` last of type."""

        markup = """
        <p id="0"></p>
        <p id="1"></p>
        <span id="2"></span>
        <span id="3"></span>
        <span id="4"></span>
        <span id="5"></span>
        <span id="6"></span>
        <p id="7"></p>
        <p id="8"></p>
        <p id="9"></p>
        <p id="10"></p>
        <span id="11"></span>
        """

        self.assert_selector(
            markup,
            "p:nth-last-of-type(3)",
            ['8'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:nth-last-of-type(2n + 1)",
            ['1', '8', '10'],
            flags=util.HTML5
        )

    def test_checked(self):
        """Test checked."""

        markup = """
        <div>
          <input type="radio" name="my-input" id="yes" checked>
          <label for="yes">Yes</label>

          <input type="radio" name="my-input" id="no">
          <label for="no">No</label>
        </div>

        <div>
          <input type="checkbox" name="my-checkbox" id="opt-in" checked>
          <label for="opt-in">Check me!</label>
        </div>

        <select name="my-select" id="fruit">
          <option id="1" value="opt1">Apples</option>
          <option id="2" value="opt2" selected>Grapes</option>
          <option id="3" value="opt3">Pears</option>
        </select>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['yes', 'opt-in', '2'],
            flags=util.HTML5
        )

    def test_disabled(self):
        """
        Test disabled.

        Form elements that have `disabled`.
        `option` that is child of disabled `optgroup`.
        Form elements that are children of a disabled `fieldset`, but not it's `legend`.
        """

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
          <optgroup>
            <option id="7" disabled>option</option>
          </optgroup>
          <optgroup id="8" disabled>
            <option id="9">option</option>
          </optgroup>
        </form>
        """

        markup2 = """
        <form action="#">
          <fieldset id='a' disabled>
            <legend>
              Simple fieldset <input type="radio" id="1" checked>
              <fieldset id='b'>
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
          <optgroup>
            <option id="7" disabled>option</option>
          </optgroup>
          <optgroup id="8" disabled>
            <option id="9">option</option>
          </optgroup>
        </form>
        """

        self.assert_selector(
            markup,
            ":disabled",
            ['3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup2,
            ":disabled",
            ['4', '5', '6', '7', '8', '9', 'a', 'c'],
            flags=util.HTML5
        )

    def test_enable(self):
        """
        Test enable.

        `:any-link`
        Form elements that have `disabled`.
        Form elements that are children of a disabled `fieldset`, but not it's `legend`.
        """

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

        markup2 = """
        <form action="#">
          <fieldset id='a' disabled>
            <legend>
              Simple fieldset <input type="radio" id="1" checked>
              <fieldset id='b'>
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
            ":enabled",
            ['1', '2', 'opt-enable', 'link'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup2,
            ":enabled",
            ['1', '2', 'opt-enable', 'b', '3', 'link'],
            flags=util.HTML5
        )

    def test_target(self):
        """Test target."""

        markup = """
        <div>
        <h2 id="head-1">Header 1</h1>
        <div><p>content</p></div>
        <h2 id="head-2">Header 2</h1>
        <div><p>content</p></div>
        </div>
        """

        self.assert_selector(
            markup,
            "#head-2:target",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "#head-2:not(:target)",
            ["head-2"],
            flags=util.HTML5
        )

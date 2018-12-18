"""
Test selectors level 4.

```
[foo='bar' i]
:nth-child(an+b [of S]?)
:is(s1, s2, ...) / :matches(s1, s2, ...)
:where(s1, s2, ...) allowed, but due to our environment, works like `:is()`
:not(s1, s2, ...)
:has(> s1, ...)
:any-link
:current
:past
:future
:focus-within
:focus-visible
:target-within
:default
:indeterminate
:placeholder-shown
:lang('*-US', de-DE, ...)
```

Not supported:

- `:nth-col(n)` / `:nth-last-col(n)`: This needs further understanding before implementing and would likely only be
  implemented for HTML, XHTML, and HTML5. This would not be implemented for XML.

- `E || F`: This would need more understanding before implementation. This would likely only be implemented for HTML,
  XHTML, and HTML5. This would not be implemented for XML.

- `:blank`: This applies to inputs with empty or otherwise null input.

- `:dir(ltr)`: This applies to direction of text. This direction can be inherited from parents. Due to the way Soup
  Sieve process things, it would have to scan the parents and evaluate what is inherited. it doesn't account for the CSS
  `direction` value, which is a good thing. It is doable, but not sure worth the effort. In addition, it seems there is
  reference to being able to do something like `[dir=auto]` which would select either `ltr` or `rtl`. This seems to add
  additional logic in to attribute selections which would complicate things, but still technically doable.

- `:local-link`: In our environment, there is no document URL. This isn't currently practical.

- `:read-only` / `:read-write`: There are no plans to implement this at this time.

- `:valid` / `:invalid`: We currently to not validate values, so this doesn't make sense at this time.

- `:user-invalid`: User cannot alter things in our environment because there is no user interaction (we are not a
  browser). This will not be implemented.

- `:scope`: I'm not sure what this means or if it is even useful in our context. More information would be needed. It
  seems in an HTML document, this would normally just be `:root` as there is no way to specify a different reference at
  this time. I'm not sure it makes sense to bother implementing this.

- `:in-range` / `:out-of-range`: This applies to form elements only. You'd have to evaluate `value`, `min`, and `max`. I
  guess you can have numerical ranges and alphabetic ranges. Currently, there are no plans to implement this.

- `:playing` / `:paused`: Elements cannot be played or paused in our environment, so this will not be implemented.
"""
from . import util
import soupsieve as sv


class TestLevel4(util.TestCase):
    """Test level 4 selectors."""

    def test_attribute_case(self):
        """Test attribute value case insensitivity."""

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
            "[class*=WORDS]",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "[class*=WORDS i]",
            ["0", "3", "pre"],
            flags=util.HTML5
        )

        with self.assertRaises(SyntaxError):
            sv.compile('[id i]')

    def test_attribute_type_case(self):
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
            '[type="test" s]',
            ['2'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            '[type="test" i]',
            ['0', '2'],
            flags=util.XML
        )

    def test_is_matches_where(self):
        """Test multiple selectors with "is", "matches", and "where"."""

        markup = """
        <div>
        <p>Some text <span id="1"> in a paragraph</span>.
        <a id="2" href="http://google.com">Link</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            ":is(span, a)",
            ["1", "2"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            ":is(span, a:matches(#\\32))",
            ["1", "2"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            ":where(span, a:matches(#\\32))",
            ["1", "2"],
            flags=util.HTML5
        )

        # Each pseudo class is evaluated separately
        # So this will not match
        self.assert_selector(
            markup,
            ":is(span):not(span)",
            [],
            flags=util.HTML5
        )

        # Each pseudo class is evaluated separately
        # So this will not match
        self.assert_selector(
            markup,
            ":is(span):is(div)",
            [],
            flags=util.HTML5
        )

        # Each pseudo class is evaluated separately
        # So this will match
        self.assert_selector(
            markup,
            ":is(a):is(#\\32)",
            ['2'],
            flags=util.HTML5
        )

    def test_multi_nested_not(self):
        """Test nested not and multiple selectors."""

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
            'div :not(p, :not([id=\\35]))',
            ['5'],
            flags=util.HTML5
        )

    def test_has(self):
        """Test has."""

        markup = """
        <div id="0" class="aaaa">
            <p id="1" class="bbbb"></p>
            <p id="2" class="cccc"></p>
            <p id="3" class="dddd"></p>
            <div id="4" class="eeee">
            <div id="5" class="ffff">
            <div id="6" class="gggg">
                <p id="7" class="hhhh"></p>
                <p id="8" class="iiii zzzz"></p>
                <p id="9" class="jjjj"></p>
                <div id="10" class="kkkk">
                    <p id="11" class="llll zzzz"></p>
                </div>
            </div>
            </div>
            </div>
        </div>
        """

        markup2 = """
        <div id="0" class="aaaa">
            <p id="1" class="bbbb"></p>
        </div>
        <div id="2" class="cccc">
            <p id="3" class="dddd"></p>
        </div>
        <div id="4" class="eeee">
            <p id="5" class="ffff"></p>
        </div>
        <div id="6" class="gggg">
            <p id="7" class="hhhh"></p>
        </div>
        <div id="8" class="iiii">
            <p id="9" class="jjjj"></p>
            <span id="10"></span>
        </div>
        """

        self.assert_selector(
            markup,
            'div:not(.aaaa):has(.kkkk > p.llll)',
            ['4', '5', '6'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            'div:NOT(.aaaa):HAS(.kkkk > p.llll)',
            ['4', '5', '6'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            'p:has(+ .dddd:has(+ div .jjjj))',
            ['2'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            'p:has(~ .jjjj)',
            ['7', '8'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup2,
            'div:has(> .bbbb, .ffff, .jjjj)',
            ['0', '4', '8'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup2,
            'div:has(> :not(.bbbb, .ffff, .jjjj))',
            ['2', '6', '8'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup2,
            'div:not(:has(> .bbbb, .ffff, .jjjj))',
            ['2', '6'],
            flags=util.HTML5
        )

    def test_nth_child_of_s(self):
        """Test `nth` child with selector."""

        markup = """
        <p id="0"></p>
        <p id="1"></p>
        <span id="2" class="test"></span>
        <span id="3"></span>
        <span id="4" class="test"></span>
        <span id="5"></span>
        <span id="6" class="test"></span>
        <p id="7"></p>
        <p id="8" class="test"></p>
        <p id="9"></p>
        <p id="10" class="test"></p>
        <span id="11"></span>
        """

        self.assert_selector(
            markup,
            ":nth-child(2n + 1 of :is(p, span).test)",
            ['2', '6', '10'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            ":nth-child(-n+3 of p)",
            ['0', '1', '7'],
            flags=util.HTML5
        )

    def test_anylink(self):
        """Test any link (all links are unvisited)."""

        markup = """
        <div id="div">
        <p id="0">Some text <span id="1" class="foo:bar:foobar"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        <a id="3">Placeholder text.</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            ":any-link",
            ["2"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "a:any-link",
            [],
            flags=util.XML
        )

        self.assert_selector(
            markup,
            ":not(a:any-link)",
            ["div", "0", "1", "2", "3"],
            flags=util.XML
        )

    def test_focus_within(self):
        """Test focus within."""

        markup = """
        <form id="form">
          <input type="text">
        </form>
        """

        self.assert_selector(
            markup,
            "form:focus-within",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "form:not(:focus-within)",
            ["form"],
            flags=util.HTML5
        )

    def test_focus_visible(self):
        """Test focus visible."""

        markup = """
        <form id="form">
          <input type="text">
        </form>
        """

        self.assert_selector(
            markup,
            "form:focus-visible",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "form:not(:focus-visible)",
            ["form"],
            flags=util.HTML5
        )

    def test_target_within(self):
        """Test target within."""

        markup = """
        <a href="#head-2">Jump</a>
        <article id="article">
        <h2 id="head-1">Header 1</h1>
        <div><p>content</p></div>
        <h2 id="head-2">Header 2</h1>
        <div><p>content</p></div>
        </article>
        """

        self.assert_selector(
            markup,
            "article:target-within",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "article:not(:target-within)",
            ["article"],
            flags=util.HTML5
        )

    def test_current_past_future(self):
        """Test current, past, future."""

        markup = """
        <div id="div">
        <p id="0">Some text <span id="1" class="foo:bar:foobar"> in a paragraph</span>.
        <a id="2" class="bar" href="http://google.com">Link</a>
        <a id="3">Placeholder text.</a>
        </p>
        </div>
        """

        self.assert_selector(
            markup,
            ":current(p, div, a)",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            ":current(p, :not(div), a)",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "body :not(:current(p, div, a))",
            ["div", "0", "1", "2", "3"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "body :not(:current(p, :not(div), a))",
            ["div", "0", "1", "2", "3"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:current",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:not(:current)",
            ["0"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:past",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "p:future",
            [],
            flags=util.HTML5
        )

    def test_required(self):
        """Test required."""

        markup = """
        <form>
        <input id="1" type="name" required>
        <input id="2" type="checkbox" required>
        <input id="3" type="email">
        <textarea id="4" name="name" id="message" cols="30" rows="10" required></textarea>
        <select id="5" name="nm" id="sel" required>
            <!-- options -->
        </select>
        </form>
        """

        self.assert_selector(
            markup,
            ":required",
            ['1', '2', '4', '5'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "input:required",
            ['1', '2'],
            flags=util.HTML5
        )

    def test_optional(self):
        """Test optional."""

        markup = """
        <form>
        <input id="1" type="name" required>
        <input id="2" type="checkbox" required>
        <input id="3" type="email">
        <textarea id="4" name="name" id="message" cols="30" rows="10"></textarea>
        <select id="5" name="nm" id="sel">
            <!-- options -->
        </select>
        </form>
        """

        self.assert_selector(
            markup,
            ":optional",
            ['3', '4', '5'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "input:optional",
            ['3'],
            flags=util.HTML5
        )

    def test_default(self):
        """Test default."""

        markup = """
        <form>

        <input type="radio" name="season" id="spring">
        <label for="spring">Spring</label>

        <input type="radio" name="season" id="summer" checked>
        <label for="summer">Summer</label>

        <input type="radio" name="season" id="fall">
        <label for="fall">Fall</label>

        <input type="radio" name="season" id="winter">
        <label for="winter">Winter</label>

        <select id="pet-select">
            <option value="">--Please choose an option--</option>
            <option id="dog" value="dog">Dog</option>
            <option id="cat" value="cat">Cat</option>
            <option id="hamster" value="hamster" selected>Hamster</option>
            <option id="parrot" value="parrot">Parrot</option>
            <option id="spider" value="spider">Spider</option>
            <option id="goldfish" value="goldfish">Goldfish</option>
        </select>

        <input type="checkbox" name="enable" id="enable" checked>
        <label for="enable">Enable</label>

        <button type="button">
        not default
        </button>

        <button id="d1" type="submit">
        default1
        </button>

        <button id="d2" type="submit">
        default2
        </button>

        </form>

        <form>

        <div>
        <button id="d3" type="submit">
        default3
        </button>
        </div>

        <button id="d4" type="submit">
        default4
        </button>

        </form>

        <button id="d5" type="submit">
        default4
        </button>
        """

        self.assert_selector(
            markup,
            ":default",
            ['summer', 'd1', 'd3', 'hamster', 'enable'],
            flags=util.HTML5
        )

        # This is technically invalid use of forms, but browsers will generally evaluated the nested form
        markup2 = """
        <form>

        <form>
        <button id="d1" type="submit">
        button1
        </button>
        </form>

        <button id="d2" type="submit">
        button2
        </button>
        </form>
        """

        self.assert_selector(
            markup2,
            ":default",
            ['d1'],
            flags=util.HTML5
        )

        # For the sake of coverage, we will do this impractical select
        # to ensure we reuse the cached default.
        self.assert_selector(
            markup2,
            ":default:default",
            ['d1'],
            flags=util.HTML5
        )

        # You shouldn't nest forms, but if you do,
        # When a parent form encounters a nested form, we will bail evaluation like browsers do.
        # We should see button 1 getting found for nested form, but button 2 will not be found
        # for parent form.
        markup3 = """
        <form>

        <form>
        <span>what</span>
        </form>

        <button id="d2" type="submit">
        button2
        </button>
        </form>
        """

        self.assert_selector(
            markup3,
            ":default",
            [],
            flags=util.HTML5
        )

    def test_indeterminate(self):
        """Test indeterminate."""

        markup = """
        <input type="radio" name="" id="radio-no-name1">
        <label>No name 1</label>
        <input type="radio" name="" id="radio-no-name2" checked>
        <label>no name 2</label>
        <div>
          <input type="checkbox" id="checkbox" indeterminate>
          <label for="checkbox">This label starts out lime.</label>
        </div>
        <div>
          <input type="radio" name="test" id="radio1">
          <label for="radio">This label starts out lime.</label>
          <form>
            <input type="radio" name="test" id="radio2">
            <label for="radio">This label starts out lime.</label>

            <input type="radio" name="test" id="radio3" checked>
            <label for="radio">This label starts out lime.</label>

            <input type="radio" name="other" id="radio4">
            <label for="radio">This label starts out lime.</label>

            <input type="radio" name="other" id="radio5">
            <label for="radio">This label starts out lime.</label>
          </form>
          <input type="radio" name="test" id="radio6">
          <label for="radio">This label starts out lime.</label>
        </div>
        """

        self.assert_selector(
            markup,
            ":indeterminate",
            ['checkbox', 'radio1', 'radio6', 'radio4', 'radio5', 'radio-no-name1'],
            flags=util.HTML5
        )

    def test_placeholder(self):
        """Test placeholder shown."""

        markup = """
        <input id="0" placeholder="This is some text">
        <textarea id="1" placeholder="This is some text"></textarea>

        <input id="2" placeholder="">
        <input id="3">

        <input id="4" type="email" placeholder="This is some text">
        <input id="5" type="number" placeholder="This is some text">
        <input id="6" type="password" placeholder="This is some text">
        <input id="7" type="search" placeholder="This is some text">
        <input id="8" type="tel" placeholder="This is some text">
        <input id="9" type="text" placeholder="This is some text">
        <input id="10" type="url" placeholder="This is some text">
        <input id="11" type="" placeholder="This is some text">
        <input id="12" type placeholder="This is some text">

        <input id="13" type="button" placeholder="This is some text">
        <input id="14" type="checkbox" placeholder="This is some text">
        <input id="15" type="color" placeholder="This is some text">
        <input id="16" type="date" placeholder="This is some text">
        <input id="17" type="datetime-local" placeholder="This is some text">
        <input id="18" type="file" placeholder="This is some text">
        <input id="19" type="hidden" placeholder="This is some text">
        <input id="20" type="image" placeholder="This is some text">
        <input id="21" type="month" placeholder="This is some text">
        <input id="22" type="radio" placeholder="This is some text">
        <input id="23" type="range" placeholder="This is some text">
        <input id="24" type="reset" placeholder="This is some text">
        <input id="25" type="submit" placeholder="This is some text">
        <input id="26" type="time" placeholder="This is some text">
        <input id="27" type="week" placeholder="This is some text">
        """

        self.assert_selector(
            markup,
            ":placeholder-shown",
            ['0', '1', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
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

        # Implicit wild
        self.assert_selector(
            markup,
            "p:lang(de-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

        # Explicit wild
        self.assert_selector(
            markup,
            "p:lang(de-\\*-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

        # First wild has meaning (escaped)
        self.assert_selector(
            markup,
            "p:lang(\\*-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

        # First wild quoted
        self.assert_selector(
            markup,
            "p:lang('*-DE')",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

        # Normal quoted
        self.assert_selector(
            markup,
            "p:lang('de-DE')",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )

        # Target element with language and language attribute
        self.assert_selector(
            markup,
            "p[lang]:lang(de-DE)",
            ['6'],
            flags=util.HTML5
        )

        # Undetermined language
        markup = """
        <div>
            <p id="1"></p>
        </div>
        """

        self.assert_selector(
            markup,
            "p:lang(en)",
            [],
            flags=util.HTML5
        )

        # Find language in header
        markup = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="content-language" content="en-US">
        </head>
        <body>
        <div>
            <p id="1"></p>
        </div>
        <div>
            <p id="2"></p>
        </div>
        </body>
        """

        self.assert_selector(
            markup,
            "p:lang('*-US')",
            ['1', '2'],
            flags=util.HTML5
        )

        # XML style language when out of HTML namespace
        markup = """
        <math xml:lang="en">
            <mtext id="1"></mtext>
        </math>
        <div xml:lang="en">
            <mtext id="2"></mtext>
        </div>
        """

        self.assert_selector(
            markup,
            "mtext:lang(en)",
            ['1'],
            flags=util.HTML5
        )

        # XML style language
        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <html>
        <head>
        </head>
        <body>
        <div xml:lang="de-DE">
            <p id="1"></p>
        </div>
        <div xml:lang="de-DE-1996">
            <p id="2"></p>
        </div>
        <div xml:lang="de-Latn-DE">
            <p id="3"></p>
        </div>
        <div xml:lang="de-Latf-DE">
            <p id="4"></p>
        </div>
        <div xml:lang="de-Latn-DE-1996">
            <p id="5"></p>
        </div>
        <p id="6" xml:lang="de-DE"></p>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "p:lang(de-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.XML
        )

        # XHTML language: `lang`
        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        </head>
        <body>
        <div xml:lang="de-DE">
            <p id="1"></p>
        </div>
        <div xml:lang="de-DE-1996">
            <p id="2"></p>
        </div>
        <div xml:lang="de-Latn-DE">
            <p id="3"></p>
        </div>
        <div xml:lang="de-Latf-DE">
            <p id="4"></p>
        </div>
        <div xml:lang="de-Latn-DE-1996">
            <p id="5"></p>
        </div>
        <p id="6" xml:lang="de-DE"></p>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "p:lang(de-DE)",
            [],
            flags=util.XHTML
        )

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        </head>
        <body>
        <div lang="de-DE" xml:lang="de-DE">
            <p id="1"></p>
        </div>
        <div lang="de-DE-1996" xml:lang="de-DE-1996">
            <p id="2"></p>
        </div>
        <div lang="de-Latn-DE" xml:lang="de-Latn-DE">
            <p id="3"></p>
        </div>
        <div lang="de-Latf-DE" xml:lang="de-Latf-DE">
            <p id="4"></p>
        </div>
        <div lang="de-Latn-DE-1996" xml:lang="de-Latn-DE-1996">
            <p id="5"></p>
        </div>
        <p id="6" lang="de-DE" xml:lang="de-DE"></p>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "p:lang(de-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.XML
        )

        # Multiple languages
        markup = """
        <div lang="de-DE">
            <p id="1"></p>
        </div>
        <div lang="en">
            <p id="2"></p>
        </div>
        <div lang="de-Latn-DE">
            <p id="3"></p>
        </div>
        <div lang="de-Latf-DE">
            <p id="4"></p>
        </div>
        <div lang="en-US">
            <p id="5"></p>
        </div>
        <p id="6" lang="de-DE"></p>
        """

        self.assert_selector(
            markup,
            "p:lang(de-DE, '*-US')",
            ['1', '3', '4', '5', '6'],
            flags=util.HTML5
        )

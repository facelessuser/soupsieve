# -*- coding: utf-8 -*-
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
:user-invalid
:playing
:paused
:scope
:local-link
:read-only
:read-write
:host
:host(sel1, sel2, ...)
:host-context(sel1, sel2, ...)
:required
:optional
:in-range
:out-of-range
```

Not supported:

- `:nth-col(n)` / `:nth-last-col(n)`: This needs further understanding before implementing and would likely only be
  implemented for HTML, XHTML, and HTML5. This would not be implemented for XML.

- `E || F`: This would need more understanding before implementation. This would likely only be implemented for HTML,
  XHTML, and HTML5. This would not be implemented for XML.

- `:blank`: This applies to inputs with empty or otherwise null input.

- `:valid` / `:invalid`: We currently do not have the capability to validate all values, so this doesn't make sense yet.
"""
from __future__ import unicode_literals
from . import util
import soupsieve as sv
import textwrap
import bs4


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

    def test_scope(self):
        """Test scope."""

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

        # Scope is root when applied to a document node
        self.assert_selector(
            markup,
            ":scope",
            ["root"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            ":scope > body > div",
            ["div"],
            flags=util.HTML5
        )

        soup = bs4.BeautifulSoup(textwrap.dedent(markup.replace('\r\n', '\n')), 'html5lib')
        el = soup.html

        # Scope is the element we are applying the select to, and that element is never returned
        self.assertTrue(len(sv.select(':scope', el, flags=sv.DEBUG)) == 0)

        # Scope here means the current element under select
        ids = []
        for el in sv.select(':scope div', el, flags=sv.DEBUG):
            ids.append(el.attrs['id'])
        self.assertEqual(sorted(ids), sorted(['div']))

        el = soup.body
        ids = []
        for el in sv.select(':scope div', el, flags=sv.DEBUG):
            ids.append(el.attrs['id'])
        self.assertEqual(sorted(ids), sorted(['div']))

        # `div` is the current element under select, and it has no `div` elements.
        el = soup.div
        ids = []
        for el in sv.select(':scope div', el, flags=sv.DEBUG):
            ids.append(el.attrs['id'])
        self.assertEqual(sorted(ids), sorted([]))

        # `div` does have an element with the class `.wordshere`
        ids = []
        for el in sv.select(':scope .wordshere', el, flags=sv.DEBUG):
            ids.append(el.attrs['id'])
        self.assertEqual(sorted(ids), sorted(['pre']))

    def test_user_invalid(self):
        """Test user invalid (matches nothing)."""

        markup = """
        <form id="form">
          <input id="1" type="text">
        </form>
        """

        self.assert_selector(
            markup,
            "input:user-invalid",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "input:not(:user-invalid)",
            ["1"],
            flags=util.HTML5
        )

    def test_playing(self):
        """Test playing (matches nothing)."""

        markup = """
        <!DOCTYPE html>
        <html>
        <body>

        <video id="vid" width="320" height="240" controls>
          <source src="movie.mp4" type="video/mp4">
          <source src="movie.ogg" type="video/ogg">
          Your browser does not support the video tag.
        </video>

        </body>
        </html>
        """

        # Not actually sure how this is used, but it won't match anything anyways
        self.assert_selector(
            markup,
            "video:playing",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "video:not(:playing)",
            ["vid"],
            flags=util.HTML5
        )

    def test_paused(self):
        """Test paused (matches nothing)."""

        markup = """
        <!DOCTYPE html>
        <html>
        <body>

        <video id="vid" width="320" height="240" controls>
          <source src="movie.mp4" type="video/mp4">
          <source src="movie.ogg" type="video/ogg">
          Your browser does not support the video tag.
        </video>

        </body>
        </html>
        """

        # Not actually sure how this is used, but it won't match anything anyways
        self.assert_selector(
            markup,
            "video:paused",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "video:not(:paused)",
            ["vid"],
            flags=util.HTML5
        )

    def test_local_link(self):
        """Test local link (matches nothing)."""

        markup = """
        <a id="1" href="./somelink/index.html">Link</link>
        <a id="2" href="http://somelink.com/somelink/index.html">Another link</a>
        """

        self.assert_selector(
            markup,
            "a:local-link",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "a:not(:local-link)",
            ["1", "2"],
            flags=util.HTML5
        )

    def test_read_write(self):
        """Test read write."""

        markup = """
        <input id="0">
        <textarea id="1"></textarea>

        <input id="2">
        <input id="3" disabled>

        <input id="4" type="email">
        <input id="5" type="number">
        <input id="6" type="password">
        <input id="7" type="search">
        <input id="8" type="tel">
        <input id="9" type="text">
        <input id="10" type="url">
        <input id="11" type="">
        <input id="12" type>

        <input id="13" type="button">
        <input id="14" type="checkbox">
        <input id="15" type="color">
        <input id="16" type="date">
        <input id="17" type="datetime-local">
        <input id="18" type="file">
        <input id="19" type="hidden">
        <input id="20" type="image">
        <input id="21" type="month">
        <input id="22" type="radio">
        <input id="23" type="range">
        <input id="24" type="reset">
        <input id="25" type="submit">
        <input id="26" type="time">
        <input id="27" type="week">

        <p id="28" contenteditable="">Text</p>
        <p id="29" contenteditable="true">Text</p>
        <p id="30" contenteditable="TRUE">Text</p>
        <p id="31" contenteditable="false">Text</p>
        <p id="32">Text</p>

        <input id="33" type="number" readonly>
        """

        self.assert_selector(
            markup,
            ":read-write",
            [
                '0', '1', '2', '4', '5', '6', '7', '8', '9', '10', '11',
                '12', '16', '17', '21', '26', '27', '28', '29', '30'
            ],
            flags=util.HTML5
        )

    def test_read_only(self):
        """Test read only."""

        markup = """
        <input id="0">
        <textarea id="1"></textarea>

        <input id="2">
        <input id="3" disabled>

        <input id="4" type="email">
        <input id="5" type="number">
        <input id="6" type="password">
        <input id="7" type="search">
        <input id="8" type="tel">
        <input id="9" type="text">
        <input id="10" type="url">
        <input id="11" type="">
        <input id="12" type>

        <input id="13" type="button">
        <input id="14" type="checkbox">
        <input id="15" type="color">
        <input id="16" type="date">
        <input id="17" type="datetime-local">
        <input id="18" type="file">
        <input id="19" type="hidden">
        <input id="20" type="image">
        <input id="21" type="month">
        <input id="22" type="radio">
        <input id="23" type="range">
        <input id="24" type="reset">
        <input id="25" type="submit">
        <input id="26" type="time">
        <input id="27" type="week">

        <p id="28" contenteditable="">Text</p>
        <p id="29" contenteditable="true">Text</p>
        <p id="30" contenteditable="TRUE">Text</p>
        <p id="31" contenteditable="false">Text</p>
        <p id="32">Text</p>

        <input id="33" type="number" readonly>
        """

        self.assert_selector(
            markup,
            "body :read-only",
            [
                '3', '13', '14', '15', '18', '19', '20', '22',
                '23', '24', '25', '31', '32', '33'
            ],
            flags=util.HTML5
        )

    def test_host(self):
        """Test host (not supported)."""

        markup = """<h1>header</h1><div><p>some text</p></div>"""

        self.assert_selector(
            markup,
            ":host",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            ":host(h1)",
            [],
            flags=util.HTML5
        )

    def test_host_context(self):
        """Test host context (not supported)."""

        markup = """<h1>header</h1><div><p>some text</p></div>"""

        self.assert_selector(
            markup,
            ":host-context(h1, h2)",
            [],
            flags=util.HTML5
        )

    def test_dir(self):
        """Test direction."""

        markup = """
        <html id="0">
        <head></head>
        <body>
        <div id="1" dir="rtl">
          <span id="2">test1</span>
          <div id="3" dir="ltr">test2
            <div id="4" dir="auto"><!-- comment -->עִבְרִית<span id="5" dir="auto">()</span></div>
            <div id="6" dir="auto"><script></script><b> </b><span id="7"><!-- comment -->עִבְרִית</span></div>
            <span id="8" dir="auto">test3</span>
          </div>
          <input id="9" type="tel" value="333-444-5555" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}">
          <input id="10" type="tel" dir="auto" value="333-444-5555" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}">
          <input id="11" type="email" dir="auto" value="test@mail.com">
          <input id="12" type="search" dir="auto" value="()">
          <input id="13" type="url" dir="auto" value="https://test.com">
          <input id="14" type="search" dir="auto" value="עִבְרִית">
          <input id="15" type="search" dir="auto" value="">
          <input id="16" type="search" dir="auto">
          <textarea id="17" dir="auto">עִבְרִית</textarea>
          <textarea id="18" dir="auto"></textarea>
        </div>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "div:dir(rtl)",
            ["1", "4", "6"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "div:dir(ltr)",
            ["3"],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "div:dir(ltr):dir(rtl)",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "div:dir(ltr)",
            [],
            flags=util.XML
        )

        self.assert_selector(
            markup,
            "span:dir(rtl)",
            ['2', '5', '7'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "span:dir(ltr)",
            ['8'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            ":is(input, textarea):dir(ltr)",
            ['9', '10', '11', '12', '13'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "html:dir(ltr)",
            ['0'],
            flags=util.HTML5
        )

        markup = """
        <html id="0" dir="auto">
        <head></head>
        <body>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "html:dir(ltr)",
            ['0'],
            flags=util.HTML5
        )

        # Input is root
        markup = """<input id="1" type="text" dir="auto">"""
        soup = bs4.BeautifulSoup(markup, 'html5lib')
        fragment = soup.input.extract()
        self.assertTrue(sv.match(":root:dir(ltr)", fragment, flags=sv.DEBUG))

    def test_in_range(self):
        """Test in range."""

        markup = """
        <!-- These should all match -->
        <input id="0" type="number" min="0" max="10" value="5">
        <input id="1" type="number" min="-1" max="10" value="5">
        <input id="2" type="number" min="2.2" max="8.8" value="5.2">
        <input id="3" type="number" min="2.2" value="5.2">
        <input id="4" type="number" max="8.8" value="5.2">
        <input id="5" type="number" min="2.2" value="2.2">
        <input id="6" type="number" max="8.8" value="8.8">
        <input id="7" type="number" max="8.8">
        <input id="8" type="number" max="8.8" value="invalid">

        <!-- These should not match -->
        <input id="9" type="number" min="0" max="10" value="-1">
        <input id="10" type="number" min="0" max="10" value="10.1">
        <input id="11" type="number" max="0" min="10" value="11">

        <!-- These cannot match -->
        <input id="12" type="number" value="10">
        <input id="13" type="number" min="invalid" value="10">
        """

        self.assert_selector(
            markup,
            ":in-range",
            ['0', '1', '2', '3', '4', '5', '6', '7', '8'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should all match -->
        <input id="0" type="range" min="0" max="10" value="5">
        <input id="1" type="range" min="-1" max="10" value="5">
        <input id="2" type="range" min="2.2" max="8.8" value="5.2">
        <input id="3" type="range" min="2.2" value="5.2">
        <input id="4" type="range" max="8.8" value="5.2">
        <input id="5" type="range" min="2.2" value="2.2">
        <input id="6" type="range" max="8.8" value="8.8">
        <input id="7" type="range" max="8.8">
        <input id="8" type="range" max="8.8" value="invalid">

        <!-- These should not match -->
        <input id="9" type="range" min="0" max="10" value="-1">
        <input id="10" type="range" min="0" max="10" value="10.1">

        <!-- These cannot match -->
        <input id="11" type="range" value="10">
        <input id="12" type="range" min="invalid" value="10">
        """

        self.assert_selector(
            markup,
            ":in-range",
            ['0', '1', '2', '3', '4', '5', '6', '7', '8'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should all match -->
        <input id="0" type="month" min="1980-02" max="2004-08" value="1999-05">
        <input id="1" type="month" min="1980-02" max="2004-08" value="1980-02">
        <input id="2" type="month" min="1980-02" max="2004-08" value="2004-08">
        <input id="3" type="month" min="1980-02" value="1999-05">
        <input id="4" type="month" max="2004-08" value="1999-05">
        <input id="5" type="month" min="1980-02" max="2004-08" value="1999-13">
        <input id="6" type="month" min="1980-02" max="2004-08">

        <!-- These should not match -->
        <input id="7" type="month" min="1980-02" max="2004-08" value="1979-02">
        <input id="8" type="month" min="1980-02" max="2004-08" value="1980-01">
        <input id="9" type="month" min="1980-02" max="2004-08" value="2005-08">
        <input id="10" type="month" min="1980-02" max="2004-08" value="2004-09">

        <!-- These cannot match -->
        <input id="11" type="month" value="1999-05">
        <input id="12" type="month" min="invalid" value="1999-05">
        """

        self.assert_selector(
            markup,
            ":in-range",
            ['0', '1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should all match -->
        <input id="0" type="week" min="1980-W53" max="2004-W20" value="1999-W05">
        <input id="1" type="week" min="1980-W53" max="2004-W20" value="1980-W53">
        <input id="2" type="week" min="1980-W53" max="2004-W20" value="2004-W20">
        <input id="3" type="week" min="1980-W53" value="1999-W05">
        <input id="4" type="week" max="2004-W20" value="1999-W05">
        <input id="5" type="week" min="1980-W53" max="2004-W20" value="2005-W53">
        <input id="6" type="week" min="1980-W53" max="2004-W20" value="2005-w52">
        <input id="7" type="week" min="1980-W53" max="2004-W20">

        <!-- These should not match -->
        <input id="8" type="week" min="1980-W53" max="2004-W20" value="1979-W53">
        <input id="9" type="week" min="1980-W53" max="2004-W20" value="1980-W52">
        <input id="10" type="week" min="1980-W53" max="2004-W20" value="2005-W20">
        <input id="11" type="week" min="1980-W53" max="2004-W20" value="2004-W21">

        <!-- These cannot match -->
        <input id="12" type="week" value="1999-W05">
        <input id="13" type="week" min="invalid" value="1999-W05">
        """

        self.assert_selector(
            markup,
            ":in-range",
            ['0', '1', '2', '3', '4', '5', '6', '7'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should all match -->
        <input id="0" type="date" min="1980-02-20" max="2004-08-14" value="1999-05-16">
        <input id="1" type="date" min="1980-02-20" max="2004-08-14" value="1980-02-20">
        <input id="2" type="date" min="1980-02-20" max="2004-08-14" value="2004-08-14">
        <input id="3" type="date" min="1980-02-20" value="1999-05-16">
        <input id="4" type="date" max="2004-08-14" value="1999-05-16">
        <input id="5" type="date" min="1980-02-20" max="2004-08-14" value="1999-13-16">
        <input id="6" type="date" min="1980-02-20" max="2004-08-14">

        <!-- These should not match -->
        <input id="7" type="date" min="1980-02-20" max="2004-08-14" value="1979-02-20">
        <input id="8" type="date" min="1980-02-20" max="2004-08-14" value="1980-01-20">
        <input id="9" type="date" min="1980-02-20" max="2004-08-14" value="1980-02-19">
        <input id="10" type="date" min="1980-02-20" max="2004-08-14" value="2005-08-14">
        <input id="11" type="date" min="1980-02-20" max="2004-08-14" value="2004-09-14">
        <input id="12" type="date" min="1980-02-20" max="2004-08-14" value="2004-09-15">

        <!-- These cannot match -->
        <input id="13" type="date" value="1999-05-16">
        <input id="14" type="date" min="invalid" value="1999-05-16">
        """

        self.assert_selector(
            markup,
            ":in-range",
            ['0', '1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should all match -->
        <input id="0" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1999-05-16T20:20">
        <input id="1" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-02-20T01:30">
        <input id="2" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-08-14T18:45">
        <input id="3" type="datetime-local" min="1980-02-20T01:30" value="1999-05-16T20:20">
        <input id="4" type="datetime-local" max="2004-08-14T18:45" value="1999-05-16T20:20">
        <input id="5" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1999-05-16T24:20">
        <input id="6" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45">

        <!-- These should not match -->
        <input id="7" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1979-02-20T01:30">
        <input id="8" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-01-20T01:30">
        <input id="9" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-02-19T01:30">
        <input id="10" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-02-19T00:30">
        <input id="11" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-02-19T01:29">
        <input id="12" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2005-08-14T18:45">
        <input id="13" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-09-14T18:45">
        <input id="14" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-08-15T18:45">
        <input id="15" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-08-14T19:45">
        <input id="16" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-08-14T18:46">

        <!-- These cannot match -->
        <input id="17" type="datetime-local" value="1999-05-16T20:20">
        <input id="18" type="datetime-local" min="invalid" value="1999-05-16T20:20">
        """

        self.assert_selector(
            markup,
            ":in-range",
            ['0', '1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should all match -->
        <input id="0" type="time" min="01:30" max="18:45" value="10:20">
        <input id="1" type="time" max="01:30" min="18:45" value="20:20">
        <input id="2" type="time" min="01:30" max="18:45" value="01:30">
        <input id="3" type="time" min="01:30" max="18:45" value="18:45">
        <input id="4" type="time" min="01:30" value="10:20">
        <input id="5" type="time" max="18:45" value="10:20">
        <input id="6" type="time" min="01:30" max="18:45" value="24:20">
        <input id="7" type="time" min="01:30" max="18:45">

        <!-- These should not match -->
        <input id="8" type="time" min="01:30" max="18:45" value="00:30">
        <input id="9" type="time" min="01:30" max="18:45" value="01:29">
        <input id="10" type="time" min="01:30" max="18:45" value="19:45">
        <input id="11" type="time" min="01:30" max="18:45" value="18:46">
        <input id="12" type="time" max="01:30" min="18:45" value="02:30">
        <input id="13" type="time" max="01:30" min="18:45" value="17:45">
        <input id="14" type="time" max="01:30" min="18:45" value="18:44">

        <!-- These cannot match -->
        <input id="15" type="time" value="10:20">
        <input id="16" type="time" min="invalid" value="10:20">
        """

        self.assert_selector(
            markup,
            ":in-range",
            ['0', '1', '2', '3', '4', '5', '6', '7'],
            flags=util.HTML5
        )

    def test_out_of_range(self):
        """Test in range."""

        markup = """
        <!-- These should not match -->
        <input id="0" type="number" min="0" max="10" value="5">
        <input id="1" type="number" min="-1" max="10" value="5">
        <input id="2" type="number" min="2.2" max="8.8" value="5.2">
        <input id="3" type="number" min="2.2" value="5.2">
        <input id="4" type="number" max="8.8" value="5.2">
        <input id="5" type="number" min="2.2" value="2.2">
        <input id="6" type="number" max="8.8" value="8.8">
        <input id="7" type="number" max="8.8">
        <input id="8" type="number" max="8.8" value="invalid">

        <!-- These should match -->
        <input id="9" type="number" min="0" max="10" value="-1">
        <input id="10" type="number" min="0" max="10" value="10.1">
        <input id="11" type="number" max="0" min="10" value="11">

        <!-- These cannot match -->
        <input id="12" type="number" value="10">
        <input id="13" type="number" min="invalid" value="10">
        """

        self.assert_selector(
            markup,
            ":out-of-range",
            ['9', '10', '11'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should not match -->
        <input id="0" type="range" min="0" max="10" value="5">
        <input id="1" type="range" min="-1" max="10" value="5">
        <input id="2" type="range" min="2.2" max="8.8" value="5.2">
        <input id="3" type="range" min="2.2" value="5.2">
        <input id="4" type="range" max="8.8" value="5.2">
        <input id="5" type="range" min="2.2" value="2.2">
        <input id="6" type="range" max="8.8" value="8.8">
        <input id="7" type="range" max="8.8">
        <input id="8" type="range" max="8.8" value="invalid">

        <!-- These should match -->
        <input id="9" type="range" min="0" max="10" value="-1">
        <input id="10" type="range" min="0" max="10" value="10.1">

        <!-- These cannot match -->
        <input id="11" type="range" value="10">
        <input id="12" type="range" min="invalid" value="10">
        """

        self.assert_selector(
            markup,
            ":out-of-range",
            ['9', '10'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should not match -->
        <input id="0" type="month" min="1980-02" max="2004-08" value="1999-05">
        <input id="1" type="month" min="1980-02" max="2004-08" value="1980-02">
        <input id="2" type="month" min="1980-02" max="2004-08" value="2004-08">
        <input id="3" type="month" min="1980-02" value="1999-05">
        <input id="4" type="month" max="2004-08" value="1999-05">
        <input id="5" type="month" min="1980-02" max="2004-08" value="1999-13">
        <input id="6" type="month" min="1980-02" max="2004-08">

        <!-- These should match -->
        <input id="7" type="month" min="1980-02" max="2004-08" value="1979-02">
        <input id="8" type="month" min="1980-02" max="2004-08" value="1980-01">
        <input id="9" type="month" min="1980-02" max="2004-08" value="2005-08">
        <input id="10" type="month" min="1980-02" max="2004-08" value="2004-09">

        <!-- These cannot match -->
        <input id="11" type="month" value="1999-05">
        <input id="12" type="month" min="invalid" value="1999-05">
        """

        self.assert_selector(
            markup,
            ":out-of-range",
            ['7', '8', '9', '10'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should not match -->
        <input id="0" type="week" min="1980-W53" max="2004-W20" value="1999-W05">
        <input id="1" type="week" min="1980-W53" max="2004-W20" value="1980-W53">
        <input id="2" type="week" min="1980-W53" max="2004-W20" value="2004-W20">
        <input id="3" type="week" min="1980-W53" value="1999-W05">
        <input id="4" type="week" max="2004-W20" value="1999-W05">
        <input id="5" type="week" min="1980-W53" max="2004-W20" value="2005-W53">
        <input id="6" type="week" min="1980-W53" max="2004-W20" value="2005-w52">
        <input id="7" type="week" min="1980-W53" max="2004-W20">

        <!-- These should match -->
        <input id="8" type="week" min="1980-W53" max="2004-W20" value="1979-W53">
        <input id="9" type="week" min="1980-W53" max="2004-W20" value="1980-W52">
        <input id="10" type="week" min="1980-W53" max="2004-W20" value="2005-W20">
        <input id="11" type="week" min="1980-W53" max="2004-W20" value="2004-W21">

        <!-- These cannot match -->
        <input id="12" type="week" value="1999-W05">
        <input id="13" type="week" min="invalid" value="1999-W05">
        """

        self.assert_selector(
            markup,
            ":out-of-range",
            ['8', '9', '10', '11'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should not match -->
        <input id="0" type="date" min="1980-02-20" max="2004-08-14" value="1999-05-16">
        <input id="1" type="date" min="1980-02-20" max="2004-08-14" value="1980-02-20">
        <input id="2" type="date" min="1980-02-20" max="2004-08-14" value="2004-08-14">
        <input id="3" type="date" min="1980-02-20" value="1999-05-16">
        <input id="4" type="date" max="2004-08-14" value="1999-05-16">
        <input id="5" type="date" min="1980-02-20" max="2004-08-14" value="1999-13-16">
        <input id="6" type="date" min="1980-02-20" max="2004-08-14">

        <!-- These should match -->
        <input id="7" type="date" min="1980-02-20" max="2004-08-14" value="1979-02-20">
        <input id="8" type="date" min="1980-02-20" max="2004-08-14" value="1980-01-20">
        <input id="9" type="date" min="1980-02-20" max="2004-08-14" value="1980-02-19">
        <input id="10" type="date" min="1980-02-20" max="2004-08-14" value="2005-08-14">
        <input id="11" type="date" min="1980-02-20" max="2004-08-14" value="2004-09-14">
        <input id="12" type="date" min="1980-02-20" max="2004-08-14" value="2004-09-15">

        <!-- These cannot match -->
        <input id="13" type="date" value="1999-05-16">
        <input id="14" type="date" min="invalid" value="1999-05-16">
        """

        self.assert_selector(
            markup,
            ":out-of-range",
            ['7', '8', '9', '10', '11', '12'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should not match -->
        <input id="0" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1999-05-16T20:20">
        <input id="1" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-02-20T01:30">
        <input id="2" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-08-14T18:45">
        <input id="3" type="datetime-local" min="1980-02-20T01:30" value="1999-05-16T20:20">
        <input id="4" type="datetime-local" max="2004-08-14T18:45" value="1999-05-16T20:20">
        <input id="5" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1999-05-16T24:20">
        <input id="6" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45">

        <!-- These should match -->
        <input id="7" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1979-02-20T01:30">
        <input id="8" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-01-20T01:30">
        <input id="9" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-02-19T01:30">
        <input id="10" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-02-19T00:30">
        <input id="11" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="1980-02-19T01:29">
        <input id="12" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2005-08-14T18:45">
        <input id="13" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-09-14T18:45">
        <input id="14" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-08-15T18:45">
        <input id="15" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-08-14T19:45">
        <input id="16" type="datetime-local" min="1980-02-20T01:30" max="2004-08-14T18:45" value="2004-08-14T18:46">

        <!-- These cannot match -->
        <input id="17" type="datetime-local" value="1999-05-16T20:20">
        <input id="18" type="datetime-local" min="invalid" value="1999-05-16T20:20">
        """

        self.assert_selector(
            markup,
            ":out-of-range",
            ['7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
            flags=util.HTML5
        )

        markup = """
        <!-- These should not match -->
        <input id="0" type="time" min="01:30" max="18:45" value="10:20">
        <input id="1" type="time" max="01:30" min="18:45" value="20:20">
        <input id="2" type="time" min="01:30" max="18:45" value="01:30">
        <input id="3" type="time" min="01:30" max="18:45" value="18:45">
        <input id="4" type="time" min="01:30" value="10:20">
        <input id="5" type="time" max="18:45" value="10:20">
        <input id="6" type="time" min="01:30" max="18:45" value="24:20">
        <input id="7" type="time" min="01:30" max="18:45">

        <!-- These should match -->
        <input id="8" type="time" min="01:30" max="18:45" value="00:30">
        <input id="9" type="time" min="01:30" max="18:45" value="01:29">
        <input id="10" type="time" min="01:30" max="18:45" value="19:45">
        <input id="11" type="time" min="01:30" max="18:45" value="18:46">
        <input id="12" type="time" max="01:30" min="18:45" value="02:30">
        <input id="13" type="time" max="01:30" min="18:45" value="17:45">
        <input id="14" type="time" max="01:30" min="18:45" value="18:44">

        <!-- These cannot match -->
        <input id="15" type="time" value="10:20">
        <input id="16" type="time" min="invalid" value="10:20">
        """

        self.assert_selector(
            markup,
            ":out-of-range",
            ['8', '9', '10', '11', '12', '13', '14'],
            flags=util.HTML5
        )

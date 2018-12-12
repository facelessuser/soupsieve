"""
Test selectors level 4.

```
[foo='bar' i]
:nth-child(an+b [of S]?)
:is(s1, s2, ...) / :matches(s1, s2, ...)
:where(s1, s2, ...) allowed, but due to our environment, works like `:is()`
:not(s1, s2, ...)
:has(> s1, ...)
```

Likely to be implemented:

- `:nth-col(n)` / `:nth-last-col(n)`: This needs further understanding before implementing and would likely only be
  implemented for HTML, XHTML, and HTML5. This would not be implemented for XML.

- `E || F`: This would need more understanding before implementation. This would likely only be implemented for HTML,
  XHTML, and HTML5. This would not be implemented for XML.

Not supported (with current opinions or plans the matter):

- `:blank`: This applies to inputs with empty or otherwise null input. Currently, there is no plans to implement this.

- `:dir(ltr)`: This applies to direction of text. This direction can be inherited from parents. Due to the way Soup
  Sieve process things, it would have to scan the parents and evaluate what is inherited. it doesn't account for the CSS
  `direction` value, which is a good thing. It is doable, but not sure worth the effort. In addition, it seems there is
  reference to being able to do something like `[dir=auto]` which would select either `ltr` or `rtl`. This seems to add
  additional logic in to attribute selections which would complicate things, but still technically doable. There are
  currently no plans to implement this.

- `:lang(en-*)`: As mentioned in level 2 tests, in documents, `:lang()` can take into considerations information in
  `meta` and other things in the header. At this point, there are no plans to implement this. If a reasonable proposal
  was introduced on how to support this, it may be considered.

- `:local-link`: In our environment, there is no document URL. This isn't currently practical. This will not be
  implemented.

- `:read-only` / `:read-write`: There are no plans to implement this at this time.

- `:required` / `:optional`: There are no plans to implement this at this time.

- `:placeholder-shown`: There are no plans to implement this at this time.

- `:indeterminate`: There are no plans to implement this at this time.

- `:valid` / `:invalid`: We currently to not validate values, so this doesn't make sense at this time.

- `:user-invalid`: User cannot alter things in our environment because there is no user interaction (we are not a
  browser). This will not be implemented.

- `:scope`: I'm not sure what this means or if it is even useful in our context. More information would be needed. It
  seems in an HTML document, this would normally just be `:root` as there is no way to specify a different reference at
  this time. I'm not sure it makes sense to bother implementing this.

- `:in-range` / `:out-of-range`: This applies to form elements only. You'd have to evaluate `value`, `min`, and `max`. I
  guess you can have numerical ranges and alphabetic ranges. Currently, there are no plans to implement this.

- `:current` / `:past` / `:future`: I believe this requires a live, in browser state to determine what is current, to
  then determine what is past and future. I don't think this is applicable to our environment.

- `:default`: This is in the same vain as `:checked`. If we ever implemented that, we'd probably implement this, but
  there are no plans to do so at this time.

- `:focus-within` / `:focus-visible`: There is no focus in our environment, so this will not be implemented.

- `:target-within`: Elements cannot be "targeted" in our environment, so this will not be implemented.

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
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            "[class*=WORDS i]",
            ["0", "3", "pre"],
            flags=sv.HTML5
        )

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
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            '[type="test" i]',
            ['0', '2'],
            flags=sv.XML
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
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            ":is(span, a:matches(#2))",
            ["1", "2"],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            ":where(span, a:matches(#2))",
            ["1", "2"],
            flags=sv.HTML5
        )

        # Each pseudo class is evaluated separately
        # So this will not match
        self.assert_selector(
            markup,
            ":is(span):not(span)",
            [],
            flags=sv.HTML5
        )

        # Each pseudo class is evaluated separately
        # So this will not match
        self.assert_selector(
            markup,
            ":is(span):is(div)",
            [],
            flags=sv.HTML5
        )

        # Each pseudo class is evaluated separately
        # So this will match
        self.assert_selector(
            markup,
            ":is(a):is(#2)",
            ['2'],
            flags=sv.HTML5
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
            'div :not(p, :not([id=5]))',
            ['5'],
            flags=sv.HTML5
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
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            'p:has(+ .dddd:has(+ div .jjjj))',
            ['2'],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            'p:has(~ .jjjj)',
            ['7', '8'],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup2,
            'div:has(> .bbbb, .ffff, .jjjj)',
            ['0', '4', '8'],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup2,
            'div:has(> :not(.bbbb, .ffff, .jjjj))',
            ['2', '6', '8'],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup2,
            'div:not(:has(> .bbbb, .ffff, .jjjj))',
            ['2', '6'],
            flags=sv.HTML5
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
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            ":nth-child(-n+3 of p)",
            ['0', '1', '7'],
            flags=sv.HTML5
        )

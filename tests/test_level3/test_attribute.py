"""Test attribute selectors."""
from .. import util


class TestAttribute(util.TestCase):
    """Test attribute selectors."""

    MARKUP = """
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
    """

    def test_attribute_begins(self):
        """Test attribute whose value begins with the specified value."""

        self.assert_selector(
            self.MARKUP,
            "[class^=here]",
            ["0"],
            flags=util.HTML
        )

    def test_attribute_end(self):
        """Test attribute whose value ends with the specified value."""

        self.assert_selector(
            self.MARKUP,
            "[class$=words]",
            ["0"],
            flags=util.HTML
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
            flags=util.HTML
        )

    def test_attribute_begins_cannot_have_empty(self):
        """Test attribute `^=` will match nothing when value is empty."""

        # An empty value cannot match anything per the spec.
        self.assert_selector(
            self.MARKUP,
            '[class^=""]',
            [],
            flags=util.HTML
        )

    def test_attribute_end_cannot_have_empty(self):
        """Test attribute `$=` will match nothing when value is empty."""

        # An empty value cannot match anything per the spec.
        self.assert_selector(
            self.MARKUP,
            '[class$=""]',
            [],
            flags=util.HTML
        )

    def test_attribute_contains_cannot_have_empty(self):
        """Test attribute `*=` will match nothing when value is empty."""

        # An empty value cannot match anything per the spec.
        self.assert_selector(
            self.MARKUP,
            '[class*=""]',
            [],
            flags=util.HTML
        )

    def test_attribute_contains_with_newlines(self):
        """Test attribute `*=` will match with new lines."""

        self.assert_selector(
            "<p><span id='1' title='foo bar'>foo1</span><span id='2' title='foo\nbar'>foo1</span></p>",
            "span[title*='bar']",
            ["1", "2"],
            flags=util.HTML
        )

    def test_attribute_starts_with_newlines(self):
        """Test attribute `^=` will match with new lines."""

        self.assert_selector(
            "<p><span id='1' title='foo bar'>foo1</span><span id='2' title='foo\nbar'>foo1</span></p>",
            "span[title^='foo']",
            ["1", "2"],
            flags=util.HTML
        )

    def test_attribute_ends_with_newlines(self):
        """Test attribute `$=` will match with new lines."""

        self.assert_selector(
            "<p><span id='1' title='foo bar'>foo1</span><span id='2' title='foo\nbar'>foo1</span></p>",
            "span[title$='bar']",
            ["1", "2"],
            flags=util.HTML
        )

    def test_attribute_ends_with_trailing_newline(self):
        """Test attribute `$=` will not match when the value is followed by a trailing newline."""

        self.assert_selector(
            "<p><span id='1' title='foo bar'>foo1</span><span id='2' title='foo bar\n'>foo1</span></p>",
            "span[title$='bar']",
            ["1"],
            flags=util.HTML
        )

    def test_attribute_dash_list_with_newlines(self):
        """Test attribute `|=` will match with new lines."""

        self.assert_selector(
            "<p><span id='1' title='fo-o bar'>foo1</span><span id='2' title='fo-o\nbar'>foo1</span></p>",
            "span[title|='fo']",
            ["1", "2"],
            flags=util.HTML
        )

    def test_attribute_space_list_with_newlines(self):
        """Test attribute `~=` will match with new lines."""

        self.assert_selector(
            "<p><span id='1' title='foo bar baz'>foo1</span><span id='2' title='foo\nbar baz'>foo1</span></p>",
            "span[title~='baz']",
            ["1", "2"],
            flags=util.HTML
        )

    def test_attribute_patterns_scan_for_value(self):
        """
        Test that attribute patterns can find the value with a literal scan.

        A leading `.*?`, or `re.I`, makes the regular expression engine retry the value at every position, which takes
        time quadratic in the length of the value when it nearly matches a long attribute value.
        """

        import re
        import soupsieve as sv

        for op in ('=', '~=', '|=', '^=', '$=', '*=', '!='):
            for case in ('', ' i', ' s'):
                for attr in ('title', 'type'):
                    selector = f'[{attr}{op}"aBc"{case}]'
                    attribute = sv.compile(selector).selectors[0].attributes[0]
                    for pattern in (attribute.pattern, attribute.xml_type_pattern):
                        if pattern is None:
                            continue
                        self.assertFalse(pattern.pattern.startswith('.*'), selector)
                        self.assertFalse(pattern.flags & re.I, selector)
                    self.assertEqual(attribute.ignore_case, case == ' i' or (attr == 'type' and not case), selector)
                    if attribute.ignore_case:
                        self.assertIn('abc', attribute.pattern.pattern, selector)

    def test_attribute_case_insensitive_long_near_match(self):
        """Test case insensitive `*=` and `$=` against a long attribute value that nearly matches."""

        markup = '<div id="1" title="{}"></div><div id="2" title="{}b"></div>'.format('A' * 2000, 'A' * 2000)
        self.assert_selector(markup, '[title*="{}B" i]'.format('a' * 500), ['2'], flags=util.HTML)
        self.assert_selector(markup, '[title$="{}B" i]'.format('a' * 500), ['2'], flags=util.HTML)
        self.assert_selector(markup, '[title*="{}B"]'.format('A' * 500), [], flags=util.HTML)

    def test_attribute_case_insensitive_ascii_only(self):
        """Test that case insensitive attribute values only fold ASCII letters."""

        markup = '<div id="1" title="CAFÉ"></div><div id="2" title="Café"></div><div id="3" title="K"></div>'
        self.assert_selector(markup, '[title*="café" i]', ['2'], flags=util.HTML)
        self.assert_selector(markup, '[title="k" i]', ['3'], flags=util.HTML)
        self.assert_selector(markup, '[title="\\212a" i]', [], flags=util.HTML)

"""Test comments."""
from .. import util
from soupsieve import SelectorSyntaxError


class TestComments(util.TestCase):
    """Test comments."""

    MARKUP = """
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

    def test_comments(self):
        """Test comments."""

        self.assert_selector(
            self.MARKUP,
            """
            /* Start comment */
            div
            /* This still works as new lines and whitespace count as descendant combiner.
               This comment won't be seen. */
            span#\\33
            /* End comment */
            """,
            ['3'],
            flags=util.HTML
        )

    def test_comments_in_pseudo_classes(self):
        """Test comments in pseudo-classes."""

        self.assert_selector(
            self.MARKUP,
            """
            span:not(
                /* Comments should basically work like they do in real CSS. */
                span#\\33 /* Don't select id 3 */
            )
            """,
            ['1', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_itrailing(self):
        """Test comments trailing."""

        self.assert_selector(
            self.MARKUP,
            """
            span /* ok */
            """,
            ['1', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_complex_trailing(self):
        """Test complex comments trailing."""

        self.assert_selector(
            self.MARKUP,
            """
            div /* a /* b */ span
            """,
            ['1', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_leading(self):
        """Test a comment directly leading a selector."""

        self.assert_selector(
            self.MARKUP,
            """/* Start comment */span""",
            ['1', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_leading_multiple(self):
        """Test comments directly leading a selector."""

        self.assert_selector(
            self.MARKUP,
            """/*a*//*b*/span""",
            ['1', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_leading_combinator(self):
        """Test a comment directly leading a selector with combinators."""

        self.assert_selector(
            self.MARKUP,
            """/* comment */div span""",
            ['1', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_trailing_no_space(self):
        """Test a comment directly trailing a selector."""

        self.assert_selector(
            self.MARKUP,
            """span/* ok */""",
            ['1', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_trailing_complex_no_space(self):
        """Test a comment directly trailing a complex selector."""

        self.assert_selector(
            self.MARKUP,
            """div span/* ok */""",
            ['1', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_leading_whitespace(self):
        """Test a comment leading a selector followed by whitespace."""

        self.assert_selector(
            self.MARKUP,
            """/* comment */ span""",
            ['1', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_leading_multiple_whitespace(self):
        """Test comments and whitespace leading a selector."""

        self.assert_selector(
            self.MARKUP,
            """/* a */ /* b */
            div /* c */ > /* d */ span""",
            ['3'],
            flags=util.HTML
        )

    def test_comments_leading_whitespace_combinator(self):
        """Test a comment and whitespace leading a combinator."""

        self.assert_raises('/* comment */ > span', SelectorSyntaxError)

    def test_comments_leading_whitespace_only(self):
        """Test a selector with only a comment and whitespace."""

        self.assert_raises('/* comment */ ', SelectorSyntaxError)

    def test_comments_in_compound(self):
        """Test that a comment between parts of a compound selector does not combine them."""

        self.assert_selector(
            self.MARKUP,
            """span/* comment */[id]/* comment */:not([id="1"])""",
            ['3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_comments_around_combinator_no_space(self):
        """Test comments directly around a combinator."""

        self.assert_selector(
            self.MARKUP,
            """div/* a */>/* b */span""",
            ['3'],
            flags=util.HTML
        )

    def test_comments_between_tags(self):
        """Test that a comment is not a descendant combinator."""

        self.assert_raises('div/* comment */span', SelectorSyntaxError)

    def test_comments_unterminated(self):
        """Test unterminated comments."""

        self.assert_raises('div/* comment', SelectorSyntaxError)
        self.assert_raises('div /* comment', SelectorSyntaxError)
        self.assert_raises('/* comment', SelectorSyntaxError)

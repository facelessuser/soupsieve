"""Test placeholder shown selectors."""
from .. import util


class TestPlaceholderShown(util.TestCase):
    """Test placeholder shown selectors."""

    def test_placeholder_shown(self):
        """Test placeholder shown."""

        markup = """
        <!-- These have a placeholder. -->
        <input id="0" placeholder="This is some text">
        <textarea id="1" placeholder="This is some text"></textarea>

        <!-- These do not have a placeholder. -->
        <input id="2" placeholder="">
        <input id="3">

        <!-- All types that should register has having a placeholder. -->
        <input id="4" type="email" placeholder="This is some text">
        <input id="5" type="number" placeholder="This is some text">
        <input id="6" type="password" placeholder="This is some text">
        <input id="7" type="search" placeholder="This is some text">
        <input id="8" type="tel" placeholder="This is some text">
        <input id="9" type="text" placeholder="This is some text">
        <input id="10" type="url" placeholder="This is some text">
        <input id="11" type="" placeholder="This is some text">
        <input id="12" type placeholder="This is some text">

        <!-- Types that should not register has having a placeholder. -->
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

        <!-- Value will not override this instance as value is empty. -->
        <input id="28" type placeholder="This is some text" value="">

        <!-- Value will override this input -->
        <input id="29" type placeholder="This is some text" value="Actual value">

        <!-- Text area content overrides the placehold-->
        <textarea id="30" placeholder="This is some text">Value</textarea>
        <textarea id="31" placeholder="This is some text">


        </textarea>

        <!-- Text area is still considered empty with a single new line (does not include carriage return). -->
        <textarea id="32" placeholder="This is some text">
        </textarea>
        """

        self.assert_selector(
            markup,
            ":placeholder-shown",
            ['0', '1', '4', '5', '6', '7', '8', '9', '10', '11', '12', '28', '32'],
            flags=util.HTML
        )

    def test_placeholder_shown_unknown_type(self):
        """Test that an `input` with an unknown `type` is a text input."""

        markup = """
        <input id="0" type="foo" placeholder="This is some text">
        <input id="1" type="datetime" placeholder="This is some text">
        <input id="2" type=" text" placeholder="This is some text">
        <input id="3" type="CHECKBOX" placeholder="This is some text">
        """

        self.assert_selector(
            markup,
            ":placeholder-shown",
            ['0', '1', '2'],
            flags=util.HTML
        )

    def test_placeholder_shown_sanitized_value(self):
        """Test that an input's value is sanitized before checking that it is empty."""

        markup = """
        <!-- Line breaks are removed from the value. -->
        <input id="0" type="text" placeholder="This is some text" value="&#10;">
        <input id="1" type="password" placeholder="This is some text" value="&#13;&#10;">
        <input id="2" type="text" placeholder="This is some text" value=" ">

        <!-- Leading and trailing whitespace is removed from a URL or an email. -->
        <input id="3" type="url" placeholder="This is some text" value=" ">
        <input id="4" type="email" placeholder="This is some text" value="&#9;&#10;">
        <input id="5" type="email" placeholder="This is some text" value=" a@b ">

        <!-- A number that is not a valid floating-point number is removed. -->
        <input id="6" type="number" placeholder="This is some text" value="abc">
        <input id="7" type="number" placeholder="This is some text" value=" 7 ">
        <input id="8" type="number" placeholder="This is some text" value="+1">
        <input id="9" type="number" placeholder="This is some text" value="1.">
        <input id="10" type="number" placeholder="This is some text" value="Infinity">
        <input id="11" type="number" placeholder="This is some text" value="-.5e2">

        <!-- A number that overflows a double is removed, as in all browsers. -->
        <input id="12" type="number" placeholder="This is some text" value="1e9999">
        <input id="13" type="number" placeholder="This is some text" value="-1e9999">
        """

        self.assert_selector(
            markup,
            ":placeholder-shown",
            ['0', '1', '3', '4', '6', '7', '8', '9', '10', '12', '13'],
            flags=util.HTML
        )

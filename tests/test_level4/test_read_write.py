"""Test read write selectors."""
from .. import util


class TestReadWrite(util.TestCase):
    """Test read write selectors."""

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
            flags=util.HTML
        )

    def test_read_write_editable(self):
        """Test that editing hosts, including `plaintext-only` ones, and the editable elements inside them match."""

        markup = """
        <body>
        <div id="0" contenteditable="plaintext-only"><span id="1">Text</span></div>
        <div id="2" contenteditable="PLAINTEXT-ONLY">Text</div>
        <div id="3" contenteditable><p id="4"><b id="5">Text</b></p></div>
        <div id="6" contenteditable="true"><p id="7" contenteditable="false"><b id="8">Text</b></p></div>
        <div id="9" contenteditable="false"><p id="10" contenteditable><b id="11">Text</b></p></div>
        <div id="12" contenteditable><p id="13" contenteditable="bogus"><b id="14">Text</b></p></div>
        <div id="15" contenteditable><input id="16" readonly><input id="17"><select id="18"></select></div>
        <p id="19" contenteditable=" true">Text</p>
        </body>
        """

        self.assert_selector(
            markup,
            "body :read-write",
            ['0', '1', '2', '3', '4', '5', '6', '10', '11', '12', '13', '14', '15', '17', '18'],
            flags=util.HTML
        )

    def test_read_write_unknown_type(self):
        """Test that an `input` with an unknown `type` is a text input."""

        markup = """
        <input id="0" type="foo">
        <input id="1" type="datetime">
        <input id="2" type="foo" readonly>
        <input id="3" type="foo" disabled>
        <input id="4" type="Color">
        """

        self.assert_selector(
            markup,
            "input:read-write",
            ['0', '1'],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            "input:read-only",
            ['2', '3', '4'],
            flags=util.HTML
        )

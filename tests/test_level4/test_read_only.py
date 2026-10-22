"""Test read only selectors."""
from .. import util


class TestReadOnly(util.TestCase):
    """Test read only selectors."""

    def test_read_only(self):
        """Test read only."""

        markup = """
        <body>
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
        </body>
        """

        self.assert_selector(
            markup,
            "body :read-only",
            [
                '3', '13', '14', '15', '18', '19', '20', '22',
                '23', '24', '25', '31', '32', '33'
            ],
            flags=util.HTML
        )

    def test_read_only_editable(self):
        """Test that elements inside an editing host only match when a `contenteditable="false"` is nearer."""

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
            "body :read-only",
            ['7', '8', '9', '16', '19'],
            flags=util.HTML
        )

"""Test read write selectors."""
from .. import util
import soupsieve as sv


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

    def test_read_write_foreign_contenteditable(self):
        """Test that `contenteditable` is ignored on non-HTML elements, which inherit the state of their parent."""

        markup = """
        <body>
        <svg id="0" contenteditable><foreignObject id="1" contenteditable="true"><p id="2">Text</p>
        </foreignObject></svg>
        <svg id="3"><foreignObject id="4" contenteditable><div id="5">Text</div></foreignObject></svg>
        <div id="6" contenteditable="false">
        <svg id="7"><foreignObject id="8" contenteditable="plaintext-only"><p id="9">Text</p></foreignObject></svg>
        </div>
        <div id="10" contenteditable>
        <svg id="11"><foreignObject id="12" contenteditable="false"><p id="13">Text</p></foreignObject></svg>
        </div>
        <div id="14" contenteditable>
        <svg id="15"><foreignObject id="16"><p id="17" contenteditable="false"><b id="18" contenteditable></b></p>
        </foreignObject></svg>
        </div>
        <math id="19" contenteditable><mtext id="20" contenteditable><b id="21">Text</b></mtext></math>
        </body>
        """

        self.assert_selector(
            markup,
            "body :read-write",
            ['10', '13', '14', '18'],
            flags=util.HTML5
        )

    def test_read_write_contenteditable_no_namespaces(self):
        """Test that all elements are HTML elements, and can be editing hosts, if the parser has no namespaces."""

        markup = """
        <svg id="0" contenteditable><p id="1">Text</p></svg>
        """

        self.assert_selector(
            markup,
            ":read-write",
            ['0', '1'],
            flags=util.PYHTML
        )

    def test_read_write_iframe(self):
        """Test that the contents of an `iframe` do not inherit `contenteditable`, as they are in another document."""

        soup = self.soup('<div id="0" contenteditable><iframe id="1"></iframe></div>', 'html.parser')
        div = soup.new_tag('div', attrs={'id': '2'})
        div.append(soup.new_tag('p', attrs={'id': '3'}))
        soup.iframe.append(div)
        soup.iframe.append(soup.new_tag('p', attrs={'id': '4', 'contenteditable': ''}))

        self.assertEqual([el['id'] for el in sv.select(':read-write', soup)], ['0', '1', '4'])

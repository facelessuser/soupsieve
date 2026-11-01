"""Test direction selectors."""
from .. import util
import soupsieve as sv
from soupsieve import SelectorSyntaxError
from bs4 import BeautifulSoup

IFRAME_TEXT = BeautifulSoup('<iframe><div></div></iframe>', 'html.parser').iframe.text == '<div></div>'


class TestDir(util.TestCase):
    """Test direction selectors."""

    MARKUP = """
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
      <input id="19" dir="auto" value="עִבְרִית">
      <input id="20" type="" dir="auto" value="עִבְרִית">
    </div>
    </body>
    </html>
    """

    def test_dir_rtl(self):
        """Test general direction right to left."""

        self.assert_selector(
            self.MARKUP,
            "div:dir(rtl)",
            ["1", "4", "6"],
            flags=util.HTML
        )

    def test_dir_ltr(self):
        """Test general direction left to right."""

        self.assert_selector(
            self.MARKUP,
            "div:dir(ltr)",
            ["3"],
            flags=util.HTML
        )

    def test_dir_conflict(self):
        """Test conflicting direction."""

        self.assert_selector(
            self.MARKUP,
            "div:dir(ltr):dir(rtl)",
            [],
            flags=util.HTML
        )

    def test_dir_xml(self):
        """Test direction with XML (not supported)."""

        self.assert_selector(
            self.MARKUP,
            "div:dir(ltr)",
            [],
            flags=util.XML
        )

    def test_dir_bidi_detect(self):
        """Test bidirectional detection."""

        self.assert_selector(
            self.MARKUP,
            "span:dir(rtl)",
            ['2', '7'],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            "span:dir(ltr)",
            ['5', '8'],
            flags=util.HTML
        )

    def test_dir_on_input(self):
        """Test input direction rules."""

        self.assert_selector(
            self.MARKUP,
            ":is(input, textarea):dir(ltr)",
            ['9', '10', '11', '12', '13', '15', '16', '18'],
            flags=util.HTML5
        )

        self.assert_selector(
            self.MARKUP,
            ":is(input, textarea):dir(rtl)",
            ['14', '17', '19', '20'],
            flags=util.HTML5
        )

    def test_dir_on_input_unknown_type(self):
        """Test that `dir="auto"` uses the value of an `input` with an unknown `type`."""

        markup = """
        <html id="0">
        <head></head>
        <body>
        <input id="1" type="foo" dir="auto" value="עִבְרִית">
        <input id="2" type="datetime" dir="auto" value="עִבְרִית">
        <input id="3" type="foo" dir="auto" value="English">
        <input id="4" type="color" dir="auto" value="עִבְרִית">
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "input:dir(rtl)",
            ['1', '2'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "input:dir(ltr)",
            ['3', '4'],
            flags=util.HTML5
        )

    def test_dir_auto_nested(self):
        """Test nested auto direction resolved from ancestors."""

        markup = """
        <html id="0">
        <head></head>
        <body>
        <div id="1" dir="auto">עִבְרִית
          <div id="2" dir="auto">()
            <div id="3" dir="auto"><span id="4">()</span></div>
          </div>
          <div id="5" dir="auto">test<span id="6">()</span></div>
          <span id="7">()</span>
        </div>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            ":is(div, span):dir(rtl)",
            ["1","7"],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            markup,
            ":is(div, span):dir(ltr)",
            ["2","3","4","5","6"],
            flags=util.HTML | util.NOCACHE
        )

    def test_dir_on_root(self):
        """Test that the root is assumed left to right if not explicitly defined."""

        self.assert_selector(
            self.MARKUP,
            "html:dir(ltr)",
            ['0'],
            flags=util.HTML
        )

    def test_dir_auto_root(self):
        """Test that the root is assumed left to right if auto used."""

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
            flags=util.HTML
        )

    def test_dir_on_input_root(self):
        """Test input direction when input is the root."""

        markup = """<input id="1" type="text" dir="auto">"""
        # Input is root
        for parser in util.available_parsers('html.parser', 'lxml', 'html5lib'):
            soup = self.soup(markup, parser)
            fragment = soup.input.extract()
            self.assertTrue(sv.match(":root:dir(ltr)", fragment, flags=sv.DEBUG))

    def test_iframe(self):
        """Test direction in `iframe`."""

        markup = """
        <html>
        <head></head>
        <body>
        <div id="1" dir="auto">
        <iframe>
        <html>
        <body>
        <div id="2" dir="auto">
        <!-- comment -->עִבְרִית
        <span id="5" dir="auto">()</span></div>
        </div>
        </body>
        </html>
        </iframe>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "div:dir(ltr)",
            ['1'],
            flags=util.PYHTML
        )

        self.assert_selector(
            markup,
            "div:dir(rtl)",
            [] if IFRAME_TEXT else ['2'],
            flags=util.PYHTML
        )

    def test_xml_in_html(self):
        """Test cases for when we have XML in HTML."""

        markup = """
        <html>
        <head></head>
        <body>
        <div id="1" dir="auto">
        <math id="2">
        <!-- comment -->עִבְרִית
        </math>
        other text
        </div>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "div:dir(ltr)",
            [],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "div:dir(rtl)",
            ['1'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "math:dir(rtl)",
            ['2'],
            flags=util.HTML5
        )

    def test_auto_non_html_elements(self):
        """Test that `dir="auto"` analyzes the text of non-HTML elements, and only ignores HTML elements."""

        markup = """
        <html>
        <head></head>
        <body>
        <div id="1" dir="auto"><svg dir="ltr"><text>עִבְרִית</text></svg>text</div>
        <div id="2" dir="auto"><math dir="ltr"><mi>עִבְרִית</mi></math>text</div>
        <div id="3" dir="auto"><svg><style>עִבְרִית</style></svg>text</div>
        <div id="4" dir="auto"><svg><script>עִבְרִית</script></svg>text</div>
        <div id="5" dir="auto"><svg><bdi>עִבְרִית</bdi></svg>text</div>
        <div id="6" dir="auto"><svg><textarea>עִבְרִית</textarea></svg>text</div>
        <div id="7" dir="auto"><svg><foreignObject><p>עִבְרִית</p></foreignObject></svg>text</div>
        <div id="8" dir="auto"><svg><foreignObject><p dir="ltr">עִבְרִית</p></foreignObject></svg>text</div>
        <div id="9" dir="auto"><svg><foreignObject><bdi>עִבְרִית</bdi></foreignObject></svg>text</div>
        <bdi id="10"><math>עִבְרִית</math></bdi>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "[id]:dir(rtl)",
            ['1', '2', '3', '4', '5', '6', '7', '10'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "[id]:dir(ltr)",
            ['8', '9'],
            flags=util.HTML5
        )

    def test_auto_template(self):
        """Test that `dir="auto"` does not analyze the contents of a `template`."""

        markup = """
        <html>
        <head></head>
        <body>
        <div id="1" dir="auto"><template>עִבְרִית</template>text</div>
        <div id="2" dir="auto"><template><p>עִבְרִית</p></template></div>
        <bdi id="3"><template>עִבְרִית</template>text</bdi>
        <div dir="rtl"><template id="4" dir="auto">עִבְרִית</template></div>
        <svg><template id="5"></template></svg>
        <div id="6" dir="auto"><svg><template>עִבְרִית</template></svg>text</div>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            ":is(div, bdi, template)[id]:dir(ltr)",
            ['1', '2', '3', '4', '5'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "div[id]:dir(rtl)",
            ['6'],
            flags=util.HTML5
        )

    def test_template_contents(self):
        """Test that the contents of a `template` do not inherit from it, but still resolve among themselves."""

        markup = """
        <html id="0" dir="rtl">
        <head></head>
        <body>
        <template id="1"><p id="2"><span id="3"></span></p></template>
        <template id="4" dir="rtl"><p id="5"></p><svg id="6"><g id="7"></g></svg></template>
        <template id="8">
        <div id="9" dir="rtl"><p id="10"></p><template id="11"><p id="12"></p></template></div>
        </template>
        <template id="13"><div id="14" dir="auto">עִבְרִית<p id="15"></p></div></template>
        <template id="16"><bdi id="17">עִבְרִית</bdi></template>
        <div id="18" dir="auto">עִבְרִית<template id="19"><p id="20"></p></template></div>
        <svg id="21"><template id="22"><g id="23"></g></template></svg>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "[id]:dir(ltr)",
            ['2', '3', '5', '6', '7', '12', '20'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "[id]:dir(rtl)",
            ['0', '1', '4', '8', '9', '10', '11', '13', '14', '15', '16', '17', '18', '19', '21', '22', '23'],
            flags=util.HTML5
        )

    def test_auto_iframe_text(self):
        """Test that `dir="auto"` analyzes the text of an `iframe`, which is just a text node in a browser."""

        markup = """
        <html>
        <head></head>
        <body>
        <div id="1" dir="auto"><iframe>עִבְרִית</iframe>text</div>
        <div dir="ltr"><iframe id="2" dir="auto">עִבְרִית</iframe></div>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "[id]:dir(rtl)",
            ['1', '2'],
            flags=util.HTML5
        )

    def test_auto_iframe_elements(self):
        """Test that `dir="auto"` does not analyze elements in an `iframe`, as they are in another document."""

        soup = self.soup('<div id="1" dir="auto"><iframe id="2" dir="auto"></iframe>text</div>', 'html.parser')
        for name in ('p', 'span'):
            tag = soup.new_tag(name)
            tag.string = 'עִבְרִית'
            soup.iframe.append(tag)

        self.assertTrue(sv.match(':dir(ltr)', soup.div))
        self.assertTrue(sv.match(':dir(ltr)', soup.iframe))

    def test_iframe_top_level_elements(self):
        """Test that elements directly in an `iframe` do not inherit, even if there are many of them."""

        soup = self.soup('<div dir="rtl"><iframe></iframe></div>', 'html.parser')
        for name in ('p', 'span'):
            soup.iframe.append(soup.new_tag(name))

        self.assertTrue(sv.match(':dir(rtl)', soup.iframe))
        self.assertTrue(sv.match(':dir(ltr)', soup.p))
        self.assertTrue(sv.match(':dir(ltr)', soup.span))

    def test_top_level_elements(self):
        """Test that elements without a parent element are left to right when there is no single root."""

        markup = """
        <div id="1"><span id="2"></span></div>
        <div id="3" dir="rtl"><span id="4"></span></div>
        <div id="5"></div>
        <bdi id="6">עִבְרִית</bdi>
        """

        self.assert_selector(
            markup,
            "[id]:dir(ltr)",
            ['1', '2', '5'],
            flags=util.PYHTML
        )

        self.assert_selector(
            markup,
            "[id]:dir(rtl)",
            ['3', '4', '6'],
            flags=util.PYHTML
        )

    def test_top_level_non_html_elements(self):
        """Test that a non-HTML element without a parent element is left to right."""

        markup = '<html id="1"><head></head><body></body></html>'
        soup = self.soup(markup, 'html5lib')
        svg = soup.new_tag('svg', namespace='http://www.w3.org/2000/svg', attrs={'id': '2'})
        soup.append(svg)

        self.assertEqual([el['id'] for el in sv.select(':dir(ltr)[id]', soup)], ['1', '2'])

    def test_bdi_on_root(self):
        """Test that `bdi` uses its text for direction when it is the root."""

        markup = """<bdi id="1">עִבְרִית<span id="2"></span></bdi>"""
        for parser in util.available_parsers('html.parser', 'lxml', 'html5lib'):
            soup = self.soup(markup, parser)
            fragment = soup.bdi.extract()
            self.assertTrue(sv.match(':root:dir(rtl)', fragment))
            self.assertTrue(sv.match(':dir(rtl)', fragment.span))

    def test_dir_auto_input_value_states(self):
        """Test the `input` states that use their value for `dir="auto"`, and those that do not."""

        markup = """
        <html>
        <head></head>
        <body>
        <input id="1" type="hidden" dir="auto" value="עִבְרִית">
        <input id="2" type="password" dir="auto" value="עִבְרִית">
        <input id="3" type="submit" dir="auto" value="עִבְרִית">
        <input id="4" type="reset" dir="auto" value="עִבְרִית">
        <input id="5" type="button" dir="auto" value="עִבְרִית">
        <input id="6" type="SUBMIT" dir="auto" value="עִבְרִית">
        <input id="7" type="date" dir="auto" value="עִבְרִית">
        <input id="8" type="number" dir="auto" value="עִבְרִית">
        <input id="9" type="range" dir="auto" value="עִבְרִית">
        <input id="10" type="checkbox" dir="auto" value="עִבְרִית">
        <input id="11" type="radio" dir="auto" value="עִבְרִית">
        <input id="12" type="file" dir="auto" value="עִבְרִית">
        <input id="13" type="image" dir="auto" value="עִבְרִית">
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "input:dir(rtl)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "input:dir(ltr)",
            ['7', '8', '9', '10', '11', '12', '13'],
            flags=util.HTML5
        )

    def test_dir_unknown_value(self):
        """Test that an identifier other than `ltr` and `rtl` is valid, but does not match anything."""

        for selector in (':dir(foo)', ':dir(auto)', ':dir(ltrx)', ':dir(-x)', ':dir(--x)'):
            self.assert_selector(
                self.MARKUP,
                selector,
                [],
                flags=util.HTML
            )

        self.assert_selector(
            self.MARKUP,
            "span:not(:dir(foo))",
            ['2', '5', '7', '8'],
            flags=util.HTML
        )

    def test_dir_escaped_value(self):
        """Test that the value can be escaped and is not case sensitive."""

        self.assert_selector(
            self.MARKUP,
            r"span:dir(\72 tl)",
            ['2', '7'],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            r"span:dir(\4c TR)",
            ['5', '8'],
            flags=util.HTML
        )

    def test_dir_invalid_value(self):
        """Test that the value must be a single identifier."""

        for selector in (':dir()', ':dir( )', ':dir(ltr rtl)', ':dir(ltr, rtl)', ':dir("ltr")', ':dir(1)', ':dir(*)'):
            self.assert_raises(selector, SelectorSyntaxError)

    def test_non_html_elements_inherit_direction(self):
        """Test that non-HTML elements, which have no `dir` attribute, inherit the direction of their parent."""

        markup = """
        <html>
        <head></head>
        <body>
        <div dir="rtl">
        <svg id="1"><g id="2"></g><foreignObject id="3"><p id="4">text</p></foreignObject></svg>
        <math id="5"><mi id="6">x</mi></math>
        </div>
        <svg id="7" dir="rtl"><g id="8"></g></svg>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "[id]:dir(rtl)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML5
        )

        self.assert_selector(
            markup,
            "[id]:dir(ltr)",
            ['7', '8'],
            flags=util.HTML5
        )

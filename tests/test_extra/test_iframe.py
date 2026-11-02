"""
Test that an `iframe` is handled like any other element, as it is in a browser.

The document that a browser shows in an `iframe` is not its contents. HTML parsers escape the
contents of an `iframe`, so it only has text, and the elements in one only come from XHTML or
from adding them to the tree. Either way, browsers treat them as normal children.
"""
from .. import util
import soupsieve as sv
from bs4 import BeautifulSoup
import pytest


class TestIframe(util.TestCase):
    """Test `iframe` handling."""

    HEBREW = 'עִבְרִית'

    MARKUP = f"""
    <div id="lang" lang="de"><iframe><p id="lang-p">x</p></iframe></div>
    <div id="dir" dir="rtl"><iframe><p id="dir-p">x</p></iframe></div>
    <div id="auto" dir="auto"><iframe><span>{HEBREW}</span></iframe>text</div>
    <div id="auto-text" dir="auto"><iframe>{HEBREW}</iframe>text</div>
    <div id="edit" contenteditable="true"><iframe><p id="edit-p">x</p></iframe></div>
    <form id="form1"><iframe><button id="btn1" type="submit">a</button></iframe><button id="btn2" type="submit">b</button></form>
    <form id="f2"></form><iframe><button id="btn3" form="f2" type="submit">c</button></iframe>
    <form><input type="radio" name="a" id="r1" checked="checked"/><iframe><input type="radio" name="a" id="r2" checked="checked"/></iframe></form>
    <form><iframe><input type="radio" name="b" id="r3"/></iframe><input type="radio" name="b" id="r4" checked="checked"/></form>
    <select id="sel"><option id="o1">1</option><iframe><option id="o2" selected="selected">2</option></iframe></select>
    <iframe id="f-root"><html id="inner-html"><body><p id="root-p">x</p></body></html></iframe>
    <iframe id="f-empty-el"><p id="empty-p"></p></iframe>
    <iframe id="f-empty-text">text</iframe>
    """  # noqa: E501

    @staticmethod
    def ids(elements):
        """Get the IDs of the elements."""

        return [el['id'] for el in elements]

    def by_hand(self):
        """
        Get the markup with the escaped contents of each `iframe` added to it as elements.

        Older versions of Python's `html.parser` already parse them as elements.
        """

        soup = self.soup(self.MARKUP, 'html.parser')
        for frame in soup.find_all('iframe'):
            text = frame.string
            if text is not None and '<' in text:
                frame.clear()
                frame.extend(list(BeautifulSoup(text, 'html.parser').contents))
        return soup

    def xhtml(self):
        """Get the markup as XHTML, where the contents of each `iframe` are parsed as elements."""

        return self.soup(self.wrap_xhtml(self.MARKUP), 'xml')

    def soups(self):
        """Get every way of putting elements in an `iframe`, with every cache state."""

        makers = [self.by_hand]
        if util.LXML_PRESENT:
            makers.append(self.xhtml)
        for make in makers:
            for flags in (0, sv.NOCACHE):
                yield make(), flags

    def test_parsers_escape_contents(self):
        """Test that HTML parsers escape the contents of an `iframe`, so it only has text."""

        escaping = (util.HTML5, util.LXML_HTML) + ((util.PYHTML,) if util.PYHTML_ESCAPES_IFRAME else ())
        markup = '<div id="1"><iframe id="2"><p id="3">text</p></iframe></div>'
        for flags in escaping:
            self.assert_selector(markup, 'p', [], flags=flags)
            self.assert_selector(markup, 'iframe', ['2'], flags=flags)
            self.assert_selector(markup, 'iframe:empty', [], flags=flags)
            self.assert_selector(markup, '[id]:-soup-contains("<p")', ['1', '2'], flags=flags)

        # The text is used to find the direction, and only the text of the `iframe` is right to left.
        markup = f"""
        <div id="1" dir="auto"><iframe>{self.HEBREW}</iframe>text</div>
        <div><iframe id="2" dir="auto">{self.HEBREW}</iframe></div>
        """

        self.assert_selector(markup, '[dir=auto]:dir(rtl)', ['1', '2'], flags=util.HTML)

    @pytest.mark.skipif(util.PYHTML_ESCAPES_IFRAME, reason="requires an `html.parser` that doesn't escape `iframe`")
    def test_parser_does_not_escape_contents(self):
        """Test that older versions of Python's `html.parser` parse the contents of an `iframe` as normal children."""

        markup = '<div id="1"><iframe id="2"><p id="3">text</p></iframe></div>'

        self.assert_selector(markup, 'iframe > p', ['3'], flags=util.PYHTML)
        self.assert_selector(markup, 'div p', ['3'], flags=util.PYHTML)
        self.assert_selector(markup, 'iframe:empty', [], flags=util.PYHTML)
        self.assert_selector(markup, '[id]:-soup-contains("text")', ['1', '2', '3'], flags=util.PYHTML)

    def test_contents_are_children(self):
        """Test that the elements in an `iframe` are selected like any other children."""

        for soup, flags in self.soups():
            self.assertEqual(
                self.ids(sv.select('iframe > p', soup, flags=flags)),
                ['lang-p', 'dir-p', 'edit-p', 'empty-p']
            )
            self.assertEqual(self.ids(sv.select('#f-root p', soup, flags=flags)), ['root-p'])
            self.assertEqual(self.ids(sv.select('div p', soup, flags=flags)), ['lang-p', 'dir-p', 'edit-p'])
            self.assertEqual(self.ids(sv.select('iframe:has(> html)', soup, flags=flags)), ['f-root'])
            self.assertEqual(sv.closest('div', soup.find(id='lang-p'), flags=flags)['id'], 'lang')
            self.assertTrue(sv.match('iframe > p:first-child:only-child', soup.find(id='empty-p'), flags=flags))

    def test_contents_are_not_root(self):
        """Test that the top of the elements in an `iframe` is not the root."""

        for soup, flags in self.soups():
            self.assertFalse(sv.match(':root', soup.find(id='inner-html'), flags=flags))
            self.assertEqual(sv.select(':root', soup.find(id='f-root'), flags=flags), [])

    def test_empty(self):
        """Test that an `iframe` with elements or text is not empty."""

        for soup, flags in self.soups():
            self.assertEqual(sv.select('iframe:empty', soup, flags=flags), [])

    def test_contains(self):
        """Test that the text in an `iframe` is part of the text of its ancestors."""

        for soup, flags in self.soups():
            self.assertEqual(
                self.ids(sv.select(f'div:-soup-contains({self.HEBREW})', soup, flags=flags)),
                ['auto', 'auto-text']
            )

    def test_inherited_states(self):
        """Test that the elements in an `iframe` inherit language, direction, and editability."""

        for soup, flags in self.soups():
            self.assertTrue(sv.match(':lang(de)', soup.find(id='lang-p'), flags=flags))
            self.assertTrue(sv.match(':read-write', soup.find(id='edit-p'), flags=flags))
            self.assertTrue(sv.match(':dir(rtl)', soup.find(id='dir-p'), flags=flags))
            self.assertEqual(self.ids(sv.select('[dir=auto]:dir(rtl)', soup, flags=flags)), ['auto', 'auto-text'])

    def test_forms(self):
        """Test that the controls in an `iframe` belong to the forms around it, or that they refer to."""

        for soup, flags in self.soups():
            self.assertEqual(self.ids(sv.select('button:default', soup, flags=flags)), ['btn1', 'btn3'])
            self.assertEqual(self.ids(sv.select('input:checked', soup, flags=flags)), ['r2', 'r4'])
            self.assertEqual(sv.select(':indeterminate', soup, flags=flags), [])
            self.assertEqual(self.ids(sv.select('option:checked', soup, flags=flags)), ['o2'])

    def test_template_in_iframe(self):
        """Test that the contents of a `template` in an `iframe` are still not reached."""

        soup = self.soup('<iframe></iframe>', 'html.parser')
        soup.iframe.append(self.soup('<template id="t"><p id="1"></p></template>', 'html.parser').template)

        self.assertEqual(sv.select('p', soup), [])
        self.assertEqual(self.ids(sv.select('p', soup.template)), ['1'])

    @util.requires_lxml
    def test_not_html(self):
        """Test that an element named `iframe` in XML has normal children too."""

        markup = """<?xml version="1.0" encoding="UTF-8"?>
        <root><iframe id="1"><p id="2"></p></iframe></root>
        """

        self.assert_selector(markup, 'iframe > p', ['2'], flags=util.XML)
        self.assert_selector(markup, 'root p', ['2'], flags=util.XML)

"""Test that the contents of a `template` are treated as being separate from the document."""
from .. import util
import soupsieve as sv


class TestTemplate(util.TestCase):
    """Test `template` handling."""

    MARKUP = """
    <!DOCTYPE html>
    <html id="root">
    <head></head>
    <body id="body">
    <div id="out">
    <template id="t"><div id="in"><p id="p">text</p><i id="i"></i></div><span id="s"></span></template>
    <span id="after"></span>
    </div>
    </body>
    </html>
    """

    @staticmethod
    def ids(elements):
        """Get the IDs of the elements."""

        return [el['id'] for el in elements]

    def soups(self, markup=None):
        """Get the markup from every parser and cache state."""

        for parser in util.available_parsers('html.parser', 'lxml', 'html5lib'):
            for flags in (0, sv.NOCACHE):
                yield self.soup(self.MARKUP if markup is None else markup, parser), flags

    def test_contents_not_selected_from_document(self):
        """Test that selectors do not descend into a `template`."""

        for selector in ('p', 'i', 'div p', '#out p', 'template p', 'template > div', 'template div'):
            self.assert_selector(self.MARKUP, selector, [], flags=util.HTML | util.NOCACHE)

    def test_template_is_an_element(self):
        """Test that a `template` itself is selected like any other element."""

        self.assert_selector(self.MARKUP, '[id]', ['root', 'body', 'out', 't', 'after'], flags=util.HTML)
        self.assert_selector(self.MARKUP, 'template + span', ['after'], flags=util.HTML | util.NOCACHE)
        self.assert_selector(self.MARKUP, 'template ~ span', ['after'], flags=util.HTML | util.NOCACHE)
        self.assert_selector(self.MARKUP, '#after:nth-child(2)', ['after'], flags=util.HTML | util.NOCACHE)
        self.assert_selector(self.MARKUP, 'div:has(> template)', ['out'], flags=util.HTML | util.NOCACHE)

    def test_template_has_no_children(self):
        """Test that a `template` is treated as having no children, but still counts as a child itself."""

        markup = """
        <!DOCTYPE html>
        <html id="root">
        <head></head>
        <body>
        <div id="1"><template id="2"><p></p></template></div>
        <div id="3"><template id="4">text</template></div>
        <div id="5"></div>
        </body>
        </html>
        """

        self.assert_selector(markup, 'template:empty', ['2', '4'], flags=util.HTML)
        self.assert_selector(markup, 'div:empty', ['5'], flags=util.HTML)
        self.assert_selector(markup, 'div:has(p)', [], flags=util.HTML | util.NOCACHE)
        self.assert_selector(markup, 'template:has(p)', [], flags=util.HTML | util.NOCACHE)
        self.assert_selector(markup, 'template:has(> p)', [], flags=util.HTML | util.NOCACHE)

    def test_select_from_template(self):
        """Test that selecting from a `template` is how the contents are reached."""

        for soup, flags in self.soups():
            template = soup.template
            self.assertEqual(self.ids(sv.select('p', template, flags=flags)), ['p'])
            self.assertEqual(self.ids(sv.select('div p', template, flags=flags)), ['p'])
            self.assertEqual(self.ids(sv.select('#in, span', template, flags=flags)), ['in', 's'])
            self.assertEqual(self.ids(sv.select('[id]', template, limit=1, flags=flags)), ['in'])
            self.assertEqual(sv.select_one('p', template, flags=flags)['id'], 'p')
            self.assertEqual(self.ids(sv.iselect('i', template, flags=flags)), ['i'])
            self.assertEqual(self.ids(sv.filter('span', template, flags=flags)), ['s'])

    def test_compiled_pattern_from_different_scopes(self):
        """Test that the scope of a compiled pattern determines what it finds."""

        for soup, flags in self.soups():
            pattern = sv.compile('p', flags=flags)
            self.assertEqual(pattern.select(soup), [])
            self.assertEqual(self.ids(pattern.select(soup.template)), ['p'])
            self.assertEqual(pattern.select(soup), [])

    def test_selectors_stop_at_template(self):
        """Test that selectors in the contents can't see beyond the `template`."""

        for selector in ('#out p', 'template p', 'template > div', 'body p', 'html p', ':root p', ':scope p'):
            for soup, flags in self.soups():
                self.assertEqual(sv.select(selector, soup.template, flags=flags), [])

        for soup, flags in self.soups():
            contents = soup.find(id='in')
            self.assertEqual(self.ids(sv.select('div p', contents, flags=flags)), ['p'])
            self.assertEqual(self.ids(sv.select(':scope > p', contents, flags=flags)), ['p'])
            for selector in ('#out p', 'template p', 'body p', 'html *', ':root p'):
                self.assertEqual(sv.select(selector, contents, flags=flags), [])

    def test_match_stops_at_template(self):
        """Test that matching an element in the contents can't see beyond the `template`."""

        for soup, flags in self.soups():
            el = soup.find(id='p')
            self.assertTrue(sv.match('div p', el, flags=flags))
            self.assertTrue(sv.match('#in > p', el, flags=flags))
            for selector in ('#out p', 'template p', 'body p', 'html p', ':root p'):
                self.assertFalse(sv.match(selector, el, flags=flags))

            # `not` is also unaware of what is outside.
            self.assertTrue(sv.match('p:not(template *)', el, flags=flags))

    def test_closest_stops_at_template(self):
        """Test that closest can't leave the `template`."""

        for soup, flags in self.soups():
            el = soup.find(id='p')
            self.assertEqual(sv.closest('div', el, flags=flags)['id'], 'in')
            for selector in ('#out', 'template', 'body', 'html'):
                self.assertIsNone(sv.closest(selector, el, flags=flags))

            # The element itself is not inside.
            self.assertEqual(sv.closest('template', soup.template, flags=flags)['id'], 't')
            self.assertEqual(sv.closest('#out', soup.template, flags=flags)['id'], 'out')

    def test_contents_are_not_root(self):
        """Test that the top level contents are never the root."""

        for soup, flags in self.soups():
            self.assertEqual(sv.select(':root', soup.template, flags=flags), [])
            self.assertFalse(sv.match(':root', soup.find(id='in'), flags=flags))

    def test_top_level_siblings(self):
        """Test that the top level contents have no parent element, but they are still siblings."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <template id="t"><div id="1"></div><p id="2"></p><span id="3"></span><p id="4"></p></template>
        </body>
        </html>
        """

        cases = (
            (':first-child', ['1']),
            (':last-child', ['4']),
            (':only-child', []),
            (':nth-child(2)', ['2']),
            (':nth-last-child(2)', ['3']),
            (':nth-child(2 of p)', ['4']),
            (':nth-last-child(2 of p)', ['2']),
            ('p:first-of-type', ['2']),
            ('p:last-of-type', ['4']),
            ('p:nth-of-type(2)', ['4']),
            ('p:nth-last-of-type(2)', ['2']),
            ('div:only-of-type', ['1']),
            ('div + p', ['2']),
            ('div ~ p', ['2', '4']),
            ('div ~ span + p', ['4']),
            ('div:has(+ p)', ['1']),
            ('div:has(~ span)', ['1']),
            ('p:has(~ p)', ['2'])
        )

        for soup, flags in self.soups(markup):
            for selector, expected in cases:
                self.assertEqual(self.ids(sv.select(selector, soup.template, flags=flags)), expected)

    def test_nested_templates(self):
        """Test that selecting from a `template` does not enter any `template` it contains."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <template id="a"><template id="b"><p id="1"></p></template><p id="2"></p></template>
        </body>
        </html>
        """

        for soup, flags in self.soups(markup):
            outer = soup.find(id='a')
            inner = soup.find(id='b')
            self.assertEqual(self.ids(sv.select('p', outer, flags=flags)), ['2'])
            self.assertEqual(self.ids(sv.select('p', inner, flags=flags)), ['1'])
            self.assertEqual(self.ids(sv.select('template', outer, flags=flags)), ['b'])
            self.assertFalse(sv.match('template p', soup.find(id='1'), flags=flags))
            self.assertIsNone(sv.closest('template', soup.find(id='1'), flags=flags))
            self.assertEqual(sv.closest('template', inner, flags=flags)['id'], 'b')

    def test_contains_ignores_contents(self):
        """Test that the text of the contents is not part of an element, or the `template` itself."""

        for soup, flags in self.soups():
            self.assertEqual(sv.select(':-soup-contains(text)', soup, flags=flags), [])
            self.assertEqual(sv.select(':-soup-contains-own(text)', soup, flags=flags), [])
            self.assertEqual(self.ids(sv.select('p:-soup-contains(text)', soup.template, flags=flags)), ['p'])
            self.assertFalse(sv.match(':-soup-contains(text)', soup.template, flags=flags))

    def test_language_does_not_enter(self):
        """Test that the contents do not inherit a language."""

        markup = """
        <!DOCTYPE html>
        <html lang="he">
        <head><meta http-equiv="content-language" content="he"></head>
        <body>
        <template id="t" lang="he"><p id="1"></p><div lang="he"><p id="2"></p></div></template>
        </body>
        </html>
        """

        for soup, flags in self.soups(markup):
            self.assertEqual(self.ids(sv.select('p:lang(he)', soup.template, flags=flags)), ['2'])

    def test_disabled_does_not_enter(self):
        """Test that the contents are not disabled by a `fieldset` outside the `template`."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <fieldset disabled>
        <template id="t"><input id="1"><fieldset disabled><input id="2"></fieldset></template>
        </fieldset>
        </body>
        </html>
        """

        for soup, flags in self.soups(markup):
            self.assertEqual(self.ids(sv.select('input:disabled', soup.template, flags=flags)), ['2'])

    def test_editing_host_does_not_enter(self):
        """Test that the contents are not editable because of an editing host outside the `template`."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <div contenteditable="true">
        <template id="t"><p id="1"></p><div contenteditable="true"><p id="2"></p></div></template>
        </div>
        </body>
        </html>
        """

        for soup, flags in self.soups(markup):
            self.assertEqual(self.ids(sv.select('p:read-write', soup.template, flags=flags)), ['2'])

    def test_default_stops_at_template(self):
        """Test that a form and a default button do not see each other through a `template`."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <form>
        <template id="t"><input id="1" type="submit"></template>
        <input id="2" type="submit">
        </form>
        <template id="u"><form><input id="3" type="submit"></form></template>
        </body>
        </html>
        """

        for soup, flags in self.soups(markup):
            self.assertEqual(self.ids(sv.select(':default', soup, flags=flags)), ['2'])
            self.assertEqual(sv.select(':default', soup.find(id='t'), flags=flags), [])
            self.assertEqual(self.ids(sv.select(':default', soup.find(id='u'), flags=flags)), ['3'])

    def test_indeterminate_stops_at_template(self):
        """Test that a radio button group is contained by the `template`."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <form>
        <template id="t"><input id="1" type="radio" name="a" checked></template>
        <input id="2" type="radio" name="a">
        </form>
        <input id="3" type="radio" name="b" checked>
        <template id="u">
        <div><input id="4" type="radio" name="b"></div>
        <div><input id="5" type="radio" name="c"></div>
        <div><input id="6" type="radio" name="c" checked></div>
        </template>
        </body>
        </html>
        """

        for soup, flags in self.soups(markup):
            self.assertEqual(self.ids(sv.select(':indeterminate', soup, flags=flags)), ['2'])
            self.assertEqual(self.ids(sv.select(':indeterminate', soup.find(id='u'), flags=flags)), ['4'])

    def test_detached_template(self):
        """Test that the contents of a `template` that is the root can be reached."""

        for soup, flags in self.soups():
            template = soup.template.extract()
            self.assertEqual(self.ids(sv.select('p', template, flags=flags)), ['p'])
            self.assertTrue(sv.match(':root', template, flags=flags))

    def test_extracted_contents(self):
        """Test that the contents are normal elements once removed from the `template`."""

        for soup, flags in self.soups():
            el = soup.find(id='in').extract()
            self.assertTrue(sv.match(':root', el, flags=flags))
            self.assertEqual(self.ids(sv.select('div p', el, flags=flags)), ['p'])

    def test_iframe_in_template(self):
        """Test that a document in an `iframe` is contained in the `template` as well."""

        soup = self.soup('<template id="t"><iframe></iframe></template>', 'html.parser')
        soup.iframe.append(self.soup('<html><body><p id="1"></p></body></html>', 'html.parser').html.extract())

        self.assertEqual(sv.select('p', soup), [])
        self.assertEqual(self.ids(sv.select('p', soup.template)), ['1'])
        self.assertTrue(sv.match(':root', soup.html))

    def test_template_in_iframe(self):
        """Test that the contents of a `template` in an `iframe` are not reached."""

        soup = self.soup('<iframe></iframe>', 'html.parser')
        markup = '<html><body><template id="t"><p id="1"></p></template></body></html>'
        soup.iframe.append(self.soup(markup, 'html.parser').html.extract())

        self.assertEqual(sv.select('p', soup), [])
        self.assertEqual(self.ids(sv.select('p', soup.template)), ['1'])
        self.assertFalse(sv.match('body p', soup.p))

    def test_name_is_not_case_sensitive_in_html(self):
        """Test that the name of the element is normalized in HTML."""

        soup = self.soup('<div></div>', 'html.parser')
        template = soup.new_tag('Template')
        template.append(soup.new_tag('p', attrs={'id': '1'}))
        soup.div.append(template)

        self.assertEqual(sv.select('p', soup), [])
        self.assertEqual(self.ids(sv.select('p', template)), ['1'])

    @util.requires_html5lib
    def test_non_html_template(self):
        """Test that elements named `template` in other namespaces have normal children."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <svg><template id="1"><g id="2"></g></template></svg>
        <math><template id="3"><mi id="4"></mi></template></math>
        </body>
        </html>
        """

        for flags in (0, sv.NOCACHE):
            soup = self.soup(markup, 'html5lib')
            self.assertEqual(self.ids(sv.select('template > *', soup, flags=flags)), ['2', '4'])
            self.assertEqual(self.ids(sv.select('svg g', soup, flags=flags)), ['2'])
            self.assertEqual(sv.select('template:empty', soup, flags=flags), [])
            self.assertTrue(sv.match('body g', soup.g, flags=flags))

    @util.requires_html5lib
    def test_template_in_foreign_object(self):
        """Test that a `template` that is parsed as HTML inside SVG is a real one."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <svg><foreignObject><template id="1"><p id="2"></p></template></foreignObject></svg>
        </body>
        </html>
        """

        for flags in (0, sv.NOCACHE):
            soup = self.soup(markup, 'html5lib')
            self.assertEqual(sv.select('p', soup, flags=flags), [])
            self.assertEqual(self.ids(sv.select('p', soup.template, flags=flags)), ['2'])
            self.assertFalse(sv.match('svg p', soup.p, flags=flags))

    @util.requires_lxml
    def test_xhtml(self):
        """Test that the `template` boundary applies to XHTML, where names are case sensitive."""

        markup = """<?xml version="1.0" encoding="UTF-8"?>
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:h="http://www.w3.org/1999/xhtml">
        <head><title></title></head>
        <body>
        <template id="1"><p id="2"></p></template>
        <h:template id="3"><p id="4"></p></h:template>
        <TEMPLATE id="5"><p id="6"></p></TEMPLATE>
        <svg xmlns="http://www.w3.org/2000/svg"><template id="7"><p id="8"></p></template></svg>
        </body>
        </html>
        """

        for flags in (0, sv.NOCACHE):
            soup = self.soup(markup, 'xml')
            self.assertEqual(self.ids(sv.select('p', soup, flags=flags)), ['6', '8'])
            self.assertEqual(self.ids(sv.select('p', soup.find(id='1'), flags=flags)), ['2'])
            self.assertEqual(self.ids(sv.select('p', soup.find(id='3'), flags=flags)), ['4'])

    @util.requires_lxml
    def test_not_html(self):
        """Test that an element named `template` in XML has normal children."""

        markup = """<?xml version="1.0" encoding="UTF-8"?>
        <root><template id="1"><p id="2"></p></template></root>
        """

        self.assert_selector(markup, 'template > p', ['2'], flags=util.XML)
        self.assert_selector(markup, 'root p', ['2'], flags=util.XML)

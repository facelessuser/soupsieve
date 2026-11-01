"""Test namespace selectors."""
from .. import util
import soupsieve as sv


class TestNamespace(util.TestCase):
    """Test namespace selectors."""

    MARKUP = """
    <?xml version="1.0" encoding="UTF-8"?>
    <tag id="root">
      <head id="0"></head>
      <foo:other id="1" xmlns:foo="http://me.com/namespaces/foofoo"
             xmlns:bar="http://me.com/namespaces/foobar">
      <foo:head id="2">
        <foo:title id="3"></foo:title>
        <bar:title id="4"></bar:title>
      </foo:head>
      <body id="5">
        <foo:e1 id="6"></foo:e1>
        <bar:e1 id="7"></bar:e1>
        <e1 id="8"></e1>
        <foo:e2 id="9"></foo:e2>
        <bar:e2 id="10"></bar:e2>
        <e2 id="11"></e2>
        <foo:e3 id="12"></foo:e3>
        <bar:e3 id="13"></bar:e3>
        <e3 id="14"></e3>
      </body>
      </foo:other>
      <other id="15" xmlns="http://me.com/namespaces/other">
        <e4 id="16">Inherit</er>
      </other>
    </tag>
    """

    MARKUP_ATTR = """
    <div>
      <h1>A contrived example</h1>
      <svg viewBox="0 0 20 32" class="icon icon-1">
        <use id="0" xlink:href="images/sprites.svg#icon-undo"></use>
      </svg>
      <svg viewBox="0 0 30 32" class="icon icon-2">
        <use id="1" xlink:href="images/sprites.svg#icon-redo"></use>
      </svg>
      <svg viewBox="0 0 40 32" class="icon icon-3">
        <use id="2" xlink:href="images/sprites.svg#icon-forward"></use>
      </svg>
      <svg viewBox="0 0 50 32" class="icon icon-4">
        <use id="3" xlink:href="other/sprites.svg#icon-reply"></use>
      </svg>
      <svg viewBox="0 0 50 32" class="icon icon-4">
        <use id="4" :href="other/sprites.svg#icon-reply"></use>
      </svg>
      <svg viewBox="0 0 50 32" class="icon icon-4">
        <use id="5" other:href="other/sprites.svg#icon-reply" xlink:other="value doesn't match"></use>
      </svg>
    </div>
    """

    def wrap_xlink(self, content, xhtml=False):
        """Wrap with `xlink`."""

        xhtml_ns = 'xmlns="http://www.w3.org/1999/xhtml"' if xhtml else ''

        return f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html {xhtml_ns} xmlns:xlink="http://www.w3.org/1999/xlink">
        <head>
        </head>
        <body>
        {content}
        </body>
        </html>
        """

    def test_namespace(self):
        """Test namespace."""

        self.assert_selector(
            self.MARKUP,
            "foo|title",
            ["3"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

    def test_namespace_case(self):
        """Test that namespaces are always case sensitive."""

        # These won't match
        self.assert_selector(
            self.MARKUP,
            "FOO|title",
            [],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

        self.assert_selector(
            self.MARKUP,
            "foo|title",
            [],
            namespaces={
                "FOO": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

    def test_namespace_with_universal_tag(self):
        """Test namespace with universal selector for the tag."""

        self.assert_selector(
            self.MARKUP,
            "bar|*",
            ["4", "7", "10", "13"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

    def test_no_namespace(self):
        """Test for tags with no namespace."""

        self.assert_selector(
            self.MARKUP,
            "|head",
            ["0"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

    def test_universal_namespace(self):
        """Test for a tag with a universal namespace selector."""

        self.assert_selector(
            self.MARKUP,
            "*|e2",
            ["9", "10", "11"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

    def test_namespace_no_default(self):
        """
        Test for a tag with without specifying a default namespace.

        Because we employ level 4 selectors
        E, when no default namespace is defined, will be read as *|E.
        """

        self.assert_selector(
            self.MARKUP,
            "e3",
            ["12", "13", "14"],
            namespaces={
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

    def test_namespace_with_default(self):
        """Test for a tag with a default namespace."""

        # Now that we apply a default namespace. Null space.
        self.assert_selector(
            self.MARKUP,
            "e3",
            ["14"],
            namespaces={
                "": "",
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

        self.assert_selector(
            self.MARKUP,
            "head",
            ["0"],
            namespaces={
                "": "",
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar"
            },
            flags=util.XML
        )

    def test_namespace_inherit(self):
        """Test for a tag namespace inheritance."""

        # Because no prefix is specified for "other" in the above document,
        # `e4` inherits the other namespace. The prefix in this case doesn't matter.
        # We specify `other` as prefix in our CSS just so we can use it to target the element.
        self.assert_selector(
            self.MARKUP,
            "e4",
            [],
            namespaces={
                "": "",
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar",
                "other": "http://me.com/namespaces/other"
            },
            flags=util.XML
        )

        self.assert_selector(
            self.MARKUP,
            "other|e4",
            ['16'],
            namespaces={
                "": "",
                "foo": "http://me.com/namespaces/foofoo",
                "bar": "http://me.com/namespaces/foobar",
                "other": "http://me.com/namespaces/other"
            },
            flags=util.XML
        )

    def test_undefined_namespace(self):
        """Test undefined namespace."""

        # Namespaces are defined wrong
        markup = """
        <tag id="1" xmlns:ns1=http://namespace1/ xmlns:ns2=http://namespace2/>
            <ns1:el id="2">...</ns1:el>
            <ns2:el id="3">...</ns2:el>
        </tag>
        """

        # We are not feeding in the namespaces so they shouldn't be found.
        self.assert_selector(
            markup,
            "ns1|el, ns2|el",
            [],
            flags=util.XML
        )

    def test_attribute_namespace(self):
        """Test attribute namespace."""

        self.assert_selector(
            self.MARKUP_ATTR,
            '[xlink|href*=forw],[xlink|href="images/sprites.svg#icon-redo"]',
            ['1', '2'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

    def test_attribute_namespace_escapes(self):
        """Test attribute namespace escapes."""

        self.assert_selector(
            self.MARKUP_ATTR,
            '[xlink\\:href*=forw]',
            ['2'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

        self.assert_selector(
            self.MARKUP_ATTR,
            '[\\:href]',
            ['4'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

    def test_invalid_namespace_attribute(self):
        """Test invalid namespace attributes."""

        self.assert_selector(
            self.MARKUP_ATTR,
            '[xlink\\:nomatch*=forw]',
            [],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

        self.assert_selector(
            self.MARKUP_ATTR,
            '[bad|href*=forw]',
            [],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.HTML5
        )

    def test_attribute_namespace_xhtml(self):
        """Test attribute namespace in XHTML."""

        self.assert_selector(
            self.wrap_xlink(self.MARKUP_ATTR, True),
            '[xlink|href*=forw],[xlink|href="images/sprites.svg#icon-redo"]',
            ['1', '2'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.XHTML
        )

    def test_attribute_namespace_xml(self):
        """Test attribute namespace in XML."""

        self.assert_selector(
            self.wrap_xlink(self.MARKUP_ATTR),
            '[xlink|href*=forw],[xlink|href="images/sprites.svg#icon-redo"]',
            ['1', '2'],
            namespaces={"xlink": "http://www.w3.org/1999/xlink"},
            flags=util.XHTML
        )

    @util.requires_html5lib
    def test_non_html_root(self):
        """Test that the namespaces a parser provides are used when the root is not an HTML element."""

        namespaces = {
            "svg": "http://www.w3.org/2000/svg",
            "html": "http://www.w3.org/1999/xhtml",
            "xlink": "http://www.w3.org/1999/xlink"
        }
        markup = """
        <svg id="1" xmlns:xlink="http://www.w3.org/1999/xlink">
        <a id="2" xlink:href="target"></a>
        <foreignObject id="3"><a id="4" href="target"></a></foreignObject>
        </svg>
        """
        svg = self.soup(markup, 'html5lib').svg.extract()

        for selector, expected in (('svg|a', ['2']), ('html|a', ['4']), ('[xlink|href]', ['2'])):
            self.assertEqual([el['id'] for el in sv.select(selector, svg, namespaces=namespaces)], expected)

    def test_non_html_root_no_namespaces(self):
        """Test that everything is treated as HTML when a parser does not provide namespaces."""

        namespaces = {"svg": "http://www.w3.org/2000/svg", "html": "http://www.w3.org/1999/xhtml"}
        markup = """<svg id="1"><a id="2"></a><foreignObject id="3"><a id="4"></a></foreignObject></svg>"""

        for parser in util.available_parsers('html.parser', 'lxml'):
            svg = self.soup(markup, parser).svg.extract()
            self.assertEqual(sv.select('svg|a', svg, namespaces=namespaces), [])
            self.assertEqual([el['id'] for el in sv.select('html|a', svg, namespaces=namespaces)], ['2', '4'])

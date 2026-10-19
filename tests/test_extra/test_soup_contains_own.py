"""Test contains selectors."""
from .. import util


class TestSoupContainsOwn(util.TestCase):
    """Test soup-contains-own selectors."""

    MARKUP = """
    <body>
    <div id="1">
    Testing
    <span id="2"> that </span>
    contains works.
    </div>
    </body>
    """

    def test_contains_own_descendants(self):
        """Test contains-own won't match text if contained in descendants."""

        self.assert_selector(
            self.MARKUP,
            'body div:-soup-contains-own(that)',
            [],
            flags=util.HTML
        )

    def test_contains_own(self):
        """Test contains-own."""

        self.assert_selector(
            self.MARKUP,
            'body *:-soup-contains-own(that)',
            ['2'],
            flags=util.HTML
        )

    def test_contains_own_mixed(self):
        """Keep descendant and own text separate in compound selectors."""

        markup = '<div id="1">own text<span>child text</span></div>'
        selectors = (
            'div:-soup-contains("child text"):-soup-contains-own("own text")',
            'div:-soup-contains-own("own text"):-soup-contains("child text")',
            'div:-soup-contains("child"):-soup-contains-own("own")'
            ':-soup-contains("text"):-soup-contains-own("text")',
            'div:-soup-contains-own("own"):-soup-contains("child")'
            ':-soup-contains-own("text"):-soup-contains("text")',
            'div:-soup-contains("absent", "child"):-soup-contains-own("absent", "own")'
        )
        for selector in selectors:
            with self.subTest(selector=selector):
                self.assert_selector(markup, selector, ['1'], flags=util.HTML | util.NOCACHE)

    def test_contains_own_mixed_text_boundaries(self):
        """Do not match descendant text or join separate own text nodes."""

        markup = '<div id="1">alpha<span>beta</span>gamma</div>'
        selectors = (
            'div:-soup-contains("beta"):-soup-contains-own("b")',
            'div:-soup-contains("beta"):-soup-contains-own("alphagamma")',
            'div:-soup-contains-own("alpha"):-soup-contains("missing")'
        )
        for selector in selectors:
            with self.subTest(selector=selector):
                self.assert_selector(markup, selector, [], flags=util.HTML | util.NOCACHE)

    def test_contains_own_mixed_empty(self):
        """An empty own-text pattern still requires a direct text node."""

        markup = '<div id="1"><span>child</span></div><div id="2">own</div><div id="3"></div>'
        for selector in (
            'div:-soup-contains(""):-soup-contains-own("")',
            'div:-soup-contains-own(""):-soup-contains("")'
        ):
            with self.subTest(selector=selector):
                self.assert_selector(markup, selector, ['2'], flags=util.HTML | util.NOCACHE)

    def test_contains_own_mixed_nested(self):
        """Apply mixed text conditions inside relational and negated selectors."""

        markup = '<section id="1"><div>own text<span>child text</span></div></section>'
        for selector, expected in (
            ('section:has(> div:-soup-contains("child"):-soup-contains-own("own"))', ['1']),
            ('section:not(:has(> div:-soup-contains-own("own"):-soup-contains("child")))', [])
        ):
            with self.subTest(selector=selector):
                self.assert_selector(markup, selector, expected, flags=util.HTML | util.NOCACHE)

    def test_contains_own_cdata_html5(self):
        """Test contains CDATA in HTML5."""

        markup = """
        <body><div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div></body>
        """

        self.assert_selector(
            markup,
            'body *:-soup-contains-own("that")',
            ['1'],
            flags=util.HTML5
        )

    def test_contains_own_cdata_py_html(self):
        """Test contains CDATA in Python HTML parser."""

        markup = """
        <body><div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div></body>
        """

        self.assert_selector(
            markup,
            'body *:-soup-contains-own("that")',
            ['1'],
            flags=util.PYHTML
        )

    @util.skip_no_lxml
    def test_contains_own_cdata_lxml_html(self):
        """Test contains CDATA in `lxml` HTML."""

        from lxml import etree
        libxml_ver = etree.LIBXML_VERSION

        markup = """
        <body><div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div></body>
        """

        results = ['1', '2'] if libxml_ver >= (2, 9, 11) else ['1']
        self.assert_selector(
            markup,
            'body *:-soup-contains-own("that")',
            results,
            flags=util.LXML_HTML
        )

    def test_contains_own_cdata_xml(self):
        """Test contains-own CDATA in XML."""

        markup = """
        <div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div>
        """

        self.assert_selector(
            markup,
            '*:-soup-contains-own("that")',
            ['1', '2'],
            flags=util.XML
        )

    def test_contains_own_with_broken_text(self):
        """Test contains-own to see how it matches a broken text."""

        markup = """
        <body>
        <div id="1"> A simple test <div id="2"> to </div> show the broken text case. </div>
        </body>
        """
        self.assert_selector(
            markup,
            'body div:-soup-contains-own("test  show")',
            [],
            flags=util.HTML
        )

"""Test contains selectors."""
from .. import util
import warnings
import soupsieve as sv


class TestSoupContains(util.TestCase):
    """Test soup-contains selectors."""

    MARKUP = """
    <body>
    <div id="1">
    Testing
    <span id="2"> that </span>
    contains works.
    </div>
    </body>
    """

    def test_contains(self):
        """Test contains."""

        self.assert_selector(
            self.MARKUP,
            'body span:-soup-contains(that)',
            ['2'],
            flags=util.HTML
        )

    def test_contains_quoted_with_space(self):
        """Test contains quoted with spaces."""

        self.assert_selector(
            self.MARKUP,
            'body span:-soup-contains(" that ")',
            ['2'],
            flags=util.HTML
        )

    def test_contains_quoted_without_space(self):
        """Test contains quoted with spaces."""

        self.assert_selector(
            self.MARKUP,
            'body :-soup-contains( "Testing" )',
            ['1'],
            flags=util.HTML
        )

    def test_contains_quoted_with_escaped_newline(self):
        """Test contains quoted with escaped newline."""

        self.assert_selector(
            self.MARKUP,
            'body :-soup-contains("Test\\\ning")',
            ['1'],
            flags=util.HTML
        )

    def test_contains_quoted_with_escaped_newline_with_carriage_return(self):
        """Test contains quoted with escaped newline with carriage return."""

        self.assert_selector(
            self.MARKUP,
            'body :-soup-contains("Test\\\r\ning")',
            ['1'],
            flags=util.HTML
        )

    def test_contains_list(self):
        """Test contains list."""

        self.assert_selector(
            self.MARKUP,
            'body span:-soup-contains("does not exist", "that")',
            ['2'],
            flags=util.HTML
        )

    def test_contains_multiple(self):
        """Test contains multiple."""

        self.assert_selector(
            self.MARKUP,
            'body span:-soup-contains("th"):-soup-contains("at")',
            ['2'],
            flags=util.HTML
        )

    def test_contains_multiple_not_match(self):
        """Test contains multiple with "not" and with a match."""

        self.assert_selector(
            self.MARKUP,
            'body span:not(:-soup-contains("does not exist")):-soup-contains("that")',
            ['2'],
            flags=util.HTML
        )

    def test_contains_multiple_not_no_match(self):
        """Test contains multiple with "not" and no match."""

        self.assert_selector(
            self.MARKUP,
            'body span:not(:-soup-contains("that")):-soup-contains("that")',
            [],
            flags=util.HTML
        )

    def test_contains_with_descendants(self):
        """Test that contains returns descendants as well as the top level that contain."""

        self.assert_selector(
            self.MARKUP,
            'body :-soup-contains(" that ")',
            ['1', '2'],
            flags=util.HTML
        )

    def test_contains_bad(self):
        """Test contains when it finds no text."""

        self.assert_selector(
            self.MARKUP,
            'body :-soup-contains(bad)',
            [],
            flags=util.HTML
        )

    def test_contains_escapes(self):
        """Test contains with escape characters."""

        markup = """
        <body>
        <div id="1">Testing<span id="2">
        that</span>contains works.</div>
        </body>
        """

        self.assert_selector(
            markup,
            r'body span:-soup-contains("\0a that")',
            ['2'],
            flags=util.HTML
        )

    def test_contains_cdata_html5(self):
        """Test contains CDATA in HTML5."""

        markup = """
        <body><div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div></body>
        """

        self.assert_selector(
            markup,
            'body *:-soup-contains("that")',
            ['1'],
            flags=util.HTML5
        )

    def test_contains_cdata_py_html(self):
        """Test contains CDATA in Python HTML parser."""

        markup = """
        <body><div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div></body>
        """

        self.assert_selector(
            markup,
            'body *:-soup-contains("that")',
            ['1'],
            flags=util.PYHTML
        )

    @util.requires_lxml
    def test_contains_cdata_lxml_html(self):
        """Test contains CDATA in `lxml` HTML parser."""

        markup = """
        <body><div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div></body>
        """

        # CDATA is not text in HTML: `libxml2` drops it, or as of 2.14, turns it into a comment.
        self.assert_selector(
            markup,
            'body *:-soup-contains("that")',
            ['1'],
            flags=util.LXML_HTML
        )

    def test_contains_cdata_xhtml(self):
        """Test contains CDATA in XHTML."""

        markup = """
        <div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div>
        """

        self.assert_selector(
            self.wrap_xhtml(markup),
            'body *:-soup-contains("that")',
            ['1', '2'],
            flags=util.XHTML
        )

    def test_contains_cdata_xml(self):
        """Test contains CDATA in XML."""

        markup = """
        <div id="1">Testing that <span id="2"><![CDATA[that]]></span>contains works.</div>
        """

        self.assert_selector(
            markup,
            '*:-soup-contains("that")',
            ['1', '2'],
            flags=util.XML
        )

    def test_contains_iframe(self):
        """Test that the contents of an `iframe` are text or elements like any other."""

        markup = """
        <div id="1">
        <p>Testing text</p>
        <iframe>
        <html><body>
        <span id="2">iframe</span>
        </body></html>
        </iframe>
        </div>
        """

        self.assert_selector(
            markup,
            'div:-soup-contains("iframe")',
            ['1'],
            flags=util.PYHTML
        )

        self.assert_selector(
            markup,
            'div:-soup-contains("text")',
            ['1'],
            flags=util.PYHTML
        )

        self.assert_selector(
            markup,
            'span:-soup-contains("iframe")',
            [] if util.PYHTML_ESCAPES_IFRAME else ['2'],
            flags=util.PYHTML
        )

    def test_contains_iframe_xml(self):
        """Test contains with `iframe` which shouldn't matter in XML."""

        markup = """
        <div id="1">
        <p>Testing text</p>
        <iframe>
        <html><body>
        <span id="2">iframe</span>
        </body></html>
        </iframe>
        </div>
        """

        self.assert_selector(
            markup,
            'div:-soup-contains("iframe")',
            ['1'],
            flags=util.XML
        )

        self.assert_selector(
            markup,
            'div:-soup-contains("text")',
            ['1'],
            flags=util.XML
        )

        self.assert_selector(
            markup,
            'span:-soup-contains("iframe")',
            ['2'],
            flags=util.XML
        )

    def test_contains_warn(self):
        """Test old alias raises a warning."""

        sv.purge()

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            self.assert_selector(
                self.MARKUP,
                'body span:contains(that)',
                ['2'],
                flags=util.HTML
            )
            found = False
            target = "The pseudo class ':contains' is deprecated, ':-soup-contains' should be used moving forward."
            for warn in w:
                if target in str(warn.message):
                    found = True
                    break
            # Verify some things
            self.assertTrue(found)

    def test_contains_across_boundaries(self):
        """Test that text is found across the boundaries between text and elements, but not in what is skipped."""

        markup = """
        <div id="1"><span>ab</span>c</div>
        <div id="2">a<b>b</b><i></i><b>c</b></div>
        <div id="3">ab<!--x-->c</div>
        <div id="4">ab<template>c</template></div>
        <div id="5"><p id="6">xa</p><p id="7">b</p><p id="8">cx</p></div>
        <div id="9">a b c</div>
        <div id="10"><span id="11">abca</span></div>
        <div id="12"><div id="13">a<div id="14">b<div id="15">c</div></div></div></div>
        """

        self.assert_selector(
            markup, 'div:-soup-contains("abc")', ['1', '2', '3', '5', '10', '12', '13'], flags=util.HTML | util.NOCACHE
        )
        self.assert_selector(markup, '[id]:-soup-contains("xab", "zz")', ['5'], flags=util.HTML | util.NOCACHE)
        self.assert_selector(markup, '[id]:-soup-contains("ca")', ['10', '11'], flags=util.HTML | util.NOCACHE)
        self.assert_selector(markup, 'p:-soup-contains("")', ['6', '7', '8'], flags=util.HTML | util.NOCACHE)

    def test_contains_deeply_nested(self):
        """Test that each text is checked once for the elements of a deeply nested document."""

        from bs4 import BeautifulSoup
        from unittest import mock

        n = 32
        # `html.parser` nests each `li` in the previous one, so the text of each `li` holds that of the next.
        soup = BeautifulSoup('<ul>' + '<li>x' * n, 'html.parser')
        is_content_string = sv.css_match.CSSMatch.is_content_string
        for selector, matches in (
            ('li:-soup-contains("zzz")', 0),
            ('li:-soup-contains(x)', n),
            ('li:not(:-soup-contains("xxx"))', 2)
        ):
            with mock.patch.object(
                sv.css_match.CSSMatch, 'is_content_string', side_effect=is_content_string
            ) as patched:
                self.assertEqual(len(sv.select(selector, soup)), matches)
            self.assertLessEqual(patched.call_count, n)
            self.assertEqual(len(sv.select(selector, soup, flags=sv.NOCACHE)), matches)

    def test_contains_cache_drops_ends(self):
        """Test that only the topmost element summarized keeps the ends of its text in the cache."""

        from bs4 import BeautifulSoup

        n = 32
        soup = BeautifulSoup('<ul>' + '<li>xy' * n, 'html.parser')
        pattern = sv.compile('li:-soup-contains("zzz")')
        matcher = sv.css_match.CSSMatch(pattern.selectors, soup, pattern.namespaces, pattern.flags)
        self.assertEqual(list(matcher.select()), [])
        # Every `li` is summarized, but once its parent is, it only keeps whether its text contains the string.
        self.assertEqual(len(matcher.contains_cache), n)
        kept = [key for key, (_, head, tail, _) in matcher.contains_cache.items() if head or tail]
        self.assertEqual(kept, [(id(soup.li), id(pattern.selectors[0].contains[0]))])

    def test_contains_many_values(self):
        """Test that each element is summarized once for a list of values, however many values it has."""

        from bs4 import BeautifulSoup

        n = 32
        soup = BeautifulSoup('<ul>' + '<li>xy' * n, 'html.parser')
        values = ', '.join(f'"v{i}"' for i in range(1000))
        for selector, matches in (
            (f'li:-soup-contains({values})', 0),
            (f'li:-soup-contains({values}, "yx")', n - 1),
            (f'li:-soup-contains({values}, "y")', n),
            (f'li:-soup-contains({values}, "")', n)
        ):
            pattern = sv.compile(selector)
            matcher = sv.css_match.CSSMatch(pattern.selectors, soup, pattern.namespaces, pattern.flags)
            self.assertEqual(len(list(matcher.select())), matches)
            self.assertLessEqual(len(matcher.contains_cache), n)
            self.assertEqual(len(sv.select(selector, soup, flags=sv.NOCACHE)), matches)

    def test_contains_values_across_boundaries(self):
        """Test values of different lengths, some repeated, across the boundaries between text and elements."""

        markup = """
        <div id="1">a<span>bc</span>d</div>
        <div id="2">ab<i></i>cd<b>e</b></div>
        <div id="3"><p id="4">xyz</p><p id="5">z</p></div>
        <div id="6">a b c d</div>
        """

        self.assert_selector(markup, 'div:-soup-contains("bcd", "zz")', ['1', '2', '3'], flags=util.HTML | util.NOCACHE)
        self.assert_selector(
            markup, '[id]:-soup-contains("abcde", "b", "b", "zzz")', ['1', '2', '6'], flags=util.HTML | util.NOCACHE
        )
        self.assert_selector(
            markup, '[id]:-soup-contains("q", "yzz"):-soup-contains("x")', ['3'], flags=util.HTML | util.NOCACHE
        )

"""Test language selectors."""
from __future__ import unicode_literals
from .. import util


class TestLang(util.TestCase):
    """Test language selectors."""

    MARKUP = """
    <div lang="de-DE">
        <p id="1"></p>
    </div>
    <div lang="de-DE-1996">
        <p id="2"></p>
    </div>
    <div lang="de-Latn-DE">
        <p id="3"></p>
    </div>
    <div lang="de-Latf-DE">
        <p id="4"></p>
    </div>
    <div lang="de-Latn-DE-1996">
        <p id="5"></p>
    </div>
    <p id="6" lang="de-DE"></p>
    """

    def test_lang(self):
        """Test language and that it uses implicit wildcard."""

        # Implicit wild
        self.assert_selector(
            self.MARKUP,
            "p:lang(de-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_explicit_wildcard(self):
        """Test language with explicit wildcard (same as implicit)."""

        # Explicit wild
        self.assert_selector(
            self.MARKUP,
            "p:lang(de-\\*-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_wildcard_at_start_escaped(self):
        """
        Test language with wildcard at start (escaped).

        Wildcard in the middle is same as implicit, but at the start, it has specific meaning.
        """

        self.assert_selector(
            self.MARKUP,
            "p:lang(\\*-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_language_quoted(self):
        """Test language (quoted)."""

        # Normal quoted
        self.assert_selector(
            self.MARKUP,
            "p:lang('de-DE')",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_language_quoted_with_escaped_newline(self):
        """Test language (quoted) with escaped new line."""

        # Normal quoted
        self.assert_selector(
            self.MARKUP,
            "p:lang('de-\\\nDE')",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_wildcard_at_start_quoted(self):
        """Test language with wildcard at start (quoted)."""

        # First wild quoted
        self.assert_selector(
            self.MARKUP,
            "p:lang('*-DE')",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_avoid_implicit_language(self):
        """Test that we can narrow language selection to elements that match and explicitly state language."""

        # Target element with language and language attribute
        self.assert_selector(
            self.MARKUP,
            "p[lang]:lang(de-DE)",
            ['6'],
            flags=util.HTML
        )

    def test_language_list(self):
        """Test language list."""

        # Multiple languages
        markup = """
        <div lang="de-DE">
            <p id="1"></p>
        </div>
        <div lang="en">
            <p id="2"></p>
        </div>
        <div lang="de-Latn-DE">
            <p id="3"></p>
        </div>
        <div lang="de-Latf-DE">
            <p id="4"></p>
        </div>
        <div lang="en-US">
            <p id="5"></p>
        </div>
        <p id="6" lang="de-DE"></p>
        """

        self.assert_selector(
            markup,
            "p:lang(de-DE, '*-US')",
            ['1', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_undetermined_language(self):
        """Test undetermined language."""

        markup = """
        <div>
            <p id="1"></p>
        </div>
        """

        self.assert_selector(
            markup,
            "p:lang(en)",
            [],
            flags=util.HTML
        )

    def test_language_in_header(self):
        """Test that we can find language in header."""

        markup = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="content-language" content="en-US">
        </head>
        <body>
        <div>
            <p id="1"></p>
        </div>
        <div>
            <p id="2"></p>
        </div>
        </body>
        """

        self.assert_selector(
            markup,
            "p:lang('*-US')",
            ['1', '2'],
            flags=util.HTML
        )

    def test_xml_style_language_in_html5(self):
        """Test XML style language when out of HTML5 namespace."""

        markup = """
        <math xml:lang="en">
            <mtext id="1"></mtext>
        </math>
        <div xml:lang="en">
            <mtext id="2"></mtext>
        </div>
        """

        self.assert_selector(
            markup,
            "mtext:lang(en)",
            ['1'],
            flags=util.HTML5
        )

    def test_xml_style_language(self):
        """Test XML style language."""

        # XML style language
        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <html>
        <head>
        </head>
        <body>
        <div xml:lang="de-DE">
            <p id="1"></p>
        </div>
        <div xml:lang="de-DE-1996">
            <p id="2"></p>
        </div>
        <div xml:lang="de-Latn-DE">
            <p id="3"></p>
        </div>
        <div xml:lang="de-Latf-DE">
            <p id="4"></p>
        </div>
        <div xml:lang="de-Latn-DE-1996">
            <p id="5"></p>
        </div>
        <p id="6" xml:lang="de-DE"></p>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "p:lang(de-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.XML
        )

    def test_language_in_xhtml(self):
        """Test language in XHTML."""

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        </head>
        <body>
        <div lang="de-DE" xml:lang="de-DE">
            <p id="1"></p>
        </div>
        <div lang="de-DE-1996" xml:lang="de-DE-1996">
            <p id="2"></p>
        </div>
        <div lang="de-Latn-DE" xml:lang="de-Latn-DE">
            <p id="3"></p>
        </div>
        <div lang="de-Latf-DE" xml:lang="de-Latf-DE">
            <p id="4"></p>
        </div>
        <div lang="de-Latn-DE-1996" xml:lang="de-Latn-DE-1996">
            <p id="5"></p>
        </div>
        <p id="6" lang="de-DE" xml:lang="de-DE"></p>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "p:lang(de-DE)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.XML
        )

    def test_language_in_xhtml_without_html_style_lang(self):
        """
        Test language in XHTML.

        HTML namespace elements must use HTML style language.
        """

        # XHTML language: `lang`
        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
            "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        </head>
        <body>
        <div xml:lang="de-DE">
            <p id="1"></p>
        </div>
        <div xml:lang="de-DE-1996">
            <p id="2"></p>
        </div>
        <div xml:lang="de-Latn-DE">
            <p id="3"></p>
        </div>
        <div xml:lang="de-Latf-DE">
            <p id="4"></p>
        </div>
        <div xml:lang="de-Latn-DE-1996">
            <p id="5"></p>
        </div>
        <p id="6" xml:lang="de-DE"></p>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            "p:lang(de-DE)",
            [],
            flags=util.XHTML
        )


class TestLangQuirks(TestLang):
    """Test language selectors with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

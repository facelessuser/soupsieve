"""Test language selector."""
from __future__ import unicode_literals
from .. import util


class TestLang(util.TestCase):
    """Test language selector."""

    def test_lang(self):
        """Test language."""

        markup = """
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

        self.assert_selector(
            markup,
            "p:lang(de)",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )


class TestLangQuirks(TestLang):
    """Test language selector with quirks."""

    def setUp(self):
        """Setup."""

        self.purge()
        self.quirks = True

"""Test Soup Sieve API."""
import unittest
import bs4
import soupsieve as sv


class TestSoupSieve(unittest.TestCase):
    """Test soup sieve."""

    def test_comments(self):
        """Test selectors."""
        markup = """
        <!-- before header -->
        <html>
        <head>
        </head>
        <body>
        <!-- comment -->
        <p id="1"><code id="2"></code><img id="3" src="./image.png"/></p>
        <pre id="4"></pre>
        <p><span id="5" class="some-class"></span><span id="some-id"></span></p>
        <pre id="6" class='ignore'>
            <!-- don't ignore -->
        </pre>
        </body>
        </html>
        """

        soup = bs4.BeautifulSoup(markup, 'html5lib')
        comments = [str(c).strip() for c in sv.comments(soup, mode=sv.HTML5)]
        self.assertEqual(sorted(comments), sorted(['before header', 'comment', "don't ignore"]))

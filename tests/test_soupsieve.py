"""Test Soup Sieve API."""
import unittest
import bs4
import soupsieve as sv
import copy
import random
import pytest


class TestSoupSieve(unittest.TestCase):
    """Test soup sieve."""

    def test_comments(self):
        """Test comments."""
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

        comments = [str(c).strip() for c in sv.commentsiter(soup, limit=2, mode=sv.HTML5)]
        self.assertEqual(sorted(comments), sorted(['before header', 'comment']))

    def test_select(self):
        """Test select."""

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
        ids = []
        for el in sv.select('span[id]', soup):
            ids.append(el.attrs['id'])

        self.assertEqual(sorted(['5', 'some-id']), sorted(ids))

        ids = []
        for el in sv.selectiter('span[id]', soup):
            ids.append(el.attrs['id'])

        self.assertEqual(sorted(['5', 'some-id']), sorted(ids))

    def test_match(self):
        """Test matching."""

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
        nodes = sv.select('span[id]', soup)
        self.assertTrue(sv.match('span#5', nodes[0]))
        self.assertFalse(sv.match('span#5', nodes[1]))

    def test_filter(self):
        """Test filter."""

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
        nodes = sv.filter('pre#6', soup.html.body)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].attrs['id'], '6')

    def test_cache(self):
        """Test copy."""

        p1 = sv.compile('p[id]', mode=sv.HTML5)
        p2 = sv.compile('p[id]', mode=sv.HTML5)
        p3 = sv.compile('p[id]', mode=sv.HTML)
        p4 = copy.copy(p1)
        p5 = copy.copy(p3)

        self.assertTrue(p1 is p2)
        self.assertTrue(p1 is not p3)
        self.assertTrue(p4 is not p1)
        self.assertTrue(p4 == p1)
        self.assertTrue(p5 is not p3)
        self.assertTrue(p5 == p3)
        self.assertTrue(p5 is not p4)

        sv.purge()
        self.assertEqual(sv.cp._cached_css_compile.cache_info().currsize, 0)
        for x in range(1000):
            value = '[value={}]'.format(str(random.randint(1, 10000)))
            p = sv.compile(value)
            self.assertTrue(p.pattern == value)
            self.assertTrue(sv.cp._cached_css_compile.cache_info().currsize > 0)
        self.assertTrue(sv.cp._cached_css_compile.cache_info().currsize == 500)
        sv.purge()
        self.assertEqual(sv.cp._cached_css_compile.cache_info().currsize, 0)

    def test_recompile(self):
        """If you feed through the same object, it should pass through unless you change flags."""

        p1 = sv.compile('p[id]')
        p2 = sv.compile(p1)
        self.assertTrue(p1 is p2)

        with pytest.raises(ValueError):
            sv.compile(p1, mode=sv.HTML)

        with pytest.raises(ValueError):
            sv.compile(p1, namespaces={"": ""})

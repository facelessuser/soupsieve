"""Test Soup Sieve API."""
from __future__ import unicode_literals
import unittest
import bs4
import soupsieve as sv
from soupsieve import util as sv_util
from . import util
import copy
import random
import pytest
import pickle


class TestSoupSieve(unittest.TestCase):
    """Test Soup Sieve."""

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
        comments = [sv_util.ustr(c).strip() for c in sv.comments(soup)]
        self.assertEqual(sorted(comments), sorted(['before header', 'comment', "don't ignore"]))

        comments = [sv_util.ustr(c).strip() for c in sv.icomments(soup, limit=2)]
        self.assertEqual(sorted(comments), sorted(['before header', 'comment']))

        # Check that comments on compiled object work just like `sv.comments`
        pattern = sv.compile('', None, 0)
        comments = [sv_util.ustr(c).strip() for c in pattern.comments(soup)]
        self.assertEqual(sorted(comments), sorted(['before header', 'comment', "don't ignore"]))

        comments = [sv_util.ustr(c).strip() for c in pattern.icomments(soup, limit=2)]
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
        for el in sv.select('span[id]', soup, limit=1):
            ids.append(el.attrs['id'])

        self.assertEqual(sorted(['5']), sorted(ids))

        self.assertEqual(
            sv.select('span[id]', soup, limit=1)[0].attrs['id'],
            sv.select_one('span[id]', soup).attrs['id']
        )

        self.assertEqual(None, sv.select_one('h1', soup))

        ids = []
        for el in sv.iselect('span[id]', soup):
            ids.append(el.attrs['id'])

        self.assertEqual(sorted(['5', 'some-id']), sorted(ids))

        span = sv.select('span[id]', soup)[0]
        ids = []
        for el in sv.select('span[id]:not(#some-id)', span.parent):
            ids.append(el.attrs['id'])

        self.assertEqual(sorted(['5']), sorted(ids))

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
        self.assertTrue(sv.match('span#\\35', nodes[0]))
        self.assertFalse(sv.match('span#\\35', nodes[1]))

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
        nodes = sv.filter('pre#\\36', soup.html.body)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].attrs['id'], '6')

        nodes = sv.filter('pre#\\36', [el for el in soup.html.body.children if isinstance(el, bs4.Tag)])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].attrs['id'], '6')

    def test_closest(self):
        """Test closest."""

        markup = """
        <article id="article">
          <div id="div-01">Here is div-01
            <div id="div-02">Here is div-02
              <div id="div-04">Here is div-04</div>
              <div id="div-03">Here is div-03</div>
            </div>
            <div id="div-05">Here is div-05</div>
          </div>
        </article>
        """

        soup = bs4.BeautifulSoup(markup, 'html5lib')
        el = sv.select_one('#div-03', soup)

        self.assertTrue(sv.closest('#div-02', el).attrs['id'] == 'div-02')
        self.assertTrue(sv.closest('div div', el).attrs['id'] == 'div-03')
        self.assertTrue(sv.closest('article > div', el).attrs['id'] == 'div-01')
        self.assertTrue(sv.closest(':not(div)', el).attrs['id'] == 'article')
        self.assertTrue(sv.closest('div #div-05', el) is None)
        self.assertTrue(sv.closest('a', el) is None)

    def test_copy_pickle(self):
        """Test copy and pickle."""

        # Test that we can pickle and unpickle
        # We force a pattern that contains all custom types:
        # `Selector`, `NullSelector`, `SelectorTag`, `SelectorAttribute`,
        # `SelectorNth`, `SelectorLang`, `SelectorList`, and `Namespaces`
        p1 = sv.compile(
            'p.class#id[id]:nth-child(2):lang(en):focus', {'html': 'http://www.w3.org/TR/html4/'}
        )
        sp1 = pickle.dumps(p1)
        pp1 = pickle.loads(sp1)
        self.assertTrue(pp1 == p1)

        # Test that we pull the same one from cache
        p2 = sv.compile(
            'p.class#id[id]:nth-child(2):lang(en):focus', {'html': 'http://www.w3.org/TR/html4/'}
        )
        self.assertTrue(p1 is p2)

        # Test that we compile a new one when providing a different flags
        p3 = sv.compile(
            'p.class#id[id]:nth-child(2):lang(en):focus', {'html': 'http://www.w3.org/TR/html4/'}, flags=0x10
        )
        self.assertTrue(p1 is not p3)
        self.assertTrue(p1 != p3)

        # Test that the copy is equivalent, but not same.
        p4 = copy.copy(p1)
        self.assertTrue(p4 is not p1)
        self.assertTrue(p4 == p1)

        p5 = copy.copy(p3)
        self.assertTrue(p5 is not p3)
        self.assertTrue(p5 == p3)
        self.assertTrue(p5 is not p4)

    def test_cache(self):
        """Test cache."""

        sv.purge()
        self.assertEqual(sv.cp._cached_css_compile.cache_info().currsize, 0)
        for x in range(1000):
            value = '[value="{}"]'.format(sv_util.ustr(random.randint(1, 10000)))
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
            sv.compile(p1, flags=0x10)

        with pytest.raises(ValueError):
            sv.compile(p1, namespaces={"": ""})

    def test_immutable_object(self):
        """Test immutable object."""

        obj = sv.ct.Immutable()

        with self.assertRaises(AttributeError):
            obj.member = 3

    def test_immutable_dict(self):
        """Test immutable dictionary."""

        idict = sv.ct.ImmutableDict({'a': 'b', 'c': 'd'})
        self.assertEqual(2, len(idict))

        with self.assertRaises(TypeError):
            idict['a'] = 'f'

        with self.assertRaises(TypeError):
            sv.ct.ImmutableDict([[3, {}]])

        with self.assertRaises(TypeError):
            sv.ct.ImmutableDict([[{}, 3]])

        with self.assertRaises(TypeError):
            sv.ct.Namespaces({'a': {}})


class TestInvalid(util.TestCase):
    """Test invalid."""

    def test_invalid_combination(self):
        """
        Test invalid combination.

        Selectors cannot start with relational symbols unless in `:has()`.
        `:has()` cannot start with `,`.
        """

        self.assert_raises(', p', SyntaxError)

        self.assert_raises(':has(, p)', SyntaxError)

        self.assert_raises('div >> p', SyntaxError)

        self.assert_raises('div >', SyntaxError)

        self.assert_raises('div,, a', SyntaxError)

        self.assert_raises(':is(> div)', SyntaxError)

        self.assert_raises(':is(div, > div)', SyntaxError)

    @util.skip_quirks
    def test_invalid_non_quirk_combination(self):
        """
        Test invalid combination.

        Selectors cannot start with relational symbols unless in `:has()`.
        `:has()` cannot start with `,`.
        """

        self.assert_raises('> p', SyntaxError)

        self.assert_raises('div, > a', SyntaxError)

    def test_invalid_pseudo(self):
        """Test invalid pseudo class."""

        self.assert_raises(':before', NotImplementedError)

        self.assert_raises(':nth-child(a)', SyntaxError)

    def test_invalid_pseudo_close(self):
        """Test invalid pseudo close."""

        self.assert_raises('div)', SyntaxError)

        self.assert_raises(':is(div,)', SyntaxError)

    def test_invalid_pseudo_open(self):
        """Test invalid pseudo close."""

        self.assert_raises(':is(div', SyntaxError)

    def test_invalid_incomplete_has(self):
        """Test invalid `:has()`."""

        self.assert_raises(':has(>)', SyntaxError)

        self.assert_raises(':has()', SyntaxError)

        self.assert_raises(':has(> has,, a)', SyntaxError)

        self.assert_raises(':has(> has,, a)', SyntaxError)

        self.assert_raises(':has(> has >)', SyntaxError)

        self.assert_raises(':has(> has,)', SyntaxError)

    def test_invalid_tag(self):
        """
        Test invalid tag.

        Tag must come first.
        """

        self.assert_raises(':is(div)p', SyntaxError)

    def test_invalid_syntax(self):
        """Test invalid syntax."""

        self.assert_raises('div?', SyntaxError)

    def test_malformed_selectors(self):
        """Test malformed selectors."""

        # Malformed class
        self.assert_raises('td.+#some-id', SyntaxError)

        # Malformed id
        self.assert_raises('td#.some-class', SyntaxError)

        # Malformed pseudo-class
        self.assert_raises('td:[href]', SyntaxError)

    @util.skip_quirks
    def test_malformed_no_quirk(self):
        """Test malformed with no quirk mode."""

        # Malformed attribute
        self.assert_raises('div[attr={}]', SyntaxError)

    def test_invalid_namespace(self):
        """Test invalid namespace."""

        with self.assertRaises(TypeError):
            sv.ct.Namespaces(((3, 3),))

        with self.assertRaises(TypeError):
            sv.ct.Namespaces({'a': {}})

    def test_invalid_type_input(self):
        """Test bad input into the API."""

        flags = sv.DEBUG
        if self.quirks:
            flags = sv._QUIRKS

        with self.assertRaises(TypeError):
            sv.match('div', "not a tag", flags=flags)

        with self.assertRaises(TypeError):
            sv.select('div', "not a tag", flags=flags)

        with self.assertRaises(TypeError):
            sv.filter('div', "not a tag", flags=flags)

        with self.assertRaises(TypeError):
            sv.comments('div', "not a tag", flags=flags)


class TestInvalidQuirks(TestInvalid):
    """Test invalid with QUIRKS."""

    def setUp(self):
        """Setup."""

        sv.purge()
        self.quirks = True

"""Test Soup Sieve API."""
import soupsieve as sv
from . import util
import copy
import random
import pytest
import pickle


class TestSoupSieve(util.TestCase):
    """Test Soup Sieve."""

    def test_ignore(self):
        """Test ignore."""

        with self.assertRaises(sv.SelectorSyntaxError):
            sv.compile('*:has(a)', ignore=[':has'])

    def test_ignore_escaped_and_cased_names(self):
        """Test that an ignored pseudo-class can't be used by writing its name with escapes or another case."""

        for ignore, selector in (
            ([':has'], '*:h\\61 s(a)'),
            ([':has'], '*:\\68 as(a)'),
            ([':has'], '*:HAS(a)'),
            ([':HAS'], '*:has(a)'),
            ([':has'], 'div:not(:h\\61 s(span))'),
            ([':lang'], ':l\\61 ng(en)'),
            ([':lang'], ':is(:LANG(en))'),
            ([':nth-child'], 'p:n\\74 h-child(2)'),
            ([':-soup-contains'], ':-soup-\\63 ontains(text)'),
            ([':l\\61 ng'], ':lang(en)')
        ):
            sv.purge()
            with self.assertRaises(sv.SelectorSyntaxError, msg=selector):
                sv.compile(selector, ignore=ignore)

    def test_ignore_aliases(self):
        """Test that an alias of a pseudo-class must be ignored separately."""

        sv.purge()
        with self.assertWarns(FutureWarning):
            sv.compile(':contains(text)', ignore=[':-soup-contains'])
        sv.compile(':matches(p)', ignore=[':is'])
        for selector in (':contains(text)', ':-soup-contains(text)'):
            with self.assertRaises(sv.SelectorSyntaxError, msg=selector):
                sv.compile(selector, ignore=[':-soup-contains', ':contains'])

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

        soup = self.soup(markup, 'html.parser')
        ids = [el.attrs['id'] for el in sv.select('span[id]', soup)]

        self.assertEqual(sorted(['5', 'some-id']), sorted(ids))

    def test_select_order(self):
        """Test select order."""

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

        soup = self.soup(markup, 'html.parser')
        ids = [el.attrs['id'] for el in sv.select('[id]', soup.body)]

        self.assertEqual(['1', '2', '3', '4', '5', 'some-id', '6'], ids)

    def test_select_limit(self):
        """Test select limit."""

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

        soup = self.soup(markup, 'html.parser')

        ids = [el.attrs['id'] for el in sv.select('span[id]', soup, limit=1)]

        self.assertEqual(sorted(['5']), sorted(ids))

    def test_select_one(self):
        """Test select one."""

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

        soup = self.soup(markup, 'html.parser')
        self.assertEqual(
            sv.select('span[id]', soup, limit=1)[0].attrs['id'],
            sv.select_one('span[id]', soup).attrs['id']
        )

    def test_select_one_none(self):
        """Test select one returns none for no match."""

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

        soup = self.soup(markup, 'html.parser')
        self.assertEqual(None, sv.select_one('h1', soup))

    def test_iselect(self):
        """Test select iterator."""

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

        soup = self.soup(markup, 'html.parser')

        ids = [el.attrs['id'] for el in sv.iselect('span[id]', soup)]

        self.assertEqual(sorted(['5', 'some-id']), sorted(ids))

    def test_iselect_order(self):
        """Test select iterator order."""

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

        soup = self.soup(markup, 'html.parser')
        ids = [el.attrs['id'] for el in sv.iselect('[id]', soup)]

        self.assertEqual(['1', '2', '3', '4', '5', 'some-id', '6'], ids)

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

        soup = self.soup(markup, 'html.parser')
        nodes = sv.select('span[id]', soup)
        self.assertTrue(sv.match('span#\\35', nodes[0]))
        self.assertFalse(sv.match('span#\\35', nodes[1]))

    def test_filter_tag(self):
        """Test filter tag."""

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

        soup = self.soup(markup, 'html.parser')
        nodes = sv.filter('pre#\\36', soup.html.body)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].attrs['id'], '6')

    def test_filter_tag_order(self):
        """Test filter tag order."""

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

        soup = self.soup(markup, 'html.parser')
        ids = [tag['id'] for tag in sv.filter('[id]', soup.html.body.p)]
        self.assertEqual(['2', '3'], ids)

    def test_filter_list(self):
        """
        Test filter list.

        Even if a list is created from the content of a tag, as long as the
        content is document nodes, filter will still handle it.  It doesn't have
        to be just tags.
        """

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

        soup = self.soup(markup, 'html.parser')
        nodes = sv.filter('pre#\\36', list(soup.html.body.children))
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].attrs['id'], '6')

    def test_filter_list_mixed(self):
        """Test filtering a list of tags from different documents, detached tags, and the contents of a `template`."""

        soup1 = self.soup(
            '<div id="1" lang="en"><p id="2">ab</p><template><p id="3">ab</p></template></div>', 'html.parser'
        )
        soup2 = self.soup('<div id="4" lang="fr"><p id="5">ab</p></div><p id="6">cd</p>', 'html.parser')
        detached = self.soup('<p id="7">ab</p>', 'html.parser').p.extract()
        nodes = [
            soup2.find(id='5'), soup1, detached, soup1.find(id='2'), soup2.find(id='6'), soup1.template.p,
            soup1.div, soup1.find(id='2').string, soup2.div
        ]

        self.assertEqual([n['id'] for n in sv.filter('p:-soup-contains(ab)', nodes)], ['5', '7', '2', '3'])
        self.assertEqual([n['id'] for n in sv.filter(':lang(en)', nodes)], ['2', '1'])
        self.assertEqual([n['id'] for n in sv.filter(':has(> p)', nodes)], ['1', '4'])
        # Each top level element of a fragment is a root, and so is a detached tag.
        self.assertEqual([n['id'] for n in sv.filter(':root', nodes)], ['7', '1'])
        # Each tag is its own scope.
        self.assertEqual([n['id'] for n in sv.filter(':scope', nodes)], ['5', '7', '2', '6', '3', '1', '4'])
        self.assertEqual([n['id'] for n in sv.filter('div:has(:scope)', nodes)], [])

    def test_filter_list_shares_matcher(self):
        """Test that the tags of a list that are in the same document share one matcher and its caches."""

        from bs4 import BeautifulSoup
        from unittest import mock

        n = 32
        soup = BeautifulSoup('<ul>' + '<li>x' * n, 'html.parser')
        other = BeautifulSoup('<ul>' + '<li>x' * n, 'html.parser')
        nodes = soup.find_all(True) + other.find_all(True)
        init = sv.css_match.CSSMatch.__init__
        for selector, matches, matchers in (
            ('li:-soup-contains(x)', 2 * n, 2),
            (':has(li)', 2 * (n - 1) + 2, 2),
            (':scope', 2 * (n + 1), 2 * (n + 1))
        ):
            with mock.patch.object(sv.css_match.CSSMatch, '__init__', autospec=True, side_effect=init) as patched:
                self.assertEqual(len(sv.filter(selector, nodes)), matches)
            self.assertEqual(patched.call_count, matchers)

    def test_filter_list_top_level_shares_matcher(self):
        """Test that the top level elements of a fragment, which are siblings, share one matcher and its caches."""

        from bs4 import BeautifulSoup
        from unittest import mock

        n = 32
        soup = BeautifulSoup('<div><p>x</p></div>' * n, 'html.parser')
        detached = BeautifulSoup('<div><p>x</p></div>', 'html.parser').div.extract()
        nodes = soup.find_all(True) + detached.find_all(True) + [detached]
        init = sv.css_match.CSSMatch.__init__
        # The last or first `div` of the fragment, every `p`, and the detached `div` and its `p`.
        for selector, matches in (
            (':nth-child(2n)', n // 2),
            (':nth-last-child(1)', n + 3),
            (':first-of-type', n + 3),
            ('div:nth-of-type(n+3)', n - 2),
            (':nth-child(n of p)', n + 1),
            (':root', 1),
        ):
            with mock.patch.object(sv.css_match.CSSMatch, '__init__', autospec=True, side_effect=init) as patched:
                self.assertEqual(len(sv.filter(selector, nodes)), matches, selector)
            # One for the fragment, and one for the detached tree.
            self.assertEqual(patched.call_count, 2, selector)
            self.assertEqual(
                sv.filter(selector, nodes), [node for node in nodes if sv.match(selector, node)], selector
            )

    def test_filter_list_top_level_linear(self):
        """Test that filtering the tags of a fragment with many top level elements counts each sibling once."""

        from bs4 import BeautifulSoup
        from unittest import mock

        n = 200
        soup = BeautifulSoup('<div><p>x</p></div>' * n, 'html.parser')
        nodes = soup.find_all(True)
        candidate = sv.css_match.CSSMatch.match_nth_candidate
        for selector in (':nth-child(2n)', ':nth-last-child(n)', ':first-of-type', ':nth-of-type(n)'):
            expected = sv.select(selector, soup)
            with mock.patch.object(
                sv.css_match.CSSMatch, 'match_nth_candidate', autospec=True, side_effect=candidate
            ) as patched:
                self.assertEqual(sv.filter(selector, nodes), expected, selector)
            # Each of the `2n` elements is counted among its siblings once.
            self.assertLessEqual(patched.call_count, 2 * n, selector)

    def test_uses_scope(self):
        """Test finding `:scope` or `&` in any part of a selector, nested ones included."""

        custom = {':--div': 'div', ':--scoped': ':scope > p'}
        for selector, expected in (
            ('p', False),
            (':scope', True),
            ('& > p', True),
            ('div p > span ~ b', False),
            (':is(div, :not(:scope p))', True),
            ('div:has(> :scope)', True),
            ('p:nth-child(2n of :scope li)', True),
            ('p:nth-child(2n of li)', False),
            (':is()', False),
            (':is(), :scope', True),
            (':--div p :--div', False),
            (':--div, :--scoped, :--scoped', True)
        ):
            pattern = sv.compile(selector, custom=custom, flags=sv.NOSTRICT)
            self.assertEqual(sv.css_match.uses_scope(pattern.selectors), expected, selector)

    def test_closest_match_parent(self):
        """Test match parent closest."""

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

        soup = self.soup(markup, 'html.parser')
        el = sv.select_one('#div-03', soup)
        self.assertTrue(sv.closest('#div-02', el).attrs['id'] == 'div-02')

    def test_closest_match_complex_parent(self):
        """Test closest match complex parent."""

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

        soup = self.soup(markup, 'html.parser')
        el = sv.select_one('#div-03', soup)
        self.assertTrue(sv.closest('article > div', el).attrs['id'] == 'div-01')
        self.assertTrue(sv.closest(':not(div)', el).attrs['id'] == 'article')

    def test_closest_match_self(self):
        """Test closest match self."""

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

        soup = self.soup(markup, 'html.parser')
        el = sv.select_one('#div-03', soup)
        self.assertTrue(sv.closest('div div', el).attrs['id'] == 'div-03')

    def test_closest_must_be_parent(self):
        """Test that closest only matches parents or self."""

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

        soup = self.soup(markup, 'html.parser')
        el = sv.select_one('#div-03', soup)
        self.assertTrue(sv.closest('div #div-05', el) is None)
        self.assertTrue(sv.closest('a', el) is None)

    def test_escape_hyphen(self):
        """Test escape hyphen cases."""

        self.assertEqual(r'\-', sv.escape('-'))
        self.assertEqual(r'--', sv.escape('--'))

    def test_escape_numbers(self):
        """Test escape hyphen cases."""

        self.assertEqual(r'\33 ', sv.escape('3'))
        self.assertEqual(r'-\33 ', sv.escape('-3'))
        self.assertEqual(r'--3', sv.escape('--3'))

    def test_escape_null(self):
        """Test escape null character."""

        self.assertEqual('\ufffdtest', sv.escape('\x00test'))

    def test_escape_ctrl(self):
        """Test escape control character."""

        self.assertEqual(r'\1 test', sv.escape('\x01test'))

    def test_escape_special(self):
        """Test escape special character."""

        self.assertEqual(r'\{\}\[\]\ \(\)', sv.escape('{}[] ()'))

    def test_escape_wide_unicode(self):
        """Test handling of wide Unicode."""

        self.assertEqual('Emoji\\ \U0001F60D', sv.escape('Emoji \U0001F60D'))

    def test_escape_non_ascii_ident(self):
        """Test that non-ASCII identifier code points are not escaped."""

        for c in (
            '\u00b7', '\u00c0', '\u00f8', '\u037f', '\u200c', '\u203f',
            '\u2070', '\u2c00', '\u3001', '\uf900', '\ufdf0', '\ufffd'
        ):
            self.assertEqual(c, sv.escape(c))

    def test_escape_non_ascii_non_ident(self):
        """Test that non-ASCII code points that are not identifier code points are escaped."""

        for c in (
            '\x80', '\x9f', '\u00a0', '\u00d7', '\u00f7', '\u037e',
            '\u2000', '\u2028', '\u3000', '\ue000', '\ufdd0', '\ufffe'
        ):
            self.assertEqual('\\' + c, sv.escape(c))

    def test_escape_round_trip(self):
        """Test that escaped identifiers can be parsed and match the original value."""

        soup = self.soup('<div></div>', 'html.parser')
        el = soup.div
        for cp in range(0x01, 0x10000):
            if 0xD800 <= cp <= 0xDFFF:
                continue
            value = f'a{chr(cp)}'
            el['id'] = value
            self.assertTrue(sv.match(f'#{sv.escape(value)}', el), f'Failed to round trip U+{cp:04X}')

    def test_unescaped_non_ascii_identifiers(self):
        """Test that, like browsers, any unescaped non-ASCII code point is allowed in an identifier."""

        soup = self.soup('<div></div>', 'html.parser')
        el = soup.div
        for cp in range(0x80, 0x10000):
            if 0xD800 <= cp <= 0xDFFF:
                continue
            c = chr(cp)
            for value in (c, f'-{c}', f'a{c}b'):
                el['id'] = value
                self.assertTrue(sv.match(f'#{value}', el), f'Failed to match unescaped U+{cp:04X} in {value!r}')

    def test_escape_del_c1_ctrl(self):
        """Test escape DEL and C1 control characters."""

        for codepoint in range(0x7F, 0xA0):
            ident = f'a{chr(codepoint)}b'
            soup = self.soup(f'<p id="{ident}"></p>', 'html.parser')
            self.assertTrue(sv.match('#' + sv.escape(ident), soup.p))

    def test_copy_pickle(self):
        """Test copy and pickle."""

        # Test that we can pickle and unpickle
        # We force a pattern that contains all custom types:
        # `Selector`, `NullSelector`, `SelectorTag`, `SelectorAttribute`,
        # `SelectorNth`, `SelectorLang`, `SelectorList`, `Namespaces`,
        # `SelectorContains`, and `CustomSelectors`.
        p1 = sv.compile(
            'p.class#id[id]:nth-child(2):lang(en):focus:-soup-contains("text", "other text")',
            {'html': 'http://www.w3.org/TR/html4/'},
            custom={':--header': 'h1, h2, h3, h4, h5, h6'}
        )
        sp1 = pickle.dumps(p1)
        pp1 = pickle.loads(sp1)
        self.assertTrue(pp1 == p1)

        # Test that we pull the same one from cache
        p2 = sv.compile(
            'p.class#id[id]:nth-child(2):lang(en):focus:-soup-contains("text", "other text")',
            {'html': 'http://www.w3.org/TR/html4/'},
            custom={':--header': 'h1, h2, h3, h4, h5, h6'}
        )
        self.assertTrue(p1 is p2)

        # Test that we compile a new one when providing a different flags
        p3 = sv.compile(
            'p.class#id[id]:nth-child(2):lang(en):focus:-soup-contains("text", "other text")',
            {'html': 'http://www.w3.org/TR/html4/'},
            custom={':--header': 'h1, h2, h3, h4, h5, h6'},
            flags=0x10
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

    def test_pickle_nested(self):
        """Test pickling selectors that contain nested selector objects."""

        # Avoid "no match" pseudo-classes, such as `:focus`, as they reduce the entire compound
        # selector to `ct.Null`, and none of the nested objects would be pickled.
        markup = """
        <div>
        <p id="id" class="class a" lang="en">some text<span class="b"></span></p>
        <p id="other" class="class" lang="en">some text<span class="b"></span></p>
        </div>
        <h1 id="header"></h1>
        """

        p1 = sv.compile(
            'div > p.class#id[id]:nth-child(1 of .class):lang(en):-soup-contains("text"):has(> span:is(.a, .b)), '
            ':--header',
            {'html': 'http://www.w3.org/TR/html4/'},
            custom={':--header': 'h1, h2'}
        )
        pp1 = pickle.loads(pickle.dumps(p1))
        self.assertTrue(pp1 is not p1)
        self.assertTrue(pp1 == p1)

        # Deep copies are made in the same way as pickling.
        p2 = copy.deepcopy(p1)
        self.assertTrue(p2 is not p1)
        self.assertTrue(p2 == p1)

        soup = self.soup(markup, 'html.parser')
        ids = ['id', 'header']
        self.assertEqual([el.attrs['id'] for el in p1.select(soup)], ids)
        self.assertEqual([el.attrs['id'] for el in pp1.select(soup)], ids)
        self.assertEqual([el.attrs['id'] for el in p2.select(soup)], ids)

    def test_pickle_null_and_selector(self):
        """Test pickling a selector list that mixes null selectors with real selectors."""

        # `:focus` can never match, so the first selector is `ct.Null`, while the second is a real selector.
        p1 = sv.compile('p:focus, div')
        self.assertTrue(p1.selectors[0] is sv.ct.Null)
        self.assertTrue(isinstance(p1.selectors[1], sv.ct.Selector))

        pp1 = pickle.loads(pickle.dumps(p1))
        self.assertTrue(pp1 == p1)
        self.assertTrue(pp1.selectors[0] is sv.ct.Null)
        self.assertTrue(isinstance(pp1.selectors[1], sv.ct.Selector))
        self.assertTrue(pp1.selectors[1] is not p1.selectors[1])

    def test_pickle_shared(self):
        """Test that objects shared within a selector are still shared after pickling."""

        # The built-in selector list for `:checked` is reused each time it is referenced.
        p1 = sv.compile(':checked:checked')
        first, second = p1.selectors[0].selectors
        self.assertTrue(first is second)

        pp1 = pickle.loads(pickle.dumps(p1))
        self.assertTrue(pp1 == p1)
        first, second = pp1.selectors[0].selectors
        self.assertTrue(first is second)
        self.assertTrue(first is not p1.selectors[0].selectors[0])

        # A shared object is only stored once, so referencing it twice doesn't add to what is pickled.
        _, (nodes1,) = sv.ct._pickle(p1)
        _, (nodes2,) = sv.ct._pickle(sv.compile(':checked'))
        self.assertEqual(len(nodes1), len(nodes2))

    def test_equal_shared(self):
        """Test equality of distinct selectors that share nested objects."""

        # Different namespaces cause separate compiles, but the built-in selector list for `:checked`
        # is reused by both, so the comparison reaches the same nested object on both sides.
        p1 = sv.compile(':checked').selectors
        p2 = sv.compile(':checked', namespaces={'x': 'y'}).selectors
        self.assertTrue(p1 is not p2)
        self.assertTrue(p1[0].selectors[0] is p2[0].selectors[0])
        self.assertTrue(p1 == p2)
        self.assertFalse(p1 != p2)

    @pytest.mark.skipif(hash(-1) != hash(-2), reason='requires `-1` and `-2` to have the same hash')
    def test_equal_hash_collision(self):
        """Test that selectors with the same hash, but different values, are not equal."""

        # `-1` and `-2` have the same hash in CPython (and PyPy), so these selectors only differ by `a`
        # in `an+b`, which isn't reflected in the hash. Equality must compare the values.
        # This is an implementation detail, so the test is skipped where it doesn't hold.
        p1 = sv.compile(':nth-child(-n+3)').selectors
        p2 = sv.compile(':nth-child(-2n+3)').selectors
        self.assertEqual(p1[0].nth[0].a, -1)
        self.assertEqual(p2[0].nth[0].a, -2)
        self.assertEqual(hash(p1), hash(p2))
        self.assertFalse(p1 == p2)
        self.assertTrue(p1 != p2)

    def test_cache(self):
        """Test cache."""

        sv.purge()
        self.assertEqual(sv.cp._cached_css_compile.cache_info().currsize, 0)
        for _x in range(1000):
            value = f'[value="{random.randint(1, 10000)!s}"]'
            p = sv.compile(value)
            self.assertTrue(p.pattern == value)
            self.assertTrue(sv.cp._cached_css_compile.cache_info().currsize > 0)
        self.assertTrue(sv.cp._cached_css_compile.cache_info().currsize == 500)
        sv.purge()
        self.assertEqual(sv.cp._cached_css_compile.cache_info().currsize, 0)

    def test_nocache_tree_changes_during_iselect(self):
        """With `NOCACHE`, each element is matched against the tree as it is at that point of an `iselect()`."""

        from bs4 import BeautifulSoup

        # The content language in the header.
        soup = BeautifulSoup(
            '<html><head><meta http-equiv="content-language" content="en"></head>'
            '<body><p id="1"></p><p id="2"></p></body></html>',
            'html.parser'
        )
        found = []
        for el in sv.iselect('p:lang(en)', soup, flags=sv.NOCACHE):
            found.append(el['id'])
            soup.meta['content'] = 'fr'
        self.assertEqual(found, ['1'])

        # The checked radio button of a group, which ends it being indeterminate.
        soup = BeautifulSoup(
            '<form><input id="1" type="radio" name="a"><input id="2" type="radio" name="a">'
            '<input id="3" type="radio" name="a"></form>',
            'html.parser'
        )
        found = []
        for el in sv.iselect(':indeterminate', soup, flags=sv.NOCACHE):
            found.append(el['id'])
            soup.find(id='3')['checked'] = ''
        self.assertEqual(found, ['1'])

        # The selected option of a `select`.
        soup = BeautifulSoup(
            '<select><option id="1">a</option><option id="2">b</option><option id="3">c</option></select>',
            'html.parser'
        )
        found = []
        for el in sv.iselect('option:checked', soup, flags=sv.NOCACHE):
            found.append(el['id'])
            soup.find(id='3')['selected'] = ''
        self.assertEqual(found, ['1', '3'])

    def test_recompile(self):
        """If you feed through the same object, it should pass through unless you change parameters."""

        p1 = sv.compile('p[id]')
        p2 = sv.compile(p1)
        self.assertTrue(p1 is p2)

        with pytest.raises(ValueError):
            sv.compile(p1, flags=sv.DEBUG)

        with pytest.raises(ValueError):
            sv.compile(p1, namespaces={"": ""})

        with pytest.raises(ValueError):
            sv.compile(p1, custom={":--header": 'h1, h2, h3, h4, h5, h6'})

    def test_immutable_dict_size(self):
        """Test immutable dictionary."""

        idict = sv.ct.ImmutableDict({'a': 'b', 'c': 'd'})
        self.assertEqual(2, len(idict))


class TestInvalid(util.TestCase):
    """Test invalid."""

    def test_immutable_object(self):
        """Test immutable object."""

        obj = sv.ct.Immutable()

        with self.assertRaises(AttributeError):
            obj.member = 3

    def test_immutable_dict_read_only(self):
        """Test immutable dictionary is read only."""

        idict = sv.ct.ImmutableDict({'a': 'b', 'c': 'd'})
        with self.assertRaises(TypeError):
            idict['a'] = 'f'

    def test_immutable_dict_hashable_value(self):
        """Test immutable dictionary has a hashable value."""

        with self.assertRaises(TypeError):
            sv.ct.ImmutableDict([[3, {}]])

    def test_immutable_dict_hashable_key(self):
        """Test immutable dictionary has a hashable key."""

        with self.assertRaises(TypeError):
            sv.ct.ImmutableDict([[{}, 3]])

    def test_immutable_dict_hashable_value_dict(self):
        """Test immutable dictionary has a hashable value."""

        with self.assertRaises(TypeError):
            sv.ct.ImmutableDict({3: {}})

    def test_invalid_namespace_hashable_value(self):
        """Test namespace has hashable value."""

        with self.assertRaises(TypeError):
            sv.ct.Namespaces({'a': {}})

    def test_invalid_namespace_hashable_key(self):
        """Test namespace key is hashable."""

        with self.assertRaises(TypeError):
            sv.ct.Namespaces({{}: 'string'})

    def test_invalid_namespace_key(self):
        """Test custom selector key is hashable."""

        with self.assertRaises(TypeError):
            sv.ct.Namespaces({3: 'string'})

    def test_invalid_custom_hashable_value(self):
        """Test custom selector has hashable value."""

        with self.assertRaises(TypeError):
            sv.ct.CustomSelectors({':--a': {}})

    def test_invalid_custom_hashable_key(self):
        """Test custom selector key is hashable."""

        with self.assertRaises(TypeError):
            sv.ct.CustomSelectors({{}: 'string'})

    def test_invalid_custom_key(self):
        """Test custom selector key is hashable."""

        with self.assertRaises(TypeError):
            sv.ct.CustomSelectors({3: 'string'})

    def test_invalid_type_input_match(self):
        """Test bad input into the match API."""

        flags = sv.DEBUG

        with self.assertRaises(TypeError):
            sv.match('div', "not a tag", flags=flags)

    def test_invalid_type_input_select(self):
        """Test bad input into the select API."""

        flags = sv.DEBUG

        with self.assertRaises(TypeError):
            sv.select('div', "not a tag", flags=flags)

    def test_invalid_type_input_filter(self):
        """Test bad input into the filter API."""

        flags = sv.DEBUG

        with self.assertRaises(TypeError):
            sv.filter('div', "not a tag", flags=flags)

    def test_excessive_selectors(self):
        """Test excessive selectors."""

        # Build a 500 KB selector string: "a,a,a,...,a" (250,000 items)
        count = 10000
        selector = ",".join("a" for _ in range(count))

        # Compile the selector
        with self.assertRaises(ValueError):
            sv.compile(selector)

    def test_excessive_group_selectors(self):
        """Test excessive selectors in `:is()` and `:where()`."""

        count = 10000
        selector = f':is({"," * count})'

        # Compile the selector
        with self.assertRaises(ValueError):
            sv.compile(selector)

        selector = f':where({"," * count})'

        # Compile the selector
        with self.assertRaises(ValueError):
            sv.compile(selector)

    def test_excessive_custom_selectors(self):
        """Test excessive custom selectors."""

        # Build a 500 KB selector string: "a,a,a,...,a" (250,000 items)
        count = 10000
        selector = ",".join("a" for _ in range(count))

        # Compile the selector
        with self.assertRaises(ValueError):
            sv.compile('div:--custom', custom={':--custom': selector})

    def test_excessive_custom_and_normal_selectors(self):
        """Test excessive custom and normal selectors."""

        count = 5000
        selector = ",".join("a" for _ in range(count))

        # Compile the selector
        with self.assertRaises(ValueError):
            sv.compile(f':is({selector}):--custom', custom={':--custom': selector})


class TestSyntaxErrorReporting(util.TestCase):
    """Test reporting of syntax errors."""

    def test_syntax_error_has_text_and_position(self):
        """Test that selector syntax errors contain the position."""

        with self.assertRaises(sv.SelectorSyntaxError) as cm:
            sv.compile('input.field[type=42]')
        e = cm.exception
        self.assertEqual(e.context, 'input.field[type=42]\n           ^')
        self.assertEqual(e.line, 1)
        self.assertEqual(e.col, 12)

    def test_syntax_error_with_multiple_lines(self):
        """Test that multiline selector errors have the right position."""

        with self.assertRaises(sv.SelectorSyntaxError) as cm:
            sv.compile(
                'input\n'
                '.field[type=42]')
        e = cm.exception
        self.assertEqual(e.context, '    input\n--> .field[type=42]\n          ^')
        self.assertEqual(e.line, 2)
        self.assertEqual(e.col, 7)

    def test_syntax_error_on_third_line(self):
        """Test that multiline selector errors have the right position."""

        with self.assertRaises(sv.SelectorSyntaxError) as cm:
            sv.compile(
                'input:is(\n'
                '  [name=foo]\n'
                '  [type=42]\n'
                ')\n'
            )
        e = cm.exception
        self.assertEqual(e.line, 3)
        self.assertEqual(e.col, 3)

    def test_simple_syntax_error(self):
        """Test a simple syntax error (no context)."""

        with self.assertRaises(sv.SelectorSyntaxError) as cm:
            raise sv.SelectorSyntaxError('Syntax Message')

        e = cm.exception
        self.assertEqual(e.context, None)
        self.assertEqual(e.line, None)
        self.assertEqual(e.col, None)
        self.assertEqual(str(e), 'Syntax Message')

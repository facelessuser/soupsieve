"""
Test thread safety.

Selectors are compiled and matched concurrently, and every result must be the same as the result from a single
thread. A race can only be caught when threads switch in the right place, so the threads are run for a fixed amount
of time with a short switch interval to make switches frequent. A test like this cannot fail when there is no race,
but it is not guaranteed to catch one either. To catch a race reliably, run these tests on a free-threaded build of
Python, where threads run in parallel.
"""
import soupsieve as sv
from soupsieve import css_parser as cp
from . import util
import sys
import threading
import time

THREADS = 8
DURATION = 0.5

# Patterns that exercise every kind of token, especially tokens that are consumed without being processed (leading
# and trailing whitespace, comments) and pseudo-classes that are matched by `SpecialPseudoPattern`.
PATTERNS = (
    '  div',
    'div p ',
    'div > p',
    'a ~ b + c',
    'div, p , span',
    ':is(div, p) > /* comment */ span',
    'div /* comment */',
    'div/* comment */ > /* comment */p',
    'div:nth-child(2) span',
    ':nth-last-child(2n+1 of .a) b',
    'span:nth-of-type(2) ~ span',
    'p:lang(en) > span:dir(ltr)',
    'div:-soup-contains("x") ~ p',
    'input:checked, :default, :disabled',
    'div#d1 > p.a[class~=a]',
    'html|* > ns|tag',
    ':--custom > span',
    'div:has(> span, + div) :not(p)',
    ':root > body *|*',
    '& > div',
)

MARKUP = """
<html lang="en"><body>
<div id="d1"><p>x</p><span>one</span><p class="a">two</p></div>
<div><span>a</span><span dir="ltr">b</span><p lang="en"><span>c</span></p></div>
<form><input type="checkbox" checked><input type="radio" name="r"><button>go</button>
<fieldset disabled><input type="text"></fieldset></form>
<a></a><b></b><c></c>
</body></html>
"""

CUSTOM = {':--custom': 'div:has(> p)'}


def parse(pattern):
    """Parse a pattern bypassing the cache, so each call really parses it."""

    return cp.CSSParser(pattern, custom=sv.CustomSelectors(CUSTOM)).process_selectors()


def token_state(token):
    """
    Get the state of a token, except the compiled pattern which is created lazily.

    Nested patterns of `SpecialPseudoPattern` are included as well.
    """

    state = {}
    for k, v in vars(token).items():
        if k == '_re_pattern':
            continue
        state[k] = {name: token_state(p) for name, p in v.items()} if k == 'patterns' else v
    return state


class TestThreads(util.TestCase):
    """Test thread safety."""

    def setUp(self):
        """Use a short switch interval so threads switch often."""

        self.interval = sys.getswitchinterval()
        sys.setswitchinterval(1e-6)

    def tearDown(self):
        """Restore the switch interval."""

        sys.setswitchinterval(self.interval)

    def run_threads(self, func, args):
        """Run `func` with every argument in every thread until the time is up and collect the failures."""

        errors = []
        barrier = threading.Barrier(THREADS)

        def worker(offset):
            barrier.wait()
            stop = time.monotonic() + DURATION
            index = offset
            while time.monotonic() < stop and not errors:
                arg = args[index % len(args)]
                index += 1
                try:
                    func(arg)
                except Exception as e:  # noqa: BLE001
                    errors.append(f'{arg!r}: {type(e).__name__}: {e}')

        threads = [threading.Thread(target=worker, args=(n,)) for n in range(THREADS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(errors, [])

    def test_tokens_have_no_match_state(self):
        """
        Test that matching a token does not change its state.

        Tokens are shared by every parser, so any state that is saved on a token while matching can be changed by
        a parser in another thread before it is used. Every token is matched at every position of every pattern,
        so a token that saves anything about a match is caught.
        """

        for pattern in PATTERNS:
            for index in range(len(pattern)):
                for token in cp.CSSParser.CSS_TOKENS:
                    before = token_state(token)
                    token.match(pattern, index, 0)
                    self.assertEqual(
                        before,
                        token_state(token),
                        f'{type(token).__name__} changed its state matching {pattern!r} at {index}'
                    )

    def test_parse(self):
        """Test that parsing in many threads gives the same results as parsing in one."""

        expected = {p: parse(p) for p in PATTERNS}

        def check(pattern):
            result = parse(pattern)
            if result != expected[pattern]:
                raise AssertionError(f'parsed as {result!r}, expected {expected[pattern]!r}')

        self.run_threads(check, PATTERNS)

    def test_compile_and_purge(self):
        """Test compiling through the cache while it is purged in many threads."""

        expected = {p: parse(p) for p in PATTERNS}

        def check(pattern):
            if pattern == PATTERNS[0]:
                sv.purge()
            result = sv.compile(pattern, {'ns': 'http://example.com'}, custom=CUSTOM).selectors
            if result != expected[pattern]:
                raise AssertionError(f'compiled as {result!r}, expected {expected[pattern]!r}')

        try:
            self.run_threads(check, PATTERNS)
        finally:
            sv.purge()

    def test_select(self):
        """Test selecting with shared compiled patterns on a shared document in many threads."""

        soup = self.soup(MARKUP, 'html.parser')
        compiled = [sv.compile(p, {'ns': 'http://example.com'}, custom=CUSTOM) for p in PATTERNS]
        expected = {c: [id(el) for el in c.select(soup)] for c in compiled}

        def check(pattern):
            result = [id(el) for el in pattern.select(soup)]
            if result != expected[pattern]:
                raise AssertionError(f'{pattern.pattern!r} selected different elements')
            for el in soup.find_all(True):
                if pattern.match(el) != (id(el) in expected[pattern]):
                    raise AssertionError(f'{pattern.pattern!r} matched a different element')

        self.run_threads(check, compiled)

    def test_lazy_pseudo_selectors(self):
        """Test that pseudo-classes defined by selectors are parsed once when they are first used in many threads."""

        selectors = cp.PseudoSelectorMap(
            {':checked': cp.CSS_CHECKED, ':default': cp.CSS_DEFAULT, ':enabled': cp.CSS_ENABLED}
        )
        results = []
        barrier = threading.Barrier(THREADS)

        def worker():
            barrier.wait()
            results.append(tuple(selectors[k] for k in (':checked', ':default', ':enabled')))

        threads = [threading.Thread(target=worker) for _ in range(THREADS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(results), THREADS)
        for result in results:
            for a, b in zip(result, results[0], strict=True):
                self.assertIs(a, b)

    def test_lazy_pattern(self):
        """Test that a token's pattern is compiled once when it is first used in many threads."""

        token = cp.SelectorPattern('tag', cp.PAT_TAG)
        results = []
        barrier = threading.Barrier(THREADS)

        def worker():
            barrier.wait()
            results.append(token.re_pattern)

        threads = [threading.Thread(target=worker) for _ in range(THREADS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(results), THREADS)
        for result in results:
            self.assertIs(result, results[0])

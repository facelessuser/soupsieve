"""CSS selector parser."""
import re
from functools import lru_cache
from . import util
from . import css_match as cm
from . import css_types as ct
from collections import OrderedDict

SUPPORTED_PSEUDO = {
    ":root",
    ":empty",
    ":has",
    ":contains",
    ":is",
    ":matches",
    ":not",
    ":where",
    ":first-child",
    ":first-of-type",
    ":last-child",
    ":last-of-type",
    ":only-child",
    ":only-of-type",
    ":nth-child",
    ":nth-last-child",
    ":nth-of-type",
    ":nth-last-of-type"
}

# Sub-patterns parts
WS = r'[ \t\r\n\f]'

CSS_ESCAPES = r'(?:\\[a-f0-9]{{1,6}}{ws}?|\\.)'.format(ws=WS)

IDENTIFIER = r'''
(?:(?!-?\d|--)(?:[^\u0000-\u002c\u002e\u002f\u003A-\u0040\u005B-\u005E\u0060\u007B-\u009f]|{esc})+)
'''.format(esc=CSS_ESCAPES)

NTH = r'(?:[-+])?(?:\d+n?|n)(?:(?<=n){ws}*(?:[-+]){ws}*(?:\d+))?'.format(ws=WS)

VALUE = r'''
(?P<value>
    "(?:\\.|[^\\"]+)*?"|
    '(?:\\.|[^\\']+)*?'|
    {ident}+
)
'''.format(ident=IDENTIFIER)

ATTR = r'''(?:{ws}*(?P<cmp>[~^|*$]?=){ws}*{value}(?P<case>{ws}+[is])?)?{ws}*\]'''.format(ws=WS, value=VALUE)

# Selector patterns
PAT_ID = r'\#{ident}'.format(ident=IDENTIFIER)

PAT_CLASS = r'\.{ident}'.format(ident=IDENTIFIER)

PAT_TAG = r'(?:(?:{ident}|\*)?\|)?(?:{ident}|\*)'.format(ident=IDENTIFIER)

PAT_ATTR = r'''
\[{ws}*(?P<ns_attr>(?:(?:{ident}|\*)?\|)?{ident})
{attr}
'''.format(ws=WS, ident=IDENTIFIER, attr=ATTR)

PAT_PSEUDO_OPEN = r':(?:has|is|matches|not|where)\('

PAT_PSEUDO_CLOSE = r'{ws}*\)'.format(ws=WS)

PAT_PSEUDO = r':(?:empty|root|(?:first|last|only)-(?:child|of-type))\b'

PAT_PSEUDO_NTH_CHILD = r'''
(?P<pseudo_nth_child>:nth-(?:last-)?child
\({ws}*(?P<nth_child>{nth}|even|odd){ws}*(?:\)|(?<={ws})of{ws}+))
'''.format(ws=WS, nth=NTH)

PAT_PSEUDO_NTH_TYPE = r'''
(?P<pseudo_nth_type>:nth-(?:last-)?of-type
\({ws}*(?P<nth_type>{nth}|even|odd){ws}*\))
'''.format(ws=WS, nth=NTH)

PAT_SPLIT = r'{ws}*?(?P<relation>[,+>~]|{ws}(?![,+>~])){ws}*'.format(ws=WS)

# Extra selector patterns
PAT_PSEUDO_CONTAINS = r':contains\({ws}*{value}{ws}*\)'.format(ws=WS, value=VALUE)

PAT_PSEUDO_INVALID = r':{ident}'.format(ident=IDENTIFIER)

# CSS escape pattern
RE_CSS_ESC = re.compile(r'(?:(\\[a-f0-9]{{1,6}}{ws}?)|(\\.))'.format(ws=WS), re.I)

# Pattern to break up `nth` specifiers
RE_NTH = re.compile(r'(?P<s1>[-+])?(?P<a>\d+n?|n)(?:(?<=n){ws}*(?P<s2>[-+]){ws}*(?P<b>\d+))?'.format(ws=WS), re.I)

SPLIT = ','
REL_HAS_CHILD = ": "

_MAXCACHE = 500


@lru_cache(maxsize=_MAXCACHE)
def _cached_css_compile(pattern, namespaces, flags):
    """Cached CSS compile."""

    return cm.SoupSieve(
        pattern,
        CSSParser(pattern, flags).process_selectors(),
        namespaces,
        flags
    )


def _purge_cache():
    """Purge the cache."""

    _cached_css_compile.cache_clear()


def css_unescape(string):
    """Unescape CSS value."""

    def replace(m):
        """Replace with the appropriate substitute."""

        return chr(int(m.group(1)[1:], 16)) if m.group(1) else m.group(2)[1:]

    return RE_CSS_ESC.sub(replace, string)


class SelectorPattern:
    """Selector pattern."""

    def __init__(self, pattern):
        """Initialize."""

        self.pattern = re.compile(pattern, re.I | re.X)

    def enabled(self, flags):
        """Enabled."""

        return True


class _Selector:
    """
    Intermediate selector class.

    This stores selector data for a compound selector as we are acquiring them.
    Once we are done collecting the data for a compound selector, we freeze
    the data in an object that can be pickled and hashed.
    """

    def __init__(self, **kwargs):
        """Initialize."""

        self.tag = kwargs.get('tag', None)
        self.ids = kwargs.get('ids', [])
        self.classes = kwargs.get('classes', [])
        self.attributes = kwargs.get('attributes', [])
        self.nth = kwargs.get('nth', [])
        self.selectors = kwargs.get('selectors', [])
        self.relations = kwargs.get('relations', [])
        self.rel_type = kwargs.get('rel_type', None)
        self.contains = kwargs.get('contains', [])
        self.empty = kwargs.get('empty', False)
        self.root = kwargs.get('root', False)

    def _freeze_relations(self, relations):
        """Freeze relation."""

        if relations:
            sel = relations[0]
            sel.relations.extend(relations[1:])
            return ct.SelectorList([sel.freeze()])
        else:
            return ct.SelectorList()

    def freeze(self):
        """Freeze self."""

        return ct.Selector(
            self.tag,
            tuple(self.ids),
            tuple(self.classes),
            tuple(self.attributes),
            tuple(self.nth),
            tuple(self.selectors),
            self._freeze_relations(self.relations),
            self.rel_type,
            tuple(self.contains),
            self.empty,
            self.root
        )

    def __str__(self):  # pragma: no cover
        """String representation."""

        return (
            '_Selector(tag=%r, ids=%r, classes=%r, attributes=%r, nth=%r, selectors=%r, '
            'relations=%r, rel_type=%r, empty=%r, root=%r)'
        ) % (
            self.tag, self.ids, self.classes, self.attributes, self.nth, self.selectors,
            self.relations, self.rel_type, self.empty, self.root
        )

    __repr__ = __str__


class CSSParser:
    """Parse CSS selectors."""

    css_tokens = OrderedDict(
        [
            ("pseudo_open", SelectorPattern(PAT_PSEUDO_OPEN)),
            ("pseudo_close", SelectorPattern(PAT_PSEUDO_CLOSE)),
            ("pseudo", SelectorPattern(PAT_PSEUDO)),
            ("pseudo_contains", SelectorPattern(PAT_PSEUDO_CONTAINS)),
            ("pseudo_nth_child", SelectorPattern(PAT_PSEUDO_NTH_CHILD)),
            ("pseudo_nth_type", SelectorPattern(PAT_PSEUDO_NTH_TYPE)),
            ("pseudo_invalid", SelectorPattern(PAT_PSEUDO_INVALID)),
            ("id", SelectorPattern(PAT_ID)),
            ("class", SelectorPattern(PAT_CLASS)),
            ("tag", SelectorPattern(PAT_TAG)),
            ("attribute", SelectorPattern(PAT_ATTR)),
            ("combine", SelectorPattern(PAT_SPLIT))
        ]
    )

    def __init__(self, selector, flags=0):
        """Initialize."""

        self.pattern = selector
        self.flags = flags
        dflags = self.flags & util.DEPRECATED_FLAGS
        if dflags:
            util.warn_deprecated(
                "The following flags are deprecated and may be repurposed in the future '0x%02X'" % dflags
            )

    def parse_attribute_selector(self, sel, m, has_selector):
        """Create attribute selector from the returned regex match."""

        case = util.lower(m.group('case').strip()) if m.group('case') else None
        parts = [css_unescape(a.strip()) for a in m.group('ns_attr').split('|')]
        ns = ''
        is_type = False
        pattern2 = None
        if len(parts) > 1:
            ns = parts[0]
            attr = parts[1]
        else:
            attr = parts[0]
        if case:
            flags = re.I if case == 'i' else 0
        elif util.lower(attr) == 'type':
            flags = re.I
            is_type = True
        else:
            flags = 0

        op = m.group('cmp')
        if op:
            value = css_unescape(
                m.group('value')[1:-1] if m.group('value').startswith(('"', "'")) else m.group('value')
            )
        else:
            value = None
        if not op:
            # Attribute name
            pattern = None
        elif op.startswith('^'):
            # Value start with
            pattern = re.compile(r'^%s.*' % re.escape(value), flags)
        elif op.startswith('$'):
            # Value ends with
            pattern = re.compile(r'.*?%s$' % re.escape(value), flags)
        elif op.startswith('*'):
            # Value contains
            pattern = re.compile(r'.*?%s.*' % re.escape(value), flags)
        elif op.startswith('~'):
            # Value contains word within space separated list
            pattern = re.compile(r'.*?(?:(?<=^)|(?<= ))%s(?=(?:[ ]|$)).*' % re.escape(value), flags)
        elif op.startswith('|'):
            # Value starts with word in dash separated list
            pattern = re.compile(r'^%s(?:-.*)?$' % re.escape(value), flags)
        else:
            # Value matches
            pattern = re.compile(r'^%s$' % re.escape(value), flags)
        if is_type:
            pattern2 = re.compile(pattern.pattern)
        has_selector = True
        sel.attributes.append(ct.SelectorAttribute(attr, ns, pattern, pattern2))
        return has_selector

    def parse_tag_pattern(self, sel, m, has_selector):
        """Parse tag pattern from regex match."""

        parts = [css_unescape(x) for x in m.group(0).split('|')]
        if len(parts) > 1:
            prefix = parts[0]
            tag = parts[1]
        else:
            tag = parts[0]
            prefix = None
        sel.tag = ct.SelectorTag(tag, prefix)
        has_selector = True
        return has_selector

    def parse_pseudo(self, sel, m, has_selector):
        """Parse pseudo."""

        pseudo = util.lower(m.group(0)[1:])
        if pseudo == 'root':
            sel.root = True
        elif pseudo == 'empty':
            sel.empty = True
        elif pseudo == 'first-child':
            sel.nth.append(ct.SelectorNth(1, False, 0, False, False, ct.SelectorList()))
        elif pseudo == 'last-child':
            sel.nth.append(ct.SelectorNth(1, False, 0, False, True, ct.SelectorList()))
        elif pseudo == 'first-of-type':
            sel.nth.append(ct.SelectorNth(1, False, 0, True, False, ct.SelectorList()))
        elif pseudo == 'last-of-type':
            sel.nth.append(ct.SelectorNth(1, False, 0, True, True, ct.SelectorList()))
        elif pseudo == 'only-child':
            sel.nth.extend(
                [
                    ct.SelectorNth(1, False, 0, False, False, ct.SelectorList()),
                    ct.SelectorNth(1, False, 0, False, True, ct.SelectorList())
                ]
            )
        elif pseudo == 'only-of-type':
            sel.nth.extend(
                [
                    ct.SelectorNth(1, False, 0, True, False, ct.SelectorList()),
                    ct.SelectorNth(1, False, 0, True, True, ct.SelectorList())
                ]
            )

        has_selector = True
        return has_selector

    def parse_pseudo_nth(self, sel, m, has_selector, iselector):
        """Parse `nth` pseudo."""

        mdict = m.groupdict()
        postfix = '_child' if mdict.get('pseudo_nth_child') else '_type'
        content = mdict.get('nth' + postfix)
        if content == 'even':
            s1 = 2
            s2 = 2
            var = True
        elif content == 'odd':
            s1 = 2
            s2 = 1
            var = True
        else:
            nth_parts = RE_NTH.match(content)
            s1 = '-' if nth_parts.group('s1') and nth_parts.group('s1') == '-' else ''
            a = nth_parts.group('a')
            var = a.endswith('n')
            if a.startswith('n'):
                s1 += '1'
            elif var:
                s1 += a[:-1]
            else:
                s1 += a
            s2 = '-' if nth_parts.group('s2') and nth_parts.group('s2') == '-' else ''
            if nth_parts.group('b'):
                s2 += nth_parts.group('b')
            else:
                s2 = '0'
            s1 = int(s1, 16)
            s2 = int(s2, 16)

        pseudo_sel = util.lower(m.group('pseudo_nth' + postfix))
        if postfix == '_child':
            if pseudo_sel.strip().endswith('of'):
                # Parse the rest of `of S`.
                temp_sel = iselector
            else:
                # Use default `*|*` for `of S`. Simulate un-closed pseudo.
                temp_sel = self.selector_iter('*|*)')
            nth_sel = self.parse_selectors(
                temp_sel,
                True,
                False,
                False
            )
            if pseudo_sel.startswith(':nth-child'):
                sel.nth.append(ct.SelectorNth(s1, var, s2, False, False, nth_sel))
            elif pseudo_sel.startswith(':nth-last-child'):
                sel.nth.append(ct.SelectorNth(s1, var, s2, False, True, nth_sel))
        else:
            if pseudo_sel.startswith(':nth-of-type'):
                sel.nth.append(ct.SelectorNth(s1, var, s2, True, False, ct.SelectorList()))
            elif pseudo_sel.startswith(':nth-last-of-type'):
                sel.nth.append(ct.SelectorNth(s1, var, s2, True, True, ct.SelectorList()))
        has_selector = True
        return has_selector

    def parse_pseudo_open(self, sel, m, has_selector, iselector, is_pseudo):
        """Parse pseudo with opening bracket."""

        name = util.lower(m.group(0)[1:-1])
        sel.selectors.append(
            self.parse_selectors(
                iselector,
                True,
                name == 'not',
                name == 'has'
            )
        )
        has_selector = True
        return has_selector

    def parse_has_split(self, sel, m, has_selector, selectors, is_pseudo, rel_type):
        """Parse splitting tokens."""

        if m.group('relation') == SPLIT:
            if not has_selector:
                raise SyntaxError("Cannot start or end selector with '{}'".format(m.group('relation')))
            sel.rel_type = rel_type
            selectors[-1].relations.append(sel)
            rel_type = REL_HAS_CHILD
            selectors.append(_Selector())
        else:
            if has_selector:
                sel.rel_type = rel_type
                selectors[-1].relations.append(sel)
            rel_type = ':' + m.group('relation')
        sel = _Selector()

        has_selector = False
        return has_selector, sel, rel_type

    def parse_split(self, sel, m, has_selector, selectors, relations, is_pseudo):
        """Parse splitting tokens."""

        if not has_selector:
            raise SyntaxError("Cannot start or end selector with '{}'".format(m.group('relation')))
        if m.group('relation') == SPLIT:
            if not sel.tag and not is_pseudo:
                # Implied `*`
                sel.tag = ct.SelectorTag('*', None)
            sel.relations.extend(relations)
            selectors.append(sel)
            relations.clear()
        else:
            sel.relations.extend(relations)
            rel_type = m.group('relation').strip()
            if not rel_type:
                rel_type = ' '
            sel.rel_type = rel_type
            relations.clear()
            relations.append(sel)
        sel = _Selector()

        has_selector = False
        return has_selector, sel

    def parse_class_id(self, sel, m, has_selector):
        """Parse HTML classes and ids."""

        selector = m.group(0)
        if selector.startswith('.'):
            sel.classes.append(css_unescape(selector[1:]))
            has_selector = True
        else:
            sel.ids.append(css_unescape(selector[1:]))
            has_selector = True
        return has_selector

    def parse_contains(self, sel, m, has_selector):
        """Parse contains."""

        content = css_unescape(m.group('value').strip())
        if content.startswith(("'", '"')):
            content = content[1:-1]
        sel.contains.append(content)
        has_selector = True
        return has_selector

    def parse_selectors(self, iselector, is_pseudo=False, is_not=False, is_has=False):
        """Parse selectors."""

        sel = _Selector()
        selectors = []
        has_selector = False
        closed = False
        relations = []
        rel_type = REL_HAS_CHILD
        split_last = False
        if is_has:
            selectors.append(_Selector())

        try:
            while True:
                key, m = next(iselector)

                # Handle parts
                if key == 'pseudo_invalid':
                    if util.lower(m.group(0)) in SUPPORTED_PSEUDO:
                        raise SyntaxError("Invalid syntax for pseudo class '{}'".format(key))
                    else:
                        raise NotImplementedError(
                            "'{}' pseudo class/element is not implemented at this time".format(key)
                        )
                elif key == 'pseudo':
                    has_selector = self.parse_pseudo(sel, m, has_selector)
                elif key == 'pseudo_contains':
                    has_selector = self.parse_contains(sel, m, has_selector)
                elif key in ('pseudo_nth_type', 'pseudo_nth_child'):
                    has_selector = self.parse_pseudo_nth(sel, m, has_selector, iselector)
                elif key == 'pseudo_open':
                    has_selector = self.parse_pseudo_open(sel, m, has_selector, iselector, is_pseudo)
                elif key == 'pseudo_close':
                    if split_last:
                        raise SyntaxError("Cannot end with a combining character")
                    if is_pseudo:
                        closed = True
                        break
                    else:
                        raise SyntaxError("Unmatched '{}'".format(m.group(0)))
                elif key == 'combine':
                    if split_last:
                        raise SyntaxError("Cannot have combining character directly after a combining character")
                    if is_has:
                        has_selector, sel, rel_type = self.parse_has_split(
                            sel, m, has_selector, selectors, is_pseudo, rel_type
                        )
                    else:
                        has_selector, sel = self.parse_split(sel, m, has_selector, selectors, relations, is_pseudo)
                    split_last = True
                    continue
                elif key == 'attribute':
                    has_selector = self.parse_attribute_selector(sel, m, has_selector)
                elif key == 'tag':
                    if has_selector:
                        raise SyntaxError("Tag must come first")
                    has_selector = self.parse_tag_pattern(sel, m, has_selector)
                elif key in ('class', 'id'):
                    has_selector = self.parse_class_id(sel, m, has_selector)
                split_last = False
        except StopIteration:
            pass

        if is_pseudo and not closed:
            raise SyntaxError("Unclosed `:pseudo()`")

        if split_last:
            raise SyntaxError("Cannot end with a combining character")

        if has_selector:
            if not sel.tag and not is_pseudo:
                # Implied `*`
                sel.tag = ct.SelectorTag('*', None)
            if is_has:
                sel.rel_type = rel_type
                selectors[-1].relations.append(sel)
            else:
                sel.relations.extend(relations)
                relations.clear()
                selectors.append(sel)
        elif is_has:
            # We will always need to finish a selector when `:has()` is used as it leads with combining.
            raise SyntaxError('Missing selectors after combining type.')

        return ct.SelectorList([s.freeze() for s in selectors], is_not)

    def selector_iter(self, pattern):
        """Iterate selector tokens."""

        index = 0
        end = len(pattern) - 1
        while index <= end:
            m = None
            for k, v in self.css_tokens.items():
                if not v.enabled(self.flags):  # pragma: no cover
                    continue
                m = v.pattern.match(pattern, index)
                if m:
                    index = m.end(0)
                    yield k, m
                    break
            if m is None:
                raise SyntaxError("Invlaid character '{}'".format(pattern[index]))

    def process_selectors(self):
        """
        Process selectors.

        We do our own selectors as BeautifulSoup4 has some annoying quirks,
        and we don't really need to do nth selectors or siblings or
        descendants etc.
        """

        return self.parse_selectors(self.selector_iter(self.pattern))

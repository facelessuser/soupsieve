"""CSS selector parser."""
import re
import copyreg
from collections import namedtuple
from functools import lru_cache
from . import util
from . import css_match as cm


# Selector patterns
CSS_ESCAPES = r'(?:\\[a-fA-F0-9]{1,6}[ ]?|\\.)'
NTH = r'(?:[-+])?(?:\d+n?|n)(?:(?<=n)\s*(?:[-+])\s*(?:\d+))?'
HTML_SELECTORS = r"""
(?P<class_id>(?:\#|\.)(?:[-\w]|{esc})+) |                            #.class and #id
(?P<ns_tag>(?:(?:(?:[-\w]|{esc})+|\*)?\|)?(?:(?:[-\w]|{esc})+|\*)) | # namespace:tag
\[(?P<ns_attr>(?:(?:(?:[-\w]|{esc})+|\*)?\|)?(?:[-\w]|{esc})+)
""".format(esc=CSS_ESCAPES)
XML_SELECTORS = r"""
(?P<ns_tag>(?:(?:(?:[-\w.]|{esc})+|\*)?\|)?(?:(?:[-\w.]|{esc})+|\*)) | # namespace:tag
\[(?P<ns_attr>(?:(?:(?:[-\w]|{esc})+|\*)\|)?(?:[-\w.]|{esc})+)         # namespace:attributes
""".format(esc=CSS_ESCAPES)
SELECTORS = r'''(?x)
    (?P<pseudo_open>:(?:has|is|matches|not|where)\() |                            # optinal pseudo selector wrapper
    (?P<pseudo>:(?:empty|root|(?:first|last|only)-(?:child|of-type))) |           # Simple pseudo selector
    (?P<pseudo_nth_child>:nth-(?:last-)?child
        \(\s*(?P<nth_child>{nth}|even|odd)\s*(?:\)|(?<=\s)of\s+)) |               # Pseudo `nth-child` selectors
    (?P<pseudo_nth_type>:nth-(?:last-)?of-type
        \(\s*(?P<nth_type>{nth}|even|odd)\s*\)) |                                 # Pseudo `nth-of-type` selectors
    {doc_specific}
    (?:(?P<cmp>[~^|*$]?=)                                                         # compare
    (?P<value>"(\\.|[^\\"]+)*?"|'(\\.|[^\\']+)*?'|(?:[^'"\[\] \t\r\n]|{esc})+))?  # attribute value
    (?P<i>[ ]+i)? \] |                                                            # case insensitive
    (?P<pseudo_close>\)) |                                                        # optional pseudo selector close
    (?P<split>\s*?(?P<relation>[,+>~]|[ ](?![,+>~]))\s*) |                        # split multiple selectors
    (?P<invalid>).+                                                               # not proper syntax
'''
RE_HTML_SEL = re.compile(SELECTORS.format(esc=CSS_ESCAPES, nth=NTH, doc_specific=HTML_SELECTORS))
RE_XML_SEL = re.compile(SELECTORS.format(esc=CSS_ESCAPES, nth=NTH, doc_specific=XML_SELECTORS))

# CSS escape pattern
RE_CSS_ESC = re.compile(r'(?:(\\[a-fA-F0-9]{1,6}[ ]?)|(\\.))')

# Pattern to break up `nth` specifiers
RE_NTH = re.compile(r'(?P<s1>[-+])?(?P<a>\d+n?|n)(?:(?<=n)\s*(?P<s2>[-+])\s*(?P<b>\d+))?')

SPLIT = ','
HAS_CHILD = ": "

_MAXCACHE = 256


@lru_cache(maxsize=_MAXCACHE)
def _cached_css_compile(pattern, namespaces, mode):
    """Cached CSS compile."""

    return CSSPattern(
        pattern,
        namespaces,
        mode
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


class _Selector:
    """Intermediate selector."""

    def __init__(self, **kwargs):
        """Initialize."""

        self.tags = kwargs.get('tags', [])
        self.ids = kwargs.get('ids', [])
        self.classes = kwargs.get('classes', [])
        self.attributes = kwargs.get('attributes', [])
        self.nth = kwargs.get('nth', [])
        self.selectors = kwargs.get('selectors', [])
        self.is_not = kwargs.get('is_not', False)
        self.is_empty = kwargs.get('is_empty', False)
        self.relation = kwargs.get('relation', None)
        self.rel_type = kwargs.get('rel_type', None)
        self.is_root = kwargs.get('is_root', False)

    def set_distant_relation(self, value):
        """Set the furthest relation down the chain."""

        if self.relation:
            temp = self.relation
            while temp and temp.relation:
                temp = temp.relation
            temp.relation = value
        else:
            self.relation = value

    def _freeze_list(self, chain):
        """Create an immutable selector chain."""

        for index, item in enumerate(chain):
            if isinstance(item, list):
                chain[index] = self._freeze_list(item)
            elif isinstance(item, _Selector):
                chain[index] = item.freeze()
        return tuple(chain)

    def freeze(self):
        """Freeze self."""

        return Selector(
            self._freeze_list(self.tags),
            self._freeze_list(self.ids),
            self._freeze_list(self.classes),
            self._freeze_list(self.attributes),
            self._freeze_list(self.nth),
            self._freeze_list(self.selectors),
            self.is_not,
            self.is_empty,
            self.relation.freeze() if self.relation is not None else None,
            self.rel_type,
            self.is_root
        )

    def __str__(self):
        """String representation."""

        return (
            '_Selector(tags=%r, ids=%r, classes=%r, attributes=%r, nth=%r, selectors=%r, '
            'is_not=%r, relation=%r, rel_type=%r, is_root=%r)'
        ) % (
            self.tags, self.ids, self.classes, self.attributes, self.nth, self.selectors,
            self.is_not, self.relation, self.rel_type, self.is_root
        )

    __repr__ = __str__


class Selector(
    namedtuple(
        'Selector',
        [
            'tags', 'ids', 'classes', 'attributes', 'nth', 'selectors',
            'is_not', 'is_empty', 'relation', 'rel_type', 'is_root'
        ]
    )
):
    """Selector."""


class SelectorTag(namedtuple('SelectorTag', ['name', 'prefix'])):
    """Selector tag."""


class SelectorAttribute(namedtuple('AttrRule', ['attribute', 'prefix', 'pattern'])):
    """Selector attribute rule."""


class SelectorNth(namedtuple('SelectorNth', ['a', 'n', 'b', 'type', 'last', 'selectors'])):
    """Selector nth type."""


class CSSParser:
    """Parse CSS selectors."""

    def __init__(self, selector, mode=0):
        """Initialize."""

        self.pattern = selector

        if mode == 0:
            mode = util.HTML

        if mode in (util.HTML, util.HTML5, util.XML, util.XHTML):
            self.mode = mode
        else:
            raise ValueError("Invalid SelectorMatcher flag(s) '{}'".format(mode))
        self.re_sel = RE_HTML_SEL if self.mode != util.XML else RE_XML_SEL

    def parse_attribute_selector(self, sel, m, has_selector):
        """Create attribute selector from the returned regex match."""

        flags = re.I if m.group('i') else 0
        parts = [css_unescape(a.strip()) for a in m.group('ns_attr').split('|')]
        ns = ''
        if len(parts) > 1:
            ns = parts[0]
            attr = parts[1]
        else:
            attr = parts[0]
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
        has_selector = True
        sel.attributes.append(SelectorAttribute(attr, ns, pattern))
        return has_selector

    def parse_tag_pattern(self, sel, m, has_selector):
        """Parse tag pattern from regex match."""

        parts = [css_unescape(x) for x in m.group('ns_tag').split('|')]
        if len(parts) > 1:
            prefix = parts[0]
            tag = parts[1]
        else:
            tag = parts[0]
            prefix = None
        sel.tags.append(SelectorTag(tag, prefix))
        has_selector = True
        return has_selector

    def parse_pseudo(self, sel, m, has_selector):
        """Parse pseudo."""

        pseudo = m.group('pseudo')[1:]
        if pseudo == 'root':
            sel.is_root = True
            has_selector = True
        elif pseudo == 'empty':
            sel.is_empty = True
        elif pseudo == 'first-child':
            sel.nth.append(SelectorNth(1, False, 0, False, False, tuple()))
        elif pseudo == 'last-child':
            sel.nth.append(SelectorNth(1, False, 0, False, True, tuple()))
        elif pseudo == 'first-of-type':
            sel.nth.append(SelectorNth(1, False, 0, True, False, tuple()))
        elif pseudo == 'last-of-type':
            sel.nth.append(SelectorNth(1, False, 0, True, True, tuple()))
        elif pseudo == 'only-child':
            sel.nth.extend(
                [
                    SelectorNth(1, False, 0, False, False, tuple()),
                    SelectorNth(1, False, 0, False, True, tuple())
                ]
            )
        elif pseudo == 'only-of-type':
            sel.nth.extend(
                [
                    SelectorNth(1, False, 0, True, False, tuple()),
                    SelectorNth(1, False, 0, True, True, tuple())
                ]
            )

        return has_selector

    def parse_pseudo_nth(self, sel, m, has_selector, iselector):
        """Parse `nth` pseudo."""

        postfix = '_child' if m.group('pseudo_nth_child') else '_type'
        content = m.group('nth' + postfix)
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

        if postfix == '_child':
            if m.group('pseudo_nth' + postfix).strip().endswith('of'):
                # Parse the rest of `of S`.
                temp_sel = iselector
            else:
                # Use default `*|*` for `of S`. Simulate un-closed pseudo.
                temp_sel = self.re_sel.finditer('*|*)')
            nth_sel = tuple(
                self.parse_selectors(
                    temp_sel,
                    True,
                    False,
                    False
                )
            )
            if m.group('pseudo_nth' + postfix).startswith(':nth-child'):
                sel.nth.append(SelectorNth(s1, var, s2, False, False, nth_sel))
            elif m.group('pseudo_nth' + postfix).startswith(':nth-last-child'):
                sel.nth.append(SelectorNth(s1, var, s2, False, True, nth_sel))
        else:
            if m.group('pseudo_nth' + postfix).startswith(':nth-of-type'):
                sel.nth.append(SelectorNth(s1, var, s2, True, False, tuple()))
            elif m.group('pseudo_nth' + postfix).startswith(':nth-last-of-type'):
                sel.nth.append(SelectorNth(s1, var, s2, True, True, tuple()))
        has_selector = True
        return has_selector

    def parse_pseudo_open(self, sel, m, has_selector, iselector, is_pseudo):
        """Parse pseudo with opening bracket."""

        sel.selectors.extend(
            self.parse_selectors(
                iselector,
                True,
                m.group('pseudo_open')[1:-1] == 'not',
                m.group('pseudo_open')[1:-1] == 'has'
            )
        )
        has_selector = True
        return has_selector

    def parse_has_split(self, sel, m, has_selector, selectors, is_pseudo, rel_type):
        """Parse splitting tokens."""

        if m.group('relation') == SPLIT:
            if not has_selector:
                raise ValueError("Cannot start or end selector with '{}'".format(m.group('relation')))
            sel.rel_type = rel_type
            selectors[-1].set_distant_relation(sel)
            rel_type = HAS_CHILD
            selectors.append(_Selector())
        else:
            if has_selector:
                sel.rel_type = rel_type
                selectors[-1].set_distant_relation(sel)
            rel_type = ':' + m.group('relation')
        sel = _Selector()

        has_selector = False
        return has_selector, sel, rel_type

    def parse_split(self, sel, m, has_selector, selectors, relations, is_pseudo):
        """Parse splitting tokens."""

        if not has_selector:
            raise ValueError("Cannot start or end selector with '{}'".format(m.group('relation')))
        is_not = sel.is_not
        if m.group('relation') == SPLIT:
            if not sel.tags and not is_pseudo:
                # Implied `*`
                sel.tags.append(SelectorTag('*', None))
            sel.relation = relations[0] if relations else None
            selectors.append(sel)
            relations.clear()
        else:
            # In this particular case, we are attaching a relation to an element of interest.
            # the `:not()` applies to the element of interest, not the ancestors. `:not()` is really only
            # applied at the sub-selector level `_Selector(is_not=False, selector=[_Selector(is_not=True)])`
            # We want to see if the element has the proper ancestry, and then apply the `:not()`.
            # In the case of `:not(el1) > el2`, where the ancestor is evaluated with a not, you'd actually get:
            # ```
            # _Selector(
            #     tags=['el2'],
            #     relations=[
            #         [
            #             _Selector(
            #                 tags=['*'],
            #                 selectors=[
            #                     _Selector(
            #                         tags=['el1'],
            #                         is_not=True
            #                     )
            #                 ]
            #             )
            #         ]
            #     ],
            #     rel_type='>'
            # )
            # ```
            sel.relation = relations[0] if relations else None
            sel.rel_type = m.group('relation')
            sel.is_not = False
            relations.clear()
            relations.append(sel)
        sel = _Selector(is_not=is_not)

        has_selector = False
        return has_selector, sel

    def parse_classes(self, sel, m, has_selector):
        """Parse classes."""

        selector = m.group('class_id')
        if selector.startswith('.'):
            sel.classes.append(css_unescape(selector[1:]))
            has_selector = True
        else:
            sel.ids.append(css_unescape(selector[1:]))
            has_selector = True
        return has_selector

    def parse_selectors(self, iselector, is_pseudo=False, is_not=False, is_has=False):
        """Parse selectors."""

        sel = _Selector(is_not=is_not)
        selectors = []
        has_selector = False
        closed = False
        is_html = self.mode != util.XML
        relations = []
        rel_type = HAS_CHILD
        split_last = False
        if is_has:
            selectors.append(_Selector())

        try:
            while True:
                m = next(iselector)

                # Handle parts
                if m.group('pseudo'):
                    has_selector = self.parse_pseudo(sel, m, has_selector)
                elif m.group('pseudo_nth_type') or m.group('pseudo_nth_child'):
                    has_selector = self.parse_pseudo_nth(sel, m, has_selector, iselector)
                elif m.group('pseudo_open'):
                    has_selector = self.parse_pseudo_open(sel, m, has_selector, iselector, is_pseudo)
                elif m.group('pseudo_close'):
                    if split_last:
                        raise ValueError("Cannot end with a combining character")
                    if is_pseudo:
                        closed = True
                        break
                    else:
                        raise ValueError("Bad selector '{}'".format(m.group(0)))
                elif m.group('split'):
                    if split_last:
                        raise ValueError("Cannot have combining character after a combining character")
                    if is_has:
                        has_selector, sel, rel_type = self.parse_has_split(
                            sel, m, has_selector, selectors, is_pseudo, rel_type
                        )
                    else:
                        has_selector, sel = self.parse_split(sel, m, has_selector, selectors, relations, is_pseudo)
                    split_last = True
                    continue
                elif m.group('ns_attr'):
                    has_selector = self.parse_attribute_selector(sel, m, has_selector)
                elif m.group('ns_tag'):
                    if has_selector:
                        raise ValueError("Tag must come first")
                    has_selector = self.parse_tag_pattern(sel, m, has_selector)
                elif is_html and m.group('class_id'):
                    has_selector = self.parse_classes(sel, m, has_selector)
                elif m.group('invalid'):
                    raise ValueError("Bad selector '{}'".format(m.group(0)))
                split_last = False
        except StopIteration:
            pass

        if is_pseudo and not closed:
            raise ValueError("Unclosed `:pseudo()`")

        if split_last:
            raise ValueError("Cannot end with a combining character")

        if has_selector:
            if not sel.tags and not is_pseudo:
                # Implied `*`
                sel.tags.append(SelectorTag('*', None))
            if is_has:
                sel.rel_type = rel_type
                selectors[-1].set_distant_relation(sel)
            else:
                sel.relation = relations[0] if relations else None
                relations.clear()
                selectors.append(sel)
        elif is_has:
            # We will always need to finish a selector when `:has()` is used as it leads with combining.
            raise ValueError('Missing selectors after combining type.')

        return selectors

    def process_selectors(self):
        """
        Process selectors.

        We do our own selectors as BeautifulSoup4 has some annoying quirks,
        and we don't really need to do nth selectors or siblings or
        descendants etc.
        """

        return tuple([s.freeze() for s in self.parse_selectors(self.re_sel.finditer(self.pattern))])


class CSSPattern(util.Immutable):
    """Match tags in Beautiful Soup with CSS selectors."""

    __slots__ = ("pattern", "selectors", "namespaces", "mode", "_hash")

    def __init__(self, selectors, namespaces, mode):
        """Initialize."""

        super().__init__(
            pattern=selectors,
            selectors=CSSParser(selectors, mode).process_selectors(),
            namespaces=namespaces,
            mode=mode
        )

    def match(self, el):
        """Match selector."""

        return cm.CSSMatch(self.selectors, self.namespaces, self.mode).match(el)


def _pickle(p):
    return CSSPattern, (p.pattern, p.namespaces, p.mode)


copyreg.pickle(CSSPattern, _pickle)

"""CSS selector structure items."""
from . import util
import copyreg

__all__ = ('Selector', 'SelectorTag', 'SelectorAttribute', 'SelectorNth', 'SelectorList', 'Namespaces')


class Namespaces(util.ImmutableDict):
    """Namespaces."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        # If there are arguments, check the first index.
        # `super` should fail if the user gave multiple arguments,
        # so don't bother checking that.
        arg = args[0] if args else kwargs
        is_dict = isinstance(arg, dict)
        if is_dict and not all([isinstance(k, str) and isinstance(v, str) for k, v in arg.items()]):
            raise TypeError('Namespace keys and values must be Unicode strings')
        elif not is_dict and not all([isinstance(k, str) and isinstance(v, str) for k, v in arg]):
            raise TypeError('Namespace keys and values must be Unicode strings')

        super().__init__(*args, **kwargs)


class Selector(util.Immutable):
    """Selector."""

    __slots__ = (
        'tag', 'ids', 'classes', 'attributes', 'nth', 'selectors',
        'relation', 'rel_type', 'contains', 'lang', 'empty', 'root', 'default', 'indeterminate',
        'no_match',
        '_hash'
    )

    def __init__(
        self, tag, ids, classes, attributes, nth, selectors,
        relation, rel_type, contains, lang, empty, root, default, indeterminate,
        no_match
    ):
        """Initialize."""

        super().__init__(
            tag=tag,
            ids=ids,
            classes=classes,
            attributes=attributes,
            nth=nth,
            selectors=selectors,
            relation=relation,
            rel_type=rel_type,
            contains=contains,
            lang=lang,
            empty=empty,
            root=root,
            default=default,
            indeterminate=indeterminate,
            no_match=no_match
        )


class SelectorTag(util.Immutable):
    """Selector tag."""

    __slots__ = ("name", "prefix", "_hash")

    def __init__(self, name, prefix):
        """Initialize."""

        super().__init__(
            name=name,
            prefix=prefix
        )


class SelectorAttribute(util.Immutable):
    """Selector attribute rule."""

    __slots__ = ("attribute", "prefix", "pattern", "xml_type_pattern", "_hash")

    def __init__(self, attribute, prefix, pattern, xml_type_pattern):
        """Initialize."""

        super().__init__(
            attribute=attribute,
            prefix=prefix,
            pattern=pattern,
            xml_type_pattern=xml_type_pattern
        )


class SelectorNth(util.Immutable):
    """Selector nth type."""

    __slots__ = ("a", "n", "b", "of_type", "last", "selectors", "_hash")

    def __init__(self, a, n, b, of_type, last, selectors):
        """Initialize."""

        super().__init__(
            a=a,
            n=n,
            b=b,
            of_type=of_type,
            last=last,
            selectors=selectors
        )


class SelectorLang(util.Immutable):
    """Selector language rules."""

    __slots__ = ("languages", "_hash",)

    def __init__(self, languages):
        """Initialize."""

        super().__init__(
            languages=tuple(languages)
        )

    def __iter__(self):
        """Iterator."""

        return iter(self.languages)

    def __len__(self):  # pragma: no cover
        """Length."""

        return len(self.languages)

    def __getitem__(self, index):  # pragma: no cover
        """Get item."""

        return self.languages[index]


class SelectorList(util.Immutable):
    """Selector list."""

    __slots__ = ("selectors", "is_not", "is_html", "_hash")

    def __init__(self, selectors=tuple(), is_not=False, is_html=False):
        """Initialize."""

        super().__init__(
            selectors=tuple(selectors),
            is_not=is_not,
            is_html=is_html
        )

    def __iter__(self):
        """Iterator."""

        return iter(self.selectors)

    def __len__(self):
        """Length."""

        return len(self.selectors)

    def __getitem__(self, index):
        """Get item."""

        return self.selectors[index]


def _pickle(p):
    return p.__base__(), tuple([getattr(p, s) for s in p.__slots__[:-1]])


copyreg.pickle(Selector, _pickle)
copyreg.pickle(SelectorTag, _pickle)
copyreg.pickle(SelectorAttribute, _pickle)
copyreg.pickle(SelectorNth, _pickle)
copyreg.pickle(SelectorList, _pickle)
copyreg.pickle(SelectorLang, _pickle)

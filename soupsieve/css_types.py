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
        'relation', 'rel_type', 'contains', 'empty', 'root', '_hash'
    )

    def __init__(self, tag, ids, classes, attributes, nth, selectors, relation, rel_type, contains, empty, root):
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
            empty=empty,
            root=root
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

    __slots__ = ("attribute", "prefix", "pattern", "_hash")

    def __init__(self, attribute, prefix, pattern):
        """Initialize."""

        super().__init__(
            attribute=attribute,
            prefix=prefix,
            pattern=pattern
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


class SelectorList(util.Immutable):
    """Selector list."""

    __slots__ = ("_selectors", "is_not", "_hash")

    def __init__(self, selectors=tuple(), is_not=False):
        """Initialize."""

        super().__init__(
            _selectors=tuple(selectors),
            is_not=is_not
        )

    def __iter__(self):
        """Iterator."""

        return iter(self._selectors)

    def __len__(self):
        """Length."""

        return len(self._selectors)

    def __getitem__(self, index):
        """Get item."""

        return self._selectors[index]


def _pickle(p):
    return p.__base__(), tuple([getattr(p, s) for s in p.__slots__[:-1]])


copyreg.pickle(Selector, _pickle)
copyreg.pickle(SelectorTag, _pickle)
copyreg.pickle(SelectorAttribute, _pickle)
copyreg.pickle(SelectorNth, _pickle)
copyreg.pickle(SelectorList, _pickle)

"""CSS selector structure items."""
from __future__ import annotations
from enum import Enum
import copyreg
from .pretty import pretty
from typing import Any, Iterator, Pattern, Iterable, Mapping, TypeVar, overload

__all__ = (
    'Selector',
    'SelectorNull',
    'SelectorTag',
    'SelectorAttribute',
    'SelectorContains',
    'SelectorNth',
    'SelectorLang',
    'SelectorList',
    'Namespaces',
    'CustomSelectors'
)


SEL_EMPTY = 0x1
SEL_ROOT = 0x2
SEL_DEFAULT = 0x4
SEL_INDETERMINATE = 0x8
SEL_SCOPE = 0x10
SEL_DIR_LTR = 0x20
SEL_DIR_RTL = 0x40
SEL_IN_RANGE = 0x80
SEL_OUT_OF_RANGE = 0x100
SEL_DEFINED = 0x200
SEL_PLACEHOLDER_SHOWN = 0x400


class Immutable:
    """Immutable."""

    __slots__: tuple[str, ...] = ('_hash',)

    _hash: int

    def __init__(self, **kwargs: Any) -> None:
        """Initialize."""

        temp = []
        for k, v in kwargs.items():
            temp.append(type(v))
            temp.append(v)
            super().__setattr__(k, v)
        super().__setattr__('_hash', hash(tuple(temp)))

    @classmethod
    def __base__(cls) -> type[Immutable]:
        """Get base class."""

        return cls

    def __eq__(self, other: Any) -> bool:
        """Equal."""

        return (
            isinstance(other, self.__base__()) and
            all(getattr(other, key) == getattr(self, key) for key in self.__slots__ if key != '_hash')
        )

    def __ne__(self, other: Any) -> bool:
        """Equal."""

        return (
            not isinstance(other, self.__base__()) or
            any(getattr(other, key) != getattr(self, key) for key in self.__slots__ if key != '_hash')
        )

    def __hash__(self) -> int:
        """Hash."""

        return self._hash

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent mutability."""

        raise AttributeError(f"'{self.__class__.__name__}' is immutable")

    def __repr__(self) -> str:  # pragma: no cover
        """Representation."""

        r = ', '.join([f"{k}={getattr(self, k)!r}" for k in self.__slots__[:-1]])
        return f"{self.__class__.__name__}({r})"

    __str__ = __repr__

    def pretty(self) -> None:  # pragma: no cover
        """Pretty print."""

        print(pretty(self))


class Selector(Immutable):
    """Selector."""

    __slots__ = (
        'tag', 'ids', 'classes', 'attributes', 'nth', 'selectors',
        'relation', 'rel_type', 'contains', 'lang', 'flags', '_hash'
    )

    tag: SelectorTag | None
    ids: tuple[str, ...]
    classes: tuple[str, ...]
    attributes: tuple[SelectorAttribute, ...]
    nth: tuple[SelectorNth, ...]
    selectors: tuple[SelectorList, ...]
    relation: SelectorList
    rel_type: str | None
    contains: tuple[SelectorContains, ...]
    lang: tuple[SelectorLang, ...]
    flags: int

    def __init__(
        self,
        tag: SelectorTag | None,
        ids: tuple[str, ...],
        classes: tuple[str, ...],
        attributes: tuple[SelectorAttribute, ...],
        nth: tuple[SelectorNth, ...],
        selectors: tuple[SelectorList, ...],
        relation: SelectorList,
        rel_type: str | None,
        contains: tuple[SelectorContains, ...],
        lang: tuple[SelectorLang, ...],
        flags: int
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
            flags=flags
        )


class SelectorNull(Enum):
    """Null Selector."""

    null = 0


Null = SelectorNull.null


class SelectorTag(Immutable):
    """Selector tag."""

    __slots__ = ("name", "prefix", "_hash")

    name: str
    prefix: str | None

    def __init__(self, name: str, prefix: str | None) -> None:
        """Initialize."""

        super().__init__(name=name, prefix=prefix)


class SelectorAttribute(Immutable):
    """Selector attribute rule."""

    __slots__ = ("attribute", "prefix", "pattern", "xml_type_pattern", "_hash")

    attribute: str
    prefix: str
    pattern: Pattern[str] | None
    xml_type_pattern: Pattern[str] | None

    def __init__(
        self,
        attribute: str,
        prefix: str,
        pattern: Pattern[str] | None,
        xml_type_pattern: Pattern[str] | None
    ) -> None:
        """Initialize."""

        super().__init__(
            attribute=attribute,
            prefix=prefix,
            pattern=pattern,
            xml_type_pattern=xml_type_pattern
        )


class SelectorContains(Immutable):
    """Selector contains rule."""

    __slots__ = ("text", "own", "_hash")

    text: tuple[str, ...]
    own: bool

    def __init__(self, text: Iterable[str], own: bool) -> None:
        """Initialize."""

        super().__init__(text=tuple(text), own=own)


class SelectorNth(Immutable):
    """Selector nth type."""

    __slots__ = ("a", "n", "b", "of_type", "last", "selectors", "_hash")

    a: int
    n: bool
    b: int
    of_type: bool
    last: bool
    selectors: SelectorList

    def __init__(self, a: int, n: bool, b: int, of_type: bool, last: bool, selectors: SelectorList) -> None:
        """Initialize."""

        super().__init__(
            a=a,
            n=n,
            b=b,
            of_type=of_type,
            last=last,
            selectors=selectors
        )


class SelectorLang(Immutable):
    """Selector language rules."""

    __slots__ = ("languages", "_hash",)

    languages: tuple[str, ...]

    def __init__(self, languages: Iterable[str]):
        """Initialize."""

        super().__init__(languages=tuple(languages))

    def __iter__(self) -> Iterator[str]:
        """Iterator."""

        return iter(self.languages)

    def __len__(self) -> int:  # pragma: no cover
        """Length."""

        return len(self.languages)

    def __getitem__(self, index: int) -> str:  # pragma: no cover
        """Get item."""

        return self.languages[index]


class SelectorList(Immutable):
    """Selector list."""

    __slots__ = ("selectors", "is_not", "is_html", "count", "_hash")

    selectors: tuple[Selector | SelectorNull, ...]
    is_not: bool
    is_html: bool
    count: int

    def __init__(
        self,
        selectors: Iterable[Selector | SelectorNull] | None = None,
        is_not: bool = False,
        is_html: bool = False,
        count: int = 0,
    ) -> None:
        """Initialize."""

        super().__init__(
            selectors=tuple(selectors) if selectors is not None else (),
            is_not=is_not,
            is_html=is_html,
            count=count
        )

    def __iter__(self) -> Iterator[Selector | SelectorNull]:
        """Iterator."""

        return iter(self.selectors)

    def __len__(self) -> int:
        """Length."""

        return len(self.selectors)

    def __getitem__(self, index: int) -> Selector | SelectorNull:
        """Get item."""

        return self.selectors[index]


KT = TypeVar('KT')
VT = TypeVar('VT')
RT = TypeVar('RT')


class ImmutableDict(Mapping[KT, VT]):
    """Hashable, immutable dictionary."""

    def __init__(
        self,
        arg: Mapping[KT, VT]
    ) -> None:
        """Initialize."""

        self._d = dict(arg)
        self._hash = hash(tuple([(type(x), x, type(y), y) for x, y in sorted(self._d.items())]))

    @overload
    def get(self, key: KT, /) -> VT | None:
        ...

    @overload
    def get(self, key: KT, /, default: VT) -> VT:
        ...

    @overload
    def get(self, key: KT, /, default: RT) -> VT | RT:
        ...

    def get(self, key: KT, /, default: RT | VT | None = None) -> VT | RT | None:
        """Get value."""

        return self._d.get(key, default)

    def __iter__(self) -> Iterator[KT]:
        """Iterator."""

        return iter(self._d)

    def __len__(self) -> int:
        """Length."""

        return len(self._d)

    def __getitem__(self, key: KT) -> VT:
        """Get item: `namespace['key']`."""

        return self._d[key]

    def __hash__(self) -> int:
        """Hash."""

        return self._hash

    def __repr__(self) -> str:  # pragma: no cover
        """Representation."""

        return f"{self._d!r}"

    __str__ = __repr__


class Namespaces(ImmutableDict[str, str]):
    """Namespaces."""

    def __init__(self, arg: Mapping[str, str]) -> None:
        """Initialize."""

        self._validate(arg)
        super().__init__(arg)

    def _validate(self, arg: Mapping[str, str]) -> None:
        """Validate arguments."""

        if not all(isinstance(k, str) and isinstance(v, str) for k, v in arg.items()):
            raise TypeError(f'{self.__class__.__name__} values must be hashable')


class CustomSelectors(ImmutableDict[str, str | SelectorList]):
    """Custom selectors."""

    def __init__(self, arg: Mapping[str, str | SelectorList]) -> None:
        """Initialize."""

        self._validate(arg)
        super().__init__(arg)

    def _validate(self, arg: Mapping[str, str | SelectorList]) -> None:
        """Validate arguments."""

        if not all(isinstance(k, str) and isinstance(v, str) for k, v in arg.items()):
            raise TypeError(f'{self.__class__.__name__} values must be hashable')


def _pickle(p: Immutable) -> Any:
    """
    Reduce an immutable object for pickling.

    Selectors can be nested very deeply, and pickling them object by object would
    recurse for each level. Instead, flatten the entire structure into a table of
    nodes, children before parents, where nested immutable objects are replaced by
    their index in the table. As the table only contains leaf values, neither
    pickling nor unpickling needs to recurse.

    Each node is `(class, args, refs)`. A ref is either the index of an argument that
    is an immutable object, or `(index, positions)` for an argument that is a tuple
    containing immutable objects at the given positions.
    """

    indexes: dict[int, int] = {}
    nodes: list[tuple[type[Immutable], tuple[Any, ...], tuple[Any, ...]]] = []
    stack: list[tuple[Immutable, list[Any] | None]] = [(p, None)]

    while stack:
        obj, values = stack.pop()
        if id(obj) in indexes:
            continue

        # Queue up children to be processed before the parent.
        if values is None:
            values = [getattr(obj, s) for s in obj.__slots__[:-1]]
            stack.append((obj, values))
            for value in values:
                if isinstance(value, Immutable):
                    stack.append((value, None))
                elif value.__class__ is tuple:
                    stack.extend((v, None) for v in value if isinstance(v, Immutable))
            continue

        # All children have been processed, replace them with their index.
        refs = []  # type: list[Any]
        for i, value in enumerate(values):
            if isinstance(value, Immutable):
                values[i] = indexes[id(value)]
                refs.append(i)
            elif value.__class__ is tuple:
                positions = [j for j, v in enumerate(value) if isinstance(v, Immutable)]
                if positions:
                    items = list(value)
                    for j in positions:
                        items[j] = indexes[id(items[j])]
                    values[i] = tuple(items)
                    refs.append((i, tuple(positions)))

        indexes[id(obj)] = len(nodes)
        nodes.append((obj.__base__(), tuple(values), tuple(refs)))

    return _unpickle, (tuple(nodes),)


def _unpickle(nodes: tuple[tuple[type[Immutable], tuple[Any, ...], tuple[Any, ...]], ...]) -> Immutable:
    """Rebuild an immutable object from the flattened node table created by `_pickle`."""

    objs: list[Immutable] = []
    for cls, args, refs in nodes:
        values = list(args)
        for ref in refs:
            if isinstance(ref, int):
                values[ref] = objs[values[ref]]
            else:
                i, positions = ref
                items = list(values[i])
                for j in positions:
                    items[j] = objs[items[j]]
                values[i] = tuple(items)
        objs.append(cls(*values))
    return objs[-1]


def pickle_register(obj: Any) -> None:
    """Allow object to be pickled."""

    copyreg.pickle(obj, _pickle)


pickle_register(Selector)
pickle_register(SelectorTag)
pickle_register(SelectorAttribute)
pickle_register(SelectorContains)
pickle_register(SelectorNth)
pickle_register(SelectorLang)
pickle_register(SelectorList)

"""Utility."""
from collections import Mapping
from collections.abc import Hashable
import bs4
from functools import wraps
import warnings

HTML5 = 0x1
HTML = 0x2
XHTML = 0x4
XML = 0x8

TAG = bs4.Tag
CHILD = (TAG, bs4.Doctype, bs4.Declaration, bs4.CData, bs4.ProcessingInstruction)
COMMENT = bs4.Comment

LC_A = ord('a')
LC_Z = ord('z')
UC_A = ord('A')
UC_Z = ord('Z')


def lower(string):
    """Lower."""

    new_string = []
    for c in string:
        o = ord(c)
        new_string.append(chr(o + 32) if UC_A <= o <= UC_Z else c)
    return ''.join(new_string)


def upper(string):  # pragma: no cover
    """Lower."""

    new_string = []
    for c in string:
        o = ord(c)
        new_string.append(chr(o - 32) if LC_A <= o <= LC_Z else c)
    return ''.join(new_string)


class Immutable:
    """Immutable."""

    __slots__ = ('_hash',)

    def __init__(self, **kwargs):
        """Initialize."""

        temp = []
        for k, v in kwargs.items():
            temp.append(type(v))
            temp.append(v)
            super().__setattr__(k, v)
        super().__setattr__('_hash', hash(tuple(temp)))

    @classmethod
    def __base__(cls):
        """Get base class."""

        return cls

    def __eq__(self, other):
        """Equal."""

        return (
            isinstance(other, self.__base__()) and
            all([getattr(other, key) == getattr(self, key) for key in self.__slots__ if key != '_hash'])
        )

    def __ne__(self, other):
        """Equal."""

        return (
            not isinstance(other, self.__base__()) or
            any([getattr(other, key) != getattr(self, key) for key in self.__slots__ if key != '_hash'])
        )

    def __hash__(self):
        """Hash."""

        return self._hash

    def __setattr__(self, name, value):
        """Prevent mutability."""

        raise AttributeError('Class is immutable!')


class ImmutableDict(Mapping):
    """Hashable, immutable dictionary."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        if (
            not all([isinstance(v, Hashable) for v in kwargs.values()]) or
            not all([isinstance(v, Hashable) for k, v in args])
        ):
            raise ValueError('All values must be hashable')

        self._d = dict(*args, **kwargs)
        self._hash = hash(tuple([(type(x), x, type(y), y) for x, y in sorted(self._d.items())]))

    def __iter__(self):
        """Iterator."""

        return iter(self._d)

    def __len__(self):
        """Length."""

        return len(self._d)

    def __getitem__(self, key):
        """Get item: `namespace['key']`."""
        return self._d[key]

    def __hash__(self):
        """Hash."""

        return self._hash

    def __repr__(self):
        """Representation."""

        return "%r" % self._d

    __str__ = __repr__


def deprecated(message, stacklevel=2):
    """
    Raise a `DeprecationWarning` when wrapped function/method is called.

    Borrowed from https://stackoverflow.com/a/48632082/866026
    """

    def _decorator(func):
        @wraps(func)
        def _func(*args, **kwargs):
            warnings.warn(
                "'{}' is deprecated. {}".format(func.__name__, message),
                category=DeprecationWarning,
                stacklevel=stacklevel
            )
            return func(*args, **kwargs)
        return _func
    return _decorator

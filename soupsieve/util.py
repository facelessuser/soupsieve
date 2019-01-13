"""Utility."""
from __future__ import unicode_literals
from functools import wraps
import warnings
import sys
import struct
import os
MODULE = os.path.dirname(__file__)

PY3 = sys.version_info >= (3, 0)
PY35 = sys.version_info >= (3, 5)

if PY3:
    from functools import lru_cache  # noqa F401
    import copyreg  # noqa F401
    from collections.abc import Hashable, Mapping  # noqa F401

    ustr = str  # noqa
    bstr = bytes  # noqa
    unichar = chr  # noqa
    string = str  # noqa
else:
    from backports.functools_lru_cache import lru_cache  # noqa F401
    import copy_reg as copyreg  # noqa F401
    from collections import Hashable, Mapping  # noqa F401

    ustr = unicode  # noqa
    bstr = str  # noqa
    unichar = unichr  # noqa
    string = basestring  # noqa

_QUIRKS = 0x20000
DEBUG = 0x10000

LC_A = ord('a')
LC_Z = ord('z')
UC_A = ord('A')
UC_Z = ord('Z')


def is_doc(obj):
    """Is `BeautifulSoup` object."""

    import bs4
    return isinstance(obj, bs4.BeautifulSoup)


def is_tag(obj):
    """Is tag."""

    import bs4
    return isinstance(obj, bs4.Tag)


def is_comment(obj):
    """Is comment."""

    import bs4
    return isinstance(obj, bs4.Comment)


def is_declaration(obj):  # pragma: no cover
    """Is declaration."""

    import bs4
    return isinstance(obj, bs4.Declaration)


def is_cdata(obj):  # pragma: no cover
    """Is CDATA."""

    import bs4
    return isinstance(obj, bs4.Declaration)


def is_processing_instruction(obj):  # pragma: no cover
    """Is processing instruction."""

    import bs4
    return isinstance(obj, bs4.ProcessingInstruction)


def is_navigable_string(obj):
    """Is navigable string."""

    import bs4
    return isinstance(obj, bs4.NavigableString)


def is_special_string(obj):
    """Is special string."""

    import bs4
    return isinstance(obj, (bs4.Comment, bs4.Declaration, bs4.CData, bs4.ProcessingInstruction))


def get_navigable_string_type(obj):
    """Get navigable string type."""

    import bs4
    return bs4.NavigableString


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


def uchr(i):
    """Allow getting Unicode character on narrow python builds."""

    try:
        return unichar(i)
    except ValueError:  # pragma: no cover
        return struct.pack('i', i).decode('utf-32')


def deprecated(message, stacklevel=2):  # pragma: no cover
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


def warn_deprecated(message, stacklevel=2):  # pragma: no cover
    """Warn deprecated."""

    warnings.warn(
        message,
        category=DeprecationWarning,
        stacklevel=stacklevel
    )


class QuirksWarning(UserWarning):  # pragma: no cover
    """Warning for quirks mode."""


def warn_quirks(message, recommend, pattern):
    """Warn quirks."""

    import traceback
    import bs4  # noqa: F401

    paths = (MODULE, sys.modules['bs4'].__path__[0])
    tb = traceback.extract_stack()
    previous = None
    filename = None
    lineno = None
    for entry in tb:
        if (PY35 and entry.filename.startswith(paths)) or (not PY35 and entry[0].startswith(paths)):
            break
        previous = entry
    if previous:
        filename = previous.filename if PY35 else previous[0]
        lineno = previous.lineno if PY35 else previous[1]

    warnings.warn_explicit(
        "\nCSS selector pattern: {!r}\n".format(pattern) +
        "    {}\n".format(message) +
        "    This behavior is only allowed temporarily for Beautiful Soup's transition to Soup Sieve.\n" +
        "    In order to confrom to the CSS spec, {}\n".format(recommend) +
        "    It is strongly recommended the selector be altered to conform to the CSS spec " +
        "as an exception will be raised for this case in the future.\n",
        QuirksWarning,
        filename,
        lineno
    )

"""Utility."""
from functools import wraps
import warnings

HTML5 = 0x1
HTML = 0x2
XHTML = 0x4
XML = 0x8
DEPRECATED_FLAGS = HTML5 | HTML | XHTML | XML

LC_A = ord('a')
LC_Z = ord('z')
UC_A = ord('A')
UC_Z = ord('Z')


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


def warn_deprecated(message, stacklevel=2):
    """Warn deprecated."""

    warnings.warn(
        message,
        category=DeprecationWarning,
        stacklevel=stacklevel
    )

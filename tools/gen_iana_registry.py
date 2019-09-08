"""Generate registry helper with the IANA registry."""
import codecs
import re


class Tag:
    """Tag structure."""

    tag_type = 'Tag'
    ignore = set()

    def __init__(self):
        """Initialize."""

        self.name = ''

        self.tag = {
            'added': None,
            'comments': None,
            'deprecated': False,
            'description': None,
            'macrolanguage': None,
            'preferred': None,
            'prefix': [],
            'scope': None,
            'suppress': None,
            'type': self.tag_type.lower()
        }

    def add_prefix(self, prefix):
        """Add prefix."""

        self.tag['prefix'].append(prefix.lower())

    def set_preferred(self, preferred):
        """Set preferred."""

        self.tag['preferred'] = preferred.lower()

    def set_subtag(self, subtag):
        """Set subtag."""

        self.name = subtag.lower()

    def set_tag(self, tag):
        """Set tag."""

        self.name = tag.lower()

    def set_deprecated(self, deprecated):
        """Set deprecated."""

        self.tag['deprecated'] = deprecated.lower()

    def set_scope(self, scope):
        """Set scope."""

        self.tag['scope'] = scope.lower()

    def set_macrolanguage(self, macrolanguage):
        """Set macrolanguage."""

        self.tag['macrolanguage'] = macrolanguage.lower()

    def set_suppress(self, suppress):
        """Set suppress."""

        self.tag['suppress'] = suppress.lower()

    def set_comments(self, comments):
        """Set comments."""

        self.tag['comments'] = comments

    def set_description(self, description):
        """Set description."""

        self.tag['description'] = description

    def set_added(self, added):
        """Set added."""

        self.tag['added'] = added

    def __repr__(self):
        """Representation."""

        return str({k: v for k, v in self.tag.items() if k not in self.ignore})

    __str__ = __repr__


class Language(Tag):
    """Language."""

    ignore = set(['scope', 'suppress', 'deprecated', 'macrolanguage', 'prefix', 'added', 'comments', 'description'])
    tag_type = "Language"


class Variant(Tag):
    """Variant."""

    ignore = set(['scope', 'suppress', 'deprecated', 'macrolanguage', 'added', 'comments', 'description'])
    tag_type = "Variant"


class Extlang(Tag):
    """Extlang."""

    ignore = set(['scope', 'suppress', 'deprecated', 'macrolanguage', 'added', 'comments', 'description'])
    tag_type = "Extlang"


class Script(Tag):
    """Script."""

    ignore = set(['scope', 'deprecated', 'macrolanguage', 'prefix', 'added', 'comments', 'description'])
    tag_type = "Script"


class Region(Tag):
    """Region."""

    ignore = set(['scope', 'suppress', 'deprecated', 'macrolanguage', 'prefix', 'added', 'comments', 'description'])
    tag_type = "Region"


class Grandfathered(Tag):
    """Grandfathered."""

    ignore = set(['scope', 'suppress', 'deprecated', 'macrolanguage', 'prefix', 'added', 'comments', 'description'])
    tag_type = "Grandfathered"


class Redundant(Tag):
    """Redundant."""

    ignore = set(['scope', 'suppress', 'deprecated', 'macrolanguage', 'prefix', 'added', 'comments', 'description'])
    tag_type = "Redundant"


RE_KEY_VALUE = re.compile(r'^([-a-z0-9]+): (.*?)(?=\n[-a-z0-9]+:|\Z)', flags=re.M | re.I)

with codecs.open('tools/registry.txt', 'r', encoding='utf-8') as f:
    registry = f.read().replace('\r', '')

blocks = [x.strip() for x in registry.split('%%')]
data = {}
date = blocks.pop(0)
m = RE_KEY_VALUE.match(date, 0)
date = m.group(2)

for block in blocks:
    obj = None
    for m in RE_KEY_VALUE.finditer(block):
        key = m.group(1)
        value = m.group(2)

        if key == 'Type':
            if value == 'variant':
                obj = Variant()
            elif value == 'language':
                obj = Language()
            elif value == 'script':
                obj = Script()
            elif value == 'grandfathered':
                obj = Grandfathered()
            elif value == 'redundant':
                obj = Redundant()
            elif value == 'extlang':
                obj = Extlang()
            elif value == 'region':
                obj = Region()
            else:
                raise RuntimeError("Unexpected Type '{}'".format(value))

            if value not in data:
                data[value] = []
            if isinstance(obj.tag, str):
                raise RuntimeError('What?')
            data[value].append(obj)
            continue

        if obj is None:
            continue

        if key == 'Subtag':
            obj.set_subtag(value)
        elif key == 'Prefix':
            obj.add_prefix(value)
        elif key == 'Preferred-Value':
            obj.set_preferred(value)
        elif key == 'Tag':
            obj.set_tag(value)
        elif key == 'Deprecated':
            obj.set_deprecated(value)
        elif key == 'Suppress-Script':
            obj.set_suppress(value)
        elif key == 'Scope':
            obj.set_scope(value)
        elif key == 'Macrolanguage':
            obj.set_macrolanguage(value)
        elif key == "Comments":
            obj.set_comments(value)
        elif key == "Description":
            obj.set_description(value)
        elif key == 'Added':
            obj.set_added(value)
        else:
            raise RuntimeError("Unexpected key '{}'".format(key))

with codecs.open('soupsieve/css_lang/registry.py', 'w', encoding='utf-8') as f:
    f.write('"""IANA Registry."""\n')
    f.write('registry = {\n')
    f.write('    "filedate": {!r},\n'.format(date))
    for key in sorted(data.keys()):
        f.write('    "{}": {{\n'.format(key))
        for item in data[key]:
            f.write('        "{}": {{\n'.format(item.name))
            for k, v in sorted(item.tag.items()):
                if k not in item.ignore:
                    f.write('            "{}": {!r},\n'.format(k, v))
            f.write('        },\n')
        f.write('    },\n')
    f.write('}\n')

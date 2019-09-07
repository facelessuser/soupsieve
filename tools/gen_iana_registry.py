"""Generate registry helper with the IANA registry."""
import codecs
import re


class Tag:
    """Tag structure."""

    tag_type = 'Tag'

    def __init__(self):
        """Initialize."""

        self.name = ''

        self.tag = {
            'type': self.tag_type.lower(),
            'prefix': [],
            'deprecated': False,
            'scope': None,
            'macrolanguage': None,
            'suppress': None,
            'preferred': None
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

    def __repr__(self):
        """Representation."""

        return str(self.tag)

    __str__ = __repr__


class Language(Tag):
    """Language."""

    tag_type = "Language"


class Variant(Tag):
    """Variant."""

    tag_type = "Variant"


class Extlang(Tag):
    """Extlang."""

    tag_type = "Extlang"


class Script(Tag):
    """Script."""

    tag_type = "Script"


class Region(Tag):
    """Region."""

    tag_type = "Region"


class Grandfathered(Tag):
    """Grandfathered."""

    tag_type = "Grandfathered"


class Redundant(Tag):
    """Redundant."""

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
        elif key not in ('Comments', 'Description', 'Added'):
            raise RuntimeError("Unexpected key '{}'".format(key))

with codecs.open('soupsieve/css_lang/registry.py', 'w') as f:
    f.write('"""IANA Registry."""\n')
    f.write('registry = {\n')
    f.write('    "filedate": {!r},\n'.format(date))
    for key in sorted(data.keys()):
        f.write('    "{}": {{\n'.format(key))
        for item in data[key]:
            f.write('        "{}": {{\n'.format(item.name))
            for k, v in sorted(item.tag.items()):
                f.write('            "{}": {!r},\n'.format(k, v))
            f.write('        },\n')
        f.write('    },\n')
    f.write('}\n')

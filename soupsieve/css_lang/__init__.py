"""Language handler."""
import re
from .registry import registry

# Singleton
SINGLETON = r"[0-9a-wy-z]"

# Sub-tags
# Though the ABNF support 3 extlang tags, any tags that use these
# ranges are invalid, and always will be, per RCF5646.
# Though wellformed, We cannot canonicalize an invalid tag.
# `WELLFORMED_EXTLANG = r"[a-z]{3}(?:-[a-z]{3}){0,2}"`
EXTLANG = r"[a-z]{3}(?:-[a-z]{3}){0,2}"
SCRIPT = r"[a-z]{4}"
REGION = r"(?:[a-z]{2}|[0-9]{3})"
VARIANT = r"(?:[a-z0-9]{5,8}|[0-9][a-z0-9]{3})"
EXTENSION = r"{}(?:-[a-z0-9]{{2,8}})+".format(SINGLETON)
PRIVATEUSE = r"x(?:-[a-z0-9]{1,8})+"

# Special Tags
REGULAR = r"""
(?:
    art-lojban|cel-gaulish|no-bok|no-nyn|zh-guoyu|
    zh-hakka|zh-min|zh-min-nan|zh-xiang
)"""
IRREGULAR = r"""
(?:
    en-GB-oed|i-ami|i-bnn|i-default|i-enochian|
    i-hak|i-klingon|i-lux|i-mingo|i-navajo|i-pwn|i-tao|
    i-tay|i-tsu|sgn-BE-FR|sgn-BE-NL|sgn-CH-DE
)"""
GRANDFATHERED = r"(?:{}|{})".format(IRREGULAR, REGULAR)

# Language Tag
LANGUAGE = r"(?:[a-z]{{2,3}}(?P<extlang>-{})?|[a-z]{{4}}|[a-z]{{5,8}})".format(EXTLANG)
LANGUAGE_RANGE = r"(?:(?:[a-z]{{2,3}}|\*)(?P<extlang>-{})?|[a-z]{{4}}|[a-z]{{5,8}})".format(EXTLANG)
LANGTAG = r"""
(?P<language>{})(?P<script>-{})?(?P<region>-{})?(?P<variant>(?:-{})*)(?P<extension>(?:-{})*)(?P<privateuse>-{})?
""".format(
    LANGUAGE, SCRIPT, REGION, VARIANT, EXTENSION, PRIVATEUSE
)
LANGTAG_RANGE = r"""
(?P<language>{})(?P<script>-{})?(?P<region>-{})?(?P<variant>(?:-{})*)(?P<extension>(?:-{})*)(?P<privateuse>-{})?
""".format(
    LANGUAGE_RANGE, SCRIPT, REGION, VARIANT, EXTENSION, PRIVATEUSE
)
RE_LANGUAGETAG = re.compile(
    r"(?xi)^(?:{}|(?P<private>{})|(?P<grandfathered>{}))$".format(
        LANGTAG, PRIVATEUSE, GRANDFATHERED
    )
)
RE_LANGUAGETAG_RANGE = re.compile(
    r"(?xi)^(?:{}|(?P<private>{})|(?P<grandfathered>{}))$".format(
        LANGTAG_RANGE, PRIVATEUSE, GRANDFATHERED
    )
)

RE_PRIVATE_SCRIPT = re.compile(r'^Qa(?:a[a-z]|b[a-x])$', flags=re.I)
RE_PRIVATE_REGION = re.compile(r'^AA|Q[M-Z]|X[A-Z]|ZZ$', flags=re.I)
RE_PRIVATE_LANG = re.compile(r'^q[a-t][a-z]$', flags=re.I)

# Other patterns
RE_EXT_SPLIT = re.compile(r'(?xi)-(?={}\b)'.format(SINGLETON))
RE_WILD_STRIP = re.compile(r'(?:(?:-\*-)(?:\*(?:-|$))*|-\*$)')


class InvalidSubtagError(ValueError):
    """Invalid subtag Error."""


def normalize(language):
    """Normalize a by lower casing the tag/range and by stripping out * from ranges except when the primary subtag."""

    return RE_WILD_STRIP.sub('-', language).lower()


class Canonicalize(object):
    """
    Canonicalize language tags and ranges.

    Canonicalization is based off of RFC5646 section 4.5.
    General algorithm:

    - Normalize range or language tag. Language tags we will
      remove wildcard ranges except when the one which represents
      the primary subtag. Per the spec, all others are ignored.
      We also normalize case by lower casing the tag/range.

    - Sort extensions by singleton subtags.

    - Resolve grandfathered and redundant tags replacing them with
      their preferred form if present.

    - Languages are then resolved primary subtags are replaced with their
      preferred value. If an extlang is present, the primary tag may be
      removed in favor of the extlang. Language subtags and extlang subtags
      are also validated as to whether they are registered. Unregistered
      subtags will halt canonicalization.

    - Script and region subtags are replaced with their preferred value
      if present. Subtags are also validated as to whether they are registered.
      Unregistered subtags will halt canonicalization.

    - Variants MAY be reordered for more consistent matching results.
      Variants are first sorted alphabetically, and moved to the end if they
      have no prefixes. If they do have prefixes, they are moved directly
      after them if they are also present in the variant range. Subtags are also
      validated as to whether they are registered. Unregistered subtags will halt
      canonicalization. If all the prefixes are not present, this SHOULD be an
      error, but we do not enforce it. Particularly to better handle language
      ranges vs tags.

    """

    def __init__(self, language, debug=False):
        """Initialize."""

        self.debug = False
        self.is_range = '*' in language
        self.language = language

    def canonicalize_language(self):
        """Canonicalize language tags."""

        language = self.parts['language']

        extlang = None
        primary = None

        values = language.split('-')

        if values[0] == '*':
            if len(values) > 1:
                if values[1] not in registry['extlang']:
                    raise InvalidSubtagError("'{}' is not a registered extlang.".format(extlang))
            return

        if values[0] not in registry['language']:
            raise InvalidSubtagError("'{}' is not a registered language.".format(values[0]))
        if registry['extlang'].get(values[0]):
            extlang = values[0]
        else:
            value = registry['language'][values[0]]['preferred']
            primary = values[0] if value is None else value

        if len(values) == 2:
            if extlang:
                raise InvalidSubtagError("Unexpected extlang following extlang: '{}'".format(values[1]))
            extlang = values[1]

        if extlang:
            if extlang not in registry['extlang']:
                raise InvalidSubtagError("'{}' is not a registered extlang.".format(extlang))
            if primary and primary not in registry['extlang'][extlang]['prefix']:
                raise InvalidSubtagError("'{}' is an invalid prefix for '{}'".format(primary, extlang))
            primary = None

        # Do not allow extlang in canonical form
        if not primary:
            self.parts['language'] = extlang
            self.parts['extlang'] = ''
        elif not extlang:
            self.parts['language'] = primary
            self.parts['extlang'] = ''

    def canonicalize_script(self):
        """Canonicalize script tags."""

        script = self.parts['script'].lstrip('-')

        if script and not RE_PRIVATE_SCRIPT.match(script):
            if script not in registry['script']:
                raise InvalidSubtagError("'{}' is not a registered script".format(script))

            value = registry['script'][script]['preferred']
            if value:
                self.parts['script'] = '-' + value

    def canonicalize_region(self):
        """Canonicalize region tags."""

        region = self.parts['region'].lstrip('-')

        if region and not RE_PRIVATE_REGION.match(region):
            if region not in registry['region']:
                raise InvalidSubtagError("'{}' is not a registered region".format(region))

            value = registry['region'][region]['preferred']

            if value:
                self.parts['region'] = '-' + value

    def canonicalize_variant(self):
        """Canonicalize variant tags."""

        variant = self.parts['variant'].lstrip('-')

        if variant:
            ordered = sorted(variant.split('-'))
            variants = set(ordered)
            if len(variants) != len(ordered):
                raise InvalidSubtagError('Duplicate variants were found')

            subtags = set(self.parts['language'].split('-'))
            if self.parts['script']:
                subtags.add(self.parts['script'].lstrip('-'))
            if self.parts['region']:
                subtags.add(self.parts['region'].lstrip('-'))

            for v in ordered[:]:
                index = ordered.index(v)
                if v not in registry['variant']:
                    raise InvalidSubtagError("'{}' is not a registered variant".format(variant))
                value = registry['variant'][v]['preferred']
                if value is not None:
                    v = value
                prefixes = [p.split('-') for p in registry['variant'][v]['prefix']]

                matched = True if not prefixes else False
                if matched:
                    # No prefixes required, so lets move to the end
                    del ordered[index]
                    ordered.insert(len(ordered), v)
                    index = len(ordered) - 1

                for prefix in prefixes:
                    match = True
                    for subtag in prefix:
                        if subtag not in subtags and subtag not in variants:
                            match = False
                        elif subtag in variants:
                            # We found a prefix that is current in the variant range
                            # Move the current variant to be right after the required
                            # variant prefix.
                            i = ordered.index(subtag)
                            if i > index:
                                del ordered[index]
                                ordered.insert(i, v)
                                index = i

                    # We found at least one matching case
                    if match:
                        matched = True

                # We SHOULD require a variant to be preceded by its prefixes.
                # We do not currently require it though.
                # ```
                # if not matched:
                #     raise InvalidSubtagError("Missing proper prefixes for '{}'".format(v))
                # ```

            if ordered:
                ordered = '-'.join(ordered)

                if variant != ordered:
                    self.parts['variant'] = '-' + ordered

    def canonicalize_extension(self):
        """Canonicalize extension."""

        extension = self.parts['extension']

        if extension:
            extension = '-'.join(sorted(RE_EXT_SPLIT.split(extension.lstrip('-'))))
            self.parts['extension'] = '-' + extension if extension else extension

    def canonicalize_redundant_grandfathered(self):
        """Canonicalize redundant tags."""

        lang = None
        if self.parts['grandfathered']:
            value = registry['grandfathered'][self.parts['grandfathered']]['preferred']
            if value is not None:
                lang = value
        else:
            values = ('{language}{script}{region}{variant}{extension}{privateuse}'.format(**self.parts)).split('-')
            for n in range(3, 0, -1):
                value = registry['redundant'].get('-'.join(values[:3]), {}).get('preferred')
                if value is not None:
                    lang = '-'.join([value] + values[3:])
                    break
        if lang is not None:
            for k, v in RE_LANGUAGETAG.match(lang).groupdict(default='').items():
                self.parts[k] = v

    def to_extlang_form(self):
        """Convert to extlang form."""

        primary = self.parts['language']
        if primary and not primary.startswith('*') and not self.parts['extlang']:
            prefix = registry['extlang'].get(primary, {}).get('prefix', [])
            if len(prefix):
                self.parts['language'] = r'{}-{}'.format(prefix[0], primary)
                self.parts['extlang'] = r'-{}'.format(primary)

    def format_case(self):
        """Format case."""

        if not self.is_range or not self.parts['language'].startswith('*'):
            self.parts['script'] = self.parts['script'].title()
            self.parts['region'] = self.parts['region'].upper()

    def _canonicalize(self, extlang_form=False):
        """Canonicalize."""

        if self.debug:
            print('Language: ', self.language)
        lang = normalize(self.language)
        if self.debug:
            print('Normalized language: ', lang)
        m = (RE_LANGUAGETAG_RANGE if self.is_range else RE_LANGUAGETAG).match(lang.lower())
        self.parts = m.groupdict(default='') if m is not None else []
        if self.debug:
            print('Decomposed language: ', self.parts)

        # Don't canonicalize if we couldn't match a wellformed tag or
        # if we found more than one extlang. Wellformed does not always mean valid.
        if self.parts and not self.parts['extlang'].count('-') > 1:
            try:
                if not m.group('private'):
                    self.canonicalize_extension()
                    self.canonicalize_redundant_grandfathered()
                    self.canonicalize_language()
                    self.canonicalize_script()
                    self.canonicalize_region()
                    self.canonicalize_variant()

                    if extlang_form:
                        self.to_extlang_form()

                    self.format_case()

                # Rebuild the tag. Some variables may be empty strings.
                # For instance, when grandfathered is present, nothing else is.
                lang = '{language}{script}{region}{variant}{extension}{privateuse}{private}{grandfathered}'.format(
                    **self.parts
                )
            except InvalidSubtagError as f:
                # Canonicalization was aborted due to an invalid tag.
                if self.debug:
                    print('Invalid Tag: ', f)
        if self.debug:
            print('Canonicalized: ', lang)
        return lang

    def canonicalize(self):
        """Canonicalize."""

        return self._canonicalize()

    def canonicalize_extlang(self):
        """Canonicalize to extlang form."""

        return self._canonicalize(extlang_form=True)


def extended_filter(lang_range, lang_tags, canonicalize=False):
    """Filter the language tags."""

    lang_range = normalize(Canonicalize(lang_range).canonicalize_extlang() if canonicalize else lang_range)
    matches = []

    for tag in lang_tags:
        match = True
        if canonicalize:
            tag = Canonicalize(tag).canonicalize_extlang()
        ranges = lang_range.split('-')
        subtags = normalize(tag).split('-')
        length = len(ranges)
        rindex = 0
        sindex = 0
        r = ranges[rindex]
        s = subtags[sindex]

        # Primary tag needs to match
        if r != '*' and r != s:
            match = False

        rindex += 1
        sindex += 1

        # Match until we run out of ranges
        while match and rindex < length:
            r = ranges[rindex]
            try:
                s = subtags[sindex]
            except IndexError:
                # Ran out of subtags,
                # but we still have ranges
                match = False
                continue

            # Empty range
            if not r:
                match = False
                continue

            # Matched range
            elif s == r:
                rindex += 1

            # Implicit wildcard cannot match
            # singletons
            elif len(s) == 1:
                match = False
                continue

            # Implicitly matched, so grab next subtag
            sindex += 1

        if match:
            matches.append(tag)

    return matches


def basic_filter(lang_range, lang_tags, canonicalize=False):
    """Language tags."""

    lang_range = normalize(Canonicalize(lang_range).canonicalize_extlang() if canonicalize else lang_range)
    matches = []

    for tag in lang_tags:
        if canonicalize:
            tag = Canonicalize(tag).canonicalize_extlang()
        norm_tag = normalize(tag)
        if lang_range == '*' or lang_range == norm_tag or norm_tag.startswith(lang_range + '-'):
            matches.append(tag)

    return matches

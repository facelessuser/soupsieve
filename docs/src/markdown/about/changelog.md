# Changelog

## 2.4

- **NEW**: Update to support changes related to `:lang()` in the official CSS spec. `:lang("")` should match unspecified
  languages, e.g. `lang=""`, but not `lang=und`.
- **NEW**: Only `:is()` and `:where()` should allow forgiving selector lists according to latest CSS (as far as Soup
  Sieve supports "forgiving" which is limited to empty selectors).
- **NEW**: Formally drop Python 3.6.
- **NEW**: Formally declare support for Python 3.11.

## 2.3.2.post1

- **FIX**: Documentation for installation from source is outdated.

## 2.3.2

- **FIX**: Fix some typos in error messages.

## 2.3.1

- **FIX**: Ensure attribute selectors match tags that have new line characters in attributes. (#233)

## 2.3

- **NEW**: Officially support Python 3.10.
- **NEW**: Add static typing.
- **NEW**: `:has()`, `:is()`, and `:where()` now use use a forgiving selector list. While not as forgiving as CSS might
  be, it will forgive such things as empty sets and empty slots due to multiple consecutive commas, leading commas, or
  trailing commas. Essentially, these pseudo-classes will match all non-empty selectors and ignore empty ones. As the
  scraping environment is different than a browser environment, it was chosen not to aggressively forgive bad syntax and
  invalid features to ensure the user is alerted that their program may not perform as expected.
- **NEW**: Add support to output a pretty print format of a compiled `SelectorList` for debug purposes.
- **FIX**: Some small corner cases discovered with static typing.

## 2.2.1

- **FIX**: Fix an issue with namespaces when one of the keys is `self`.

## 2.2

- **NEW**: `:link` and `:any-link` no longer include `#!html <link>` due to a change in the level 4 selector
  specification. This actually yields more sane results.
- **FIX**: BeautifulSoup, when using `find`, is quite forgiving of odd types that a user may place in an element's
  attribute value. Soup Sieve will also now be more forgiving and attempt to match these unexpected values in a sane
  manner by normalizing them before compare. (#212)

## 2.1

- **NEW**: Officially support Python 3.9.
- **NEW**: Drop official support for Python 3.5.
- **NEW**: In order to avoid conflicts with future CSS specification changes, non-standard pseudo classes will now start
  with the `:-soup-` prefix. As a consequence, `:contains()` will now be known as `:-soup-contains()`, though for a time
  the deprecated form of `:contains()` will still be allowed with a warning that users should migrate over to
  `:-soup-contains()`.
- **NEW**: Added new non-standard pseudo class `:-soup-contains-own()` which operates similar to `:-soup-contains()`
  except that it only looks at text nodes directly associated with the currently scoped element and not its descendants.
- **FIX**: Import `bs4` globally instead of in local functions as it appears there are no adverse affects due to
  circular imports as `bs4` does not immediately reference `soupsieve` functions and `soupsieve` does not immediately
  reference `bs4` functions. This should give a performance boost to functions that had previously included `bs4`
  locally.

## 2.0.1

- **FIX**: Remove unused code.

## 2.0

- **NEW**: `SelectorSyntaxError` is derived from `Exception` not `SyntaxError`.
- **NEW**: Remove deprecated `comments` and `icomments` from the API.
- **NEW**: Drop support for EOL Python versions (Python 2 and Python < 3.5).
- **FIX**: Corner case with splitting namespace and tag name that that have an escaped `|`.

## 1.9.6

!!! note "Last version for Python 2.7"

- **FIX**: Prune dead code.
- **FIX**: Corner case with splitting namespace and tag name that that have an escaped `|`.

## 1.9.5

- **FIX**: `:placeholder-shown` should not match if the element has content that overrides the placeholder.

## 1.9.4

- **FIX**: `:checked` rule was too strict with `option` elements. The specification for `:checked` does not require an
  `option` element to be under a `select` element.
- **FIX**: Fix level 4 `:lang()` wildcard match handling with singletons. Implicit wildcard matching should not
  match any singleton. Explicit wildcard matching (`*` in the language range: `*-US`) is allowed to match singletons.

## 1.9.3

- **FIX**: `[attr!=value]` pattern was mistakenly using `:not([attr|=value])` logic instead of `:not([attr=value])`.
- **FIX**: Remove undocumented `_QUIRKS` mode flag. Beautiful Soup was meant to use it to help with transition to Soup
  Sieve, but never released with it. Help with transition at this point is no longer needed.

## 1.9.2

- **FIX**: Shortcut last descendant calculation if possible for performance.
- **FIX**: Fix issue where `Doctype` strings can be mistaken for a normal text node in some cases.
- **FIX**: A top level tag is not a `:root` tag if it has sibling text nodes or tag nodes. This is an issue that mostly
  manifests when using `html.parser` as the parser will allow multiple root nodes.

## 1.9.1

- **FIX**: `:root`, `:contains()`, `:default`, `:indeterminate`, `:lang()`, and `:dir()` will properly account for HTML
  `iframe` elements in their logic when selecting or matching an element. Their logic will be restricted to the document
  for which the element under consideration applies.
- **FIX**: HTML pseudo-classes will check that all key elements checked are in the XHTML namespace (HTML parsers that do
  not provide namespaces will assume the XHTML namespace).
- **FIX**: Ensure that all pseudo-class names are case insensitive and allow CSS escapes.

## 1.9

- **NEW**: Allow `:contains()` to accept a list of text to search for. (#115)
- **NEW**: Add new `escape` function for escaping CSS identifiers. (#125)
- **NEW**: Deprecate `comments` and `icomments` functions in the API to ensure Soup Sieve focuses only on CSS selectors.
  `comments` and `icomments` will most likely be removed in 2.0. (#130)
- **NEW**: Add Python 3.8 support. (#133)
- **FIX**: Don't install test files when installing the `soupsieve` package. (#111)
- **FIX**: Improve efficiency of `:contains()` comparison.
- **FIX**: Null characters should translate to the Unicode REPLACEMENT CHARACTER (`U+FFFD`) according to the
  specification. This applies to CSS escaped NULL characters as well. (#124)
- **FIX**: Escaped EOF should translate to `U+FFFD` outside of CSS strings. In a string, they should just be ignored,
  but as there is no case where we could resolve such a string and still have a valid selector, string handling remains
  the same. (#128)

## 1.8

- **NEW**: Add custom selector support. (#92)(#108)
- **FIX**: Small tweak to CSS identifier pattern to ensure it matches the CSS specification exactly. Specifically, you
  can't have an identifier of only `-`. (#107)
- **FIX**: CSS string patterns should allow escaping newlines to span strings across multiple lines. (#107)
- **FIX**: Newline regular expression for CSS newlines should treat `\r\n` as a single character, especially in cases
  such as string escapes: `\\\r\n`. (#107)
- **FIX**: Allow `--` as a valid identifier or identifier start. (#107)
- **FIX**: Bad CSS syntax now raises a `SelectorSyntaxError`, which is still currently derived from `SyntaxError`, but
  will most likely be derived from `Exception` in the future.

## 1.7.3

- **FIX**: Fix regression with tag names in regards to case sensitivity, and ensure there are tests to prevent breakage
  in the future.
- **FIX**: XHTML should always be case sensitive like XML.

## 1.7.2

- **FIX**: Fix HTML detection `type` selector.
- **FIX**: Fixes for `:enabled` and `:disabled`.
- **FIX**: Provide a way for Beautiful Soup to parse selectors in a quirks mode to mimic some of the quirks of the old
  select method prior to Soup Sieve, but with warnings. This is to help old scripts to not break during the transitional
  period with newest Beautiful Soup. In the future, these quirks will raise an exception as Soup Sieve requires
  selectors to follow the CSS specification.

## 1.7.1

- **FIX**: Fix issue with `:has()` selector where a leading combinator can only be provided in the first selector in a
  relative selector list.

## 1.7

- **NEW**: Add support for `:in-range` and `:out-of-range` selectors. (#60)
- **NEW**: Add support for `:defined` selector. (#76)
- **FIX**: Fix pickling issue when compiled selector contains a `NullSelector` object. (#70)
- **FIX**: Better exception messages in the CSS selector parser and fix a position reporting issue that can occur in
  some exceptions. (#72, #73)
- **FIX**: Don't compare prefixes when evaluating attribute namespaces, compare the actual namespace. (#75)
- **FIX**: Split whitespace attribute lists by all whitespace characters, not just space.
- **FIX**: `:nth-*` patterns were converting numbers to base 16 when they should have been converting to base 10.

## 1.6.2

- **FIX**: Fix pattern compile issues on Python < 2.7.4.
- **FIX**: Don't use `\d` in Unicode `Re` patterns as they will contain characters outside the range of `[0-9]`.

## 1.6.1

- **FIX**: Fix warning about not importing `Mapping` from `collections.abc`.

## 1.6

- **NEW**: Add `closest` method to the API that matches closest ancestor.
- **FIX**: Add missing `select_one` reference to module's `__all__`.

## 1.5

- **NEW**: Add `select_one` method like Beautiful Soup has.
- **NEW**: Add `:dir()` selector (HTML only).
- **FIX**: Fix issues when handling HTML fragments (elements without a `BeautifulSoup` object as a parent).
- **FIX**: Fix internal `nth` range check.

## 1.4.0

- **NEW**: Throw `NotImplementedError` for at-rules: `@page`, etc.
- **NEW**: Match nothing for `:host`, `:host()`, and `:host-context()`.
- **NEW**: Add support for `:read-write` and `:read-only`.
- **NEW**: Selector patterns can be annotated with CSS comments.
- **FIX**: `\r`, `\n`, and `\f` cannot be escaped with `\` in CSS. You must use Unicode escapes.

## 1.3.1

- **FIX**: Fix issue with undefined namespaces.

## 1.3

- **NEW**: Add support for `:scope`.
- **NEW**: `:user-invalid`, `:playing`, `:paused`, and `:local-link` will not cause a failure, but all will match
  nothing as their use cases are not possible in an environment outside a web browser.
- **FIX**: Fix `[attr~=value]` handling of whitespace. According to the spec, if the value contains whitespace, or is an
  empty string, it should not match anything.
- **FIX**: Precompile internal patterns for pseudo-classes to prevent having to parse them again.

## 1.2.1

- **FIX**: More descriptive exceptions. Exceptions will also now mention position in the pattern that is problematic.
- **FIX**: `filter` ignores `NavigableString` objects in normal iterables and `Tag` iterables. Basically, it filters all
  Beautiful Soup document parts regardless of iterable type where as it used to only filter out a `NavigableString` in a
  `Tag` object. This is viewed as fixing an inconsistency.
- **FIX**: `DEBUG` flag has been added to help with debugging CSS selector parsing. This is mainly for development.
- **FIX**: If forced to search for language in `meta` tag, and no language is found, cache that there is no language in
  the `meta` tag to prevent searching again during the current select.
- **FIX**: If a non `BeautifulSoup`/`Tag` object is given to the API to compare against, raise a `TypeError`.

## 1.2

- **NEW**: Add Python 2.7 support.
- **NEW**: Remove old pre 1.0 deprecations.

## 1.1

- **NEW**: Adds support for `[attr!=value]` which is equivalent to `:not([attr=value])`.
- **NEW**: Add support for `:active`, `:focus`, `:hover`, `:visited`, `:target`, `:focus-within`, `:focus-visible`,
  `:target-within`, `:current()`/`:current`, `:past`, and `:future`, but they will never match as these states don't
  exist in the Soup Sieve environment.
- **NEW**: Add support for `:checked`, `:enabled`, `:disabled`, `:required`, `:optional`, `:default`, and
  `:placeholder-shown` which will only match in HTML documents as these concepts are not defined in XML.
- **NEW**: Add support for `:link` and `:any-link`, both of which will target all `<a>`, `<area>`, and `<link>` elements
  with an `href` attribute as all links will be treated as unvisited in Soup Sieve.
- **NEW**: Add support for `:lang()` (CSS4) which works in XML and HTML.
- **NEW**: Users must install Beautiful Soup themselves. This requirement is removed in the hopes that Beautiful Soup
  may use this in the future.
- **FIX**: Attributes in the form `prefix:attr` can be matched with the form `[prefix\:attr]` without specifying a
  namespaces if desired.
- **FIX**: Fix exception when `[type]` is used (with no value).

## 1.0.2

- **FIX**: Use proper CSS identifier patterns for tag names, classes, ids, etc. Things like `#3` or `#-3` should not
  match and should require `#\33` or `#-\33`.
- **FIX**: Do not raise `NotImplementedError` for supported pseudo classes/elements with bad syntax, instead raise
  `SyntaxError`.

## 1.0.1

- **FIX**: When giving a tag to `select`, it should only return the children of that tag, never the tag itself.
- **FIX**: For informational purposes, raise a `NotImplementedError` when an unsupported pseudo class is used.

## 1.0

- **NEW**: Official 1.0.0 release.

## 1.0.0b2

- **NEW**: Drop document flags. Document type can be detected from the Beautiful Soup object directly.
- **FIX**: CSS selectors should be evaluated with CSS whitespace rules.
- **FIX**: Processing instructions, CDATA, and declarations should all be ignored in `:contains` and child
  considerations for `:empty`.
- **FIX**: In Beautiful Soup, the document itself is the first tag. Do not match the "document" tag by returning false
  for any tag that doesn't have a parent.

## 1.0.0b1

- **NEW**: Add support for non-standard `:contains()` selector.
- **FIX**: Compare pseudo class names case insensitively when matching unexpected cases.
- **FIX**: Don't allow attribute case flags when no attribute value is defined.

## 0.6

- **NEW**: `mode` attribute is now called `flags` to allow for other options in the future.
- **FIX**: More corner cases for `nth` selectors.

## 0.5.3

- **FIX**: Previously, all pseudo classes' selector lists were evaluated as one big group, but now each pseudo classes'
  selector lists are evaluated separately.
- **FIX**: CSS selector tokens are not case sensitive.

## 0.5.2

- **FIX**: Add missing `s` flag to attribute selector for forced case sensitivity of attribute values.
- **FIX**: Relax attribute pattern matching to allow non-essential whitespace.
- **FIX**: Attribute selector flags themselves are not case sensitive.
- **FIX**: `type` attribute in HTML is handled special. While all other attributes values are case sensitive, `type` in
  HTML is usually treated special and is insensitive. In XML, this is not the case.

## 0.5.1

- **FIX**: Fix namespace check for `:nth-of-type`.

## 0.5

- **NEW**: Deprecate `commentsiter` and `selectiter` in favor of `icomments` and `iselect`. Expect removal in version
1.0.

## 0.4

- **NEW**: Initial prerelease.

# Changelog

## 1.2.1

- **FIX**: More descriptive exceptions. Exceptions will also now mention position in the pattern that is problematic.
- **FIX**: `filter` ignores `NavigableString` objects in normal iterables and `Tag` iterables. Basically, it filters all Beautiful Soup document parts regardless of iterable type where as it used to only filter out a `NavigableString` in a `Tag` object. This is viewed as fixing an inconsistency.
- **FIX**: `DEBUG` flag has been added to help with debugging CSS selector parsing. This is mainly for development.
- **FIX**: If forced to search for language in `meta` tag, and no language is found, cache that there is no language in the `meta` tag to prevent searching again during the current select.
- **FIX**: If a non `BeautifulSoup`/`Tag` object is given to the API to compare against, raise a `TypeError`.

## 1.2.0

- **NEW**: Add Python 2.7 support.
- **NEW**: Remove old pre 1.0 deprecations.

## 1.1.0

- **NEW**: Adds support for `[attr!=value]` which is equivalent to `:not([attr=value])`.
- **NEW**: Add support for `:active`, `:focus`, `:hover`, `:visited`, `:target`, `:focus-within`, `:focus-visible`, `:target-within`, `:current()`/`:current`, `:past`, and `:future`, but they will never match as these states don't exist in the Soup Sieve environment.
- **NEW**: Add support for `:checked`, `:enabled`, `:disabled`, `:required`, `:optional`, `:default`, and `:placeholder-shown` which will only match in HTML documents as these concepts are not defined in XML.
- **NEW**: Add support for `:link` and `:any-link`, both of which will target all `<a>`, `<area>`, and `<link>` elements with an `href` attribute as all links will be treated as unvisited in Soup Sieve.
- **NEW**: Add support for `:lang()` (CSS4) which works in XML and HTML.
- **NEW**: Users must install Beautiful Soup themselves. This requirement is removed in the hopes that Beautiful Soup may use this in the future.
- **FIX**: Attributes in the form `prefix:attr` can be matched with the form `[prefix\:attr]` without specifying a namespaces if desired.
- **FIX**: Fix exception when `[type]` is used (with no value).

## 1.0.2

- **FIX**: Use proper CSS identifier patterns for tag names, classes, ids, etc. Things like `#3` or `#-3` should not match and should require `#\33` or `#-\33`.
- **FIX**: Do not raise `NotImplementedError` for supported pseudo classes/elements with bad syntax, instead raise `SyntaxError`.

## 1.0.1

- **FIX**: When giving a tag to `select`, it should only return the children of that tag, never the tag itself.
- **FIX**: For informational purposes, raise a `NotImplementedError` when an unsupported pseudo class is used.

## 1.0.0

- **NEW**: Official 1.0.0 release.

## 1.0.0b2

- **NEW**: Drop document flags. Document type can be detected from the Beautiful Soup object directly.
- **FIX**: CSS selectors should be evaluated with CSS whitespace rules.
- **FIX**: Processing instructions, CDATA, and declarations should all be ignored in `:contains` and child considerations for `:empty`.
- **FIX**: In Beautiful Soup, the document itself is the first tag. Do not match the "document" tag by returning false for any tag that doesn't have a parent.

## 1.0.0b1

- **NEW**: Add support for non-standard `:contains()` selector.
- **FIX**: Compare pseudo class names case insensitively when matching unexpected cases.
- **FIX**: Don't allow attribute case flags when no attribute value is defined.

## 0.6.0

- **NEW**: `mode` attribute is now called `flags` to allow for other options in the future.
- **FIX**: More corner cases for `nth` selectors.

## 0.5.3

- **FIX**: Previously, all pseudo classes' selector lists were evaluated as one big group, but now each pseudo classes' selector lists are evaluated separately.
- **FIX**: CSS selector tokens are not case sensitive.

## 0.5.2

- **FIX**: Add missing `s` flag to attribute selector for forced case sensitivity of attribute values.
- **FIX**: Relax attribute pattern matching to allow non-essential whitespace.
- **FIX**: Attribute selector flags themselves are not case sensitive.
- **FIX**: `type` attribute in HTML is handled special. While all other attributes values are case sensitive, `type` in HTML is usually treated special and is insensitive. In XML, this is not the case.

## 0.5.1

- **FIX**: Fix namespace check for `:nth-of-type`.

## 0.5.0

- **NEW**: Deprecate `commentsiter` and `selectiter` in favor of `icomments` and `iselect`. Expect removal in version 1.0.

## 0.4.0

- **NEW**: Initial prerelease.

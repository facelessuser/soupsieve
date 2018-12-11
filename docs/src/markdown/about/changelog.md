# Changelog

## 0.5.3

- **FIX**: Previously all pseudo classes' selector lists were evaluated as one big group, but now each pseudo classes' selector lists are evaluated separately.

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

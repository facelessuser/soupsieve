# API

Soup Sieve implements most of the selectors from the stable specification and even many from the latest draft
specification. Selectors can be used to detect and filter elements. To learn more about which specific selectors are
implemented, see [CSS Selectors](./selectors/index.md).

Soup Sieve will detect the document type being used from the Beautiful Soup object that is given to it, and depending on
the document type, its behavior may be slightly different.

When detecting XHTML, Soup Sieve simply looks to see if the root element of an XML document is under the XHTML namespace
and does not currently look at the `doctype`. If in the future there is a need for stricter XHTML detection, this may
change.

- HTML document types (HTML, HTML5) will have their tag names and attribute names treated without case
sensitivity, like most browsers do.

- XML document types (including XHTML) will have their tag names and attribute names treated with case sensitivity.

- HTML5, XHTML and XML documents will have namespaces evaluated per the document's support (provided via the
parser). Some additional configuration is required when using namespaces, see [Namespace](#namespaces) for more
information.

    !!! tip "Getting Proper Namespaces"
        The `html5lib` parser provides proper namespaces for HTML5, but `lxml`'s HTML parser will not. If you need
        namespace support for HTML5, consider using `html5lib`.

        For XML, the `lxml-xml` parser (`xml` for short) will provide proper namespaces. It is generally suggested that
        `lxml-xml` is used to parse XHTML documents to take advantage of namespaces.

- While attribute values are generally treated as case sensitive, HTML5 and HTML treat the `type` attribute
special. The `type` attribute's value is always case insensitive. This is generally how most browsers treat `type`. If
you need `type` to be sensitive, you can use the `s` flag: `#!css [type="submit" s]`.

While Soup Sieve access is exposed through Beautiful Soup's API, Soup Sieve's API can always be imported and accessed
directly for more controlled tag selection if needed.

## Flags

### `soupseive.DEBUG`

Print debug output when parsing a selector.

```pycon3
>>> import soupsieve as sv
>>> sv.compile('p:has(#id) > span.some-class:contains(text)', flags=sv.DEBUG)
## PARSING: 'p:has(#id) > span.some-class:contains(text)'
TOKEN: 'tag' --> 'p' at position 0
TOKEN: 'pseudo_class' --> ':has(' at position 1
    is_pseudo: True
    is_open: True
    is_relative: True
TOKEN: 'id' --> '#id' at position 6
TOKEN: 'pseudo_close' --> ')' at position 9
TOKEN: 'combine' --> ' > ' at position 10
TOKEN: 'tag' --> 'span' at position 13
TOKEN: 'class' --> '.some-class' at position 17
TOKEN: 'pseudo_contains' --> ':contains(text)' at position 28
## END PARSING
SoupSieve(pattern='p:has(#id) > span.some-class:contains(text)', namespaces=None, custom=None, flags=1)
```

## `soupsieve.select_one()`

```py3
def select_one(select, tag, namespaces=None, flags=0, **kwargs):
    """Select the specified tags."""
```

`select_one` will return the first tag under the given tag that matches the given CSS selectors provided, or it will
return `None` if a suitable tag was not found.

`select_one` accepts a CSS selector string, a `Tag`/`BeautifulSoup` object, an optional [namespace](#namespaces)
dictionary, and `flags`.

```pycon3
>>> import soupsieve as sv
>>> sv.select_one('p:is(.a, .b, .c)', soup)
<p class="a">Cat</p>
```

## `soupsieve.select()`

```py3
def select(select, tag, namespaces=None, limit=0, flags=0, **kwargs):
    """Select the specified tags."""
```

`select` will return all tags under the given tag that match the given CSS selectors provided. You can also limit the
number of tags returned by providing a positive integer via the `limit` parameter (0 means to return all tags).

`select` accepts a CSS selector string, a `Tag`/`BeautifulSoup` object, an optional [namespace](#namespaces) dictionary,
a `limit`, and `flags`.

```pycon3
>>> import soupsieve as sv
>>> sv.select('p:is(.a, .b, .c)', soup)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

## `soupsieve.iselect()`

```py3
def iselect(select, node, namespaces=None, limit=0, flags=0, **kwargs):
    """Select the specified tags."""
```

`iselect` is exactly like `select` except that it returns a generator instead of a list.

## `soupsieve.closest()`

```py3
def closest(select, tag, namespaces=None, flags=0, **kwargs):
    """Match closest ancestor to the provided tag."""
```

`closest` returns the tag closest to the given tag that matches the given selector. The element found must be a direct
ancestor of the tag or the tag itself.

`closest` accepts a CSS selector string, a `Tag`/`BeautifulSoup` object, an optional [namespace](#namespaces)
dictionary, and `flags`.

## `soupsieve.match()`

```py3
def match(select, tag, namespaces=None, flags=0, **kwargs):
    """Match node."""
```

The `match` function matches a given tag with a given CSS selector.

`match` accepts a CSS selector string, a `Tag`/`BeautifulSoup` object, an optional [namespace](#namespaces) dictionary,
and flags.

```pycon3
>>> nodes = sv.select('p:is(.a, .b, .c)', soup)
>>> sv.match('p:not(.b)', nodes[0])
True
>>> sv.match('p:not(.b)', nodes[1])
False
```

## `soupsieve.filter()`

```py3
def filter(select, nodes, namespaces=None, flags=0, **kwargs):
    """Filter list of nodes."""
```

`filter` takes an iterable containing HTML nodes and will filter them based on the provided CSS selector string. If
given a `Tag`/`BeautifulSoup` object, it will iterate the direct children filtering them.

`filter` accepts a CSS selector string, an iterable containing nodes, an optional [namespace](#namespaces) dictionary,
and flags.

```pycon3
>>> sv.filter('p:not(.b)', soup.div)
[<p class="a">Cat</p>, <p class="c">Mouse</p>]
```

## `soupsieve.escape()`

```py3
def escape(ident):
    """Escape CSS identifier."""
```

`escape` is used to escape CSS identifiers. It follows the [CSS specification][cssom] and escapes any character that
would normally cause an identifier to be invalid.

```pycon3
>>> sv.escape(".foo#bar")
'\\.foo\\#bar'
>>> sv.escape("()[]{}")
'\\(\\)\\[\\]\\{\\}'
>>> sv.escape('--a')
'--a'
>>> sv.escape('0')
'\\30 '
>>> sv.escape('\0')
'�'
```

!!! new "New in 1.9.0"
    `escape` is a new API function added in 1.9.0.

## `soupsieve.compile()`

```py3
def compile(pattern, namespaces=None, flags=0, **kwargs):
    """Compile CSS pattern."""
```

`compile` will pre-compile a CSS selector pattern returning a `SoupSieve` object. The `SoupSieve` object has the same
selector functions available via the module without the need to specify the selector, namespaces, or flags.

```py3
class SoupSieve:
    """Match tags in Beautiful Soup with CSS selectors."""

    def match(self, tag):
        """Match."""

    def closest(self, tag):
        """Match closest ancestor."""

    def filter(self, iterable):
        """Filter."""

    def select_one(self, tag):
        """Select a single tag."""

    def select(self, tag, limit=0):
        """Select the specified tags."""

    def iselect(self, tag, limit=0):
        """Iterate the specified tags."""
```

## `soupsieve.purge()`

Soup Sieve caches compiled patterns for performance. If for whatever reason, you need to purge the cache, simply call
`purge`.

## Custom Selectors

The custom selector feature is loosely inspired by the `css-extensions` [proposal][custom-extensions-1]. In its current
form, Soup Sieve allows assigning a complex selector to a custom pseudo-class name. The pseudo-class name must start
with `:--` to avoid conflicts with any future pseudo-classes.

To create custom selectors, you simply need to pass a dictionary containing the custom pseudo-class names (keys) with
the associated CSS selectors that the pseudo-classes are meant to represent (values). It is important to remember that
pseudo-class names are not case sensitive, so even though a dictionary will allow you to specify multiple keys with the
same name (as long as the character cases are different), Soup Sieve will not and will throw an exception if you attempt
to do so.

In the following example, we will define our own custom selector called `#!css :--header` that will be an alias for
`#!css h1, h2, h3, h4, h5, h6`.

```py3
import soupsieve as sv
import bs4

markup = """
<html>
<body>
<h1 id="1">Header 1</h1>
<h2 id="2">Header 2</h2>
<p id="3"></p>
<p id="4"><span>child</span></p>
</body>
</html
"""

soup = bs4.BeautifulSoup(markup, 'lxml')
print(sv.select(':--header', soup, custom={':--header': 'h1, h2, h3, h4, h5, h6'}))
```

The above code, when run, should yield the following output:

```
[<h1 id="1">Header 1</h1>, <h2 id="2">Header 2</h2>]
```

Custom selectors can also be dependent upon other custom selectors. You don't have to worry about the order in the
dictionary as custom selectors will be compiled "just in time" when they are needed. Be careful though, if you create
a circular dependency, you will get a `SelectorSyntaxError`.

Assuming the same markup as in the first example, we will now create a custom selector that should find any element that
has child elements, we will call the selector `:--parent`. Then we will create another selector called
`:--parent-paragraph` that will use the `:--parent` selector to find `#!html <p>` elements that are also parents:

```py3
custom = {
    ":--parent": ":has(> *|*)",
    ":--parent-paragraph": "p:--parent"
}
print(sv.select(':--parent-paragraph', soup, custom=custom))
```

The above code will yield the only paragraph that is a parent:

```
[<p id="4"><span>child</span></p>]
```

## Namespaces

Many of Soup Sieve's selector functions take an optional namespace dictionary. Namespaces, just like CSS, must be
defined for Soup Sieve to evaluate `ns|tag` type selectors. This is analogous to CSS's namespace at-rule:

```css
@namespace url("http://www.w3.org/1999/xhtml");
@namespace svg url("http://www.w3.org/2000/svg");
```

A namespace dictionary should have keys (prefixes) and values (namespaces). An empty key string for a key would denote
the default key.  An empty value would essentially represent a null namespace.  To represent the above CSS example for
Soup Sieve, we would configure it like so:

```py3

namespace = {
    "": "http://www.w3.org/1999/xhtml",   # Default namespace is for XHTML
    "svg": "http://www.w3.org/2000/svg",  # The SVG namespace defined with prefix of "svg"
}
```

Prefixes used in the namespace dictionary do not have to match the prefixes in the document. The provided prefix is
never compared against the prefixes in the document, only the namespaces are compared. The prefixes in the document are
only there for the parser to know which tags get which namespace. And the prefixes in the namespace dictionary are only
defined in order to provide an alias for the namespaces when using the namespace selector syntax: `ns|name`.

Tags do not necessarily have to have a prefix for Soup Sieve to recognize them either.  For instance, in HTML5, SVG
*should* automatically get the SVG namespace. Depending how namespaces were defined in the document, tags may inherit
namespaces in some conditions.  Namespace assignment is mainly handled by the parser and exposed through the Beautiful
Soup API. Soup Sieve uses the Beautiful Soup API to then compare namespaces for supported documents.

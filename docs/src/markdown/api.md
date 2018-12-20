# API

Soup Sieve uses a subset of the CSS4 selector specification to detect and filter elements. To learn more about which specific selectors are implemented, see [CSS Selectors](./selectors.md).

Soup Sieve will detect the document type being used from the Beautiful Soup object that is given to it, and depending on the document type, its behavior may be slightly different:

- All HTML document types (HTML, HTML5, and XHTML) will have their tag names and attribute names treated without case sensitivity, like most browsers do. Though XHTML is XML, which traditionally is case sensitive, it will still be treated like HTML in this respect.

- XML document types will have their tag names and attribute names treated with case sensitivity.

- HTML5, XHTML and XML document types will have namespaces evaluated per the document's support (provided via the parser).

    `html5lib` provides proper namespaces for HTML5, but `lxml` will not. If you need namespace support for HTML5, consider using `html5lib`.

    For XML, `lxml` will provide proper namespaces. It is generally suggested that `lxml` is used to parse XHTML documents. Some additional configuration is required when using namespaces, see [Namespace](#namespaces) for more information.

- While attribute values are generally treated as case sensitive, HTML5, XHTML, and HTML treat the `type` attribute special. The `type` attribute's value is always case insensitive. This is generally how most browsers treat `type`. If you need `type` to be sensitive, you can use the `s` flag: `#!css [type="submit" s]`.

## `soupsieve.select()`

```py3
def select(select, parent, namespaces=None, limit=0, flags=0):
    """Select the specified tags."""
```

`select` will return all tags under the given tag that match the given CSS selectors provided. You can also limit the number of tags returned by providing a positive integer via the `limit` parameter (0 means to return all tags).

`select` accepts a CSS selector string, a `Tag`/`BeautifulSoup` object, an optional [namespace](#namespaces) dictionary, a `limit`, and `flags`.

```pycon3
>>> import soupsieve as sv
>>> sv.select('p:is(.a, .b, .c)', soup)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

## `soupsieve.iselect()`

```py3
def iselect(select, node, namespaces=None, limit=0, flags=0):
    """Select the specified tags."""
```

`iselect` is exactly like `select` except that it returns a generator instead of a list.

## `soupsieve.match()`

```py3
def match(select, tag, namespaces=None, flags=0):
    """Match node."""
```

The `match` function matches a given tag with a given CSS selector.

`match` accepts a CSS selector string, a `Tag`/`BeautifulSoup` object, an optional [namespace](#namespaces) dictionary, and flags.

```pycon3
>>> nodes = sv.select('p:is(.a, .b, .c)', soup)
>>> sv.match('p:not(.b)', nodes[0])
True
>>> sv.match('p:not(.b)', nodes[1])
False
```

## `soupsieve.filter()`

```py3
def filter(select, nodes, namespaces=None, flags=0):
    """Filter list of nodes."""
```

`filter` takes an iterable containing HTML nodes and will filter them based on the provided CSS selector string. If given a `Tag`/`BeautifulSoup` object, it will iterate the direct children filtering them.

`filter` accepts a CSS selector string, an iterable containing nodes, an optional [namespace](#namespaces) dictionary, and flags.

```pycon3
>>> sv.filter('p:not(.b)', soup.div)
[<p class="a">Cat</p>, <p class="c">Mouse</p>]
```

## `soupsieve.comments()`

```
def comments(parent, limit=0, flags=0):
    """Get comments only."""
```

The `comments` function can be used to extract all comments from a document or document tag. It will return comments from the given tag down through all of its children.  You can limit how many comments are returned with `limit`.

`comments` accepts a `Tag`/`BeautifulSoup` object, a `limit`, and flags.

## `soupsieve.icomments()`

```
def icomments(node, limit=0, flags=0):
    """Get comments only."""
```

`icomments` is exactly like `comments` except that it returns a generator instead of a list.

## `soupsieve.compile()`

```py3
def compile(pattern, namespaces=None, flags=0):
    """Compile CSS pattern."""
```

`compile` will pre-compile a CSS selector pattern returning a `SoupSieve` object. The `SoupSieve` object has the same selector functions available via the module without the need to specify the selector, namespaces, or flags.

```py3
class SoupSieve:
    """Match tags in Beautiful Soup with CSS selectors."""

    def match(self, tag):
        """Match."""

    def filter(self, iterable):
        """Filter."""

    def comments(self, parent, limit=0):
        """Get comments only."""

    def icomments(self, parent, limit=0):
        """Iterate comments only."""

    def select(self, parent, limit=0):
        """Select the specified tags."""

    def iselect(self, parent, limit=0):
        """Iterate the specified tags."""
```

## `soupsieve.purge()`

Soup Sieve caches compiled patterns for performance. If for whatever reason, you need to purge the cache, simply call `purge`.


## Namespaces

Many of Soup Sieve's selector functions take an optional namespace dictionary. Namespaces, just like CSS, must be defined for Soup Sieve to evaluate `ns|tag` type selectors. This is analogous to CSS's namespace at-rule:

```css
@namespace url("http://www.w3.org/1999/xhtml");
@namespace svg url("http://www.w3.org/2000/svg");
```

A namespace dictionary should have keys (prefixes) and values (namespaces). An empty key string for a key would denote the default key.  An empty value would essentially represent a null namespace.  To represent the above CSS example for Soup Sieve, we would configure it like so:

```py3

namespace = {
    "": "http://www.w3.org/1999/xhtml",   # Default namespace is for XHTML
    "svg": "http://www.w3.org/2000/svg",  # The SVG namespace defined with prefix of "svg"
}
```

Tags do not necessarily have to have a prefix for Soup Sieve to recognize them.  For instance, in HTML5, SVG *should* automatically get the SVG namespace. Depending how namespaces were defined in the documentation, tags may inherit namespaces in some conditions.  Namespace assignment is mainly handled by the parser and exposed through the Beautiful Soup API. Soup Sieve uses the Beautiful Soup API to then compare namespaces for supported documents.

--8<--
refs.txt
--8<--

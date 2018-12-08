## API

### `soupsieve.HTML5`

`HTML5` is a flag that instructs Soup Sieve to use HTML5 logic. When `HTML5` mode is used, Soup Sieve will take into account namespaces for known embedded HTML5 namespaces such as SVG. `HTML5` will also not compare tag names and attribute names with case sensitivity.

Keep in mind, that Soup Sieve itself is not responsible for deciding what tag has or does not have a namespace.  This is actually determined by the parser used in Beautiful Soup. This flag only tells Soup Sieve that the parser should be calculating namespaces, so it is okay to look at them. The user is responsible for using an appropriate parser for HTML5.  If using the [lxml][lxml] or [html5lib][html5lib] with Beautiful Soup, HTML5 namespaces *should* be accounted for in the parsing. If you are using Python's builtin HTML parser, this may not be the case.

### `soupsieve.HTML`

`HTML` is a flag that instructs Soup Sieve to use pre HTML5 logic. When `HTML` mode is used, Soup Sieve will not consider namespaces when evaluating elements. `HTML` will also not compare tag names  and attribute names with case sensitivity.

### `soupsieve.XML`

`XML` is a flag that instructs Soup Sieve to use XML logic. `XML` will cause Soup Sieve to take namespaces into considerations, and it will evaluate tag names and attribute names with case sensitivity. It will also relax what it considers valid tag name and attribute characters. It will also disable `.class` and `#id` selectors this is more an HTML concept.

### `soupsieve.XHTML`

`XHTML` is a flag that instructs Soup Sieve to use XHTML logic. This will cause Soup Sieve to take namespaces into considerations, and evaluate tag names and attributes names with no case sensitivity as this is how most browsers deal with XHTML tags. `.class` and `#id` are perfectly valid in XHTML.

It is recommend to use the `xml` mode in Beautiful Soup when parsing XHTML documents.

### `soupsieve.select()`

```py3
def select(select, node, namespaces=None, limit=0, mode=HTML5):
    """Select the specified tags."""
```

`select` given a tag, will select all tags that match the provided CSS selector string. You can give `limit` a positive integer to return a specific number tags (0 means to return all tags).

`select` accepts a CSS selector string, a `node` or element, an optional [namespace](#namespaces) dictionary, a `limit`, and a document `mode` (default is HTML5).

```pycon3
>>> import soupsieve as sv
>>> sv.select('p:is(.a, .b, .c)', soup)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

### `soupsieve.selectiter()`

```py3
def selectiter(select, node, namespaces=None, limit=0, mode=HTML5):
    """Select the specified tags."""
```

`selectiter` is exactly like `select` except that it returns a generator instead of a list.

### `soupsieve.match()`

```py3
def match(select, node, namespaces=None, mode=HTML5):
    """Match node."""
```

`match` matches a given node/element with a given CSS selector.

`match` accepts a CSS selector string, a `node` or element, an optional [namespace](#namespaces) dictionary, and document mode (default is HTML5).

```pycon3
>>> nodes = sv.select('p:is(.a, .b, .c)', soup)
>>> sv.match('p:not(.b)', nodes[0])
True
>>> sv.match('p:not(.b)', nodes[1])
False
```

### `soupsieve.filter()`

```py3
def filter(select, nodes, namespaces=None, mode=HTML5):
    """Filter list of nodes."""
```

`filter` takes an iterable containing HTML nodes and will filter them based on the provided CSS selector string. If given a Beautiful Soup tag, it will iterate the children that are tags.

`filter` accepts a CSS selector string, an iterable containing tags, an optional [namespace](#namespaces) dictionary, and document mode (default is HTML5).

```pycon3
>>> sv.filter('p:not(.b)', soup.div)
[<p class="a">Cat</p>, <p class="c">Mouse</p>]
```

### `soupsieve.comments()`

```
def comments(node, limit=0, mode=HTML5):
    """Get comments only."""
```

`comments` if useful to extract all comments from a document or document tag. It will extract from the given tag down through all of its children.  You can limit how many comments are returned with `limit`.

`comments` accepts a `node` or element, a `limit`, and a document mode.

### `soupsieve.commentsiter()`

```
def comments(node, limit=0, mode=HTML5):
    """Get comments only."""
```

`commentsiter` is exactly like `comments` except that it returns a generator instead of a list.

### `soupsieve.compile()`

```py3
def compile(pattern, namespaces=None, mode=HTML5):
    """Compile CSS pattern."""
```

`compile` will pre-compile a CSS selector pattern returning a `SoupSieve` object. The `SoupSieve` object has the same selector functions available via the module without the need to specify the selector, namespaces, or modes.

```py3
class SoupSieve:
    """Match tags in Beautiful Soup with CSS selectors."""

    def match(self, node):
        """Match."""

    def filter(self, nodes):
        """Filter."""

    def comments(self, node, limit=0):
        """Get comments only."""

    def select(self, node, limit=0):
        """Select the specified tags."""
```

### `soupsieve.purge()`

Soup Sieve caches compiled patterns for performance. If for whatever reason you need to purge the cache, simply call `purge`.


### Namespaces

Many of Soup Sieve's selector functions take an optional namespaces dictionary. Namespaces, just like CSS, must be defined for Soup Sieve to evaluate `ns|tag` type selectors. This is analogous to CSS's namespace at-rule:

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

Tags do not necessarily have to have a prefix for Soup Sieve to recognize them.  For instance, in HTML5, SVG *should* automatically get the SVG namespace. Depending how namespaces were defined in the documentation, tags may inherit namespaces in some conditions.  Namespace assignment is mainly handled by the parser and exposed through the Beautiful Soup API. Soup Sieve uses the Beautiful Soup API to then compare namespaces when the appropriate document that supports namespaces is set.

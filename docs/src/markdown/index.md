# Soup Sieve

## Overview

Soup Sieve is a CSS selector library designed to be used with [Beautiful Soup 4][bs4]. It aims to provide selecting, matching, and filtering using modern CSS selectors. Soup Sieve currently provides selectors from a subset of the CSS4 specification.

While Beautiful Soup comes with a builtin CSS selection API, it is not without issues. In addition, it also lacks support for some more modern CSS features.

Soup Sieve implements most of the CSS4 selectors, though there are a number that don't make sense in a non-browser environment. Selectors that cannot provide meaningful functionality simply do not match anything. Some of the supported selectors are:

- `#!css .classes`
- `#!css #ids`
- `#!css [attributes=value]`
- `#!css parent child`
- `#!css parent > child`
- `#!css sibling ~ sibling`
- `#!css sibling + sibling`
- `#!css :not(element.class, element2.class)`
- `#!css :is(element.class, element2.class)`
- `#!css parent:has(> child)`
- and many more

Checkout [CSS Selectors](./selectors.md) to see the full list.

## Installation

You must have Beautiful Soup already installed:

```
pip install beautifulsoup4
```

Then use `pip` to install Soup Sieve:

```
pip install soupsieve
```

If you want to manually install it, run `#!bash python setup.py build` and `#!bash python setup.py install`.

## Usage

To use Soup Sieve, you must create a `BeautifulSoup` object:

```pycon3
>>> import bs4

>>> text = """
... <div>
... <!-- These are animals -->
... <p class="a">Cat</p>
... <p class="b">Dog</p>
... <p class="c">Mouse</p>
... </div>
... """
>>> soup = bs4.BeautifulSoup(text, 'html5lib')
```

Then you can begin to use Soup Sieve to select a single tag:

```pycon3
>>> import soupsieve as sv
>>> sv.select_one('p:is(.a, .b, .c)', soup)
<p class="a">Cat</p>
```

To select all tags:

```pycon3
>>> import soupsieve as sv
>>> sv.select('p:is(.a, .b, .c)', soup)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

To filter:

```pycon3
>>> sv.filter('p:not(.b)', soup.div)
[<p class="a">Cat</p>, <p class="c">Mouse</p>]
```

To match:

```pycon3
>>> nodes = sv.select('p:is(.a, .b, .c)', soup)
>>> sv.match(nodes[0], 'p:not(.b)')
True
>>> sv.match(nodes[1], 'p:not(.b)')
False
```

Or even just extracting comments:

```pycon3
>>> sv.comments(soup)
[' These are animals ']
```

Selectors do not have to be constrained to one line either. You can span selectors over multiple lines just like you would in a CSS file.

```pycon3
>>> selector = """
... .a,
... .b,
... .c
... """
>>> sv.select(selector, soup)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

You can even use comments to annotate a particularly complex selector.

```pycon3
>>> selector = """
... /* This isn't complicated, but we're going to annotate it anyways.
...    This is the a class */
... .a,
... /* This is the b class */
... .b,
... /* This is the c class */
... .c
... """
>>> sv.select(selector, soup)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

If you've ever used Python's Re library for regular expressions, you may know that it is often useful to pre-compile a regular expression pattern, especially if you plan to use it more than once.  The same is true for Soup Sieve's matchers, though is not required.  If you have a pattern that you want to use more than once, it may be wise to pre-compile it early on:

```pycon3
>>> selector = sv.compile('p:is(.a, .b, .c)')
>>> selector.filter(soup.div)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

A compiled object has all the same methods, though the parameters will be slightly different as they don't need things like the pattern or flags once compiled. See [API](./api.md) documentation for more info.

Compiled patterns are cached, so if for any reason you need to clear the cache, simply issue the `purge` command.

```pycon3
>>> sv.purge()
```

--8<--
refs.txt
--8<--

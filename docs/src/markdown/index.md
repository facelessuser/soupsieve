# Soup Sieve

## Overview

Soup Sieve is a CSS4 selector library designed to be used with [Beautiful Soup 4][bs4]. It aims to provide selecting, matching, and filtering with using modern CSS selectors.

While Beautiful Soup comes with a builtin CSS selection API, it is not without issues. In addition, it also lacks support for some more modern CSS features.

Soup Sieve supports a subset of CSS4 selectors which allows for filtering of tags in a Beautiful Soup object. Soup
Sieve does not attempt to support all CSS4 selectors as many don't make sense in a non-browser environment. Some of the supported selectors are:

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

```
pip install soupsieve
```

## Usage

Using Soup Sieve is easy. Simply create a Beautiful Soup object:

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

Then create you can begin to use Soup Sieve to select:

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

If you've ever used Python's Re library for regular expression, you may know that it is often useful to pre-compile a regular expression pattern, especially if you plan to use it more than once.  The same is true for Soup Sieve's matchers.  If you have a pattern that you want to use more than once, it may be wise to pre-compile it early on:

```pycon3
>>> selector = sv.compile('p:is(.a, .b, .c)')
>>> selector.filter(soup.div)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

A compiled object has all the same methods.

--8<--
refs.txt
--8<--

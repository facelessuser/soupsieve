# Quick Start

## Overview

Soup Sieve is a CSS selector library designed to be used with [Beautiful Soup 4][bs4]. It aims to provide selecting,
matching, and filtering using modern CSS selectors. Soup Sieve currently provides selectors from the CSS level 1
specifications up through the latest CSS level 4 drafts and beyond (though some are not yet implemented).

Soup Sieve was written with the intent to replace Beautiful Soup's builtin select feature, and as of Beautiful Soup
version 4.7.0, it now is :confetti_ball:. Soup Sieve can also be imported in order to use its API directly for
more controlled, specialized parsing.

Soup Sieve has implemented most of the CSS selectors up through the latest CSS draft specifications, though there are a
number that don't make sense in a non-browser environment. Selectors that cannot provide meaningful functionality simply
do not match anything. Some of the supported selectors are:

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
- and [many more](./selectors/index.md)

## Installation

You must have Beautiful Soup already installed:

```
pip install beautifulsoup4
```

In most cases, assuming you've installed version 4.7.0, that should be all you need to do, but if you've installed via
some alternative method, and Soup Sieve is not automatically installed, you can install it directly:

```
pip install soupsieve
```

If you want to manually install it from source, first ensure that [`build`][build] is installed:

```
pip install build
```

Then navigate to the root of the project and build the wheel and install (replacing `<ver>` with the current version):

```
python -m build -w
pip install dist/soupsive-<ver>-py3-none-any.whl
```

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

For most people, using the Beautiful Soup 4.7.0+ API may be more than sufficient. Beautiful Soup offers two methods that employ
Soup Sieve: `select` and `select_one`. Beautiful Soup's select API is identical to Soup Sieve's, except that you don't
have to hand it the tag object, the calling object passes itself to Soup Sieve:

```pycon3
>>> soup = bs4.BeautifulSoup(text, 'html5lib')
>>> soup.select_one('p:is(.a, .b, .c)')
<p class="a">Cat</p>
```

```pycon3
>>> soup = bs4.BeautifulSoup(text, 'html5lib')
>>> soup.select('p:is(.a, .b, .c)')
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

You can also use the Soup Sieve API directly to get access to the full range of possibilities that Soup Sieve offers.
You can select a single tag:

```pycon3
>>> import soupsieve as sv
>>> sv.select_one('p:is(.a, .b, .c)', soup)
<p class="a">Cat</p>
```

You can select all tags:

```pycon3
>>> import soupsieve as sv
>>> sv.select('p:is(.a, .b, .c)', soup)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

You can select the closest ancestor:

```pycon3
>>> import soupsieve as sv
>>> el = sv.select_one('.c', soup)
>>> sv.closest('div', el)
<div>
<!-- These are animals -->
<p class="a">Cat</p>
<p class="b">Dog</p>
<p class="c">Mouse</p>
</div>
```

You can filter a tag's Children (or an iterable of tags):

```pycon3
>>> sv.filter('p:not(.b)', soup.div)
[<p class="a">Cat</p>, <p class="c">Mouse</p>]
```

You can match a single tag:

```pycon3
>>> els = sv.select('p:is(.a, .b, .c)', soup)
>>> sv.match(els[0], 'p:not(.b)')
True
>>> sv.match(els[1], 'p:not(.b)')
False
```

Or even just extract comments:

```pycon3
>>> sv.comments(soup)
[' These are animals ']
```

Selectors do not have to be constrained to one line either. You can span selectors over multiple lines just like you
would in a CSS file.

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

If you've ever used Python's Re library for regular expressions, you may know that it is often useful to pre-compile a
regular expression pattern, especially if you plan to use it more than once.  The same is true for Soup Sieve's
matchers, though is not required.  If you have a pattern that you want to use more than once, it may be wise to
pre-compile it early on:

```pycon3
>>> selector = sv.compile('p:is(.a, .b, .c)')
>>> selector.filter(soup.div)
[<p class="a">Cat</p>, <p class="b">Dog</p>, <p class="c">Mouse</p>]
```

A compiled object has all the same methods, though the parameters will be slightly different as they don't need things
like the pattern or flags once compiled. See [API](./api.md) documentation for more info.

Compiled patterns are cached, so if for any reason you need to clear the cache, simply issue the `purge` command.

```pycon3
>>> sv.purge()
```

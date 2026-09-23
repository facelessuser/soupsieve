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

-   `#!css .classes`
-   `#!css #ids`
-   `#!css [attributes=value]`
-   `#!css parent child`
-   `#!css parent > child`
-   `#!css sibling ~ sibling`
-   `#!css sibling + sibling`
-   `#!css :not(element.class, element2.class)`
-   `#!css :is(element.class, element2.class)`
-   `#!css parent:has(> child)`
-   and [many more](./selectors/index.md)

## Installation

You must have Beautiful Soup already installed:

```console
$ pip install beautifulsoup4
```

In most cases, assuming you've installed version 4.7.0, that should be all you need to do, but if you've installed via
some alternative method, and Soup Sieve is not automatically installed, you can install it directly:

```console
$ pip install soupsieve
```

If you want to manually install it from source, first ensure that [`build`][build] is installed:

```console
$ pip install build
```

Then navigate to the root of the project and build the wheel and install (replacing `<ver>` with the current version):

```console
$ python -m build -w
$ pip install dist/soupsive-<ver>-py3-none-any.whl
```

## Usage

To use Soup Sieve, you must create a `BeautifulSoup` object:

```py play session="example"
from bs4 import BeautifulSoup
text = """
<div>
<!-- These are animals -->
<p class="a">Cat</p>
<p class="b">Dog</p>
<p class="c">Mouse</p>
</div>
"""
soup = BeautifulSoup(text, 'html5lib')
```

For most people, using the Beautiful Soup 4.7.0+ API may be more than sufficient. Beautiful Soup offers two methods that
employ Soup Sieve: `select` and `select_one`. Beautiful Soup's select API is identical to Soup Sieve's, except that you
don't have to hand it the tag object, the calling object passes itself to Soup Sieve:

```py play session="example"
soup.select_one('p:is(.a, .b, .c)')
```

```py play session="example"
soup.select('p:is(.a, .b, .c)')
```

You can also use the Soup Sieve API directly to get access to the full range of possibilities that Soup Sieve offers.
You can select a single tag:

```py play session="example"
import soupsieve as sv
sv.select_one('p:is(.a, .b, .c)', soup)
```

You can select all tags:

```py play session="example"
import soupsieve as sv
sv.select('p:is(.a, .b, .c)', soup)
```

You can select the closest ancestor:

```py play session="example"
import soupsieve as sv
el = sv.select_one('.c', soup)
sv.closest('div', el)
```

You can filter a tag's Children (or an iterable of tags):

```py play session="example"
sv.filter('p:not(.b)', soup.div)
```

You can match a single tag:

```py play session="example"
els = sv.select('p:is(.a, .b, .c)', soup)
sv.match('p:not(.b)', els[0])
sv.match('p:not(.b)', els[1])
```

Selectors do not have to be constrained to one line either. You can span selectors over multiple lines just like you
would in a CSS file.

```py play session="example"
selector = """
.a,
.b,
.c
"""
sv.select(selector, soup)
```

You can even use comments to annotate a particularly complex selector.

```py play session="example"
selector = """
/* This isn't complicated, but we're going to annotate it anyways.
   This is the a class */
.a,
/* This is the b class */
.b,
/* This is the c class */
.c
"""
sv.select(selector, soup)
```

If you've ever used Python's Re library for regular expressions, you may know that it is often useful to pre-compile a
regular expression pattern, especially if you plan to use it more than once.  The same is true for Soup Sieve's
matchers, though is not required.  If you have a pattern that you want to use more than once, it may be wise to
pre-compile it early on:

```py play session="example"
selector = sv.compile('p:is(.a, .b, .c)')
selector.filter(soup.div)
```

A compiled object has all the same methods, though the parameters will be slightly different as they don't need things
like the pattern or flags once compiled. See [API](./api.md) documentation for more info.

Compiled patterns are cached, so if for any reason you need to clear the cache, simply issue the `purge` command.

```py play session="example"
sv.purge()
```

## Security Concerns

Soup Sieve is a library built for Beautiful Soup that takes user specified CSS language style inputs and uses them to
walk the HTML/XML tree and return elements according to the CSS Specification. While performance concerns are taken
seriously, not all selectors are equal in regard to performance as specified via the CSS specification.

Soup Sieve attempts to do various tricks to help improve performance, but some selectors will always have non-linear
performance in certain situations.

Selectors like the descendant and subsequent sibling combinators (`#!css a b` and `#!css a ~ b`) often cause entire
subtrees of the main document tree to be crawled when evaluating a single element. If used poorly, this can impact
performance in a non-linear ways. It should be noted that Soup Sieve employs caching to reduce performance concerns
in various cases, but there will always be the potential produce non-linear cases simply due to how the selectors work.

Selectors like the `#!css :nth-*` family of selectors will evaluate numerous children under one parent to find a
suitable element. These can also be a potential concern for performance if used poorly. Soup Sieve also employs caching
in these cases to dramatically improve performance in a number of problematic circumstances, but again, there will
likely always be some cases that will exhibit performance that is inferior to other cases.

The `#!css :has()` selector acts like a lookahead in regular expression. And paired with  descendant and subsequent
sibling combinators, can exhibit non-linear performance. Much like regular expression lookaheads, it is an extremely
powerful selector, but will always open the door for poor performance if not used thoughtfully.

The `#!css :-soup-contains()` selector is also a very useful selector that can crawl entire subtrees of the main
document tree. This is by design, and provides useful utility, but admittedly, if not used in an intelligent manner,
using tight patterns to narrow the scope of operation, can degrade performance.

This is not an exhaustive list of all possibilities in which CSS selectors can be performance bottleneck, but is meant
to accomplish a few things.

1.  Make clear to all users that taking untrusted user input in a time critical system, without any kind of mitigation
    to abort long running operations will open you up to performance concerns.

2.  Encourage users, before deploying solutions, to test understand how the selectors work, and thoughtfully apply them
    after testing them .

As always, we here at Soup Sieve are happy to hear about real performance concerns that are within our power to improve,
and will always take them seriously, but it should be noted that exposing time critical systems, with large document
trees, to untrusted user inputs, will open you up to performance related exploits.

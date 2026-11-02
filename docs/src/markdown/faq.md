---
icon: lucide/message-circle-question-mark
---
# Frequent Asked Questions

## Why do selectors not work the same in Beautiful Soup 4.7+?

Soup Sieve is the official CSS selector library in Beautiful Soup 4.7+, and with this change, Soup Sieve introduces a
number of changes that break some of the expected behaviors that existed in versions prior to 4.7.

In short, Soup Sieve follows the CSS specifications fairly close, and this broke a number of non-standard behaviors.
These non-standard behaviors were not allowed according to the CSS specifications. Soup Sieve has no intentions of
bringing back these behaviors.

For more details on specific changes, and the reasoning why a specific change is considered a good change, or simply a
feature that Soup Sieve cannot/will not support, see [Beautiful Soup Differences](./differences.md).

## How does `#!html <template>` handling work? {#how-does-template-handling-work}

> [!new] New in 4.0

The contents of an HTML `#!html <template>` are not part of the document. They are held for later use, and in a web
browser, they are kept in a separate document fragment that is available from the `content` property of the element.
Soup Sieve treats them the same way: selectors do not descend into a `#!html <template>`, and elements inside one can't
see anything outside of it. This is true of everything, including combinators and pseudo-classes like
[`#!css :lang()`](./selectors/pseudo-classes.md#:lang), [`#!css :disabled`](./selectors/pseudo-classes.md#:disabled),
and [`#!css :default`](./selectors/pseudo-classes.md#:default). A `#!html <template>` itself is an element like any
other that can be selected, but it is considered to have no children.

Beautiful Soup has no `content` property, so to select the contents, call `select` on the `#!html <template>`.

```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<div>
<template><p>Template content</p></template>
</div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
print(soup.select('p'))
print(soup.template.select('p'))
print(soup.template.select('div p'))
```

Any `#!html <template>` within the contents is not entered, select from that `#!html <template>` to get its contents.

This only applies to HTML elements. Something like `#!html <svg><template>` is not an HTML `#!html <template>`, so it
has normal children, but only parsers that provide namespaces can make that distinction.

## How does `#!html <iframe>` handling work? {#how-does-iframe-handling-work}

> [!new] Changed in 4.0

In a web browser, the document that an `#!html <iframe>` displays comes from its `src` or `srcdoc` attribute and is
kept separately from the document the `#!html <iframe>` is in. It is not the content of the `#!html <iframe>` element,
and selectors called on the outer document never reach it. Beautiful Soup does not load these documents, so Soup Sieve
never sees them.

What is between `#!html <iframe>` and `#!html </iframe>` is something else. Browsers parse it as text, and recent
versions of Python's `html.parser`, `lxml`, and `html5lib` do the same, so in HTML, an `#!html <iframe>` only ever
contains text. Like in a browser, that text is part of the `#!html <iframe>`: the `#!html <iframe>` is not
[`#!css :empty`](./selectors/pseudo-classes.md#:empty), the text is used to find the direction of an element with
`#!html dir="auto"`, and [`#!css :-soup-contains()`](./selectors/pseudo-classes.md#:-soup-contains) sees it.

Older versions of Python may have an `html.parser` that still does not escape this content, in those cases, the raw
elements under it will be treated like normal children.

```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<div>
<iframe><p>Frame content</p></iframe>
</div>
</body>
</html>
"""
soup = bs(html, 'html.parser')
print(soup.select('iframe p'))
print(soup.select('iframe:-soup-contains("<p>")'))
```

Elements only end up inside an `#!html <iframe>` in XHTML, older versions of Python, or when they are added to the tree
by hand. Browsers treat these as normal children of the `#!html <iframe>`, and so does Soup Sieve. They can be selected
with combinators like any other element, and they are part of the same document, so they inherit things like the
language, direction, and editability of the elements around them, and they belong to the forms around them.

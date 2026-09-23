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

## How does `#!html <iframe>` handling work?

> [!note]
> Recent versions of Python's `html.parser`, `lxml`, and `html5lib` all seem to escape `iframe` content.

In web browsers, CSS selectors do not usually select content inside an `#!html <iframe>` element if the selector is
called on an element outside of the `iframe`. Each HTML document is usually encapsulated and CSS selector leakage across
this `#!html <iframe>` boundary is usually prevented.

In it's current iteration, Soup Sieve is not aware of the origin of the documents in the `#!html <iframe>`, and Soup
Sieve will not prevent selectors from crossing these boundaries. Soup Sieve is not used to style documents, but to
scrape documents. For this reason, it seems to be more helpful to allow selector combinators to cross these boundaries.

Soup Sieve isn't entirely unaware of `#!html <iframe>` elements though. In Soup Sieve 1.9.1, it was noticed that some
pseudo-classes behaved in unexpected ways without awareness to `#!html <iframe>`, this was fixed in 1.9.1.
Pseudo-classes such as [`#!css :default`](./selectors/pseudo-classes.md#:default),
[`#!css :indeterminate`](./selectors/pseudo-classes.md#:indeterminate), [`#!css :dir()`](./selectors/pseudo-classes.md#:dir),
[`:lang()`](./selectors/pseudo-classes.md#:lang), [`#!css :root`](./selectors/pseudo-classes.md#:root), and
[`#!css :contains()`](./selectors/pseudo-classes.md#:-soup-contains) were given awareness of `#!html <iframe>` elements
to ensure they behaved properly and returned the expected elements. This doesn't mean that `select` won't return
elements in an `#!html <iframe>`, but it won't allow something like `#!css :default` to select a `#!html <button>` in an
`#!html <iframe>` whose parent `#!html <form>` is outside the `#!html <iframe>`. Or better put, a default
`#!html <button>` will be evaluated in the context of the document it is in.

With all of this said, if your selectors have issues with `#!html <iframe>` elements, it is most likely because
`#!html <iframe>` elements are handled differently by different parsers. `html.parser` will usually parse
`#!html <iframe>` elements as it sees them. `lxml` parser will often remove `#!html <html>` and `#!html <body>` tags of
an `#!html <iframe>` HTML document. `lxml-xml` will simply ignore the content in a XHTML document. And `html5lib` will
HTML escape the content of an `#!html <iframe>` making traversal impossible.

In short, Soup Sieve will return elements from all documents, even `#!html <iframe>` elements. But certain
pseudo-classes may take into consideration the context of the document they are in. But even with all of this, a
parser's handling of `#!html <iframe>` elements may make handling its content difficult if it doesn't parse it as HTML
	elements, or augments its structure.

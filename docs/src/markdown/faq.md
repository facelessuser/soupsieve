# Frequent Asked Questions

## Why do selectors not work the same in Beautiful Soup 4.7+?

Soup Sieve is the official CSS selector library in Beautiful Soup 4.7+, and with this change, Soup Sieve introduces a
number of changes that break some of the expected behaviors that existed in versions prior to 4.7.

In short, Soup Sieve follows the CSS specifications fairly close, and this broke a number of non-standard behaviors.
These non-standard behaviors were not allowed according to the CSS specifications. Soup Sieve has no intentions of
bringing back these behaviors.

For more details on specific changes, and the reasoning why a specific change is considered a good change, or simply a
feature that Soup Sieve cannot/will not support, see [Beautiful Soup Differences](./differences.md).

## How does `iframe` handling work?

In web browsers, CSS selectors do not usually select content inside an `iframe` element if the selector is called on an
element outside of the `iframe`. Each HTML document is usually encapsulated and CSS selector leakage across this
`iframe` boundary is usually prevented.

In it's current iteration, Soup Sieve is not aware of the origin of the documents in the `iframe`, and Soup Sieve will
not prevent selectors from crossing these boundaries. Soup Sieve is not used to style documents, but to scrape
documents. For this reason, it seems to be more helpful to allow selector combinators to cross these boundaries.

Soup Sieve isn't entirely unaware of `iframe` elements though. In Soup Sieve 1.9.1, it was noticed that some
pseudo-classes behaved in unexpected ways without awareness to `iframes`, this was fixed in 1.9.1. Pseudo-classes such
as [`:default`](./selectors/pseudo-classes.md#:default), [`:indeterminate`](./selectors/pseudo-classes.md#:indeterminate),
[`:dir()`](./selectors/pseudo-classes.md#:dir), [`:lang()`](./selectors/pseudo-classes.md#:lang),
[`:root`](./selectors/pseudo-classes.md#:root), and [`:contains()`](./selectors/pseudo-classes.md#:contains) where
given awareness of `iframes` to ensure they behaved properly and returned the expected elements. This doesn't mean that
`select` won't return elements in `iframes`, but it won't allow something like `:default` to select a `button` in an
`iframe` whose parent `form` is outside the `iframe`. Or better put, a default `button` will be evaluated in the context
of the document it is in.

With all of this said, if your selectors have issues with `iframes`, it is most likely because `iframes` are handled
differently by different parsers. `html.parser` will usually parse `iframe` elements as it sees them. `lxml` parser will
often remove `html` and `body` tags of an `iframe` HTML document. `lxml-xml` will simply ignore the content in a XHTML
document. And `html5lib` will HTML escape the content of an `iframe` making traversal impossible.

In short, Soup Sieve will return elements from all documents, even `iframes`. But certain pseudo-classes may take into
consideration the context of the document they are in. But even with all of this, a parser's handling of `iframes` may
make handling its content difficult if it doesn't parse it as HTML elements, or augments its structure.

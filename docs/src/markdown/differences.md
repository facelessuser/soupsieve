# Beautiful Soup Differences

Soup Sieve is the official CSS "select" implementation of Beautiful Soup 4.7.0+. While the inclusion of Soup Sieve fixes
many issues and greatly expands CSS support in Beautiful Soup, it does introduce some differences which may surprise
some who've become accustom to the old "select" implementation.

Beautiful Soup's old select method had numerous limitations and quirks that do not align with the actual CSS
specifications. Most are insignificant, but there are a couple differences that people over the years had come to rely
on. Soup Sieve, which aims to follow the CSS specification closely, does not support these differences.

## Attribute Values

Beautiful Soup was very relaxed when it came to attribute values in selectors: `#!css [attribute=value]`. Beautiful
Soup would allow almost anything for a valid unquoted value. Soup Sieve, on the other hand, follows the CSS
specification and requires that a value be a valid identifier, or it must be quoted. If you get an error complaining
about a malformed attribute, you may need to quote the value.

For instance, if you previously used a selector like this:

```py3
soup.select('[attr={}]')
```

You would need to quote the value as `{}` is not a valid CSS identifier, so it must be quoted:

```py3
soup.select('[attr="{}"]')
```

You can also use the [escape](./api.md#soupsieveescape) function to escape dynamic content:

```py3
import soupsieve
soup.select('[attr=%s]' % soupsieve.escape('{}'))
```

## CSS Identifiers

Since Soup Sieve follows the CSS specification, class names, id names, tag names, etc. must be valid identifiers. Since
identifiers, according to the CSS specification, cannot *start* with a number, some users may find that their old class,
id, or tag name selectors that started with numbers will not work. To specify such selectors, you'll have to use CSS
escapes.

So if you used to use:

```py3
soup.select('.2class')
```

You would need to update with:

```py3
soup.select(r'.\32 class')
```

Numbers in the middle or at the end of a class will work as they always did:

```py3
soup.select('.class2')
```

## Relative Selectors

Whether on purpose or on accident, Beautiful Soup used to allow relative selectors:

```py3
soup.select('> div')
```

The above is not a valid CSS selector according the CSS specifications. Relative selector lists have only recently been
added to the CSS specifications, and they are only allowed in a `#!css :has()` pseudo-class:

```css
article:has(> div)
```

But, in the level 4 CSS specifications, the `:scope` pseudo-class has been added which allows for the same feel as using
`#!css > div`. Since Soup Sieve supports the `:scope` pseudo-class, it can be used to produce the same behavior as the
legacy select method.

In CSS, the `:scope` pseudo-class represents the element that the CSS select operation is called on. In supported
browsers, the following JavaScript example would treats `:scope` as the element that `el` references:

```js
el.querySelectorAll(':scope > .class')
```

Just like in the JavaScript example above, Soup Sieve would also treat `:scope` as the element that `el` references:

```py3
el.select(':scope > .class')
```

In the case where the element is the document node, `:scope` would simply represent the root element of the document.

So, if you used to to have selectors such as:

```py3
soup.select('> div')
```

You can simply add `:scope`, and it should work the same:

```py3
soup.select(':scope > div')
```

While this will generally give you what is expected for the relative, descendant selectors, this will not work for
sibling selectors, and the reasons why are covered in more details in [Out of Scope Selectors](#out-of-scope-selectors).

## Out of Scope Selectors

In a browser, when requesting a selector via `querySelectorAll`, the element that `querySelectorAll` is called on is
the *scoped* element. So in the following example, `el` is the *scoped* element.

```js
el.querySelectorAll('.class')
```

This same concept applies to Soup Sieve, where the element that `select` or `select_one` is called on is also the
*scoped* element. So in the following example, `el` is also the *scoped* element:

```py3
el.select('.class')
```

In browsers, `querySelectorAll` and `querySelector` only return elements under the *scoped* element. They do not return
the *scoped* element itself, its parents, or its siblings. Only when `querySelectorAll` or `querySelector` is called on
the document node will it return the *scoped* selector, which would be the *root* element, as the query is being called
on the document itself and not the *scoped* element.

Soup Sieve aims to essentially mimic the browser functions such as `querySelector`, `querySelectorAll`, `matches`, etc.
In Soup Sieve `select` and `select_one` are analogous to `querySelectorAll` and `querySelector` respectively. For this
reason, Soup Sieve also only returns elements under the *scoped* element. The idea is to provide a familiar interface
that behaves, as close as possible, to what people familiar with CSS selectors are used to.

So while Soup Sieve will find elements relative to `:scope` with `>` or <code>&nbsp;</code>:

```py3
soup.select(':scope > div')
```

It will not find elements relative to `:scope` with `+` or `~` as siblings to the *scoped* element are not under the
*scoped* element:

```py3
soup.select(':scope + div')
```

This is by design and is in align with the behavior exhibited in all web browsers.

## Selected Element Order

Another quirk of Beautiful Soup's old implementation was that it returned the HTML nodes in the order of how the
selectors were defined. For instance, Beautiful Soup, if given the pattern `#!css article, body` would first return
`#!html <article>` and then `#!html <body>`.

Soup Sieve does not, and frankly cannot, honor Beautiful Soup's old ordering convention due to the way it is designed.
Soup Sieve returns the nodes in the order they are defined in the document as that is how the elements are searched.
This much more efficient and provides better performance.

So, given the earlier selector pattern of `article, body`, Soup Sieve would return the element `#!html <body>` and then
`#!html <article>` as that is how it is ordered in the HTML document.

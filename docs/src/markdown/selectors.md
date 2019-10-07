# CSS Selectors

## Overview

The CSS selectors are based off of the CSS specification and includes not only stable selectors, but may also include
selectors currently under development from the draft specifications. Primarily support has been added for selectors that
were feasible to implement and most likely to get practical use. In addition to the selectors in the specification,
Soup Sieve also supports a couple non-standard selectors.

Soup Sieve aims to allow users to target XML/HTML elements with CSS selectors. It implements many pseudo classes, but it
does not currently implement any pseudo elements and has no plans to do so. Soup Sieve also will not match anything for
pseudo classes that are only relevant in a live, browser environment, but it will gracefully handle them if they've been
implemented; such pseudo classes are non-applicable in the Beautiful Soup environment and are noted in [Non-Applicable
Pseudo Classes](#non-applicable-pseudo-classes).

When speaking about namespaces, they only apply to XML, XHTML, or when dealing with recognized foreign tags in HTML5.
Currently, Beautiful Soup's `html5lib` parser is the only parser that will return the appropriate namespaces for a HTML5
document. If you are using XHTML, you have to use the Beautiful Soup's `lxml-xml` parser (or `xml` for short) to get the
appropriate namespaces in an XHTML document. In addition to using the correct parser, you must provide a dictionary of
namespaces to Soup Sieve in order to use namespace selectors. See the documentation on [namespaces](./api.md#namespaces)
to learn more.

While an effort is made to mimic CSS selector behavior, there may be some differences or quirks, please report issues if
any are found.

<table markdown="1">
<tr>
    <th>Symbol</th>
    <th>Description</th>
</tr>
<tr markdown="1">
<td><span class="html5"></span></td>
<td markdown="1">
Some selectors are very specific to HTML and either have no meaningful representation in XML, or such functionality has
not been implemented. Selectors that are HTML only will be noted with <span class="html5"></span>,
and will match nothing if used in XML.
</td>
</tr>
<tr markdown="1">
<td><span class="star"></span></td>
<td markdown="1">
Soup Sieve has implemented a couple non-standard selectors. These can contain useful selectors that were rejected
from the official CSS specifications, selectors implemented by other systems such as JQuery, or even selectors
specifically created for Soup Sieve. If a selector is considered non standard, it will be marked with
<span class="star"></span>.
</td>
</tr>
<tr markdown="1">
<td><span class="lab"></span></td>
<td markdown="1">
All selectors that are from the current working draft of CSS4 are considered experimental and are marked with
<span class="lab"></span>. Additionally, if there are other immature selectors, they may be marked as experimental as
well. Experimental may mean we are not entirely sure if our implementation is correct, that things may still be in flux
as they are part of a working draft, or even both.

If at anytime a working draft drops a selector from the current draft, it will most likely also be removed here,
most likely with a deprecation path, except where there may be a conflict that requires a less graceful transition.
One exception is in the rare case that the selector is found to be far too useful despite being rejected. In these
cases, we may adopt them as "custom" selectors.
</td>
</tr>
</table>

!!! tip "Additional Reading"
    If usage of a selector is not clear in this documentation, you can find more information by reading these specification
    documents:

    [CSS Level 3 Specification](https://www.w3.org/TR/selectors-3/)
    : Contains the latest official document outlying official behaviors of CSS selectors.

    [CSS Level 4 Working Draft](https://www.w3.org/TR/selectors-4/)
    : Contains the latest published working draft of the CSS level 4 selectors which outlines the experimental new
    selectors and experimental behavioral changes.

    [HTML5](https://www.w3.org/TR/html50/)
    : The HTML 5.0 specification document. Defines the semantics regarding HTML.

    [HTML Living Standard](https://html.spec.whatwg.org/)
    : The HTML Living Standard document. Defines semantics regarding HTML.

## Selector Terminology

Certain terminology is used throughout this document when describing selectors. In order to fully understand the syntax
a selector may implement, it is important to understand a couple of key terms.

### Selector

Selector is used to describe any selector whether it is a [simple](#simple-selector), [compound](#compound-selector), or
[complex](#complex-selector) selector.

### Simple Selector

A simple selector represents a single condition on an element. It can be a [type selector](#type-selectors),
[universal selector](#universal-selectors), [ID selector](#id-selectors), [class selector](#class-selectors),
[attribute selector](#attribute-selectors), or [pseudo class selector](#pseudo-classes).

### Compound Selector

A [compound](#compound-selector) selector is a sequence of [simple](#simple-selector) selectors. They do not contain any
[combinators](#combinators-and-selector-lists). If a universal or type selector is used, they must come first, and only
one instance of either a universal or type selector can be used, both cannot be used at the same time.

### Complex Selector

A complex selector consists of multiple [simple](#simple-selector) or [compound](#compound-selector) selectors joined
with [combinators](#combinators-and-selector-lists).

### Selector List

A selector list is a list of selectors joined with a comma (`,`). A selector list is used to specify that a match is
valid if any of the selectors in a list matches.

## Escapes

Soup Sieve selectors support using CSS escapes. So if you need provide Unicode, or non-standard characters, you can use
CSS style escapes.

Escapes can be specified with a backslash followed by 1 - 6 hexadecimal digits: `#!css \20AC`, `#!css \0020AC`, etc. If
you need to terminate an escape to avoid it accumulating unintended hexadecimal characters, you can use a space:
`#!css \0020AC dont-escape-me`. You can also escape any non-hexadecimal character, and it will be treated as that
character: `#!css \+` --> `+`. The one exception is that you cannot escape the form feed, newline, or carriage
return.

You can always use Soup Sieve's [escape command](./api.md#soupsieveescape) to escape identifiers as well.

## Basic Selectors

### Type Selectors

Type selectors match elements by node name.

If a default namespace is defined in the [namespace dictionary](./api.md#namespaces), and no
[namespace](#namespace-selectors) is explicitly defined, it will be assumed that the element must be in the default
namespace.

```css tab="Syntax"
element
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
...   <div>Here is some text.</div>
...   <div>Here is some more text.</div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('div'))
[<div>Here is some text.</div>, <div>Here is some more text.</div>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/Type_selectors

### Universal Selectors

The Universal selector (`*`) matches elements of any type.

```css tab="Syntax"
*
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
...    <p>Here is some text.</p>
...    <div>Here is some more text.</div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('*'))
[<html><head></head>
<body>
   <div>Here is some text.</div>
   <div>Here is some more text.</div>


</body></html>, <head></head>, <body>
   <div>Here is some text.</div>
   <div>Here is some more text.</div>


</body>, <div>Here is some text.</div>, <div>Here is some more text.</div>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/Universal_selectors

### ID Selectors

The ID selector matches an element based on its `id` attribute. The ID must match exactly.

```css tab="Syntax"
#id
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
...    <div id="some-id">Here is some text.</div>
...    <div>Here is some more text.</div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('#some-id'))
[<div id="some-id">Here is some text.</div>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/ID_selectors

!!! note "XML Support"
    While the use of the `id` attribute (in the context of CSS) is a very HTML centric idea, it is supported for XML as
    well because Beautiful Soup supported it before Soup Sieve's existence.

### Class Selectors

The class selector matches an element based on the values contained in the `class` attribute. The `class` attribute is
treated as a whitespace separated list, where each item is a **class**.

```css tab="Syntax"
.class
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
...    <div class="some-class">Here is some text.</div>
...    <div>Here is some more text.</div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('.some-class'))
[<div class="some-class">Here is some text.</div>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/Class_selectors

!!! note "XML Support"
    While the use of the `class` attribute (in the context of CSS) is a very HTML centric idea, it is supported for XML
    as well because Beautiful Soup supported it before Soup Sieve's existence.

### Attribute Selectors

The attribute selector matches an element based on its attributes. When specifying a value of an attribute, if it
contains whitespace or special characters, you should quote them with either single or double quotes.

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors

`[attribute]`
: 
    Represents elements with an attribute named **attribute**.

    ```css tab="Syntax"
    [attr]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <ul>
    ...   <li><a href="#internal">Internal link</a></li>
    ...   <li><a href="http://example.com">Example link</a></li>
    ...   <li><a href="#InSensitive">Insensitive internal link</a></li>
    ...   <li><a href="http://example.org">Example org link</a></li>
    ... </ul>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('[href]'))
    [<a href="#internal">Internal link</a>, <a href="http://example.com">Example link</a>, <a href="#InSensitive">Insensitive internal link</a>, <a href="http://example.org">Example org link</a>]
    ```

`[attribute=value]`
: 
    Represents elements with an attribute named **attribute** that also has a value of **value**.

    ```css tab="Syntax"
    [attr=value]
    [attr="value"]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <ul>
    ...   <li><a href="#internal">Internal link</a></li>
    ...   <li><a href="http://example.com">Example link</a></li>
    ...   <li><a href="#InSensitive">Insensitive internal link</a></li>
    ...   <li><a href="http://example.org">Example org link</a></li>
    ... </ul>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('[href="#internal"]'))
    [<a href="#internal">Internal link</a>]
    ```

`[attribute~=value]`
: 
    Represents elements with an attribute named **attribute** whose value is a space separated list which contains
    **value**.

    ```css tab="Syntax"
    [attr~=value]
    [attr~="value"]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <ul>
    ...   <li><a href="#internal" class="class1 class2 class3">Internal link</a></li>
    ...   <li><a href="http://example.com">Example link</a></li>
    ...   <li><a href="#InSensitive">Insensitive internal link</a></li>
    ...   <li><a href="http://example.org">Example org link</a></li>
    ... </ul>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('[class~=class2]'))
    [<a class="class1 class2 class3" href="#internal">Internal link</a>]
    ```

`[attribute|=value]`
: 
    Represents elements with an attribute named **attribute** whose value is a dash separated list that starts with
    **value**.

    ```css tab="Syntax"
    [attr|=value]
    [attr|="value"]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <div lang="en">Some text</div>
    ... <div lang="en-US">Some more text</div>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('a[href!="#internal"]'))
    [<div lang="en">Some text</div>, <div lang="en-US">Some more text</div>]
    ```

`[attribute^=value]`
: 
    Represents elements with an attribute named **attribute** whose value starts with **value**.

    ```css tab="Syntax"
    [attr^=value]
    [attr^="value"]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <ul>
    ...   <li><a href="#internal">Internal link</a></li>
    ...   <li><a href="http://example.com">Example link</a></li>
    ...   <li><a href="#InSensitive">Insensitive internal link</a></li>
    ...   <li><a href="http://example.org">Example org link</a></li>
    ... </ul>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('[href^=http]'))
    [<a href="http://example.com">Example link</a>, <a href="http://example.org">Example org link</a>]
    ```

`[attribute$=value]`
: 
    Represents elements with an attribute named **attribute** whose value ends with **value**.

    ```css tab="Syntax"
    [attr$=value]
    [attr$="value"]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <ul>
    ...   <li><a href="#internal">Internal link</a></li>
    ...   <li><a href="http://example.com">Example link</a></li>
    ...   <li><a href="#InSensitive">Insensitive internal link</a></li>
    ...   <li><a href="http://example.org">Example org link</a></li>
    ... </ul>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('[href$=org]'))
    [<a href="http://example.org">Example org link</a>]
    ```

`[attribute*=value]`
: 
    Represents elements with an attribute named **attribute** whose value containing the substring **value**.

    ```css tab="Syntax"
    [attr*=value]
    [attr*="value"]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <ul>
    ...   <li><a href="#internal">Internal link</a></li>
    ...   <li><a href="http://example.com">Example link</a></li>
    ...   <li><a href="#InSensitive">Insensitive internal link</a></li>
    ...   <li><a href="http://example.org">Example org link</a></li>
    ... </ul>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('[href*="example"]'))
    [<a href="http://example.com">Example link</a>, <a href="http://example.org">Example org link</a>]
    ```

`[attribute!=value]`<span class="star badge"></span>
: 
    Equivalent to `#!css :not([attribute=value])`.

    ```css tab="Syntax"
    [attr!=value]
    [attr!="value"]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <ul>
    ...   <li><a href="#internal">Internal link</a></li>
    ...   <li><a href="http://example.com">Example link</a></li>
    ...   <li><a href="#InSensitive">Insensitive internal link</a></li>
    ...   <li><a href="http://example.org">Example org link</a></li>
    ... </ul>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('a[href!="#internal"]'))
    [<a href="http://example.com">Example link</a>, <a href="#InSensitive">Insensitive internal link</a>, <a href="http://example.org">Example org link</a>]
    ```

`[attribute operator value i]`<span class="lab badge"></span>
: 
    Represents elements with an attribute named **attribute** and whose value, when the **operator** is applied, matches
    **value** *without* case sensitivity. In general, attribute comparison is insensitive in normal HTML, but not XML.
    `i` is most useful in XML documents.

    ```css tab="Syntax"
    [attr=value i]
    [attr="value" i]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <ul>
    ...   <li><a href="#internal">Internal link</a></li>
    ...   <li><a href="http://example.com">Example link</a></li>
    ...   <li><a href="#InSensitive">Insensitive internal link</a></li>
    ...   <li><a href="http://example.org">Example org link</a></li>
    ... </ul>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('[href="#INTERNAL" i]'))
    [<a href="#internal">Internal link</a>]
    ```

`[attribute operator value s]` <span class="lab badge"></span>
: 
    Represents elements with an attribute named **attribute** and whose value, when the **operator** is applied, matches
    **value** *with* case sensitivity.

    ```css tab="Syntax"
    [attr=value s]
    [attr="value" s]
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <ul>
    ...   <li><a href="#internal">Internal link</a></li>
    ...   <li><a href="http://example.com">Example link</a></li>
    ...   <li><a href="#InSensitive">Insensitive internal link</a></li>
    ...   <li><a href="http://example.org">Example org link</a></li>
    ... </ul>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('[href="#INTERNAL" s]'))
    []
    >>> print(soup.select('[href="#internal" s]'))
    [<a href="#internal">Internal link</a>]
    ```

### Namespace Selectors

Namespace selectors are used in conjunction with type and universal selectors as well as attribute names in attribute
selectors. They are specified by declaring the namespace and the selector separated with `|`: `namespace|selector`.
`namespace`, in this context, is the prefix defined via the [namespace dictionary](./api.md#namespaces). The prefix
defined for the CSS selector does not need to match the prefix name in the document as it is the namespace associated
with the prefix that is compared, not the prefix itself.

The universal selector (`*`) can be used to represent any namespace just as it can with types.

By default, type selectors without a namespace selector will match any element whose type matches, regardless of
namespace. But if a CSS default namespace is declared (one with an empty key: `{"": "http://www.w3.org/1999/xhtml"}`),
all type selectors will assume the default namespace unless an explicit namespace selector is specified. For example,
if the default name was defined to be `http://www.w3.org/1999/xhtml`, the selector `a` would only match `a` tags that
are within the `http://www.w3.org/1999/xhtml` namespace. The one exception is within pseudo classes (`:not()`, `:has()`,
etc.) as namespaces are not considered within pseudo classes unless one is explicitly specified.

If the namespace is omitted (`|element`), any element without a namespace will be matched. In HTML documents that
support namespaces (XHTML and HTML5), HTML elements are counted as part of the `http://www.w3.org/1999/xhtml` namespace,
but attributes usually do not have a namespace unless one is explicitly defined in the markup.

Namespaces can be used with attribute selectors as well except that when `[|attribute`] is used, it is equivalent to
`[attribute]`.

```css tab="Syntax"
ns|element
ns|*
*|*
*|element
|element
[ns|attr]
[*|attr]
[|attr]
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <h1>SVG Example</h1>
... <p><a href="http://facelessuser.github.io/soupsieve/">Soup Sieve Docs</a></p>
... 
... <svg viewBox="0 0 160 40" xmlns="http://www.w3.org/2000/svg">
...   <a xlink:href="https://developer.mozilla.org/"><text x="10" y="25">MDN Web Docs</text></a>
... </svg>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('svg|a', namespaces={'svg': 'http://www.w3.org/2000/svg'}))
[<a xlink:href="https://developer.mozilla.org/"><text x="10" y="25">MDN Web Docs</text></a>]  
>>> print(soup.select('a', namespaces={'svg': 'http://www.w3.org/2000/svg'}))
[<a href="http://facelessuser.github.io/soupsieve/">Soup Sieve Docs</a>, <a xlink:href="https://developer.mozilla.org/"><text x="10" y="25">MDN Web Docs</text></a>]
>>> print(soup.select('a', namespaces={'': 'http://www.w3.org/1999/xhtml', 'svg': 'http://www.w3.org/2000/svg'}))
[<a href="http://facelessuser.github.io/soupsieve/">Soup Sieve Docs</a>]
>>> print(soup.select('[xlink|href]', namespaces={'xlink': 'http://www.w3.org/1999/xlink'}))
[<a xlink:href="https://developer.mozilla.org/"><text x="10" y="25">MDN Web Docs</text></a>]
>>> print(soup.select('[|href]', namespaces={'xlink': 'http://www.w3.org/1999/xlink'}))
[<a href="http://facelessuser.github.io/soupsieve/">Soup Sieve Docs</a>]
```

## Combinators and Selector Lists

CSS employs a number of tokens in order to represent lists or to provide relational context between two selectors.

### Selector Lists

Selector lists use the comma (`,`) to join multiple selectors in a list. When presented with a selector list, any
selector in the list that matches an element will return that element.

```css tab="Syntax"
element1, element2
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <h1>Title</h1>
... <p>Paragraph</p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('h1, p'))
[<h1>Title</h1>, <p>Paragraph</p>]
```

### Descendant Combinator

Descendant combinators combine two selectors with whitespace (<code> </code>) in order to signify that the second
element is matched if it has an ancestor that matches the first element.

```css tab="Syntax"
parent descendant
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <div><p>Paragraph 1</p></div>
... <div><p>Paragraph 2</p></div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('body p'))
[<p>Paragraph 1</p>, <p>Paragraph 2</p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/Descendant_combinator

### Child combinator

Child combinators combine two selectors with `>` in order to signify that the second element is matched if it has a
parent that matches the first element.

```css tab="Syntax"
parent > child
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <div><p>Paragraph 1</p></div>
... <div><ul><li><p>Paragraph 2</p></li></ul></div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('div > p'))
[<p>Paragraph 1</p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/Child_combinator

### General sibling combinator

General sibling combinators combine two selectors with `~` in order to signify that the second element is matched if it
has a sibling that precedes it that matches the first element.

```css tab="Syntax"
prevsibling ~ sibling
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <h1>Title</h1>
... <p>Paragraph 1</p>
... <p>Paragraph 2</p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('h1 ~ p'))
[<p>Paragraph 1</p>, <p>Paragraph 2</p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/General_sibling_combinator

### Adjacent sibling combinator

Adjacent sibling combinators combine two selectors with `+` in order to signify that the second element is matched if it
has an adjacent sibling that precedes it that matches the first element.


```css tab="Syntax"
prevsibling + nextsibling
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <h1>Title</h1>
... <p>Paragraph 1</p>
... <p>Paragraph 2</p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('h1 ~ p'))
[<p>Paragraph 1</p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/Adjacent_sibling_combinator

## Pseudo-Classes

These are pseudo classes that are either fully or partially supported. Partial support is usually due to limitations of
not being in a live, browser environment. Pseudo classes that cannot be implemented are found under
[Non-Applicable Pseudo Classes](#non-applicable-pseudo-classes). Any selectors that are not found here or under the
non-applicable either are under consideration, have not yet been evaluated, or are too new and viewed as a risk to
implement as they might not stick around.

### `:any-link`<span class="html5 badge"></span><span class="lab badge"></span> {:#:any-link}

Selects every `#!html <a>`, `#!html <area>`, or `#!html <link>` element that has an `href` attribute, independent of
whether it has been visited.

```css tab="Syntax"
:any-link
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p>A link to <a href="http://example.com">click</a></p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':any-link'))
[<a href="http://example.com">click</a>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:any-link

### `:checked`<span class="html5 badge"></span> {:#:checked}

Selects any `#!html <input type="radio"/>`, `#!html <input type="checkbox"/>`, or `#!html <option>` element (in a
`#!html <select>` element) that is checked or toggled to an on state.

```css tab="Syntax"
:checked
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... 
... <div>
...   <input type="radio" name="my-input" id="yes" checked>
...   <label for="yes">Yes</label>
... 
...   <input type="radio" name="my-input" id="no">
...   <label for="no">No</label>
... </div>
... 
... <select name="my-select" id="fruit">
...   <option id="1" value="opt1">Apples</option>
...   <option id="2" value="opt2" selected>Grapes</option>
...   <option id="3" value="opt3">Pears</option>
... </select>
... 
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':checked'))
[<input checked="" id="yes" name="my-input" type="radio"/>, <option id="2" selected="" value="opt2">Grapes</option>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:checked

### `:contains()`<span class="star badge"></span> {:#:contains}

Selects elements that contain the provided text. Text can be found in either itself, or its descendants.

Contains was originally included in a [CSS early draft][contains-draft], but was, in the end, dropped from the draft.
Soup Sieve implements it how it was originally proposed in the draft with the addition that `:contains()` can accept
either a single value, or a comma separated list of values. An element needs only to match at least one of the items
in the comma separated list to be considered matching.

!!! warning "Contains"
    `:contains()` is an expensive operation as it scans all the text nodes of an element under consideration, which
    includes all descendants. Using highly specific selectors can reduce how often it is evaluated.

```css tab="Syntax"
:contains(text)
:contains("This text", "or this text")
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
...   <div>Here is <span>some text</span>.</div>
...   <div>Here is some more text.</div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('div:contains("some text")'))
[<div>Here is <span>some text</span>.</div>]
```

### `:default`<span class="html5 badge"></span><span class="lab badge"></span> {:#:default}

Selects any form element that is the default among a group of related elements, including: `#!html <button>`,
`#!html <input type="checkbox">`, `#!html <input type="radio">`, `#!html <option>` elements.

```css tab="Syntax"
:default
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <form>
... 
... <input type="radio" name="season" id="spring">
... <label for="spring">Spring</label>
... 
... <input type="radio" name="season" id="summer" checked>
... <label for="summer">Summer</label>
... 
... <input type="radio" name="season" id="fall">
... <label for="fall">Fall</label>
... 
... <input type="radio" name="season" id="winter">
... <label for="winter">Winter</label>
... 
... <select id="pet-select">
...     <option value="">--Please choose an option--</option>
...     <option id="dog" value="dog">Dog</option>
...     <option id="cat" value="cat">Cat</option>
...     <option id="hamster" value="hamster" selected>Hamster</option>
...     <option id="parrot" value="parrot">Parrot</option>
...     <option id="spider" value="spider">Spider</option>
...     <option id="goldfish" value="goldfish">Goldfish</option>
... </select>
... </form>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':default'))
[<input checked="" id="summer" name="season" type="radio"/>, <option id="hamster" selected="" value="hamster">Hamster</option>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:default

### `:defined`<span class="html5 badge"></span></span><span class="lab badge"></span> {:#:defined}

In a browser environment, this represents *defined* elements (names without hyphens) and custom elements (names with
hyphens) that have been properly added to the custom element registry. Since elements cannot be added to a custom
element registry in Beautiful Soup, this will select all elements that are not custom tags. `:defined` is a HTML
specific selector, so it doesn't apply to XML.

```css tab="Syntax"
:defined
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <custom-element text="Custom element example text"></custom-element>
... <p>Standard paragraph example text</p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('body > *:defined'))
[<p>Standard paragraph example text</p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:defined

### `:dir()`<span class="html5 badge"></span><span class="lab badge"></span> {:#:dir}

Selects elements based on text directionality. Accepts either `ltr` or `rtl` for "left to right" and "right to left"
respectively.

```css tab="Syntax"
:dir(ltr)
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <div>
... <span dir="auto">זאת השפה העברית</span>
... <span dir="ltr">Text</span>
... </div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':dir(rtl)'))
[<span dir="auto">זאת השפה העברית</span>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:dir

### `:disabled`<span class="html5 badge"></span> {:#:disabled}

Selects any element that is disabled.

```css tab="Syntax"
:disabled
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <form action="#">
...   <fieldset id="shipping">
...     <legend>Shipping address</legend>
...     <input type="text" placeholder="Name">
...     <input type="text" placeholder="Address">
...     <input type="text" placeholder="Zip Code">
...   </fieldset>
...   <br>
...   <fieldset id="billing">
...     <legend>Billing address</legend>
...     <label for="billing-checkbox">Same as shipping address:</label>
...     <input type="checkbox" id="billing-checkbox" checked>
...     <br>
...     <input type="text" placeholder="Name" disabled>
...     <input type="text" placeholder="Address" disabled>
...     <input type="text" placeholder="Zip Code" disabled>
...   </fieldset>
... </form>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('input:disabled'))
[<input disabled="" placeholder="Name" type="text"/>, <input disabled="" placeholder="Address" type="text"/>, <input disabled="" placeholder="Zip Code" type="text"/>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:disabled

### `:empty`<span class="lab badge"></span> {:#:empty}

Selects elements that have no children and no text (whitespace is ignored).

```css tab="Syntax"
:empty
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <span> <!-- comment --> </span>
... <span></span>
... <span><span>    </span></span>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('body :empty'))
[<span> <!-- comment --> </span>, <span></span>, <span>    </span>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:empty

### `:enabled`<span class="html5 badge"></span> {:#:enabled}

Selects any element that is enabled.

```css tab="Syntax"
:enabled
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <form action="#">
...   <fieldset id="shipping">
...     <legend>Shipping address</legend>
...     <input type="text" placeholder="Name">
...     <input type="text" placeholder="Address">
...     <input type="text" placeholder="Zip Code">
...   </fieldset>
...   <br>
...   <fieldset id="billing">
...     <legend>Billing address</legend>
...     <label for="billing-checkbox">Same as shipping address:</label>
...     <input type="checkbox" id="billing-checkbox" checked>
...     <br>
...     <input type="text" placeholder="Name" disabled>
...     <input type="text" placeholder="Address" disabled>
...     <input type="text" placeholder="Zip Code" disabled>
...   </fieldset>
... </form>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('input:enabled'))
[<input placeholder="Name" type="text"/>, <input placeholder="Address" type="text"/>, <input placeholder="Zip Code" type="text"/>, <input checked="" id="billing-checkbox" type="checkbox"/>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:enabled

### `:first-child` {:#:first-child}

Selects the first child in a group of sibling elements.

```css tab="Syntax"
:first-child
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p id="0"></p>
... <p id="1"></p>
... <p id="2"></p>
... <p id="3"></p>
... <p id="4"></p>
... <p id="5"></p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('p:first-child'))
[<p id="0"></p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:first-child

### `:first-of-type` {:#:first-of-type}

Selects the first child of a given type in a group of sibling elements.

```css tab="Syntax"
element:first-of-type
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p id="0"></p>
... <p id="1"></p>
... <span id="2"></span>
... <span id="3"></span>
... <span id="4"></span>
... <span id="5"></span>
... <span id="6"></span>
... <p id="7"></p>
... <p id="8"></p>
... <p id="9"></p>
... <p id="10"></p>
... <span id="11"></span>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('span:first-of-type'))
[<span id="2"></span>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:first-of-type

### `:has()`<span class="lab badge"></span> {:#has}

Selects an element if any of the relative selectors passed as parameters (which are relative to the `:scope` of the
given element), match at least one element.

While the level 4 specifications state that [compound](#compound-selector) selectors are supported, complex selectors
are planned for level 5 CSS selectors. Soup Sieve supports [complex](#complex-selector) selectors.

```css tab="Syntax"
:has(selector)
:has(> selector)
:has(~ selector)
:has(+ selector)
:has(selector1, > selector2, ~ selector3, + selector4)
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <div><p>Test <span>paragraph</span></p></div>
... <div><p class="class">Another test paragraph</p></div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('div:has(span, > .class)'))
[<div><p>Test <span>paragraph</span></p></div>, <div><p class="class">Another test paragraph</p></div>]  
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:has

### `:in-range`<span class="html5 badge"></span><span class="lab badge"></span> {:#:in-range}

Selects all `#!html <input>` elements whose values are in range according to their `type`, `min`, and `max` attributes.

```css tab="Syntax"
:in-range
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <input id="0" type="month" min="1980-02" max="2004-08" value="1999-05">
... <input id="7" type="month" min="1980-02" max="2004-08" value="1979-02">
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':in-range'))
[<input id="0" max="2004-08" min="1980-02" type="month" value="1999-05"/>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:in-range

### `:indeterminate`<span class="html5 badge"></span><span class="lab badge"></span> {:#:indeterminate}

Selects all form elements whose are in an indeterminate state.

An element is considered indeterminate if:

- The element is of type `#!html <input type="checkbox"/>` and the `indeterminate` attribute is set.
- The element is of type `#!html <input type="radio"/>` and all other radio controls with the same name are not
selected.
- The element is of type `#!html <progress>` with no value.

```css tab="Syntax"
:indeterminate
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <input type="checkbox" id="checkbox1" indeterminate>
... <label for="checkbox1">I like cats.</label>
... 
... <input type="checkbox" id="checkbox2">
... <label for="checkbox2">I like dogs.</label>
... 
... <form>
...     <input type="radio" name="test" id="radio1">
...     <label for="radio1">Yes</label>
... 
...     <input type="radio" name="test" id="radio2">
...     <label for="radio2">No</label>
... 
...     <input type="radio" name="test" id="radio3">
...     <label for="radio3">Maybe</label>
... </form>
... <form>
...     <input type="radio" name="another" id="radio4">
...     <label for="radio4">Red</label>
... 
...     <input type="radio" name="another" id="radio5" checked>
...     <label for="radio5">Green</label>
... 
...     <input type="radio" name="another" id="radio6">
...     <label for="radio6">Blue</label>
... </form>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':indeterminate'))
[<input id="checkbox1" indeterminate="" type="checkbox"/>, <input id="radio1" name="test" type="radio"/>, <input id="radio2" name="test" type="radio"/>, <input id="radio3" name="test" type="radio"/>] 
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:indeterminate

### `:is()`<span class="lab badge"></span> {:#:is}

Selects an element, but only if it matches at least one selector in the selector list.

The alias `:matches()` is also supported as it was the original name for the selector, and some browsers support it.
It is strongly encouraged to use `:is()` instead as support for `:matches()` may be dropped in the future.

While the level 4 specifications state that [compound](#compound-selector) selectors are supported, some browsers
(Safari) support complex selectors which are planned for level 5 CSS selectors. Soup Sieve also supports
[complex](#complex-selector) selectors.

```css tab="Syntax"
:is(selector1, selector2)
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p id="0">Some text <span id="1"> in a paragraph</span>.
... <a id="2" href="http://google.com">Link.</a></p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('[id]:is(a, span)'))
[<span id="1"> in a paragraph</span>, <a href="http://google.com" id="2">Link.</a>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:is

### `:lang()` {:#:lang}

Level 3 CSS
: 
    Selects an element whose associated language matches the provided **language** or whose language starts with the
    provided **language** followed by a `-`. Language is determined by the rules of the document type.

    ```css tab="Syntax"
    :lang(language)
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <div lang="de-DE">
    ...     <p id="1"></p>
    ... </div>
    ... <div lang="de-DE-1996">
    ...     <p id="2"></p>
    ... </div>
    ... <div lang="de-Latn-DE">
    ...     <p id="3"></p>
    ... </div>
    ... <div lang="de-Latf-DE">
    ...     <p id="4"></p>
    ... </div>
    ... <div lang="de-Latn-DE-1996">
    ...     <p id="5"></p>
    ... </div>
    ... <p id="6" lang="de-DE"></p>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('p:lang(de)'))
    [<p id="1"></p>, <p id="2"></p>, <p id="3"></p>, <p id="4"></p>, <p id="5"></p>, <p id="6" lang="de-DE"></p>]
    ```

Level 4 CSS<span class="lab badge"></span>
: 
    The level 4 CSS specifications adds the ability to define multiple language tags using a comma separated list. The
    specifications also allow for BCP 47 language ranges as described in [RFC4647](https://tools.ietf.org/html/rfc4647)
    for extended filtering. This enables implicit wildcard matching between subtags. For instance, `:lang(de-DE)` will
    match all of `de-DE`, `de-DE-1996`, `de-Latn-DE`, `de-Latf-DE`, and `de-Latn-DE-1996`. Implicit wildcard matching
    will not take place at the beginning on the primary language tag, `*` must be used to force wildcard matching at the
    beginning of the language. If desired an explicit wildcard between subtags can be used, but since implicit wildcard
    matching already takes place between subtags, it is not needed: `de-*-DE` would be the same as just using `de-DE`.

    ```css tab="Syntax"
    :lang('*-language', language2)
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <div lang="de-DE">
    ...     <p id="1"></p>
    ... </div>
    ... <div lang="en">
    ...     <p id="2"></p>
    ... </div>
    ... <div lang="de-Latn-DE">
    ...     <p id="3"></p>
    ... </div>
    ... <div lang="de-Latf-DE">
    ...     <p id="4"></p>
    ... </div>
    ... <div lang="en-US">
    ...     <p id="5"></p>
    ... </div>
    ... <p id="6" lang="de-DE"></p>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('p:lang(de-DE, "*-US")'))
    [<p id="1"></p>, <p id="3"></p>, <p id="4"></p>, <p id="5"></p>, <p id="6" lang="de-DE"></p>]
    ```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:lang

### `:last-child` {:#:last-child}

Selects the last element among a group of sibling elements.

```css tab="Syntax"
:last-child
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p id="0"></p>
... <p id="1"></p>
... <p id="2"></p>
... <p id="3"></p>
... <p id="4"></p>
... <p id="5"></p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('p:last-child'))
[<p id="5"></p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:last-child

### `:last-of-type` {:#:last-of-type}

Selects the last child of a given type in a group of sibling elements.

```css tab="Syntax"
element:last-of-type
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p id="0"></p>
... <p id="1"></p>
... <span id="2"></span>
... <span id="3"></span>
... <span id="4"></span>
... <span id="5"></span>
... <span id="6"></span>
... <p id="7"></p>
... <p id="8"></p>
... <p id="9"></p>
... <p id="10"></p>
... <span id="11"></span>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('span:last-of-type'))
[<span id="11"></span>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:last-of-type

### `:link`<span class="html5 badge"></span> {:#:link}

Selects a link (every `#!html <a>`, `#!html <link>`, and `#!html <area>` element with an `href` attribute) that has not
yet been visited.

Since Beautiful Soup does not have *visited* states, this will match all links, essentially making the behavior the same
as `:any-link`.

```css tab="Syntax"
:link
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p>A link to <a href="http://example.com">click</a></p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':link'))
[<a href="http://example.com">click</a>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:link

### `:not()` {:#:not}

Level 3 CSS
: 
    Selects all elements that do not match the selector. The level 3 CSS specification states that `:not()` only
    supports simple selectors.

    ```css tab="Syntax"
    :not(simple-selector)
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ...    <div>Here is some text.</div>
    ...    <div>Here is some more text.</div>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('div:not(:contains(more))'))
    [<div>Here is some text.</div>]
    ```

Level 4+ CSS<span class="lab badge"></span>
: 
    Selects all elements that do not match any of the selectors in the selector list. While the level 4 specifications
    state that [compound](#compound-selector) selectors are supported, some browsers (Safari) support complex selectors
    which are planned for level 5 CSS selectors. Soup Sieve also supports [complex](#complex-selector) selectors.

    ```css tab="Syntax"
    :not(compound.selector, complex > selector)
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ...    <div>Here is some text.</div>
    ...    <div>Here is some more text.</div>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('*:not(html, head, body)'))
    [<div>Here is some text.</div>, <div>Here is some more text.</div>]
    ```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:not

### `:nth-child()` {:#:nth-child}

`:nth-child()` matches elements based on their position in a group of siblings.


Level 3 CSS
: 
    - The keywords `even` and `odd`  will respectively select elements whose position is either even or odd amongst a
      group of siblings.

    - Patterns in the form `an+b` selects elements based on their position in a group of siblings, for every positive
      integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both be integers.

    ```css tab="Syntax"
    :nth-child(even)
    :nth-child(odd)
    :nth-child(2)
    :nth-child(2n+2)
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <p id="0"></p>
    ... <p id="1"></p>
    ... <p id="2"></p>
    ... <p id="3"></p>
    ... <p id="4"></p>
    ... <p id="5"></p>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('p:nth-child(even)'))
    [<p id="1"></p>, <p id="3"></p>, <p id="5"></p>]
    >>> print(soup.select('p:nth-child(odd)'))
    [<p id="0"></p>, <p id="2"></p>, <p id="4"></p>]
    >>> print(soup.select('p:nth-child(2)'))
    [<p id="1"></p>]
    >>> print(soup.select('p:nth-child(-n+3)'))
    [<p id="0"></p>, <p id="1"></p>, <p id="2"></p>]
    ```

Level 4+ CSS<span class="lab badge"></span>
: 
    Level 4 CSS adds the additional pattern in the form `an+b of S` where `S` represents a selector list. `an+b` can
    also be substituted with `even` or `odd`.

    Wen using the pattern `an+b of S`, the pattern will select elements from a sub-group of sibling elements that all
    match the selector list (`[of S]?`), based on their position within that sub-group, using the pattern `an+b`, for
    every positive integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both
    be integers.

    Essentially, `#!css img:nth-of-type(2)` would be equivalent to `#!css :nth-child(2 of img)`. The advantage of using
    `:nth-child(an+b [of S]?)` over `:nth-of-type` is that `:nth-of-type` is restricted to types, while
    `:nth-child(an+b [of S]?)` can use [complex](#complex-selector) selectors.

    While the level 4 specifications state that [compound](#compound-selector) selectors are supported, complex
    selectors are planned for level 5 CSS selectors. Soup Sieve supports [complex](#complex-selector) selectors.

    ```css tab="Syntax"
    :nth-child(2 of img)
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <p id="0"></p>
    ... <p id="1"></p>
    ... <p id="2"></p>
    ... <p id="3"></p>
    ... <p id="4"></p>
    ... <p id="5"></p>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('*:nth-child(-n+3 of [id])'))
    [<p id="0"></p>, <p id="1"></p>, <p id="2"></p>]
    ```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child

### `:nth-last-child()` {:#:nth-last-child}

`:nth-last-child()` matches elements based on their position in a group of siblings, counting from the end.

Level 3 CSS
: 
    - Counting from the end, the keywords `even` and `odd`  will respectively select elements whose position is either
      even or odd amongst a group of siblings.

    - Counting from the end, patterns in the form `an+b` selects elements based on their position in a group of
      siblings, for every positive integer or zero value of `n`. The index of the first element is `1`. The values `a`
      and `b` must both be integers.

    ```css tab="Syntax"
    :nth-last-child(even)
    :nth-last-child(odd)
    :nth-last-child(2)
    :nth-last-child(2n+2)
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <p id="0"></p>
    ... <p id="1"></p>
    ... <p id="2"></p>
    ... <p id="3"></p>
    ... <p id="4"></p>
    ... <p id="5"></p>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('p:nth-last-child(even)'))
    [<p id="0"></p>, <p id="2"></p>, <p id="4"></p>]
    >>> print(soup.select('p:nth-last-child(odd)'))
    [<p id="1"></p>, <p id="3"></p>, <p id="5"></p>]
    >>> print(soup.select('p:nth-last-child(2)'))
    [<p id="4"></p>]
    >>> print(soup.select('p:nth-last-child(-n+3)'))
    [<p id="3"></p>, <p id="4"></p>, <p id="5"></p>]
    ```

Level 4+ CSS<span class="lab badge"></span>
: 
    Level 4 CSS adds the additional pattern in the form `an+b of S` where `S` represents a selector list. `an+b` can
    also be substituted with `even` or `odd`.

    Wen using the pattern `an+b of S`, the pattern will select elements from a sub-group of sibling elements that all
    match the selector list (`[of S]?`), based on their position within that sub-group, using the pattern `an+b`, for
    every positive integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both
    be integers. Elements will be counted from the end.

    Essentially, `#!css img:nth-last-of-type(2)` would be equivalent to `#!css :nth-last-child(2 of img)`. The advantage
    of using `:nth-last-child(an+b [of S]?)` over `:nth-last-of-type` is that `:nth-last-of-type` is restricted to
    types, while `:nth-last-child(an+b [of S]?)` can use [complex](#complex-selector) selectors.

    While the level 4 specifications state that [compound](#compound-selector) selectors are supported, complex
    selectors are planned for level 5 CSS selectors. Soup Sieve supports [complex](#complex-selector) selectors.

    ```css tab="Syntax"
    :nth-last-child(2 of img)
    ```

    ```pycon3 tab="Usage"
    >>> from bs4 import BeautifulSoup as bs
    >>> html = """
    ... <html>
    ... <head></head>
    ... <body>
    ... <p id="0"></p>
    ... <p id="1"></p>
    ... <p id="2"></p>
    ... <p id="3"></p>
    ... <p id="4"></p>
    ... <p id="5"></p>
    ... </body>
    ... </html>
    ... """
    >>> soup = bs(html, 'html5lib')
    >>> print(soup.select('*:nth-last-child(-n+3 of [id])'))
    [<p id="3"></p>, <p id="4"></p>, <p id="5"></p>]
    ```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-last-child

### `:nth-last-of-type()` {:#:nth-last-of-type}

`:nth-of-type()` matches elements of a given type, based on their position among a group of siblings, counting from the
end.

- The keywords `even` and `odd`, and will respectively select elements, from a sub-group of
  sibling elements that all match the given type, whose position is either even or odd amongst that sub-group of
  siblings. Starting position is counted from the end.

- Patterns in the form `an+b` select from a sub-group of sibling elements that all match the given type, based on their
  position within that sub-group, for every positive integer or zero value of `n`. The index of the first element is
  `1`. The values `a` and `b` must both be integers. Starting position is counted from the end.

```css tab="Syntax"
element:nth-last-of-type(even)
element:nth-last-of-type(odd)
element:nth-last-of-type(2)
element:nth-last-of-type(2n+2)
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p id="0"></p>
... <p id="1"></p>
... <span id="2"></span>
... <span id="3"></span>
... <span id="4"></span>
... <span id="5"></span>
... <span id="6"></span>
... <p id="7"></p>
... <p id="8"></p>
... <p id="9"></p>
... <p id="10"></p>
... <span id="11"></span>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('span:nth-last-of-type(even)'))
[<span id="2"></span>, <span id="4"></span>, <span id="6"></span>]
>>> print(soup.select('span:nth-last-of-type(odd)'))
[<span id="3"></span>, <span id="5"></span>, <span id="11"></span>]
>>> print(soup.select('p:nth-last-of-type(2)'))
[<p id="9"></p>]
>>> print(soup.select('p:nth-last-of-type(-n+3)'))
[<p id="8"></p>, <p id="9"></p>, <p id="10"></p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-last-of-type

### `:nth-of-type()` {:#:nth-of-type}

`:nth-of-type()` matches elements of a given type, based on their position among a group of siblings.

- The keywords `even` and `odd`, and will respectively select elements, from a sub-group of
  sibling elements that all match the given type, whose position is either even or odd amongst that sub-group of
  siblings.

- Patterns in the form `an+b` select from a sub-group of sibling elements that all match the given type, based on their
  position within that sub-group, for every positive integer or zero value of `n`. The index of the first element is
  `1`. The values `a` and `b` must both be integers.

```css tab="Syntax"
element:nth-of-type(even)
element:nth-of-type(odd)
element:nth-of-type(2)
element:nth-of-type(2n+2)
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p id="0"></p>
... <p id="1"></p>
... <span id="2"></span>
... <span id="3"></span>
... <span id="4"></span>
... <span id="5"></span>
... <span id="6"></span>
... <p id="7"></p>
... <p id="8"></p>
... <p id="9"></p>
... <p id="10"></p>
... <span id="11"></span>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('span:nth-of-type(even)'))
[<span id="3"></span>, <span id="5"></span>, <span id="11"></span>]
>>> print(soup.select('span:nth-of-type(odd)'))
[<span id="2"></span>, <span id="4"></span>, <span id="6"></span>]
>>> print(soup.select('p:nth-of-type(2)'))
[<p id="1"></p>]
>>> print(soup.select('p:nth-of-type(-n+3)'))
[<p id="0"></p>, <p id="1"></p>, <p id="7"></p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-of-type

### `:only-child` {:#:only-child}

Selects element without any siblings.

```css tab="Syntax"
:only-child
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <div>
...     <p id="0"></p>
...     <p id="1"></p>
...     <p id="2"></p>
...     <p id="3"></p>
...     <p id="4"></p>
...     <p id="5"></p>
... </div>
... <div>
...     <p id="6"></p>
... </div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('p:only-child'))
[<p id="6"></p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:only-child

### `:only-of-type` {:#:only-of-type}

Selects element without any siblings that matches a given type.

```css tab="Syntax"
element:only-of-type
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p id="0"></p>
... <p id="1"></p>
... <span id="2"></span>
... <p id="3"></p>
... <p id="4"></p>
... <p id="5"></p>
... <p id="6"></p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('span:only-of-type'))
[<span id="2"></span>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:only-of-type

### `:optional`<span class="html5 badge"></span><span class="lab badge"></span> {:#:optional}

Selects any `#!html <input>`, `#!html <select>`, or `#!html <textarea>` element that does not have the `required`
attribute set on it.

```css tab="Syntax"
:optional
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <form>
... <input type="name" required>
... <input type="checkbox" required>
... <input type="email">
... <textarea name="name" cols="30" rows="10" required></textarea>
... <select name="nm" required>
...     <!-- options -->
... </select>
... </form>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':optional'))
[<input type="email"/>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:optional

### `:out-of-range`<span class="html5 badge"></span><span class="lab badge"></span> {:#:out-of-range}

Selects all `#!html <input>` elements whose values are out of range according to their `type`, `min`, and `max`
attributes.

```css tab="Syntax"
:out-of-range
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <input id="0" type="month" min="1980-02" max="2004-08" value="1999-05">
... <input id="7" type="month" min="1980-02" max="2004-08" value="1979-02">
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':out-of-range'))
[<input id="7" max="2004-08" min="1980-02" type="month" value="1979-02"/>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:out-of-range

### `:placeholder-shown`<span class="html5 badge"></span><span class="lab badge"></span> {:#:placeholder-shown}

Selects any `#!html <input>` or `#!html <textarea>` element that is currently displaying placeholder text via the
`placeholder` attribute.

```css tab="Syntax"
:placeholder-shown
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <input id="0" placeholder="This is some text">
... <textarea id="1" placeholder="This is some text"></textarea>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':placeholder-shown'))
[<input id="0" placeholder="This is some text"/>, <textarea id="1" placeholder="This is some text"></textarea>]
```

!!! note "Parser Differences"
    In general, when an input has a placeholder, but the element also has valid content, the placeholder is not shown.
    For instance, when a `textarea` has actual text associated with the element, the placeholder is overridden with the
    actual content. A `textarea` is allowed no more than a single newline to be considered as having no content
    (carriage returns don't count).

    `html5lib` will strip out carriage returns, but `lxml` and `html.parser` will not. This will cause a difference
    between the parsers when dealing with Windows style line endings and `textareas`. `html5lib` seems to follow
    *closest* to what real browsers do. Soup Sieve is simply following the specification as best it can. Unfortunately,
    it can't account for the quirks of the parsers in this case without introducing other issues.

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:placeholder-shown

### `:read-only`<span class="html5 badge"></span><span class="lab badge"></span> {:#:read-only}

Selects elements (such as `#!html <input>` or `#!html <textarea>`) that are *not* editable by the user. This does not
just apply to form elements with `readonly` set, but it applies to **any** element that cannot be edited by the user.


```css tab="Syntax"
:read-only
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... 
... <input id="0">
... <input id="1" disabled>
... <input id="2" type="number" readonly>
... 
... <textarea id="3"></textarea>
... 
... <p id="4">Not editable</p>
... <p id="5" contenteditable="true">Editable text</p>
... 
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('body :read-only'))
[<input disabled="" id="1"/>, <input id="2" readonly="" type="number"/>, <p id="4">Not editable</p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:read-only

### `:read-write`<span class="html5 badge"></span><span class="lab badge"></span> {:#:read-write}

Selects elements (such as `#!html <input>` or `#!html <textarea>`) that are editable by the user. This does not just
apply to form elements as it applies to **any** element that can be edited by the user, such as a `#!html <p>` element
with `contenteditable` set on it.

```css tab="Syntax"
:read-only
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... 
... <input id="0">
... <input id="1" disabled>
... <input id="2" type="number" readonly>
... 
... <textarea id="3"></textarea>
... 
... <p id="4">Not editable</p>
... <p id="5" contenteditable="true">Editable text</p>
... 
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('body :read-write'))
[<input id="0"/>, <textarea id="3"></textarea>, <p contenteditable="true" id="5">Editable text</p>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:read-write

### `:required`<span class="html5 badge"></span><span class="lab badge"></span> {:#:required}

Selects any `#!html <input>`, `#!html <select>`, or `#!html <textarea>` element that has the `required` attribute set on
it.

```css tab="Syntax"
:required
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <form>
... <input type="name" required>
... <input type="checkbox" required>
... <input type="email">
... <textarea name="name" cols="30" rows="10" required></textarea>
... <select name="nm" required>
...     <!-- options -->
... </select>
... </form>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':required'))
[<input required="" type="name"/>, <input required="" type="checkbox"/>, <textarea cols="30" name="name" required="" rows="10"></textarea>, <select name="nm" required="">
    <!-- options -->
</select>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:required

### `:root` {:#:root}

Selects the root element of a document tree.

```css tab="Syntax"
:root
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
...    <div>Here is some text.</div>
...    <div>Here is some more text.</div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select(':root'))
[<html><head></head>
<body>
    <div>Here is some text.</div>
    <div>Here is some more text.</div>


</body></html>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:root

### `:scope`<span class="lab badge"></span> {:#:scope}

`:scope` represents the the element a `match`, `select`, or `filter` is being called on. If we were, for instance,
using `:scope` on a div (`#!py3 sv.select(':scope > p', soup.div)`) `:scope` would represent **that** div element, and
no others. If called on the Beautiful Soup object which represents the entire document, it would simply select
[`:root`](#:root).

```css tab="Syntax"
:scope
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
...    <div>Here is some text.</div>
...    <div>Here is some more text.</div>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select_one('body').select(':scope > div'))
[<div>Here is some text.</div>, <div>Here is some more text.</div>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:scope

### `:where()`<span class="lab badge"></span> {:#:where}

Selects an element, but only if it matches at least one selector in the selector list. In browsers, this also has zero
specificity, but this only has relevance in a browser environment where you have multiple CSS styles, and specificity is
used to see which applies. Beautiful Soup and Soup Sieve don't care about specificity so `:where()` is essentially just
an alias for `:is()`.

While the level 4 specifications state that [compound](#compound-selector) selectors are supported, some browsers
(Safari) support complex selectors which are planned for level 5 CSS selectors. Soup Sieve also supports
[complex](#complex-selector) selectors.

```css tab="Syntax"
:where(selector1, selector2)
```

```pycon3 tab="Usage"
>>> from bs4 import BeautifulSoup as bs
>>> html = """
... <html>
... <head></head>
... <body>
... <p id="0">Some text <span id="1"> in a paragraph</span>.
... <a id="2" href="http://google.com">Link.</a></p>
... </body>
... </html>
... """
>>> soup = bs(html, 'html5lib')
>>> print(soup.select('[id]:where(a, span)'))
[<span id="1"> in a paragraph</span>, <a href="http://google.com" id="2">Link.</a>]
```

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/:where

## Non-Applicable Pseudo Classes

These pseudo classes are recognized by the parser, and have been identified as not being applicable in a Beautiful Soup
environment. While the pseudo-classes will parse correctly, they will not match anything. This is because they cannot be
implemented outside a live, browser environment. If at any time these are dropped from the CSS spec, they will simply
be removed.

### `:active`<span class="html5 badge"></span> {:#:active}

Selects active elements.

```css tab="Syntax"
:active
```

### `:current`<span class="html5 badge"></span><span class="lab badge"></span> {:#:current}

`:current` selects the element, or an ancestor of the element, that is currently being displayed. The functional form of
`:current()` takes a compound selector list.

```css tab="Syntax"
:current
:current(selector1, selector2)
```

### `:focus`<span class="html5 badge"></span> {:#:focus}

Represents an an element that has received focus.

```css tab="Syntax"
:focus
```

### `:focus-visible`<span class="html5 badge"></span><span class="lab badge"></span> {:#:focus-visible}

Selects an element that matches `:focus` and the user agent determines that the focus should be made evident on the
element.

```css tab="Syntax"
:focus-visible
```

### `:focus-within`<span class="html5 badge"></span><span class="lab badge"></span> {:#:focus-within}

Selects an element that has received focus or contains an element that has received focus.

```css tab="Syntax"
:focus-within
```

### `:future`<span class="html5 badge"></span><span class="lab badge"></span> {:#:future}

Selects an element that is defined to occur entirely after a `:current` element.

```css tab="Syntax"
:future
```

### `:host`<span class="html5 badge"></span><span class="lab badge"></span> {:#host}

`:host` selects the element hosting a shadow tree. While the function form of `:host()` takes a complex selector list
and matches the shadow host only if it matches one of the selectors in the list.

```css tab="Syntax"
:host
:host(selector1, selector2)
```

### `:host-context()`<span class="html5 badge"></span><span class="lab badge"></span> {:#:host-context}

Selects the element hosting shadow tree, but only if one of the element's ancestors match a selector in the selector
list.

```css tab="Syntax"
:host-context(parent descendant)
```

### `:hover`<span class="html5 badge"></span> {:#:hover}

Selects an element when the user interacts with it by hovering over it with a pointing device.

```css tab="Syntax"
:hover
```

### `:local-link`<span class="html5 badge"></span><span class="lab badge"></span> {:#:local-link}

Selects link (every `#!html <a>`, `#!html <link>`, and `#!html <area>` element with an `href` attribute) elements whose
absolute URL matches the element’s own document URL.

```css tab="Syntax"
:local-link
```

### `:past`<span class="html5 badge"></span><span class="lab badge"></span> {:#:past}

Selects an element that is defined to occur entirely prior to a `:current` element.

```css tab="Syntax"
:past
```

### `:paused`<span class="html5 badge"></span><span class="lab badge"></span> {:#:paused}

Selects an element that is capable of being played or paused (such as an audio, video, or similar resource) and is
currently "paused".

```css tab="Syntax"
:paused
```

### `:playing`<span class="html5 badge"></span><span class="lab badge"></span> {:#:playing}

Selects an element that is capable of being played or paused (such as an audio, video, or similar resource) and is
currently “playing”.

```css tab="Syntax"
:playing
```

### `:target`<span class="html5 badge"></span> {:#:target}

Selects a unique element (the target element) with an id matching the URL's fragment.

```css tab="Syntax"
:target
```

### `:target-within`<span class="html5 badge"></span><span class="lab badge"></span> {:#:target-within}

Selects a unique element with an id matching the URL's fragment or an element which contains the element.

```css tab="Syntax"
:target-within
```

### `:user-invalid`<span class="html5 badge"></span><span class="lab badge"></span> {:#:user-invalid}

Selects an element with incorrect input, but only after the user has significantly interacted with it.

```css tab="Syntax"
:user-invalid
```

### `:visited`<span class="html5 badge"></span> {:#:visited}

Selects links that have already been visited.

```css tab="Syntax"
:visited
```

--8<--
selector_styles.txt
refs.txt
--8<--

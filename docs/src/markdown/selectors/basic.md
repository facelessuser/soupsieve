# Basic Selectors

Syntax and notation for basic selectors.

## Escapes

Soup Sieve selectors support using CSS escapes. So if you need provide Unicode, or non-standard characters, you can use
CSS style escapes.

Escapes can be specified with a backslash followed by 1 - 6 hexadecimal digits: `#!css \20AC`, `#!css \0020AC`, etc. If
you need to terminate an escape to avoid it accumulating unintended hexadecimal characters, you can use a space:
`#!css \0020AC dont-escape-me`. You can also escape any non-hexadecimal character, and it will be treated as that
character: `#!css \+` --> `+`. The one exception is that you cannot escape the form feed, newline, or carriage
return.

You can always use Soup Sieve's [escape command](../api.md#soupsieveescape) to escape identifiers as well.

## Type Selectors

Type selectors match elements by node name.

If a default namespace is defined in the [namespace dictionary](../api.md#namespaces), and no
[namespace](#namespace-selectors) is explicitly defined, it will be assumed that the element must be in the default
namespace.

=== "Syntax"
    ```css
    element
    ```

=== "Usage"
    ```pycon3
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

## Universal Selectors

The Universal selector (`*`) matches elements of any type.

=== "Syntax"
    ```css
    *
    ```

=== "Usage"
    ```pycon3
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

## ID Selectors

The ID selector matches an element based on its `id` attribute. The ID must match exactly.

=== "Syntax"
    ```css
    #id
    ```

=== "Usage"
    ```pycon3
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

## Class Selectors

The class selector matches an element based on the values contained in the `class` attribute. The `class` attribute is
treated as a whitespace separated list, where each item is a **class**.

=== "Syntax"
    ```css
    .class
    ```

=== "Usage"
    ```pycon3
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

## Attribute Selectors

The attribute selector matches an element based on its attributes. When specifying a value of an attribute, if it
contains whitespace or special characters, you should quote them with either single or double quotes.

!!! tip "Additional Reading"
    https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors

`[attribute]`
: 
    Represents elements with an attribute named **attribute**.

    === "Syntax"
        ```css
        [attr]
        ```

    === "Usage"
        ```pycon3
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

    === "Syntax"
        ```css
        [attr=value]
        [attr="value"]
        ```

    === "Usage"
        ```pycon3
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

    === "Syntax"
        ```css
        [attr~=value]
        [attr~="value"]
        ```

    === "Usage"
        ```pycon3
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

    === "Syntax"
        ```css
        [attr|=value]
        [attr|="value"]
        ```

    === "Usage"
        ```pycon3
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
        >>> print(soup.select('div[lang|="en"]'))
        [<div lang="en">Some text</div>, <div lang="en-US">Some more text</div>]
        ```

`[attribute^=value]`
: 
    Represents elements with an attribute named **attribute** whose value starts with **value**.

    === "Syntax"
        ```css
        [attr^=value]
        [attr^="value"]
        ```

    === "Usage"
        ```pycon3
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

    === "Syntax"
        ```css
        [attr$=value]
        [attr$="value"]
        ```

    === "Usage"
        ```pycon3
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

    === "Syntax"
        ```css
        [attr*=value]
        [attr*="value"]
        ```

    === "Usage"
        ```pycon3
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

`[attribute!=value]`:material-star:{: title="Custom" data-md-color-primary="green" .icon}
: 
    Equivalent to `#!css :not([attribute=value])`.

    === "Syntax"
        ```css
        [attr!=value]
        [attr!="value"]
        ```

    === "Usage"
        ```pycon3
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

`[attribute operator value i]`:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}
: 
    Represents elements with an attribute named **attribute** and whose value, when the **operator** is applied, matches
    **value** *without* case sensitivity. In general, attribute comparison is insensitive in normal HTML, but not XML.
    `i` is most useful in XML documents.

    === "Syntax"
        ```css
        [attr=value i]
        [attr="value" i]
        ```

    === "Usage"
        ```pycon3
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

`[attribute operator value s]` :material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}
: 
    Represents elements with an attribute named **attribute** and whose value, when the **operator** is applied, matches
    **value** *with* case sensitivity.

    === "Syntax"
        ```css
        [attr=value s]
        [attr="value" s]
        ```

    === "Usage"
        ```pycon3
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

## Namespace Selectors

Namespace selectors are used in conjunction with type and universal selectors as well as attribute names in attribute
selectors. They are specified by declaring the namespace and the selector separated with `|`: `namespace|selector`.
`namespace`, in this context, is the prefix defined via the [namespace dictionary](../api.md#namespaces). The prefix
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

=== "Syntax"
    ```css
    ns|element
    ns|*
    *|*
    *|element
    |element
    [ns|attr]
    [*|attr]
    [|attr]
    ```

=== "Usage"
    ```pycon3
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

--8<--
selector_styles.md
--8<--

# CSS Selectors

The CSS selectors are based off of the CSS level 4 specification. Primarily support has been added for selectors that
were feasible to implement and most likely to get practical use.

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
<td><span class="null"></span></td>
<td markdown="1">
Some selectors are dependent upon certain states in a web browser or other context which is simply not present outside a
web browser. An example would be the `:focus` selector. In Soup Sieve, `:focus` will match nothing because elements
cannot be focused outside of a browser without simulation, or somehow connecting to a browser. These types of selectors,
that provide no meaningful information in Soup Sieve, will be marked with <span class="null"></span>.
</td>
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

!!! warning "Working Draft Selectors"

    If at anytime a working draft drops a selector from the current draft, it will most likely also be removed here,
    most likely with a deprecation path, except where there may be a conflict that requires a less graceful transition.
    One exception is in the rare case that the selector is found to be far too useful despite being rejected. In these
    cases, we may adopt them as "custom" selectors.

!!! danger "Not Implemented"
    Pseudo elements are not supported as they do not represent real elements.

    At-rules (`@page`, etc.) are also not supported.

## Escapes

Soup Sieve selectors support using CSS escapes. So if you need provide Unicode, or non-standard characters, you can use
CSS style escapes.

Escapes can be specified with a backslash followed by 1 - 6 hexadecimal digits: `#!css \20AC`, `#!css \0020AC`, etc. If
you need to terminate an escape to avoid it accumulating unintended hexadecimal characters, you can use a space:
`#!css \0020AC dont-escape-me`. You can also escape any non-hexadecimal character, and it will be treated as that
character: `#!css \+` --> `+`. The one exception is that you cannot escape the form feed, newline, or carriage
return.

## Basic Selectors

### Type Selectors

Type selectors match elements by node name.

If a default namespace is defined in the [namespace dictionary](./api.md#namespaces), and no
[namespace](#namespace-selectors) is explicitly defined, it will be assumed that the element must be in the default
namespace.

!!! example "Type Example"
    The following would select all `#!html <div>` elements.

    ```css
    div
    ```

### Universal Selectors

The Universal selector (`*`) matches elements of any type.

!!! example
    The following would match any element: `div`, `a`, `p`, etc.

    ```css
    *
    ```

### ID Selectors

The ID selector matches an element based on its `id` attribute. The ID must match exactly.

!!! example
    The following would select the element with the id `some-id`.

    ```css
    #some-id
    ```

### Class Selectors

The class selector matches an element based on the values contained in the `class` attribute. The `class` attribute is
treated as a whitespace separated list, where each item is a **class**.

!!! example
    The following would select the elements with the class `some-class`.

    ```css
    .some-class
    ```

### Attribute Selectors

The attribute selector matches an element based on its attributes. When specifying a value of an attribute, if it
contains whitespace or special characters, you should quote them with either single or double quotes.

`[attribute]`
: 
    Represents elements with an attribute named **attribute**.

    !!! example
        The following would select all elements with a `target` attribute.

        ```css
        [target]
        ```

`[attribute=value]`
: 
    Represents elements with an attribute named **attribute** that also has a value of **value**.

    !!! example
        The following would select all elements with the `target` attribute whose value was `_blank`.

        ```css
        [target=_blank]
        ```

`[attribute~=value]`
: 
    Represents elements with an attribute named **attribute** whose value is a space separated list which contains
    **value**.

    !!! example
        The following would select all elements with a `title` attribute containing the word `flower`.

        ```css
        [title~=flower]
        ```

`[attribute|=value]`
: 
    Represents elements with an attribute named **attribute** whose value is a dash separated list that starts with
    **value**.

    !!! example
        The following would select all elements with a `lang` attribute value starting with `en`.

        ```css
        [lang|=en]
        ```

`[attribute^=value]`
: 
    Represents elements with an attribute named **attribute** whose value starts with **value**.

    !!! example
        The following selects every `#!html <a>` element whose `href` attribute value begins with `https`.

        ```css
        a[href^="https"]
        ```

`[attribute$=value]`
: 
    Represents elements with an attribute named **attribute** whose value ends with **value**.

    !!! example
        The following would select every `#!html <a>` element whose `href` attribute value ends with `.pdf`.

        ```css
        a[href$=".pdf"]
        ```

`[attribute*=value]`
: 
    Represents elements with an attribute named **attribute** whose value containing the substring **value**.

    !!! example
        The following would select every `#!html <a>` element whose `href` attribute value contains the substring
        `sometext`.

        ```css
        a[href*="sometext"]
        ```

`[attribute!=value]`<span class="star badge"></span>
: 
    Equivalent to `#!css :not([attribute=value])`.

    !!! example
        Selects all elements who do not have a `target` attribute or do not have one with a value that matches `_blank`.

        ```css
        [target!=_blank]
        ```

`[attribute operator value i]`<span class="lab badge"></span>
: 
    Represents elements with an attribute named **attribute** and whose value, when the **operator** is applied, matches
    **value** *without* case sensitivity.

    !!! example
        The following would select any element with a `title` that equals `flower` regardless of case.

        ```css
        [title=flower i]
        ```

`[attribute operator value s]` <span class="lab badge"></span>
: 
    Represents elements with an attribute named **attribute** and whose value, when the **operator** is applied, matches
    **value** *with* case sensitivity.

    !!! example
        The following would select any element with a `type` that equals `submit`. Case sensitivity will be forced.

        ```css
        [type=submit s]
        ```

### Namespace Selectors

Namespace selectors are used in conjunction with type selectors. They are specified with by declaring the namespace and
the type separated with `|`: `namespace|type`. `namespace` in this context is the prefix defined via the [namespace
dictionary](./api.md#namespaces). The prefix does not need to match the prefix in the document as it is the namespace
that is compared, not the prefix.

The universal selector (`*`) can be used to represent any namespace as it can with type.

Namespaces can be used with attribute selectors as well except that when `[|attribute`] is used, it is equivalent to
`[attribute]`.

`*|*`
: 
    Represents any element with or without a namespace.

    !!! example
        The following would select the `#!html <div>` element with or without a namespace.

        ```css
        *|div
        ```

`namespace|*`
: 
    Represents any element with a namespace that is associated with the prefix `namespace` as defined in the [namespace
    dictionary](./api.md#namespaces).

    !!! example
        The following would select the `#!html <circle>` element with the namespace `svg`.

        ```css
        svg|circle
        ```

`|*`
: 
    Represents any element with no defined namespace.

    !!! example
        The following would select a `#!html <div>` element that has no namespace.

        ```css
        |div
        ```

## Combinators and Selector Lists

CSS employs a number of tokens in order to represent lists or to provide relational context between two selectors.

### Selector Lists

Selector lists use the comma (`,`) to join multiple selectors in a list.

!!! example
    The following would select both `#!html <div>` elements and `#!html <h1>` elements.

    ```
    div, h1
    ```

### Descendant Combinator

Descendant combinators combine two selectors with whitespace (<code> </code>) in order to signify that the second
element is matched if it has an ancestor that matches the first element.

!!! example
    The following would select all `#!html <p>` elements inside `#!html <div>` elements.

    ```css
    div p
    ```

### Child combinator

Child combinators combine two selectors with `>` in order to signify that the second element is matched if it has a
parent that matches the first element.

!!! example
    The following would select all `#!html <p>` elements where the parent is a `#!html <div>` element.

    ```css
    div > p
    ```

### General sibling combinator

General sibling combinators combine two selectors with `~` in order to signify that the second element is matched if it
has a sibling that precedes it that matches the first element.

!!! example
    The following would select every `#!html <ul>` element that is preceded by a `#!html <p>` element.

    ```css
    p ~ ul
    ```

### Adjacent sibling combinator

Adjacent sibling combinators combine two selectors with `+` in order to signify that the second element is matched if it
has an adjacent sibling that precedes it that matches the first element.

!!! example
    The following would select all `#!html <p>` elements that are placed immediately after `#!html <div>` elements.

    ```css
    div + p
    ```

## Pseudo-Classes

### `:active`<span class="html5 badge"></span><span class="null badge"></span> {:#:active}

Selects active elements.

!!! example
    Active states are not applicable, so this will never match.

    ```css
    a:active
    ```

### `:any-link`<span class="html5 badge"></span><span class="lab badge"></span> {:#:any-link}

Selects every `#!html <a>`, `#!html <area>`, or `#!html <link>` element that has an `href` attribute, independent of
whether it has been visited.

!!! example
    All links are treated as unvisited, so this will match every `#!html <a>` element with an `href` attribute.

    ```css
    a:any-link
    ```

### `:checked`<span class="html5 badge"></span> {:#:checked}

Selects any `#!html <input type="radio"/>`, `#!html <input type="checkbox"/>`, or `#!html <option>` element (in a
`#!html <select>` element) that is checked or toggled to an on state.

!!! example
    Selects every checked `#!html <input>` element.

    ```css
    input:checked
    ```

### `:contains()`<span class="star badge"></span> {:#:contains}

Selects elements that contain the text provided text. Text can be found in either itself, or its descendants.

Contains was originally included in a [CSS early draft][contains-draft], but was in the end dropped from the draft.
Soup Sieve implements it how it was originally proposed in the draft with the addition that `:contains()` can accept
either a single value, or a comma separated list of values. An element needs only to match at least one of the items
in the comma separated list to be considered matching.

!!! warning "Contains"
    `:contains()` is an expensive operation as it scans all the text nodes of an element under consideration, which
    includes all descendants. Using highly specific selectors can reduce how often it is evaluated.

!!! example
    Select all `#!html <p>` elements that contain "text" in their content.

    ```css
    p:contains(text)
    ```

### `:current`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:current}

`:current`
: 
    Selects the element, or an ancestor of the element, that is currently being displayed.

    !!! example
        Time-dimensional pseudo-classes require a user agent which is not present in Beautiful Soup, so this will match
        nothing.

        ```css
        p:current
        ```

`:current(sel1, sel2, ...)`
: 
    The functional form is like `:is()` and takes a selector list:

    !!! example
        Time-dimensional pseudo-classes require a user agent which is not present in Beautiful Soup, so this will match
        nothing.

        ```css
        :current(p, li, dt, dd)
        ```

### `:default`<span class="html5 badge"></span><span class="lab badge"></span> {:#:default}

Selects any form element that is the default among a group of related elements, including: `#!html <button>`,
`#!html <input type="checkbox">`, `#!html <input type="radio">`, `#!html <option>` elements.

!!! example
    Selects all `#!html <inputs>` elements that are the default among their related elements.

    ```css
    input:default
    ```

### `:defined`<span class="html5 badge"></span> {:#:defined}

Normally, this represents normal elements (names without hyphens) and custom elements (names with hyphens) that have
been properly added to the custom element registry. Since elements cannot be added to a custom element registry in
Beautiful Soup, this will select all elements that are not custom tags. `:defined` is a HTML specific selector, so it
doesn't apply to XML.

!!! example
    Selects all defined elements under body.

    ```css
    body :defined
    ```

### `:dir()`<span class="html5 badge"></span><span class="lab badge"></span> {:#:dir}

Selects elements based on text directionality. Accepts either `ltr` or `rtl` for "left to right" and "right to left"
respectively.

!!! example
    Selects all `#!html <div>` elements that have a text direction of left to right.

    ```css
    div:dir(ltr)
    ```

### `:disabled`<span class="html5 badge"></span> {:#:disabled}

Selects any element that is disabled.

!!! example
    Selects every disabled `#!html <input>` element.

    ```css
    input:disabled
    ```

### `:empty`<span class="lab badge"></span> {:#:empty}

Selects elements that have no children and no text (whitespace is ignored).

!!! example
    Selects every `#!html <p>` element that has no children and either no text.

    ```css
    p:empty
    ```

### `:enabled`<span class="html5 badge"></span> {:#:enabled}

Selects any element that is enabled.

!!! example
    Selects every enabled `#!html <input>` element.

    ```css
    input:enabled
    ```

### `:first-child` {:#:first-child}

Selects the first child in a group of sibling elements.

!!! example
    Selects every `#!html <p>` that is also the first child of its parent.

    ```css
    p:first-child
    ```

### `:first-of-type` {:#:first-of-type}

Selects the first child of a given type in a group of sibling elements.

!!! example
    Selects every `#!html <p>` element that is the first `#!html <p>` element of its parent.

    ```css
    p:first-of-type
    ```

### `:focus`<span class="html5 badge"></span><span class="null badge"></span> {:#:focus}

Represents an an element that has received focus.

!!! example
    Focus states are not possible in Beautiful Soup, so this will never match.

    ```css
    input:focus
    ```

### `:focus-visible`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:focus-visible}

Selects an element that matches `:focus` and the user agent determines that the focus should be made evident on the
element.

!!! example

    Focus states are not possible in Beautiful Soup, and since a user agent also needs to raise that the focus should be
    made evident, this will never match.

    ```css
    a:focus-visible
    ```

### `:focus-within`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:focus-within}

Selects an element that has received focus or contains an element that has received focus.

!!! example

    Focus states are not possible in Beautiful Soup, so this will never match.

    ```css
    div:focus-within
    ```

### `:future`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:future}

Selects an element that is defined to occur entirely after a `:current` element.

!!! example
    Time-dimensional pseudo-classes require a user agent which is not present in Beautiful Soup, so this will match
    nothing.

    ```css
    p:future
    ```

### `:has()`<span class="lab badge"></span> {:#has}

Selects an element if any of the relative selectors passed as parameters (which are relative to the `:scope` of the
given element), match at least one element.

!!! example
    Selects elements that have a direct child that is a `#!html <div>` or that have a sibling of `#!html <p>`
    immediately following it.

    ```css
    :has(> div, + p)
    ```

### `:host`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#host}

`:host`
: 
    Select the element hosting a shadow tree.

    !!! example
        Matches nothing as there is no Shadow DOM in Beautiful Soup.

        ```css
        :host
        ```

`:host(sel1, sel2, ...)`
: 

    The functional form of `:host` takes a selector list and matches the shadow host only if it matches one of the
    selectors in the list.

    !!! example
        Matches nothing as there is no Shadow DOM in Beautiful Soup.

        ```css
        :host(h1)
        ```

### `:host-context()`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:host-context}

Selects the element hosting shadow tree, but only if one of the element's ancestors match a selector in the selector
list.

!!! example
    Matches nothing as there is no Shadow DOM in Beautiful Soup.

    ```css
    :host-context(main article)
    ```

### `:hover`<span class="html5 badge"></span><span class="null badge"></span> {:#:hover}

Selects an element when the user interacts with it by hovering over it with a pointing device.

!!! example
    Hovering is not possible in Beautiful Soup, so this will match nothing.

    ```css
    a:hover
    ```

### `:in-range`<span class="html5 badge"></span><span class="lab badge"></span> {:#:in-range}

Selects all `#!html <input>` elements whose values are in range according to their `type`, `min`, and `max` attributes.

!!! example
    Matches all `#!html <input type="number"/>` elements whose values are in range.

    ```css
    input[type="number"]:in-range
    ```

### `:indeterminate`<span class="html5 badge"></span><span class="lab badge"></span> {:#:indeterminate}

Selects all form elements whose are in an indeterminate state.

!!! example
    Matches all `#!html <input type="radio"/>` elements that are in a form and none of the other radio controls with the
    same name are selected.

    ```css
    input[type="radio"]:indeterminate
    ```

### `:is()`<span class="lab badge"></span> {:#:is}

Selects an element, but only if it matches at least one selector in the selector list.

!!! example
    Matches `#!html <div>` elements and `#!html <p>` elements.

    ```css
    :is(div, p)
    ```

### `:lang()` {:#:lang}

`:lang(language)`
: 
    Selects an element whose associated language matches the provided **language** or whose language starts with the
    provided **language** followed by a `-`. Language is determined by the rules of the document type.

    !!! example
        Selects all elements with language `en`. Will also match languages of `en-US`, `en-GB`, etc.

        ```css
        :lang(en)
        ```

`:lang(language1, language2, ...)`<span class="lab badge"></span>
: 
    The level 4 `:lang()` adds the ability to define multiple languages, the ability to use `*` for wildcard language
    matching.

    !!! example
        Select all elements with language `de-CH`, `it-CH`, `fr-CH`, and `rm-CH`. Will also match `en`, `en-US`, and
        `en-GB`. See CSS4 specification for more info on wildcard matching rules.

        ```css
        :lang('*-CH', en)
        ```

### `:last-child` {:#:last-child}

Selects the last element among a group of sibling elements.

!!! example
    Selects every `#!html <p>` element that is also the last child of its parent.

    ```css
    p:last-child
    ```

### `:last-of-type` {:#:last-of-type}

Selects the last child of a given type in a group of sibling elements.

!!! example
    Selects every `#!html <p>` element that is the last `#!html <p>` element of its parent.

    ```css
    p:last-of-type
    ```

### `:link`<span class="html5 badge"></span> {:#:link}

Selects a link (every `#!html <a>`, `#!html <link>`, and `#!html <area>` element with an `href` attribute) that has not
yet been visited.

!!! example
    Selects all `#!html <a>` elements since Beautiful Soup does not have *visited* states.

    ```css
    a:link
    ```

### `:local-link`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:local-link}

Selects link (every `#!html <a>`, `#!html <link>`, and `#!html <area>` element with an `href` attribute) elements whose
absolute URL matches the element’s own document URL.

!!! example
    Since documents in Beautiful Soup are not live documents, they do not contain the context of the document's URL, so
    this will not match anything.

    ```css
    a:local-link
    ```

### `:not()` {:#:not}

`:not(selector)`
: 
    Selects all elements that do not match the selector.

    !!! example
        Selects all `#!html <p>` elements that do not have class `exclude`.

        ```css
        p:not(.exclude)
        ```

`:not(selector1, selector2, ...)`<span class="lab badge"></span>
: 
    Selects all elements that do not match any of the selectors in the selector list.

    !!! example
        Selects all `#!html <p>` elements that do not have class `exclude` and attribute `style`.

        ```css
        p:not(.exclude, [style])
        ```

### `:nth-child()` {:#:nth-child}

`:nth-child(keyword)`
: 
    `:nth-child` allows the keywords `even` and `odd`, and will respectively select elements whose position is either
    even or odd amongst a group of siblings.

    !!! example
        Select every odd element that is also a `#!html <p>` element.

        ```css
        p:nth-child(odd)
        ```

`:nth-child(an+b)`
: 
    Selects elements based on their position in a group of siblings, using the pattern `an+b`, for every positive integer
    or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both be integers.

    !!! example
        Selects the first three elements: `1 = 1*0+3`, `2 = -1*1+3`, `3 = -1*2+3`.

        ```css
        :nth-child(-n+3)
        ```

`:nth-child(an+b [of S]?)`</span><span class="lab badge"></span>
: 
    Selects from a sub-group of sibling elements that all match the selector list (`[of S]?`), based on their position
    within that sub-group, using the pattern `an+b`, for every positive integer or zero value of `n`. The index of the
    first element is `1`. The values `a` and `b` must both be integers.

    Essentially, `#!css img:nth-of-type(2)` would be equivalent to `#!css :nth-child(2 of img)`. The advantage of this
    of using `:nth-child(an+b [of S]?)` is that `:nth-of-type` is restricted to types, while `:nth-child(an+b [of S]?)`
    can use compound selectors.

    !!! example
        Selects the second element of a group of sibling elements that match all match `img`.

        ```css
        :nth-child(2 of img)
        ```

### `:nth-last-child()` {:#:nth-last-child}

`:nth-last-child(keyword)`
: 
    `:nth-last-child` allows the keywords `even` and `odd`, and will respectively select elements whose position is either
    even or odd amongst a group of siblings, counting from the end.

    !!! example
        Select every odd element that is also a `#!html <p>` element, counting from the end.

        ```css
        p:nth-child(odd)
        ```

`:nth-last-child(an+b)`
: 
    Counting from the end, selects elements based on their position in a group of siblings, using the pattern `an+b`,
    for every positive integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must
    both be integers.

    !!! example
        Selects the last three elements: `1 = 1*0+3`, `2 = -1*1+3`, `3 = -1*2+3`.

        ```css
        :nth-child(-n+3)
        ```

`:nth-last-child(an+b [of S]?)`</span><span class="lab badge"></span>
: 
    Counting from the end, selects from a sub-group of sibling elements that all match the selector list (`[of S]?`),
    based on their position within that sub-group, using the pattern `an+b`, for every positive integer or zero value of
    `n`. The index of the first element is `1`. The values `a` and `b` must both be integers.

    Essentially, `#!css img:nth-last-of-type(2)` would be equivalent to `#!css :nth-last-child(2 of img)`. The advantage
    of this of using `:nth-last-child(an+b [of S]?)` is that `:nth-last-of-type` is restricted to types, while
    `:nth-last-child(an+b [of S]?)` can use compound selectors.

    !!! example
        Selects the second element (counting from the end) of a group of sibling elements that match all match `img`.

        ```css
        :nth-last-child(2 of img)
        ```

### `:nth-last-of-type()` {:#:nth-last-of-type}

`:nth-last-of-type(keyword)`
: 
    `:nth-last-of-type` allows the keywords `even` and `odd`, and will respectively select elements, from a sub-group of
    sibling elements that all match the given type, whose position is either even or odd amongst that sub-group of
    siblings, counting from the end.

    !!! example
        Counting from the end, selects every even `#!html <p>` amongst sibling `#!html <p>` elements.

        ```css
        p:nth-last-of-type(even)
        ```

`:nth-last-of-child(an+b)`
: 
    Counting from the end, selects from a sub-group of sibling elements that all match the given type, based on their
    position within that sub-group, using the pattern `an+b`, for every positive integer or zero value of `n`. The index
    of the first element is `1`. The values `a` and `b` must both be integers.

    !!! example
        Counting from the end, selects every `#!html <p>` element that is the second `#!html <p>` element of its parent.

        ```css
        p:nth-last-of-type(2)
        ```

### `:nth-of-type()` {:#:nth-of-type}

`:nth-of-type(keyword)`
: 
    `:nth-of-type` allows the keywords `even` and `odd`, and will respectively select elements, from a sub-group of
    sibling elements that all match the given type, whose position is either even or odd amongst that sub-group of
    siblings.

    !!! example
        Selects every even `#!html <p>` amongst sibling `#!html <p>` elements.

        ```css
        p:nth-last-of-type(even)
        ```

`:nth-of-type(an+b)`
: 
    Selects from a sub-group of sibling elements that all match the given type, based on their position within that
    sub-group, using the pattern `an+b`, for every positive integer or zero value of `n`. The index of the first element
    is `1`. The values `a` and `b` must both be integers.

    !!! example
        Selects every `#!html <p>` element that is the second `#!html <p>` element of its parent.

        ```css
        p:nth-of-type(2)
        ```

### `:only-child` {:#:only-child}

Selects element without any siblings.

!!! example
    Selects any `#!html <p>` element that is the only child of its parent.

    ```css
    p:only-child
    ```

### `:only-of-type` {:#:only-of-type}

Selects element without any siblings that matches a given type.

!!! example
    Selects every `#!html <p>` element that is the only `#!html <p>` element of its parent.

    ```css
    p:only-of-type
    ```

### `:optional`<span class="html5 badge"></span><span class="lab badge"></span> {:#:optional}

Selects any `#!html <input>`, `#!html <select>`, or `#!html <textarea>` element that does not have the `required`
attribute set on it.

!!! example
    Select every `#!html <input>` element without a `required` attribute.

    ```css
    input:optional
    ```

### `:out-of-range`<span class="html5 badge"></span><span class="lab badge"></span> {:#:out-of-range}

Selects all `#!html <input>` elements whose values are out of range according to their `type`, `min`, and `max`
attributes.

!!! example
    Matches all `#!html <input type="number"/>` elements whose values are out of range.

    ```css
    input[type="number"]:out-of-range
    ```

### `:past`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:past}

Selects an element that is defined to occur entirely prior to a `:current` element.

!!! example
    Time-dimensional pseudo-classes require a user agent which is not present in Beautiful Soup, so this will match
    nothing.

    ```css
    p:past
    ```

### `:paused`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:paused}

Selects an element that is capable of being played or paused (such as an audio, video, or similar resource) and is
currently "paused".

!!! example
    It is not possible to play or pause a media element in Beautiful Soup, so this will match nothing.

    ```css
    :paused
    ```

### `:placeholder-shown`<span class="html5 badge"></span><span class="lab badge"></span> {:#:placeholder-shown}

Selects any `#!html <input>` or `#!html <textarea>` element that is currently displaying placeholder text via the
`placeholder` attribute.

!!! example
    Matches all `#!html <input>` elements that have placeholder text that is shown.

    ```css
    input:placeholder-shown
    ```

### `:playing`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:playing}

Selects an element that is capable of being played or paused (such as an audio, video, or similar resource) and is
currently “playing”.

!!! example
    It is not possible to play or pause a media element in Beautiful Soup, so this will match nothing.

    ```css
    :playing
    ```

### `:read-only`<span class="html5 badge"></span><span class="lab badge"></span> {:#:read-only}

Selects elements (such as `#!html <input>` or `#!html <textarea>`) that are *not* editable by the user. This does not
just apply to form elements with `readonly` set, but it applies to **any** element that cannot be edited by the user.

!!! example
    Selects every `#!html <input>` element that is not editable by the user.

    ```css
    input:read-only
    ```

### `:read-write`<span class="html5 badge"></span><span class="lab badge"></span> {:#:read-write}

Selects elements (such as `#!html <input>` or `#!html <textarea>`) that are editable by the user. This does not just
apply to form elements as it applies to **any** element that can be edited by the user, such as a `#!html <p>` element
with `contenteditable` set on it.

!!! example
    Selects every `#!html <input>` element that is editable by the user.

    ```css
    input:read-only
    ```

### `:required`<span class="html5 badge"></span><span class="lab badge"></span> {:#:required}

Selects any `#!html <input>`, `#!html <select>`, or `#!html <textarea>` element that has the `required` attribute set on
it.

!!! example
    Select every `#!html <input>` element with a `required` attribute.

    ```css
    input:required
    ```

### `:root` {:#:root}

Selects the root element of a document tree.

!!! example
    For HTML, this would select the `#!html <html>` element.

    ```css
    :root
    ```

### `:scope`<span class="lab badge"></span> {:#:scope}

`:scope` represents the the element a `match`, `select`, or `filter` is being called on. If we had were for instance
using scope in on a div (`#!py3 sv.select(':scope > p', soup.div)`) soup would represent **that** div element, and no
others. If called on the Beautiful Soup object which represents the entire document, it would simply select
[`:root`](#:root).

!!! example
    Assuming that the following selector was called on a div element, it would select all `#!html <p>` elements that
    are direct children of **that** associated `#!html <div>` element.

    ```css
    :scope > p
    ```

### `:target`<span class="html5 badge"></span><span class="null badge"></span> {:#:target}

Selects a unique element (the target element) with an id matching the URL's fragment.

!!! example
    Since there is no concept of a "targeted" element outside a user agent/browser without simulation, this will match
    nothing.

    ```css
    h1:target
    ```

### `:target-within`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:target-within}

Selects a unique element with an id matching the URL's fragment or an element which contains the element.

!!! example
    Since there is no concept of a "targeted" element outside a user agent/browser without simulation, this will match
    nothing.

    ```css
    div:target-within
    ```

### `:user-invalid`<span class="html5 badge"></span><span class="lab badge"></span><span class="null badge"></span> {:#:user-invalid}

Selects an element with incorrect input, but only after the user has significantly interacted with it.

!!! example
    Since a user cannot interact with the HTML outside a user agent (or some simulated environment), this will match
    nothing.

    ```css
    input:user-invalid
    ```

### `:visited`<span class="html5 badge"></span><span class="null badge"></span> {:#:visited}

Selects links that have already been visited.

!!! example
    In the Beautiful Soup, links cannot be "visited", that is a concept that only applies with a
    user agent/browser. As all links in Beautiful Soup are considered to be unvisited, this will match nothing.

    ```css
    a:visited
    ```

### `:where()`<span class="lab badge"></span> {:#:where}

Selects an element, but only if it matches at least one selector in the selector list. In browsers, this also has zero
specificity, but this only has relevance in a browser environment where you have multiple CSS styles, and specificity is
used to see which applies. Beautiful Soup and Soup Sieve don't care about specificity.

!!! example
    Matches `#!html <div>` elements and `#!html <p>` elements.

    ```css
    :where(div, p)
    ```

--8<--
selector_styles.txt
refs.txt
--8<--

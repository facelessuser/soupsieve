# General Details

## Implementation Specifics

The CSS selectors are based off of the CSS specification and includes not only stable selectors, but may also include
selectors currently under development from the draft specifications. Primarily support has been added for selectors that
were feasible to implement and most likely to get practical use. In addition to the selectors in the specification,
Soup Sieve also supports a couple non-standard selectors.

Soup Sieve aims to allow users to target XML/HTML elements with CSS selectors. It implements many pseudo classes, but it
does not currently implement any pseudo elements and has no plans to do so. Soup Sieve also will not match anything for
pseudo classes that are only relevant in a live, browser environment, but it will gracefully handle them if they've been
implemented; such pseudo classes are non-applicable in the Beautiful Soup environment and are noted in [Non-Applicable
Pseudo Classes](./unsupported.md#non-applicable-pseudo-classes).

When speaking about namespaces, they only apply to XML, XHTML, or when dealing with recognized foreign tags in HTML5.
Currently, Beautiful Soup's `html5lib` parser is the only parser that will return the appropriate namespaces for a HTML5
document. If you are using XHTML, you have to use the Beautiful Soup's `lxml-xml` parser (or `xml` for short) to get the
appropriate namespaces in an XHTML document. In addition to using the correct parser, you must provide a dictionary of
namespaces to Soup Sieve in order to use namespace selectors. See the documentation on
[namespaces](../api.md#namespaces) to learn more.

While an effort is made to mimic CSS selector behavior, there may be some differences or quirks, please report issues if
any are found.

## Selector Context Key

<table markdown="1">
<tr>
    <th>Symbol</th>
    <th>Name</th>
    <th>Description</th>
</tr>
<tr markdown="1">
<td markdown="1">:material-language-html5:{: data-md-color-primary="orange" .big-icon}</td>
<td>HTML</td>
<td markdown="1">
Some selectors are very specific to HTML and either have no meaningful representation in XML, or such functionality has
not been implemented. Selectors that are HTML only will be noted with :material-language-html5:{: data-md-color-primary="orange"},
and will match nothing if used in XML.
</td>
</tr>
<tr markdown="1">
<td markdown="1">:material-star:{: data-md-color-primary="green" .big-icon}</td>
<td>Custom</td>
<td markdown="1">
Soup Sieve has implemented a couple non-standard selectors. These can contain useful selectors that were rejected
from the official CSS specifications, selectors implemented by other systems such as JQuery, or even selectors
specifically created for Soup Sieve. If a selector is considered non standard, it will be marked with
:material-star:{: title="Custom" data-md-color-primary="green"}.
</td>
</tr>
<tr markdown="1">
<td markdown="1">:material-flask:{: title="Experimental" data-md-color-primary="purple" .big-icon}</td>
<td>Experimental</td>
<td markdown="1">
All selectors that are from the current working draft of CSS4 are considered experimental and are marked with
:material-flask:{: title="Experimental" data-md-color-primary="purple"}. Additionally, if there are other immature selectors, they may be marked as experimental as
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
    If usage of a selector is not clear in this documentation, you can find more information by reading these
    specification documents:

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

--8<--
selector_styles.md
--8<--

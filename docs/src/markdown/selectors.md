# CSS Selectors

## Level 1-4 Selectors

The CSS selectors are based on a limited subset of CSS4 selectors. Primarily support has been added for selectors that were feasible to implement and most likely to get practical use.

Below shows accepted selectors. When speaking about namespaces, they only apply to XML, XHTML, or when dealing with recognized foreign tags in HTML5. You must configure the CSS [namespaces](./api.md#namespaces) when attempting to evaluate namespaces.

While an effort is made to mimic CSS selector behavior, there may be some differences or quirks, please report issues if any are found. We do not support all CSS selector features, but enough to make filtering and searching more enjoyable.

Selector                        | Example                             | Description
------------------------------- | ----------------------------------- | -----------
`Element`                       | `#!css div`                         | Select the `#!html <div>` element (will be under the default namespace if defined for XHTML).
`Element, Element`              | `#!css div, h1`                     | Select the `#!html <div>` element and the `#!html <h1>` element.
`Element Element`               | `#!css div p`                       | Select all `#!html <p>` elements inside `#!html <div>` elements.
`Element>Element`               | `#!css div > p`                     | Select all `#!html <p>` elements where the parent is a `#!html <div>` element.
`Element+Element`               | `#!css div + p`                     | Select all `#!html <p>` elements that are placed immediately after `#!html <div>` elements.
`Element~Element`               | `#!css p ~ ul`                      | Select every `#!html <ul>` element that is preceded by a `#!html <p>` element.
`namespace|Element`             | `#!css svg|circle`                  | Select the `#!html <circle>` element which also has the namespace `svg`.
`*|Element`                     | `#!css *|div`                       | Select the `#!html <div>` element with or without a namespace.
`namespace|*`                   | `#!css svg|*`                       | Select any element with the namespace `svg`.
`|Element`                      | `#!css |div`                        | Select `#!html <div>` elements without a namespace.
`|*`                            | `#!css |*`                          | Select any element without a namespace.
`*|*`                           | `#!css *|*`                         | Select all elements with any or no namespace.
`*`                             | `#!css *`                           | Select all elements. If a default namespace is defined, it will be any element under the default namespace.
`.class`                        | `#!css .some-class`                 | Select all elements with the class `some-class`.
`#id`                           | `#!css #some-id`                    | Select the element with the ID `some-id`.
`[attribute]`                   | `#!css [target]`                    | Selects all elements with a `target` attribute.
`[ns|attribute]`                | `#!css [xlink|href]`                | Selects elements with the attribute `href` and the namespace `xlink` (assuming it has been configured in the `namespaces` option).
`[*|attribute]`                 | `#!css [*|name]`                    | Selects any element with a `name` attribute that has a namespace or not.
`[|attribute]`                  | `#!css [|name]`                     | Selects any element with a `name` attribute. `[|name]` is equivalent to `[name]`.
`[attribute=value]`             | `#!css [target=_blank]`             | Selects all attributes with `target="_blank"`.
`[attribute~=value]`            | `#!css [title~=flower]`             | Selects all elements with a `title` attribute containing the word `flower`.
`[attribute|=value]`            | `#!css [lang|=en]`                  | Selects all elements with a `lang` attribute value starting with `en`.
`[attribute^=value]`            | `#!css a[href^="https"]`            | Selects every `#!html <a>` element whose `href` attribute value begins with `https`.
`[attribute$=value]`            | `#!css a[href$=".pdf"]`             | Selects every `#!html <a>` element whose `href` attribute value ends with `.pdf`.
`[attribute*=value]`            | `#!css a[href*="sometext"]`         | Selects every `#!html <a>` element whose `href` attribute value contains the substring `sometext`.
`[attribute=value i]`           | `#!css [title=flower i]`            | Selects any element with a `title` that equals `flower` regardless of case.
`[attribute=value s]`           | `#!css [type=submit s]`             | Selects any element with a `type` that equals `submit`. Case sensitivity will be forced.
`:not(sel, sel)`                | `#!css :not(.some-class, #some-id)` | Selects elements that do not have class `some-class` and ID `some-id`.
`:is(sel, sel)`                 | `#!css :is(div, .some-class)`       | Selects elements that are not `#!html <div>` and do not have class `some-class`. The alias `:matches` is allowed as well. In CSS4 `:where` is like `:is` except specificity is always zero. Soup Sieve doesn't care about specificity, so `:where` is exactly like `:is`.
`:has(> sel, + sel)`            | `#!css :has(> div, + p)`            | Selects elements that have a direct child that is a `#!html <div>` or that have sibling of `#!html <p>` immediately following.
`:first-child`                  | `#!css p:first-child`               | Selects every `#!html <p>` element that is the first child of its parent.
`:last-child`                   | `#!css p:last-child`                | Selects every `#!html <p>` element that is the last child of its parent.
`:first-of-type`                | `#!css p:first-of-type`             | Selects every `#!html <p>` element that is the first `#!html <p>` element of its parent.
`:last-of-type`                 | `#!css p:last-of-type`              | Selects every `#!html <p>` element that is the last `#!html <p>` element of its parent.
`:only-child`                   | `#!css p:only-child`                | Selects every `#!html <p>` element that is the only child of its parent.
`:only-of-type`                 | `#!css p:only-of-type`              | Selects every `#!html <p>` element that is the only `#!html <p>` element of its parent.
`:nth-child(an+b [of S]?)`      | `#!css p:nth-child(2)`              | Selects every `#!html <p>` element that is the second child of its parent. Please see CSS specification for more info on format.
`:nth-last-child(an+b [of S]?)` | `#!css p:nth-last-child(2)`         | Selects every `#!html <p>` element that is the second child of its parent, counting from the last child. Please see CSS specification for more info on format.
`:nth-of-type(an+b)`            | `#!css p:nth-of-type(2)`            | Selects every `#!html <p>` element that is the second `#!html <p>` element of its parent. Please see CSS specification for more info on format.
`:nth-last-of-type(an+b)`       | `#!css p:nth-last-of-type(2)`       | Selects every `#!html <p>` element that is the second `#!html <p>` element of its parent, counting from the last child. Please see CSS specification for more info on format.
`:root`                         | `#!css :root`                       | Selects the root element. In HTML, this is usually the `#!html <html>` element.
`:empty`                        | `#!css p:empty`                     | Selects every `#!html <p>` element that has no children and either no text. Whitespace and comments are ignored.

!!! warning "Experimental Selectors"
    `:has()` implementation is experimental and may change. There are currently no reference implementation available in any browsers, not to mention the CSS4 specifications have not been finalized, so current implementation is based on our best interpretation.

    Recent addition of `:nth-*`, `:first-*`, `:last-*`, and `:only-*` is experimental. It has been implemented to the best of our understanding, especially `of S` support. Any issues with should be reported.

## Custom Selectors

Below is listed non-standard CSS selectors. These can contain useful selectors that were rejected from the official CSS specifications, selectors implemented by other systems such as JQuery, or even selectors specific to Soup Sieve.

Just because we include selectors from one source, does not mean we have intentions of implementing other selectors from the same source.

Selector                        | Example                             | Description
------------------------------- | ----------------------------------- | -----------
`:contains(text)`               | `#!css p:contains(text)`            | Select all `#!html <p>` elements that contain "text" in their content, either directly in themselves or indirectly in their decedents.

# CSS Selectors

## Level 1-4 Selectors

### HTML and XML Selectors

The CSS selectors are based off of the CSS level 4 specification. Primarily support has been added for selectors that were feasible to implement and most likely to get practical use. Selectors that cannot provide meaningful matches will match nothing. An example would be `:focus` which will match nothing because elements cannot be focused outside of a browser. Though most of the selectors have been implemented, there are still a few that have not.

Below shows accepted selectors. When speaking about namespaces, they only apply to XML, XHTML, or when dealing with recognized foreign tags in HTML5. You must configure the CSS [namespaces](./api.md#namespaces) when attempting to evaluate namespaces.

While an effort is made to mimic CSS selector behavior, there may be some differences or quirks, please report issues if any are found.

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
`:empty`                        | `#!css p:empty`                     | Selects every `#!html <p>` element that has no children and either no text. Whitespace and comments are ignored.
`:first-child`                  | `#!css p:first-child`               | Selects every `#!html <p>` element that is the first child of its parent.
`:first-of-type`                | `#!css p:first-of-type`             | Selects every `#!html <p>` element that is the first `#!html <p>` element of its parent.
`:has(> sel, + sel)`            | `#!css :has(> div, + p)`            | Selects elements that have a direct child that is a `#!html <div>` or that have sibling of `#!html <p>` immediately following.
`:is(sel, sel)`                 | `#!css :is(div, .some-class)`       | Selects elements that are not `#!html <div>` and do not have class `some-class`. The alias `:matches` is allowed as well. In CSS4 `:where` is like `:is` except specificity is always zero. Soup Sieve doesn't care about specificity, so `:where` is exactly like `:is`.
`:lang(l1, l2)`                 | `#!css :lang('*-CH', en)`           | Select all elements with language `de-CH`, `it-CH`, `fr-CH`, and `rm-CH`. Will also match `en`, `en-US`, and `en-GB`. See CSS4 specification for more info.
`:last-child`                   | `#!css p:last-child`                | Selects every `#!html <p>` element that is the last child of its parent.
`:last-of-type`                 | `#!css p:last-of-type`              | Selects every `#!html <p>` element that is the last `#!html <p>` element of its parent.
`:not(sel, sel)`                | `#!css :not(.some-class, #some-id)` | Selects elements that do not have class `some-class` and ID `some-id`.
`:nth-child(an+b [of S]?)`      | `#!css p:nth-child(2)`              | Selects every `#!html <p>` element that is the second child of its parent. Please see CSS specification for more info on format.
`:nth-last-child(an+b [of S]?)` | `#!css p:nth-last-child(2)`         | Selects every `#!html <p>` element that is the second child of its parent, counting from the last child. Please see CSS specification for more info on format.
`:nth-last-of-type(an+b)`       | `#!css p:nth-last-of-type(2)`       | Selects every `#!html <p>` element that is the second `#!html <p>` element of its parent, counting from the last child. Please see CSS specification for more info on format.
`:nth-of-type(an+b)`            | `#!css p:nth-of-type(2)`            | Selects every `#!html <p>` element that is the second `#!html <p>` element of its parent. Please see CSS specification for more info on format.
`:only-child`                   | `#!css p:only-child`                | Selects every `#!html <p>` element that is the only child of its parent.
`:only-of-type`                 | `#!css p:only-of-type`              | Selects every `#!html <p>` element that is the only `#!html <p>` element of its parent.
`:root`                         | `#!css :root`                       | Selects the root element. In HTML, this is usually the `#!html <html>` element.
`:scope`                        | `#!css :scope div`                  | Selects all `#!html <div>` elements under the current scope element. `:scope` is the element under match or select. In the case where a document (`BeautifulSoup` object, not a `Tag` object) is under select or match, `:scope` equals `:root`.

!!! warning "Expensive Selectors"
    Some selectors are more expensive to use than others. For instance, `:has()` can be a bit more expensive as `:has(a)` will search all children of every element to find if the element contains an `#!html <a>` element.

    While an effort is made to prioritize evaluation of less expensive selectors first in the hopes to invalidate the search early on and avoid evaluating expensive selectors unless needed, you should still try to be as specific as possible to limit how often expensive selectors are evaluated. For instance, using `p.special:has(a)` will limit evaluating `:has()` to only `#!html <p>` elements that contain the `special` class.

!!! warning "CSS4 Selectors"

    In general, CSS4 specific features and selectors are not finalized in the official CSS4 specification, and may change in the future. While some are most likely quite stable, some may be less certain.

    Some implementations are based off our interpretation of the specification. It is possible our interpretation is incorrect. This is more likely with selectors that currently have no reference implementations in browsers, such as `:has()` and `of S` support in `:nth-child(an+b [of S]?)`. If any issues are discovered please report the issue with details and examples so we can get them right.

    If at anytime CSS4 drops a selector from the current draft, it will most likely also be removed here, except in the rare case that the selector is found to be far too useful despite being rejected.

!!! danger "Not Implemented"
    Pseudo elements are not supported as they do not represent real elements.

    At-rules (`@page`, etc.) are not supported.

### HTML Only Selectors

There are a number of selectors that apply specifically to HTML documents. Such selectors will only match tags in HTML documents. Use of these selectors are not restricted from XML, but when used with XML documents, they will never match.

Selectors that require states that only exist within a live HTML document, or are specifically tied to user interaction with a live document are allowed (if implemented), but will never match as well.

Selector                        | Example                             | Description
------------------------------- | ----------------------------------- | -----------
`:active`                       | `#!css a:active`                    | Active states are not applicable, so this will never match.
`:any-link`                     | `#!css a:any-link`                  | All links are treated as unvisited, so this will match every `#!html <a>` element with an `href` attribute.
`:checked`                      | `#!css input:checked`               | Selects every checked `#!html <input>` element.
`:current`                      | `#!css p:current`                   | As the document is not rendered, this will never match.
`:current(sel, sel)`            | `#!css :current(p, li, dt, dd)`     | As the document is not rendered, this will never match.
`:default`                      | `#!css input:default`               | Selects all `#!html <inputs>` elements that are the default among their related elements. See CSS specification to learn more about all that this targets.
`:dir(direction)`               | `#!css div:dir(ltr)`                | Selects all `#!html <div>` elements that have a text direction of left to right.
`:disabled`                     | `#!css input:disabled`              | Selects every disabled `#!html <input>` element.
`:enabled`                      | `#!css input:enabled`               | Selects every enabled `#!html <input>` element.
`:focus`                        | `#!css input:focus`                 | Focus states are not applicable, so this will never match.
`:future`                       | `#!css p:future`                    | As the document is not rendered, this will never match.
`:host`                         | `#!css :host`                       | Matches nothing as there is no Shadow DOM.
`:host(sel, sel)`               | `#!css :host(h1)`                   | Matches nothing as there is no Shadow DOM.
`:host-context(sel, sel)`       | `#!css :host-context(h1)`           | Matches nothing as there is no Shadow DOM.
`:hover`                        | `#!css a:focus`                     | Focus states are not applicable, so this will never match.
`:link`                         | `#!css a:link`                      | All links are treated as unvisited, so this will match every `#!html <a>` element with an `href` attribute.
`:optional`                     | `#!css input:optional`              | Select every `#!html <input>` element without a `required` attribute.
`:past`                         | `#!css p:past`                      | As the document is not rendered, this will never match.
`:paused`                       | `#!css :paused`                     | Pausing is not applicable in the Soup Sieve environment, so this will match nothing.
`:placeholder-shown`            | `#!css input:placeholder-shown`     | Selects every `#!html <input>` element that is showing a placeholder via the `placeholder` attribute.
`:playing`                      | `#!css :playing`                    | Playing is not applicable in the Soup Sieve environment, so this will match nothing.
`:read-only`                    | `#!css input:read-only`             | Selects every `#!html <input>` element that is not editable by the user.
`:read-write`                   | `#!css input:read-write`            | Selects every `#!html <input>` element that is editable by the user. 
`:required`                     | `#!css input:required`              | Select every `#!html <input>` element with a `required` attribute.
`:target`                       | `#!css #news:target`                | Elements cannot be targeted, so this will never match.
`:user-invalid`                 | `#!css input:user-invalid`          | User interaction is not applicable, so this will never match.
`:visited`                      | `#!css a:visited`                   | All links are treated unvisited, so this will never match.

## Custom Selectors

Below is a list of non-standard CSS selectors that we support. These can contain useful selectors that were rejected from the official CSS specifications, selectors implemented by other systems such as JQuery, or even selectors specifically created for Soup Sieve.

Just because we include selectors from one source, does not mean we have intentions of implementing other selectors from the same such source.

Selector                        | Example                             | Description
------------------------------- | ----------------------------------- | -----------
`[attribute!=value]`            | `#!css [target!=_blank]`            | Equivalent to `#!css :not([target=_blank])`.
`:contains(text)`               | `#!css p:contains(text)`            | Select all `#!html <p>` elements that contain "text" in their content, either directly in themselves or indirectly in their descendants.

!!! warning "Contains"
    `:contains()` is an expensive operation as it scans all the text nodes of an element under consideration, which includes all descendants. Using highly specific selectors can reduce how often it is evaluated.

--8<--
refs.txt
--8<--

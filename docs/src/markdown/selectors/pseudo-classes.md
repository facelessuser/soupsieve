# Pseudo-Classes

## Overview

These are pseudo classes that are either fully or partially supported. Partial support is usually due to limitations of
not being in a live, browser environment. Pseudo classes that cannot be implemented are found under
[Non-Applicable Pseudo Classes](./unsupported.md). Any selectors that are not found here or under the non-applicable
either are under consideration, have not yet been evaluated, or are too new and viewed as a risk to implement as they
might not stick around.

## `#!css :any-link`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:any-link}

Selects every `#!html <a>`, or `#!html <area>` element that has an `href` attribute, independent of
whether it has been visited.

/// tab | Syntax
```css
:any-link
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p>A link to <a href="http://example.com">click</a></p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':any-link')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:any-link

> [!new] New in 2.2
> The CSS specification recently updated to not include `#!html <link>` in the definition; therefore, Soup Sieve has
> removed it as well.

## `#!css :checked`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:checked}

Selects any `#!html <input type="radio"/>`, `#!html <input type="checkbox"/>`, or `#!html <option>` element (in a
`#!html <select>` element) that is checked or toggled to an on state.

/// tab | Syntax
```css
:checked
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>

<div>
  <input type="radio" name="my-input" id="yes" checked>
  <label for="yes">Yes</label>

  <input type="radio" name="my-input" id="no">
  <label for="no">No</label>
</div>

<select name="my-select" id="fruit">
  <option id="1" value="opt1">Apples</option>
  <option id="2" value="opt2" selected>Grapes</option>
  <option id="3" value="opt3">Pears</option>
</select>

</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':checked')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:checked

## `#!css :default`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:default}

Selects any form element that is the default among a group of related elements, including: `#!html <button>`,
`#!html <input type="checkbox">`, `#!html <input type="radio">`, `#!html <option>` elements.

/// tab | Syntax
```css
:default
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<form>

<input type="radio" name="season" id="spring">
<label for="spring">Spring</label>

<input type="radio" name="season" id="summer" checked>
<label for="summer">Summer</label>

<input type="radio" name="season" id="fall">
<label for="fall">Fall</label>

<input type="radio" name="season" id="winter">
<label for="winter">Winter</label>

<select id="pet-select">
    <option value="">--Please choose an option--</option>
    <option id="dog" value="dog">Dog</option>
    <option id="cat" value="cat">Cat</option>
    <option id="hamster" value="hamster" selected>Hamster</option>
    <option id="parrot" value="parrot">Parrot</option>
    <option id="spider" value="spider">Spider</option>
    <option id="goldfish" value="goldfish">Goldfish</option>
</select>
</form>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':default')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:default

## `#!css :defined`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:defined}

In a browser environment, this represents *defined* elements (names without hyphens) and custom elements (names with
hyphens) that have been properly added to the custom element registry. Since elements cannot be added to a custom
element registry in Beautiful Soup, this will select all elements that are not custom tags. `:defined` is a HTML
specific selector, so it doesn't apply to XML.

/// tab | Syntax
```css
:defined
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<custom-element text="Custom element example text"></custom-element>
<p>Standard paragraph example text</p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('body > *:defined')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:defined

## `#!css :dir()`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:dir}

Selects elements based on text directionality. Accepts either `ltr` or `rtl` for "left to right" and "right to left"
respectively.

/// tab | Syntax
```css
:dir(ltr)
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<div>
<span dir="auto">זאת השפה העברית</span>
<span dir="ltr">Text</span>
</div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':dir(rtl)')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:dir

## `#!css :disabled`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:disabled}

Selects any element that is disabled.

/// tab | Syntax
```css
:disabled
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<form action="#">
  <fieldset id="shipping">
    <legend>Shipping address</legend>
    <input type="text" placeholder="Name">
    <input type="text" placeholder="Address">
    <input type="text" placeholder="Zip Code">
  </fieldset>
  <br>
  <fieldset id="billing">
    <legend>Billing address</legend>
    <label for="billing-checkbox">Same as shipping address:</label>
    <input type="checkbox" id="billing-checkbox" checked>
    <br>
    <input type="text" placeholder="Name" disabled>
    <input type="text" placeholder="Address" disabled>
    <input type="text" placeholder="Zip Code" disabled>
  </fieldset>
</form>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('input:disabled')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:disabled

## `#!css :empty`:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:empty}

Selects elements that have no children and no text (whitespace is ignored).

/// tab | Syntax
```css
:empty
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<span> <!-- comment --> </span>
<span></span>
<span><span>    </span></span>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('body :empty')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:empty

## `#!css :enabled`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:enabled}

Selects any element that is enabled.

/// tab | Syntax
```css
:enabled
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<form action="#">
  <fieldset id="shipping">
    <legend>Shipping address</legend>
    <input type="text" placeholder="Name">
    <input type="text" placeholder="Address">
    <input type="text" placeholder="Zip Code">
  </fieldset>
  <br>
  <fieldset id="billing">
    <legend>Billing address</legend>
    <label for="billing-checkbox">Same as shipping address:</label>
    <input type="checkbox" id="billing-checkbox" checked>
    <br>
    <input type="text" placeholder="Name" disabled>
    <input type="text" placeholder="Address" disabled>
    <input type="text" placeholder="Zip Code" disabled>
  </fieldset>
</form>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('input:enabled')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:enabled

## `#!css :first-child` {:#:first-child}

Selects the first child in a group of sibling elements.

/// tab | Syntax
```css
:first-child
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p id="0"></p>
<p id="1"></p>
<p id="2"></p>
<p id="3"></p>
<p id="4"></p>
<p id="5"></p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('p:first-child')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:first-child

## `#!css :first-of-type` {:#:first-of-type}

Selects the first child of a given type in a group of sibling elements.

/// tab | Syntax
```css
element:first-of-type
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p id="0"></p>
<p id="1"></p>
<span id="2"></span>
<span id="3"></span>
<span id="4"></span>
<span id="5"></span>
<span id="6"></span>
<p id="7"></p>
<p id="8"></p>
<p id="9"></p>
<p id="10"></p>
<span id="11"></span>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('span:first-of-type')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:first-of-type

## `#!css :has()` {:#:has}

Selects an element if any of the relative selectors passed as parameters (which are relative to the `:scope` of the
given element), match at least one element.

The CSS level 4 specifications, restricts the `#!css :has()` selector to only [compound](./index.md#compound-selector)
selectors. Additionally, the nesting of `#!css :has()` within another `#!css :has()` is also prohibited. It is possible
that in the future `#!css :has()` could be extended to support [complex](./index.md#complex-selector) selectors and
nesting of `#!css :has()`, but these restriction are placed upon the selector for performance reasons.

> [!new] Change in 3.0
> Prior Soup Sieve 3.0, `#!css :has()` allowed both [complex](./index.md#complex-selector) selectors and the nesting of
> `#!css :has()`. While certainly powerful, it was not the best default for performance. To relax the rules as they were
> previously to 3.0, you can pass in the `NOSTRICT` flag.
> 
> ```py
> sv.select(':has(a ~ b)', flags=sv.NOSTRICT)
> ```

> [!note] Performance Considerations
> Certain uses of the `#!css :has()` pseudo-class can significantly impact performance.
>
> The anchor selector (the `#!css A` in `#!css A:has(B)`) should not be an element that has too many children.
> Additionally, too general an anchor, such as `*`, can cause `#!css :has()` to be applied to every element.
>
> > [!failure] Avoid
> > ```css
> > /* Avoid anchoring :has() to broad elements */
> > body:has(.content)
> > *:has(.content)
> > ```
>
> > [!success] Recommended
> > ```css
> > /* Use specific containers to limit scope */
> > .container:has(.sidebar-expanded)
> > .content-wrapper:has(> article[data-priority="high"])
> > .gallery:has(> img[data-loaded="false"])
> > ```
>
> The inner selector (the `#!css B` in `#!css A:has(B)`) should use combinators like `>` or `+` to limit traversal. When the
> selector inside `#!css :has()` is not tightly constrained, Soup Sieve might need to traverse the entire subtree of the
> anchor element to check if the condition holds.
>
> > [!failure] Avoid
> > ```css
> > /* May trigger full subtree traversal */
> > .ancestor:has(.foo)
> > ```
>
> > [!success] Recommended
> > ```css
> > /* More constrained - limits traversal */
> > .ancestor:has(> .foo)
> > .ancestor:has(+ .sibling .foo)
> > ```
>
> If the risk of performance concerns from untrusted user input cannot be tolerated in a specific project, `:has` can
> be disabled using the [`ignore`](../api.md#ignore-pseudo-class) option.

/// tab | Syntax
```css
:has(selector)
:has(> selector)
:has(~ selector)
:has(+ selector)
:has(selector1, > selector2, ~ selector3, + selector4)
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<div><p>Test <span>paragraph</span></p></div>
<div><p class="class">Another test paragraph</p></div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('div:has(span, > .class)')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:has

## `#!css :in-range`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:in-range}

Selects all `#!html <input>` elements whose values are in range according to their `type`, `min`, and `max` attributes.

/// tab | Syntax
```css
:in-range
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<input id="0" type="month" min="1980-02" max="2004-08" value="1999-05">
<input id="7" type="month" min="1980-02" max="2004-08" value="1979-02">
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':in-range')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:in-range

## `#!css :indeterminate`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:indeterminate}

Selects all form elements whose are in an indeterminate state.

An element is considered indeterminate if:

-   The element is of type `#!html <input type="checkbox"/>` and the `indeterminate` attribute is set.
-   The element is of type `#!html <input type="radio"/>` and all other radio controls with the same name are not
    selected.
-   The element is of type `#!html <progress>` with no value.

/// tab | Syntax
```css
:indeterminate
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<input type="checkbox" id="checkbox1" indeterminate>
<label for="checkbox1">I like cats.</label>

<input type="checkbox" id="checkbox2">
<label for="checkbox2">I like dogs.</label>

<form>
    <input type="radio" name="test" id="radio1">
    <label for="radio1">Yes</label>

    <input type="radio" name="test" id="radio2">
    <label for="radio2">No</label>

    <input type="radio" name="test" id="radio3">
    <label for="radio3">Maybe</label>
</form>
<form>
    <input type="radio" name="another" id="radio4">
    <label for="radio4">Red</label>

    <input type="radio" name="another" id="radio5" checked>
    <label for="radio5">Green</label>

    <input type="radio" name="another" id="radio6">
    <label for="radio6">Blue</label>
</form>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':indeterminate')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:indeterminate

## `#!css :is()` {:#:is}

Selects an element, but only if it matches at least one selector in the selector list. `#!css is()` accepts a list of
[complex](./index.md#complex-selector) selectors.

The alias `#!css :matches()` is also supported as it was the original name for the selector, and some browsers support
it. It is strongly encouraged to use `#!css :is()` instead as support for `#!css :matches()` may be dropped in the
future.

/// tab | Syntax
```css
:is(selector1, selector2)
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p id="0">Some text <span id="1"> in a paragraph</span>.
<a id="2" href="http://google.com">Link.</a></p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('[id]:is(a, span)')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:is

## `#!css :lang()` {:#:lang}

//// define
Level 3 CSS

-   Selects an element whose associated language matches the provided **language** or whose language starts with the
    provided **language** followed by a `-`. Language is determined by the rules of the document type.

    /// tab | Syntax
    ```css
    :lang(language)
    ```
    ///

    /// tab | Usage
    ```py play
    from bs4 import BeautifulSoup as bs
    html = """
    <html>
    <head></head>
    <body>
    <div lang="de-DE">
        <p id="1"></p>
    </div>
    <div lang="de-DE-1996">
        <p id="2"></p>
    </div>
    <div lang="de-Latn-DE">
        <p id="3"></p>
    </div>
    <div lang="de-Latf-DE">
        <p id="4"></p>
    </div>
    <div lang="de-Latn-DE-1996">
        <p id="5"></p>
    </div>
    <p id="6" lang="de-DE"></p>
    </body>
    </html>
    """
    soup = bs(html, 'html5lib')
    soup.select('p:lang(de)')
    ```
    ///
////

//// define
Level 4 CSS:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}

-   The level 4 CSS specifications adds the ability to define multiple language tags using a comma separated list. The
    specifications also allow for BCP 47 language ranges as described in [RFC4647](https://tools.ietf.org/html/rfc4647)
    for extended filtering. This enables implicit wildcard matching between subtags. For instance, `#!css :lang(de-DE)`
    will match all of `de-DE`, `de-DE-1996`, `de-Latn-DE`, `de-Latf-DE`, and `de-Latn-DE-1996`. Implicit wildcard
    matching will not take place at the beginning on the primary language tag, `*` must be used to force wildcard
    matching at the beginning of the language. If desired an explicit wildcard between subtags can be used, but since
    implicit wildcard matching already takes place between subtags, it is not needed: `de-*-DE` would be the same as
    just using `de-DE`.

    /// tab | Syntax
    ```css
    :lang('*-language', language2)
    ```
    ///

    /// tab | Usage
    ```py play
    from bs4 import BeautifulSoup as bs
    html = """
    <html>
    <head></head>
    <body>
    <div lang="de-DE">
        <p id="1"></p>
    </div>
    <div lang="en">
        <p id="2"></p>
    </div>
    <div lang="de-Latn-DE">
        <p id="3"></p>
    </div>
    <div lang="de-Latf-DE">
        <p id="4"></p>
    </div>
    <div lang="en-US">
        <p id="5"></p>
    </div>
    <p id="6" lang="de-DE"></p>
    </body>
    </html>
    """
    soup = bs(html, 'html5lib')
    soup.select('p:lang(de-DE, "*-US")')
    ```
    ///
////

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:lang

## `#!css :last-child` {:#:last-child}

Selects the last element among a group of sibling elements.

/// tab | Syntax
```css
:last-child
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p id="0"></p>
<p id="1"></p>
<p id="2"></p>
<p id="3"></p>
<p id="4"></p>
<p id="5"></p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('p:last-child')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:last-child

## `#!css :last-of-type` {:#:last-of-type}

Selects the last child of a given type in a group of sibling elements.

/// tab | Syntax
```css
element:last-of-type
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p id="0"></p>
<p id="1"></p>
<span id="2"></span>
<span id="3"></span>
<span id="4"></span>
<span id="5"></span>
<span id="6"></span>
<p id="7"></p>
<p id="8"></p>
<p id="9"></p>
<p id="10"></p>
<span id="11"></span>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('span:last-of-type')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:last-of-type

## `#!css :link`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:link}

Selects a link (every `#!html <a>` and `#!html <area>` element with an `href` attribute) that has not
yet been visited.

Since Beautiful Soup does not have *visited* states, this will match all links, essentially making the behavior the same
as `#!css :any-link`.

/// tab | Syntax
```css
:link
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p>A link to <a href="http://example.com">click</a></p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':link')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:link

> [!new] New in 2.2
> The CSS specification recently updated to not include `#!html <link>` in the definition; therefore, Soup Sieve has
> removed it as well.

## `#!css :muted`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:muted}

Selects an element that is capable of being played or paused (such as an audio, video, or similar resource) and is
currently "muted".

Soup Sieve can only detect muted media elements that have the `muted` attribute explicitly applied.

/// tab | Syntax
```css
:muted
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<video id="vid1" width="320" height="240" controls muted>
  <source src="movie.mp4" type="video/mp4">
  <source src="movie.ogg" type="video/ogg">
  Your browser does not support the video tag.
</video>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('video:muted')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:muted

## `#!css :not()` {:#:not}

//// define
Level 3 CSS

-   Selects all elements that do not match the selector. The level 3 CSS specification states that `#!css :not()` only
    supports simple selectors.

    /// tab | Syntax
    ```css
    :not(simple-selector)
    ```
    ///

    /// tab | Usage
    ```py play
    from bs4 import BeautifulSoup as bs
    html = """
    <html>
    <head></head>
    <body>
       <div>Here is some text.</div>
       <div>Here is some more text.</div>
    </body>
    </html>
    """
    soup = bs(html, 'html5lib')
    soup.select('div:not(:-soup-contains(more))')
    ```
    ///
////

//// define
Level 4+ CSS:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}

-   Selects all elements that do not match any of the selectors in the selector list. While the level 4 specifications
    state that [compound](./index.md#compound-selector) selectors are supported, some browsers (Safari) support complex
    selectors which are planned for level 5 CSS selectors. Soup Sieve also supports
    [complex](./index.md#complex-selector) selectors.

    /// tab | Syntax
    ```css
    :not(compound.selector, complex > selector)
    ```
    ///

    /// tab | Usage
    ```py play
    from bs4 import BeautifulSoup as bs
    html = """
    <html>
    <head></head>
    <body>
       <div>Here is some text.</div>
       <div>Here is some more text.</div>
    </body>
    </html>
    """
    soup = bs(html, 'html5lib')
    soup.select('*:not(html, head, body)')
    ```
    ///
////

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:not

## `#!css :nth-child()` {:#:nth-child}

`#!css :nth-child()` matches elements based on their position in a group of siblings.

//// define
Level 3 CSS

- 
    -   The keywords `even` and `odd`  will respectively select elements whose position is either even or odd amongst a
        group of siblings.

    -   Patterns in the form `an+b` selects elements based on their position in a group of siblings, for every positive
        integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both be
        integers.

    /// tab | Syntax
    ```css
    :nth-child(even)
    :nth-child(odd)
    :nth-child(2)
    :nth-child(2n+2)
    ```
    ///

    /// tab | Usage
    ```py play
    from bs4 import BeautifulSoup as bs
    html = """
    <html>
    <head></head>
    <body>
    <p id="0"></p>
    <p id="1"></p>
    <p id="2"></p>
    <p id="3"></p>
    <p id="4"></p>
    <p id="5"></p>
    </body>
    </html>
    """
    soup = bs(html, 'html5lib')
    soup.select('p:nth-child(even)')
    soup.select('p:nth-child(odd)')
    soup.select('p:nth-child(2)')
    soup.select('p:nth-child(-n+3)')
    ```
    ///
////

//// define
Level 4+ CSS:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}

-   Level 4 CSS adds the additional pattern in the form `an+b of S` where `S` represents a selector list. `an+b` can
    also be substituted with `even` or `odd`.

    When using the pattern `an+b of S`, the pattern will select elements from a sub-group of sibling elements that all
    match the selector list (`[of S]?`), based on their position within that sub-group, using the pattern `an+b`, for
    every positive integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both
    be integers.

    Essentially, `#!css img:nth-of-type(2)` would be equivalent to `#!css :nth-child(2 of img)`. The advantage of using
    `#!css :nth-child(an+b [of S]?)` over `#!css :nth-of-type` is that `#!css :nth-of-type` is restricted to types,
    while `#!css :nth-child(an+b [of S]?)` can use [complex](./index.md#complex-selector) selectors.

    /// tab | Syntax
    ```css
    :nth-child(2 of img)
    ```
    ///

    /// tab | Usage
    ```py play
    from bs4 import BeautifulSoup as bs
    html = """
    <html>
    <head></head>
    <body>
    <p id="0"></p>
    <p id="1"></p>
    <p id="2"></p>
    <p id="3"></p>
    <p id="4"></p>
    <p id="5"></p>
    </body>
    </html>
    """
    soup = bs(html, 'html5lib')
    soup.select('*:nth-child(-n+3 of [id])')
    ```
    ///
////

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child

## `#!css :nth-last-child()` {:#:nth-last-child}

`#!css :nth-last-child()` matches elements based on their position in a group of siblings, counting from the end.

//// define
Level 3 CSS

- 
    -   Counting from the end, the keywords `even` and `odd`  will respectively select elements whose position is either
        even or odd amongst a group of siblings.

    -   Counting from the end, patterns in the form `an+b` selects elements based on their position in a group of
        siblings, for every positive integer or zero value of `n`. The index of the first element is `1`. The values `a`
        and `b` must both be integers.

    /// tab | Syntax
    ```css
    :nth-last-child(even)
    :nth-last-child(odd)
    :nth-last-child(2)
    :nth-last-child(2n+2)
    ```
    ///

    /// tab | Usage
    ```py play
    from bs4 import BeautifulSoup as bs
    html = """
    <html>
    <head></head>
    <body>
    <p id="0"></p>
    <p id="1"></p>
    <p id="2"></p>
    <p id="3"></p>
    <p id="4"></p>
    <p id="5"></p>
    </body>
    </html>
    """
    soup = bs(html, 'html5lib')
    soup.select('p:nth-last-child(even)')
    soup.select('p:nth-last-child(odd)')
    soup.select('p:nth-last-child(2)')
    soup.select('p:nth-last-child(-n+3)')
    ```
    ///
////

//// define
Level 4+ CSS:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}

-   Level 4 CSS adds the additional pattern in the form `an+b of S` where `S` represents a selector list. `an+b` can
    also be substituted with `even` or `odd`.

    When using the pattern `an+b of S`, the pattern will select elements from a sub-group of sibling elements that all
    match the selector list (`[of S]?`), based on their position within that sub-group, using the pattern `an+b`, for
    every positive integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both
    be integers. Elements will be counted from the end.

    Essentially, `#!css img:nth-last-of-type(2)` would be equivalent to `#!css :nth-last-child(2 of img)`. The advantage
    of using `#!css :nth-last-child(an+b [of S]?)` over `#!css :nth-last-of-type` is that `#!css :nth-last-of-type` is
    restricted to types, while `#!css :nth-last-child(an+b [of S]?)` can use [complex](./index.md#complex-selector)
    selectors.

    /// tab | Syntax
    ```css
    :nth-last-child(2 of img)
    ```
    ///

    /// tab | Usage
    ```py play
    from bs4 import BeautifulSoup as bs
    html = """
    <html>
    <head></head>
    <body>
    <p id="0"></p>
    <p id="1"></p>
    <p id="2"></p>
    <p id="3"></p>
    <p id="4"></p>
    <p id="5"></p>
    </body>
    </html>
    """
    soup = bs(html, 'html5lib')
    soup.select('*:nth-last-child(-n+3 of [id])')
    ```
    ///
////

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-last-child

## `#!css :nth-last-of-type()` {:#:nth-last-of-type}

`#!css :nth-of-type()` matches elements of a given type, based on their position among a group of siblings, counting
from the end.

-   The keywords `even` and `odd`, and will respectively select elements, from a sub-group of
    sibling elements that all match the given type, whose position is either even or odd amongst that sub-group of
    siblings. Starting position is counted from the end.

-   Patterns in the form `an+b` select from a sub-group of sibling elements that all match the given type, based on
    their position within that sub-group, for every positive integer or zero value of `n`. The index of the first
    element is `1`. The values `a` and `b` must both be integers. Starting position is counted from the end.

/// tab | Syntax
```css
element:nth-last-of-type(even)
element:nth-last-of-type(odd)
element:nth-last-of-type(2)
element:nth-last-of-type(2n+2)
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p id="0"></p>
<p id="1"></p>
<span id="2"></span>
<span id="3"></span>
<span id="4"></span>
<span id="5"></span>
<span id="6"></span>
<p id="7"></p>
<p id="8"></p>
<p id="9"></p>
<p id="10"></p>
<span id="11"></span>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('span:nth-last-of-type(even)')
soup.select('span:nth-last-of-type(odd)')
soup.select('p:nth-last-of-type(2)')
soup.select('p:nth-last-of-type(-n+3)')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-last-of-type

## `#!css :nth-of-type()` {:#:nth-of-type}

`#!css :nth-of-type()` matches elements of a given type, based on their position among a group of siblings.

-   The keywords `even` and `odd`, and will respectively select elements, from a sub-group of
    sibling elements that all match the given type, whose position is either even or odd amongst that sub-group of
    siblings.

-   Patterns in the form `an+b` select from a sub-group of sibling elements that all match the given type, based on
    their position within that sub-group, for every positive integer or zero value of `n`. The index of the first
    element is `1`. The values `a` and `b` must both be integers.

/// tab | Syntax
```css
element:nth-of-type(even)
element:nth-of-type(odd)
element:nth-of-type(2)
element:nth-of-type(2n+2)
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p id="0"></p>
<p id="1"></p>
<span id="2"></span>
<span id="3"></span>
<span id="4"></span>
<span id="5"></span>
<span id="6"></span>
<p id="7"></p>
<p id="8"></p>
<p id="9"></p>
<p id="10"></p>
<span id="11"></span>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('span:nth-of-type(even)')
soup.select('span:nth-of-type(odd)')
soup.select('p:nth-of-type(2)')
soup.select('p:nth-of-type(-n+3)')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-of-type

## `#!css :open`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:open}

Selects an element that has open and closed states, but only when it is in the open state.

Due to limitations of not being in a live, browser environment, Soup Sieve can currently only target `#!html <details>`
and `#!html <dialog>` elements with an `open` attribute. It cannot target `#!html <input>` elements (such as color
pickers) when they are open as there is no indication in a non-live environment.

/// tab | Syntax
```css
:open
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<details open>
<summary>A summary</summary>
<p>Content</p>
</details>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('details:open')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:open

## `#!css :optional`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:optional}

Selects any `#!html <input>`, `#!html <select>`, or `#!html <textarea>` element that does not have the `required`
attribute set on it.

/// tab | Syntax
```css
:optional
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<form>
<input type="name" required>
<input type="checkbox" required>
<input type="email">
<textarea name="name" cols="30" rows="10" required></textarea>
<select name="nm" required>
    <!-- options -->
</select>
</form>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':optional')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:optional

## `#!css :only-child` {:#:only-child}

Selects element without any siblings.

/// tab | Syntax
```css
:only-child
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<div>
    <p id="0"></p>
    <p id="1"></p>
    <p id="2"></p>
    <p id="3"></p>
    <p id="4"></p>
    <p id="5"></p>
</div>
<div>
    <p id="6"></p>
</div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('p:only-child')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:only-child

## `#!css :only-of-type` {:#:only-of-type}

Selects element without any siblings that matches a given type.

/// tab | Syntax
```css
element:only-of-type
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p id="0"></p>
<p id="1"></p>
<span id="2"></span>
<p id="3"></p>
<p id="4"></p>
<p id="5"></p>
<p id="6"></p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('span:only-of-type')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:only-of-type

## `#!css :out-of-range`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:out-of-range}

Selects all `#!html <input>` elements whose values are out of range according to their `type`, `min`, and `max`
attributes.

/// tab | Syntax
```css
:out-of-range
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<input id="0" type="month" min="1980-02" max="2004-08" value="1999-05">
<input id="7" type="month" min="1980-02" max="2004-08" value="1979-02">
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':out-of-range')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:out-of-range

## `#!css :placeholder-shown`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:placeholder-shown}

Selects any `#!html <input>` or `#!html <textarea>` element that is currently displaying placeholder text via the
`placeholder` attribute.

/// tab | Syntax
```css
:placeholder-shown
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<input id="0" placeholder="This is some text">
<textarea id="1" placeholder="This is some text"></textarea>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':placeholder-shown')
```
///

> [!note] Parser Differences
> In general, when an input has a placeholder, but the element also has valid content, the placeholder is not shown.
> For instance, when a `textarea` has actual text associated with the element, the placeholder is overridden with the
> actual content. A `textarea` is allowed no more than a single newline to be considered as having no content
> (carriage returns don't count).
>
> `html5lib` will strip out carriage returns, but `lxml` and `html.parser` will not. This will cause a difference
> between the parsers when dealing with Windows style line endings and `textareas`. `html5lib` seems to follow
> *closest* to what real browsers do. Soup Sieve is simply following the specification as best it can. Unfortunately,
> it can't account for the quirks of the parsers in this case without introducing other issues.

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:placeholder-shown

## `#!css :read-only`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:read-only}

Selects elements (such as `#!html <input>` or `#!html <textarea>`) that are *not* editable by the user. This does not
just apply to form elements with `readonly` set, but it applies to **any** element that cannot be edited by the user.

/// tab | Syntax
```css
:read-only
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>

<input id="0">
<input id="1" disabled>
<input id="2" type="number" readonly>

<textarea id="3"></textarea>

<p id="4">Not editable</p>
<p id="5" contenteditable="true">Editable text</p>

</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('body :read-only')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:read-only

## `#!css :read-write`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:read-write}

Selects elements (such as `#!html <input>` or `#!html <textarea>`) that are editable by the user. This does not just
apply to form elements as it applies to **any** element that can be edited by the user, such as a `#!html <p>` element
with `contenteditable` set on it.

/// tab | Syntax
```css
:read-only
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>

<input id="0">
<input id="1" disabled>
<input id="2" type="number" readonly>

<textarea id="3"></textarea>

<p id="4">Not editable</p>
<p id="5" contenteditable="true">Editable text</p>

</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('body :read-write')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:read-write

## `#!css :required`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:required}

Selects any `#!html <input>`, `#!html <select>`, or `#!html <textarea>` element that has the `required` attribute set on
it.

/// tab | Syntax
```css
:required
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<form>
<input type="name" required>
<input type="checkbox" required>
<input type="email">
<textarea name="name" cols="30" rows="10" required></textarea>
<select name="nm" required>
    <!-- options -->
</select>
</form>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':required')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:required

## `#!css :root` {:#:root}

Selects the root element of a document tree.

/// tab | Syntax
```css
:root
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
   <div>Here is some text.</div>
   <div>Here is some more text.</div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select(':root')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:root

## `#!css :scope` {:#:scope}

> [!new] New 2.6
> `&`, which was introduced in [CSS Nesting Level 1](https://www.w3.org/TR/css-nesting-1/#nest-selector) can be used as
> an alternative to `:scope` and is essentially equivalent. Soup Sieve does not support nesting selectors, but `&`, when
> not used in the context of nesting is treated as the scoping root per the specification.
>
> `#!py3 sv.select('& > p', soup.div)` is equivalent to `#!py3 sv.select(':scope > p', soup.div)`.

`#!css :scope` represents the element a `match`, `select`, or `filter` is being called on. If we were, for instance,
using `#!css :scope` on a div (`#!py3 sv.select(':scope > p', soup.div)`) `:scope` would represent **that** div element,
and no others. If called on the Beautiful Soup object which represents the entire document, it would simply select
[`#!css :root`](#:root).

/// tab | Syntax
```css
:scope
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
   <div>Here is some text.</div>
   <div>Here is some more text.</div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select_one('body').select(':scope > div')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:scope

## `#!css :where()` {:#:where}

Selects an element, but only if it matches at least one selector in the selector list. `#!css where()` accepts a list of
[complex](./index.md#complex-selector) selectors.

In browsers, this also has zero specificity, but this only has relevance in a browser environment where you have
multiple CSS styles, and specificity is used to see which applies. Beautiful Soup and Soup Sieve don't care about
specificity so `#!css :where()` is essentially just an alias for `#!css :is()`. `#!css where()` accepts a list of
[complex](./index.md#complex-selector) selectors.

/// tab | Syntax
```css
:where(selector1, selector2)
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<p id="0">Some text <span id="1"> in a paragraph</span>.
<a id="2" href="http://google.com">Link.</a></p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('[id]:where(a, span)')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/:where

## `#!css :-soup-contains()`:material-star:{: title="Custom" data-md-color-primary="green" .icon} {:#:-soup-contains}

Selects elements that contain the provided text. Text can be found in either itself, or its descendants.

Originally, there was a pseudo-class called `#!css :contains()` that was originally included in a
[CSS early draft][contains-draft], but was dropped from the draft in the end. Soup Sieve implements it how it was
originally proposed except for two differences: it is called `#!css :-soup-contains()` instead of `#!css :contains()`,
and it can accept either a single value, or a comma separated list of values. An element needs only to match at least
one of the items in the comma separated list to
be considered matching.

> [!note] Performance Considerations
> `#!css :-soup-contains()` is an expensive operation as it scans all the text nodes of an element under consideration,
> which includes all descendants. This has the potential to cause scanning the entire tree, potentially multiple times.
>
> While sometimes, scanning large portions of the tree may be exactly what you want, and the outcome is worth the
> performance hit. Anchoring `#!css :-soup_contains` to a very broad element, like `*`, can cause every element to have
> all of its children scanned. Using highly specific selectors can reduce how often it is evaluated and limiting usage
> to shallow elements with a small amount of descendants can reduce the amount of content that is checked.
>
> > [!failure] Avoid
> > ```css
> > /* Avoid anchoring :-soup-contains() to broad elements */
> > body:-soup-contains('text')
> > *:-soup-contains('text')
> > ```
>
> > [!success] Recommended
> > ```css
> > /* Use specific containers to limit scope */
> > .container:-soup-contains('text')
> > ```
>
> Additionally, using [`#!css anchor:-soup-contains-own()`](#:-soup-contains-own) can limit crawling to just the
> immediate children under the anchor, providing better performance at the cost of of a more shallow search.
>
> If the risk of performance concerns from untrusted user input cannot be tolerated in a specific project,
> `#!css :-soup-contains` can be disabled using the [`ignore`](../api.md#ignore-pseudo-class) option.

> [!warning] Rename 2.1
> The name `#!css :-soup-contains()` is new in version 2.1. Previously, it was known by `#!css :contains()`. While the
> alias of `#!css :contains()` is currently allowed, this alias is deprecated moving forward and will be removed in a
> future version. It is recommended to migrate to the name `#!css :-soup-contains` moving forward.

/// tab | Syntax
```css
:-soup-contains(text)
:-soup-contains("This text", "or this text")
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
  <div>Here is <span>some text</span>.</div>
  <div>Here is some more text.</div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('div:-soup-contains("some text")')
```
///

## `#!css :-soup-contains-own()`:material-star:{: title="Custom" data-md-color-primary="green" .icon} {:#:-soup-contains-own}

Selects elements that contain the provided text. Text must be found in the target element and not in its descendants. If
text is broken up with descendant elements, each text node will be evaluated separately.

Syntax is the same as [`#!css :-soup-contains()`](#:-soup-contains).

/// tab | Syntax
```css
:-soup-contains-own(text)
:-soup-contains-own("This text", "or this text")
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
  <div>Here is <span>some text</span>.</div>
  <div>Here is some more text.</div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('div:-soup-contains-own("some")')
```
///

> [!new] New in 2.1
> `#!css :-soup-contains-own()` was added in 2.1.

--8<--
selector_styles.md
--8<--

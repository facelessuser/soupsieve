# Pseudo-Classes

## Overview

These are pseudo classes that are either fully or partially supported. Partial support is usually due to limitations of
not being in a live, browser environment. Pseudo classes that cannot be implemented are found under
[Non-Applicable Pseudo Classes](./unsupported.md/#non-applicable-pseudo-classes). Any selectors that are not found here or under the
non-applicable either are under consideration, have not yet been evaluated, or are too new and viewed as a risk to
implement as they might not stick around.

## `:any-link`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:any-link}

Selects every `#!html <a>`, or `#!html <area>` element that has an `href` attribute, independent of
whether it has been visited.

=== "Syntax"
    ```css
    :any-link
    ```

=== "Usage"
    ```pycon3
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

!!! new "New in 2.2"
    The CSS specification recently updated to not include `#!html <link>` in the definition; therefore, Soup Sieve has
    removed it as well.

## `:checked`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:checked}

Selects any `#!html <input type="radio"/>`, `#!html <input type="checkbox"/>`, or `#!html <option>` element (in a
`#!html <select>` element) that is checked or toggled to an on state.

=== "Syntax"
    ```css
    :checked
    ```

=== "Usage"
    ```pycon3
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

## `:default`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:default}

Selects any form element that is the default among a group of related elements, including: `#!html <button>`,
`#!html <input type="checkbox">`, `#!html <input type="radio">`, `#!html <option>` elements.

=== "Syntax"
    ```css
    :default
    ```

=== "Usage"
    ```pycon3
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

## `:defined`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}</span>:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:defined}

In a browser environment, this represents *defined* elements (names without hyphens) and custom elements (names with
hyphens) that have been properly added to the custom element registry. Since elements cannot be added to a custom
element registry in Beautiful Soup, this will select all elements that are not custom tags. `:defined` is a HTML
specific selector, so it doesn't apply to XML.

=== "Syntax"
    ```css
    :defined
    ```

=== "Usage"
    ```pycon3
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

## `:dir()`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:dir}

Selects elements based on text directionality. Accepts either `ltr` or `rtl` for "left to right" and "right to left"
respectively.

=== "Syntax"
    ```css
    :dir(ltr)
    ```

=== "Usage"
    ```pycon3
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

## `:disabled`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:disabled}

Selects any element that is disabled.

=== "Syntax"
    ```css
    :disabled
    ```

=== "Usage"
    ```pycon3
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

## `:empty`:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:empty}

Selects elements that have no children and no text (whitespace is ignored).

=== "Syntax"
    ```css
    :empty
    ```

=== "Usage"
    ```pycon3
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

## `:enabled`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:enabled}

Selects any element that is enabled.

=== "Syntax"
    ```css
    :enabled
    ```

=== "Usage"
    ```pycon3
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

## `:first-child` {:#:first-child}

Selects the first child in a group of sibling elements.

=== "Syntax"
    ```css
    :first-child
    ```

=== "Usage"
    ```pycon3
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

## `:first-of-type` {:#:first-of-type}

Selects the first child of a given type in a group of sibling elements.

=== "Syntax"
    ```css
    element:first-of-type
    ```

=== "Usage"
    ```pycon3
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

## `:has()`:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#has}

Selects an element if any of the relative selectors passed as parameters (which are relative to the `:scope` of the
given element), match at least one element.

While the level 4 specifications state that [compound](#compound-selector) selectors are supported, complex selectors
are planned for level 5 CSS selectors. Soup Sieve supports [complex](#complex-selector) selectors.

In addition to supporting complex selectors, Soup Sieve also supports nested `:has()` which has been excluded from the
level 4 specifications to help encourage browsers to implement `:has()`. This exclusion helps to reduces complexity and
improves performance in a live environment. As these performance concerns are not an issue in a scraping environment
compared to a web browser, Soup Sieve has no intentions on restricting the nesting of `:has()`. Users can always choose
not to nest `:has()` if there are concerns.

=== "Syntax"
    ```css
    :has(selector)
    :has(> selector)
    :has(~ selector)
    :has(+ selector)
    :has(selector1, > selector2, ~ selector3, + selector4)
    ```

=== "Usage"
    ```pycon3
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

## `:in-range`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:in-range}

Selects all `#!html <input>` elements whose values are in range according to their `type`, `min`, and `max` attributes.

=== "Syntax"
    ```css
    :in-range
    ```

=== "Usage"
    ```pycon3
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

## `:indeterminate`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:indeterminate}

Selects all form elements whose are in an indeterminate state.

An element is considered indeterminate if:

- The element is of type `#!html <input type="checkbox"/>` and the `indeterminate` attribute is set.
- The element is of type `#!html <input type="radio"/>` and all other radio controls with the same name are not
selected.
- The element is of type `#!html <progress>` with no value.

=== "Syntax"
    ```css
    :indeterminate
    ```

=== "Usage"
    ```pycon3
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

## `:is()`:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:is}

Selects an element, but only if it matches at least one selector in the selector list.

The alias `:matches()` is also supported as it was the original name for the selector, and some browsers support it.
It is strongly encouraged to use `:is()` instead as support for `:matches()` may be dropped in the future.

While the level 4 specifications state that [compound](#compound-selector) selectors are supported, some browsers
(Safari) support complex selectors which are planned for level 5 CSS selectors. Soup Sieve also supports
[complex](#complex-selector) selectors.

=== "Syntax"
    ```css
    :is(selector1, selector2)
    ```

=== "Usage"
    ```pycon3
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

## `:lang()` {:#:lang}

Level 3 CSS
: 
    Selects an element whose associated language matches the provided **language** or whose language starts with the
    provided **language** followed by a `-`. Language is determined by the rules of the document type.

    === "Syntax"
        ```css
        :lang(language)
        ```

    === "Usage"
        ```pycon3
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

Level 4 CSS:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}
: 
    The level 4 CSS specifications adds the ability to define multiple language tags using a comma separated list. The
    specifications also allow for BCP 47 language ranges as described in [RFC4647](https://tools.ietf.org/html/rfc4647)
    for extended filtering. This enables implicit wildcard matching between subtags. For instance, `:lang(de-DE)` will
    match all of `de-DE`, `de-DE-1996`, `de-Latn-DE`, `de-Latf-DE`, and `de-Latn-DE-1996`. Implicit wildcard matching
    will not take place at the beginning on the primary language tag, `*` must be used to force wildcard matching at the
    beginning of the language. If desired an explicit wildcard between subtags can be used, but since implicit wildcard
    matching already takes place between subtags, it is not needed: `de-*-DE` would be the same as just using `de-DE`.

    === "Syntax"
        ```css
        :lang('*-language', language2)
        ```

    === "Usage"
        ```pycon3
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

## `:last-child` {:#:last-child}

Selects the last element among a group of sibling elements.

=== "Syntax"
    ```css
    :last-child
    ```

=== "Usage"
    ```pycon3
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

## `:last-of-type` {:#:last-of-type}

Selects the last child of a given type in a group of sibling elements.

=== "Syntax"
    ```css
    element:last-of-type
    ```

=== "Usage"
    ```pycon3
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

## `:link`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:link}

Selects a link (every `#!html <a>` and `#!html <area>` element with an `href` attribute) that has not
yet been visited.

Since Beautiful Soup does not have *visited* states, this will match all links, essentially making the behavior the same
as `:any-link`.

=== "Syntax"
    ```css
    :link
    ```

=== "Usage"
    ```pycon3
    >>> from bs4 import BeautifulSoup as bsx
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

!!! new "New in 2.2"
    The CSS specification recently updated to not include `#!html <link>` in the definition; therefore, Soup Sieve has
    removed it as well.

## `:not()` {:#:not}

Level 3 CSS
: 
    Selects all elements that do not match the selector. The level 3 CSS specification states that `:not()` only
    supports simple selectors.

    === "Syntax"
        ```css
        :not(simple-selector)
        ```

    === "Usage"
        ```pycon3
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
        >>> print(soup.select('div:not(:-soup-contains(more))'))
        [<div>Here is some text.</div>]
        ```

Level 4+ CSS:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}
: 
    Selects all elements that do not match any of the selectors in the selector list. While the level 4 specifications
    state that [compound](#compound-selector) selectors are supported, some browsers (Safari) support complex selectors
    which are planned for level 5 CSS selectors. Soup Sieve also supports [complex](#complex-selector) selectors.

    === "Syntax"
        ```css
        :not(compound.selector, complex > selector)
        ```

    === "Usage"
        ```pycon3
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

## `:nth-child()` {:#:nth-child}

`:nth-child()` matches elements based on their position in a group of siblings.


Level 3 CSS
: 
    - The keywords `even` and `odd`  will respectively select elements whose position is either even or odd amongst a
      group of siblings.

    - Patterns in the form `an+b` selects elements based on their position in a group of siblings, for every positive
      integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both be integers.

    === "Syntax"
        ```css
        :nth-child(even)
        :nth-child(odd)
        :nth-child(2)
        :nth-child(2n+2)
        ```

    === "Usage"
        ```pycon3
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

Level 4+ CSS:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}
: 
    Level 4 CSS adds the additional pattern in the form `an+b of S` where `S` represents a selector list. `an+b` can
    also be substituted with `even` or `odd`.

    When using the pattern `an+b of S`, the pattern will select elements from a sub-group of sibling elements that all
    match the selector list (`[of S]?`), based on their position within that sub-group, using the pattern `an+b`, for
    every positive integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both
    be integers.

    Essentially, `#!css img:nth-of-type(2)` would be equivalent to `#!css :nth-child(2 of img)`. The advantage of using
    `:nth-child(an+b [of S]?)` over `:nth-of-type` is that `:nth-of-type` is restricted to types, while
    `:nth-child(an+b [of S]?)` can use [complex](#complex-selector) selectors.

    While the level 4 specifications state that [compound](#compound-selector) selectors are supported, complex
    selectors are planned for level 5 CSS selectors. Soup Sieve supports [complex](#complex-selector) selectors.

    === "Syntax"
        ```css
        :nth-child(2 of img)
        ```

    === "Usage"
        ```pycon3
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

## `:nth-last-child()` {:#:nth-last-child}

`:nth-last-child()` matches elements based on their position in a group of siblings, counting from the end.

Level 3 CSS
: 
    - Counting from the end, the keywords `even` and `odd`  will respectively select elements whose position is either
      even or odd amongst a group of siblings.

    - Counting from the end, patterns in the form `an+b` selects elements based on their position in a group of
      siblings, for every positive integer or zero value of `n`. The index of the first element is `1`. The values `a`
      and `b` must both be integers.

    === "Syntax"
        ```css
        :nth-last-child(even)
        :nth-last-child(odd)
        :nth-last-child(2)
        :nth-last-child(2n+2)
        ```

    === "Usage"
        ```pycon3
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

Level 4+ CSS:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon}
: 
    Level 4 CSS adds the additional pattern in the form `an+b of S` where `S` represents a selector list. `an+b` can
    also be substituted with `even` or `odd`.

    When using the pattern `an+b of S`, the pattern will select elements from a sub-group of sibling elements that all
    match the selector list (`[of S]?`), based on their position within that sub-group, using the pattern `an+b`, for
    every positive integer or zero value of `n`. The index of the first element is `1`. The values `a` and `b` must both
    be integers. Elements will be counted from the end.

    Essentially, `#!css img:nth-last-of-type(2)` would be equivalent to `#!css :nth-last-child(2 of img)`. The advantage
    of using `:nth-last-child(an+b [of S]?)` over `:nth-last-of-type` is that `:nth-last-of-type` is restricted to
    types, while `:nth-last-child(an+b [of S]?)` can use [complex](#complex-selector) selectors.

    While the level 4 specifications state that [compound](#compound-selector) selectors are supported, complex
    selectors are planned for level 5 CSS selectors. Soup Sieve supports [complex](#complex-selector) selectors.

    === "Syntax"
        ```css
        :nth-last-child(2 of img)
        ```

    === "Usage"
        ```pycon3
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

## `:nth-last-of-type()` {:#:nth-last-of-type}

`:nth-of-type()` matches elements of a given type, based on their position among a group of siblings, counting from the
end.

- The keywords `even` and `odd`, and will respectively select elements, from a sub-group of
  sibling elements that all match the given type, whose position is either even or odd amongst that sub-group of
  siblings. Starting position is counted from the end.

- Patterns in the form `an+b` select from a sub-group of sibling elements that all match the given type, based on their
  position within that sub-group, for every positive integer or zero value of `n`. The index of the first element is
  `1`. The values `a` and `b` must both be integers. Starting position is counted from the end.

=== "Syntax"
    ```css
    element:nth-last-of-type(even)
    element:nth-last-of-type(odd)
    element:nth-last-of-type(2)
    element:nth-last-of-type(2n+2)
    ```

=== "Usage"
    ```pycon3
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

## `:nth-of-type()` {:#:nth-of-type}

`:nth-of-type()` matches elements of a given type, based on their position among a group of siblings.

- The keywords `even` and `odd`, and will respectively select elements, from a sub-group of
  sibling elements that all match the given type, whose position is either even or odd amongst that sub-group of
  siblings.

- Patterns in the form `an+b` select from a sub-group of sibling elements that all match the given type, based on their
  position within that sub-group, for every positive integer or zero value of `n`. The index of the first element is
  `1`. The values `a` and `b` must both be integers.

=== "Syntax"
    ```css
    element:nth-of-type(even)
    element:nth-of-type(odd)
    element:nth-of-type(2)
    element:nth-of-type(2n+2)
    ```

=== "Usage"
    ```pycon3
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

## `:only-child` {:#:only-child}

Selects element without any siblings.

=== "Syntax"
    ```css
    :only-child
    ```

=== "Usage"
    ```pycon3
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

## `:only-of-type` {:#:only-of-type}

Selects element without any siblings that matches a given type.

=== "Syntax"
    ```css
    element:only-of-type
    ```

=== "Usage"
    ```pycon3
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

## `:optional`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:optional}

Selects any `#!html <input>`, `#!html <select>`, or `#!html <textarea>` element that does not have the `required`
attribute set on it.

=== "Syntax"
    ```css
    :optional
    ```

=== "Usage"
    ```pycon3
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

## `:out-of-range`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:out-of-range}

Selects all `#!html <input>` elements whose values are out of range according to their `type`, `min`, and `max`
attributes.

=== "Syntax"
    ```css
    :out-of-range
    ```

=== "Usage"
    ```pycon3
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

## `:placeholder-shown`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:placeholder-shown}

Selects any `#!html <input>` or `#!html <textarea>` element that is currently displaying placeholder text via the
`placeholder` attribute.

=== "Syntax"
    ```css
    :placeholder-shown
    ```

=== "Usage"
    ```pycon3
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

## `:read-only`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:read-only}

Selects elements (such as `#!html <input>` or `#!html <textarea>`) that are *not* editable by the user. This does not
just apply to form elements with `readonly` set, but it applies to **any** element that cannot be edited by the user.

=== "Syntax"
    ```css
    :read-only
    ```

=== "Usage"
    ```pycon3
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

## `:read-write`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:read-write}

Selects elements (such as `#!html <input>` or `#!html <textarea>`) that are editable by the user. This does not just
apply to form elements as it applies to **any** element that can be edited by the user, such as a `#!html <p>` element
with `contenteditable` set on it.

=== "Syntax"
    ```css
    :read-only
    ```

=== "Usage"
    ```pycon3
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

## `:required`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:required}

Selects any `#!html <input>`, `#!html <select>`, or `#!html <textarea>` element that has the `required` attribute set on
it.

=== "Syntax"
    ```css
    :required
    ```

=== "Usage"
    ```pycon3
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

## `:root` {:#:root}

Selects the root element of a document tree.

=== "Syntax"
    ```css
    :root
    ```

=== "Usage"
    ```pycon3
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

## `:scope`:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:scope}

`:scope` represents the the element a `match`, `select`, or `filter` is being called on. If we were, for instance,
using `:scope` on a div (`#!py3 sv.select(':scope > p', soup.div)`) `:scope` would represent **that** div element, and
no others. If called on the Beautiful Soup object which represents the entire document, it would simply select
[`:root`](#:root).

=== "Syntax"
    ```css
    :scope
    ```

=== "Usage"
    ```pycon3
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

## `:where()`:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:where}

Selects an element, but only if it matches at least one selector in the selector list. In browsers, this also has zero
specificity, but this only has relevance in a browser environment where you have multiple CSS styles, and specificity is
used to see which applies. Beautiful Soup and Soup Sieve don't care about specificity so `:where()` is essentially just
an alias for `:is()`.

While the level 4 specifications state that [compound](#compound-selector) selectors are supported, some browsers
(Safari) support complex selectors which are planned for level 5 CSS selectors. Soup Sieve also supports
[complex](#complex-selector) selectors.

=== "Syntax"
    ```css
    :where(selector1, selector2)
    ```

=== "Usage"
    ```pycon3
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

## `:-soup-contains()`:material-star:{: title="Custom" data-md-color-primary="green" .icon} {:#:-soup-contains}

Selects elements that contain the provided text. Text can be found in either itself, or its descendants.

Originally, there was a pseudo-class called `:contains()` that was originally included in a [CSS early draft][contains-draft],
but was dropped from the draft in the end. Soup Sieve implements it how it was originally proposed accept for two
differences: it is called `:-soup-contains()` instead of `:contains()`, and it can accept either a single value, or a
comma separated list of values. An element needs only to match at least one of the items in the comma separated list to
be considered matching.

!!! warning "Rename 2.1"
    The name `:-soup-contains()` is new in version 2.1. Previously, it was known by `:contains()`. While the alias of
    `:contains()` is currently allowed, this alias is deprecated moving forward and will be removed in a future version.
    It is recommended to migrate to the name `:-soup-contains` moving forward.

!!! warning "Expensive Operation"
    `:-soup-contains()` is an expensive operation as it scans all the text nodes of an element under consideration,
    which includes all descendants. Using highly specific selectors can reduce how often it is evaluated.

=== "Syntax"
    ```css
    :-soup-contains(text)
    :-soup-contains("This text", "or this text")
    ```

=== "Usage"
    ```pycon3
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
    >>> print(soup.select('div:-soup-contains("some text")'))
    [<div>Here is <span>some text</span>.</div>]
    ```

## `:-soup-contains-own()`:material-star:{: title="Custom" data-md-color-primary="green" .icon} {:#:-soup-contains-own}

Selects elements that contain the provided text. Text must be found in the target element and not in its descendants. If
text is broken up with with descendant elements, each text node will be evaluated separately.

Syntax is the same as [`:-soup-contains()`](#:-soup-contains).

=== "Syntax"
    ```css
    :-soup-contains-own(text)
    :-soup-contains-own("This text", "or this text")
    ```

=== "Usage"
    ```pycon3
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
    >>> print(soup.select('div:-soup-contains-own("some")'))
    [<div>Here is some more text.</div>]
    ```

!!! new "New in 2.1"
    `:-soup-contains-own()` was added in 2.1.

--8<--
selector_styles.md
--8<--

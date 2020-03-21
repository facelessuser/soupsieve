# Non-Applicable Pseudo Classes

## Overview

These pseudo classes are recognized by the parser, and have been identified as not being applicable in a Beautiful Soup
environment. While the pseudo-classes will parse correctly, they will not match anything. This is because they cannot be
implemented outside a live, browser environment. If at any time these are dropped from the CSS spec, they will simply
be removed.

## `:active`<span class="html5 badge"></span> {:#:active}

Selects active elements.

=== "Syntax"
    ```css
    :active
    ```

## `:current`<span class="html5 badge"></span><span class="lab badge"></span> {:#:current}

`:current` selects the element, or an ancestor of the element, that is currently being displayed. The functional form of
`:current()` takes a compound selector list.

=== "Syntax"
    ```css
    :current
    :current(selector1, selector2)
    ```

## `:focus`<span class="html5 badge"></span> {:#:focus}

Represents an an element that has received focus.

=== "Syntax"
    ```css
    :focus
    ```

## `:focus-visible`<span class="html5 badge"></span><span class="lab badge"></span> {:#:focus-visible}

Selects an element that matches `:focus` and the user agent determines that the focus should be made evident on the
element.

=== "Syntax"
    ```css
    :focus-visible
    ```

## `:focus-within`<span class="html5 badge"></span><span class="lab badge"></span> {:#:focus-within}

Selects an element that has received focus or contains an element that has received focus.

=== "Syntax"
    ```css
    :focus-within
    ```

## `:future`<span class="html5 badge"></span><span class="lab badge"></span> {:#:future}

Selects an element that is defined to occur entirely after a `:current` element.

=== "Syntax"
    ```css
    :future
    ```

## `:host`<span class="html5 badge"></span><span class="lab badge"></span> {:#host}

`:host` selects the element hosting a shadow tree. While the function form of `:host()` takes a complex selector list
and matches the shadow host only if it matches one of the selectors in the list.

=== "Syntax"
    ```css
    :host
    :host(selector1, selector2)
    ```

## `:host-context()`<span class="html5 badge"></span><span class="lab badge"></span> {:#:host-context}

Selects the element hosting shadow tree, but only if one of the element's ancestors match a selector in the selector
list.

=== "Syntax"
    ```css
    :host-context(parent descendant)
    ```

## `:hover`<span class="html5 badge"></span> {:#:hover}

Selects an element when the user interacts with it by hovering over it with a pointing device.

=== "Syntax"
    ```css
    :hover
    ```

## `:local-link`<span class="html5 badge"></span><span class="lab badge"></span> {:#:local-link}

Selects link (every `#!html <a>`, `#!html <link>`, and `#!html <area>` element with an `href` attribute) elements whose
absolute URL matches the element’s own document URL.

=== "Syntax"
    ```css
    :local-link
    ```

## `:past`<span class="html5 badge"></span><span class="lab badge"></span> {:#:past}

Selects an element that is defined to occur entirely prior to a `:current` element.

=== "Syntax"
    ```css
    :past
    ```

## `:paused`<span class="html5 badge"></span><span class="lab badge"></span> {:#:paused}

Selects an element that is capable of being played or paused (such as an audio, video, or similar resource) and is
currently "paused".

=== "Syntax"
    ```css
    :paused
    ```

## `:playing`<span class="html5 badge"></span><span class="lab badge"></span> {:#:playing}

Selects an element that is capable of being played or paused (such as an audio, video, or similar resource) and is
currently "playing".

=== "Syntax"
    ```css
    :playing
    ```

## `:target`<span class="html5 badge"></span> {:#:target}

Selects a unique element (the target element) with an id matching the URL's fragment.

=== "Syntax"
    ```css
    :target
    ```

## `:target-within`<span class="html5 badge"></span><span class="lab badge"></span> {:#:target-within}

Selects a unique element with an id matching the URL's fragment or an element which contains the element.

=== "Syntax"
    ```css
    :target-within
    ```

## `:user-invalid`<span class="html5 badge"></span><span class="lab badge"></span> {:#:user-invalid}

Selects an element with incorrect input, but only after the user has significantly interacted with it.

=== "Syntax"
    ```css
    :user-invalid
    ```

## `:visited`<span class="html5 badge"></span> {:#:visited}

Selects links that have already been visited.

=== "Syntax"
    ```css
    :visited
    ```

--8<--
selector_styles.txt
refs.txt
--8<--

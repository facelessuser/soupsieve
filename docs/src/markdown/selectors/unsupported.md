# Non-Applicable Pseudo Classes

## Overview

These pseudo classes are recognized by the parser, and have been identified as not being applicable in a Beautiful Soup
environment. While the pseudo-classes will parse correctly, they will not match anything. This is because they cannot be
implemented outside a live, browser environment. If at any time these are dropped from the CSS spec, they will simply
be removed.

## `:active`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:active}

Selects active elements.

=== "Syntax"
    ```css
    :active
    ```

## `:current`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:current}

`:current` selects the element, or an ancestor of the element, that is currently being displayed. The functional form of
`:current()` takes a compound selector list.

=== "Syntax"
    ```css
    :current
    :current(selector1, selector2)
    ```

## `:focus`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:focus}

Represents an an element that has received focus.

=== "Syntax"
    ```css
    :focus
    ```

## `:focus-visible`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:focus-visible}

Selects an element that matches `:focus` and the user agent determines that the focus should be made evident on the
element.

=== "Syntax"
    ```css
    :focus-visible
    ```

## `:focus-within`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:focus-within}

Selects an element that has received focus or contains an element that has received focus.

=== "Syntax"
    ```css
    :focus-within
    ```

## `:future`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:future}

Selects an element that is defined to occur entirely after a `:current` element.

=== "Syntax"
    ```css
    :future
    ```

## `:host`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#host}

`:host` selects the element hosting a shadow tree. While the function form of `:host()` takes a complex selector list
and matches the shadow host only if it matches one of the selectors in the list.

=== "Syntax"
    ```css
    :host
    :host(selector1, selector2)
    ```

## `:host-context()`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:host-context}

Selects the element hosting shadow tree, but only if one of the element's ancestors match a selector in the selector
list.

=== "Syntax"
    ```css
    :host-context(parent descendant)
    ```

## `:hover`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:hover}

Selects an element when the user interacts with it by hovering over it with a pointing device.

=== "Syntax"
    ```css
    :hover
    ```

## `:local-link`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:local-link}

Selects link (every `#!html <a>`, `#!html <link>`, and `#!html <area>` element with an `href` attribute) elements whose
absolute URL matches the element’s own document URL.

=== "Syntax"
    ```css
    :local-link
    ```

## `:past`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:past}

Selects an element that is defined to occur entirely prior to a `:current` element.

=== "Syntax"
    ```css
    :past
    ```

## `:paused`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:paused}

Selects an element that is capable of being played or paused (such as an audio, video, or similar resource) and is
currently "paused".

=== "Syntax"
    ```css
    :paused
    ```

## `:playing`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:playing}

Selects an element that is capable of being played or paused (such as an audio, video, or similar resource) and is
currently "playing".

=== "Syntax"
    ```css
    :playing
    ```

## `:target`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:target}

Selects a unique element (the target element) with an id matching the URL's fragment.

=== "Syntax"
    ```css
    :target
    ```

## `:target-within`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:target-within}

Selects a unique element with an id matching the URL's fragment or an element which contains the element.

=== "Syntax"
    ```css
    :target-within
    ```

## `:user-invalid`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon}:material-flask:{: title="Experimental" data-md-color-primary="purple" .icon} {:#:user-invalid}

Selects an element with incorrect input, but only after the user has significantly interacted with it.

=== "Syntax"
    ```css
    :user-invalid
    ```

## `:visited`:material-language-html5:{: title="HTML" data-md-color-primary="orange" .icon} {:#:visited}

Selects links that have already been visited.

=== "Syntax"
    ```css
    :visited
    ```

--8<--
selector_styles.md
--8<--

# Combinators and Selector Lists

CSS employs a number of tokens in order to represent lists or to provide relational context between two selectors.

## Selector Lists

Selector lists use the comma (`,`) to join multiple selectors in a list. When presented with a selector list, any
selector in the list that matches an element will return that element.

=== "Syntax"
    ```css
    element1, element2
    ```

=== "Usage"
    ```pycon3
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

## Descendant Combinator

Descendant combinators combine two selectors with whitespace (<code> </code>) in order to signify that the second
element is matched if it has an ancestor that matches the first element.

=== "Syntax"
    ```css
    parent descendant
    ```

=== "Usage"
    ```pycon3
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

## Child combinator

Child combinators combine two selectors with `>` in order to signify that the second element is matched if it has a
parent that matches the first element.

=== "Syntax"
    ```css
    parent > child
    ```

=== "Usage"
    ```pycon3
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

## General sibling combinator

General sibling combinators combine two selectors with `~` in order to signify that the second element is matched if it
has a sibling that precedes it that matches the first element.

=== "Syntax"
    ```css
    prevsibling ~ sibling
    ```

=== "Usage"
    ```pycon3
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

## Adjacent sibling combinator

Adjacent sibling combinators combine two selectors with `+` in order to signify that the second element is matched if it
has an adjacent sibling that precedes it that matches the first element.

=== "Syntax"
    ```css
    prevsibling + nextsibling
    ```

=== "Usage"
    ```pycon3
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

--8<--
selector_styles.md
--8<--

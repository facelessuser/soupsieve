# Combinators and Selector Lists

CSS employs a number of tokens in order to represent lists or to provide relational context between two selectors.

## Selector Lists

Selector lists use the comma (`#!css ,`) to join multiple selectors in a list. When presented with a selector list, any
selector in the list that matches an element will return that element.

/// tab | Syntax
```css
element1, element2
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<h1>Title</h1>
<p>Paragraph</p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('h1, p')
```
///

## Descendant Combinator

Descendant combinators combine two selectors with whitespace (<code> </code>) in order to signify that the second
element is matched if it has an ancestor that matches the first element.

/// tab | Syntax
```css
parent descendant
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<div><p>Paragraph 1</p></div>
<div><p>Paragraph 2</p></div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('body p')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/Descendant_combinator

> [!warning]
> Selectors like the descendant and subsequent sibling combinators (`#!css a b` and `#!css a ~ b`) often cause entire
> subtrees of the main document tree to be crawled when evaluating a single element. If used poorly, this can impact
> performance in a non-linear ways. It should be noted that Soup Sieve employs caching to reduce performance concerns in
> various cases, but there will always be the potential produce non-linear cases simply due to how the selectors work.

## Child combinator

Child combinators combine two selectors with `>` in order to signify that the second element is matched if it has a
parent that matches the first element.

/// tab | Syntax
```css
parent > child
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<div><p>Paragraph 1</p></div>
<div><ul><li><p>Paragraph 2</p></li></ul></div>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('div > p')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/Child_combinator

## General Sibling Combinator

General sibling combinators combine two selectors with `#!css ~` in order to signify that the second element is matched
if it has a sibling that precedes it that matches the first element.

/// tab | Syntax
```css
prevsibling ~ sibling
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<h1>Title</h1>
<p>Paragraph 1</p>
<p>Paragraph 2</p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('h1 ~ p')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/General_sibling_combinator

> [!warning]
> Selectors like the descendant and subsequent sibling combinators (`#!css a b` and `#!css a ~ b`) often cause entire
> subtrees of the main document tree to be crawled when evaluating a single element. If used poorly, this can impact
> performance in a non-linear ways. It should be noted that Soup Sieve employs caching to reduce performance concerns in
> various cases, but there will always be the potential produce non-linear cases simply due to how the selectors work.

## Adjacent Sibling Combinator

Adjacent sibling combinators combine two selectors with `#!css +` in order to signify that the second element is matched
if it has an adjacent sibling that precedes it that matches the first element.

/// tab | Syntax
```css
prevsibling + nextsibling
```
///

/// tab | Usage
```py play
from bs4 import BeautifulSoup as bs
html = """
<html>
<head></head>
<body>
<h1>Title</h1>
<p>Paragraph 1</p>
<p>Paragraph 2</p>
</body>
</html>
"""
soup = bs(html, 'html5lib')
soup.select('h1 + p')
```
///

> [!tip] Additional Reading
> https://developer.mozilla.org/en-US/docs/Web/CSS/Adjacent_sibling_combinator

--8<--
selector_styles.md
--8<--

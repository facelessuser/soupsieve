# Soup Sieve (WIP)

Soup Sieve is a CSS4 selector library designed to be used with Beautiful Soup 4.

Beautiful Soup is a useful library for processing HTML documents.  It comes with a builtin CSS selection API.
Unfortunately, the CSS API is not without some issues. In addition, it also lacks support for useful pseudo classes.

Soup Sieve supports a subset of CSS4 selectors which allows useful filtering of tags in a Beautiful Soup structure. Soup
Sieve does not attempt to support all CSS4 selectors as many don't make sense in a non-browser environment. Soup Sieve
does support many selectors that are useful for parsing such as: `.classes`, `#ids`, `[attributes=value]`,
`parent child`, `parent > child`, `sibling ~ sibling`, `sibling + sibling`, `:not(element.class, element2.class)`,
`:is(element.class, element2.class)`, `parent:has(> child)`, and many more.

## Documentation

Coming soon!

## License

MIT License

Copyright (c) 2018 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

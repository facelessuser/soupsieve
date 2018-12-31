[![Unix Build Status][travis-image]][travis-link]
[![Windows Build Status][appveyor-image]][appveyor-link]
[![Coverage Status][codecov-image]][codecov-link]
[![PyPI Version][pypi-image]][pypi-link]
![License][license-image-mit]

# Soup Sieve

## Overview

Soup Sieve is a CSS selector library designed to be used with [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/#). It aims to provide selecting, matching, and filtering using modern CSS selectors. Soup Sieve currently provides selectors from the CSS level 1 specifications up through the latest CSS level 4 drafts (though some are not yet implemented).

While Beautiful Soup comes with a builtin CSS selection API, it is very basic and not without issues. It lacks support for many modern CSS features. Soup Sieve is planned to officially replace Beautiful Soup's current internal CSS selector implementation, but can also be imported in order to use its API directly.

Soup Sieve implements most of the CSS selectors, though there are a number that don't make sense in a non-browser environment. Selectors that cannot provide meaningful functionality simply do not match anything. Some of the supported selectors are:

- `#!css .classes`
- `#!css #ids`
- `#!css [attributes=value]`
- `#!css parent child`
- `#!css parent > child`
- `#!css sibling ~ sibling`
- `#!css sibling + sibling`
- `#!css :not(element.class, element2.class)`
- `#!css :is(element.class, element2.class)`
- `#!css parent:has(> child)`
- and [many more](https://facelessuser.github.io/soupsieve/selectors/)


## Installation

You must have Beautiful Soup already installed:

```
pip install beautifulsoup4
```

Then use `pip` to install Soup Sieve:

```
pip install soupsieve
```

## Documentation

Documentation is found here: http://facelessuser.github.io/soupsieve/.

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

[codecov-image]: https://img.shields.io/codecov/c/github/facelessuser/soupsieve/master.svg
[codecov-link]: https://codecov.io/github/facelessuser/soupsieve
[travis-image]: https://img.shields.io/travis/facelessuser/soupsieve/master.svg?label=Unix%20Build&logo=travis
[travis-link]: https://travis-ci.org/facelessuser/soupsieve
[appveyor-image]: https://img.shields.io/appveyor/ci/facelessuser/soupsieve/master.svg?label=Windows%20Build&logo=appveyor
[appveyor-link]: https://ci.appveyor.com/project/facelessuser/soupsieve
[pypi-image]: https://img.shields.io/pypi/v/soupsieve.svg?logo=python&logoColor=white
[pypi-link]: https://pypi.python.org/pypi/soupsieve
[license-image-mit]: https://img.shields.io/badge/license-MIT-blue.svg

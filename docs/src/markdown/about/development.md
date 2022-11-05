# Development

## Project Layout

There are a number of files for build, test, and continuous integration in the root of the project, but in general, the
project is broken up like so.

```
├── docs
│   └── src
│       ├── dictionary
│       └── markdown
├── soupsieve
├── requirements
└── tests
```

Directory             | Description
--------------------- | -----------
`docs/src/dictionary` | Contains the spell check wordlist(s) for the project.
`docs/src/markdown`   | Contains the content for the documentation.
`soupsieve`           | Contains the source code for the project.
`requirements`        | Contains files with lists of dependencies that are required for the project, and required for continuous integration.
`tests`               | Contains unit test files.

## Coding Standards

When writing code, the code should roughly conform to PEP8 and PEP257 suggestions.  The project utilizes the Flake8
linter (with some additional plugins) to ensure code conforms (give or take some of the rules).  When in doubt, follow
the formatting hints of existing code when adding files or modifying existing files.  Listed below are the modules used:

- @gitlab:pycqa/flake8
- @gitlab:pycqa/flake8-docstrings
- @gitlab:pycqa/pep8-naming
- @ebeweber/flake8-mutable
- @gforcada/flake8-builtins

Usually this can be automated with Tox (assuming it is installed): `tox -e lint`.

## Building and Editing Documents

Documents are in Markdown (with with some additional syntax provided by extensions) and are converted to HTML via Python
Markdown. If you would like to build and preview the documentation, you must have these packages installed:

- @Python-Markdown/markdown: the Markdown parser.
- @mkdocs/mkdocs: the document site generator.
- @squidfunk/mkdocs-material: a material theme for MkDocs.
- @facelessuser/pymdown-extensions: this Python Markdown extension bundle.

It is advised that you just install document dependencies with the following as the above list may not include all
document plugins:

```
pip install -r requirements/docs.txt
```

In order to build and preview the documents, just run the command below from the root of the project and you should be
able to view the documents at `localhost:8000` in your browser. After that, you should be able to update the documents
and have your browser preview update live.

```
mkdocs serve
```

## Spell Checking Documents

Spell checking is performed via @facelessuser/pyspelling.

During validation we build the docs and spell check various files in the project. [Aspell][aspell] must be installed and
in the path.  Currently this project uses one of the more recent versions of Aspell.  It is not expected that everyone
will install and run Aspell locally, but it will be run in CI tests for pull requests.

In order to perform the spell check locally, it is expected you are setup to build the documents, and that you have
Aspell installed in your system path (if needed you can use the `--binary` option to point to the location of your
Aspell binary). It is also expected that you have the `en` dictionary installed as well. To initiate the spell check,
run the following command from the root of the project.

You will need to make sure the documents are built first:

```
mkdocs build --clean
```

And then run the spell checker.

```
pyspelling
```

It should print out the files with the misspelled words if any are found.  If you find it prints words that are not
misspelled, you can add them in `docs/src/dictionary/en-custom.text`.

## Validation Tests

In order to preserve good code health, a test suite has been put together with pytest (@pytest-dev/pytest).  To run
these tests, you can use the following command:

```
pytest
```

### Running Validation With Tox

Tox (@tox-dev/tox) is a great way to run the validation tests, spelling checks, and linting in virtual environments so
as not to mess with your current working environment. Tox will use the specified Python version for the given
environment and create a virtual environment and install all the needed requirements (minus Aspell).  You could also
setup your own virtual environments with the Virtualenv module without Tox, and manually do the same.

First, you need to have Tox installed:

```
pip install tox
```

By running Tox, it will walk through all the environments and create them (assuming you have all the python versions on
your machine) and run the related tests.  See `tox.ini` to learn more.

```
tox
```

If you don't have all the Python versions needed to test all the environments, those entries will fail. To run the tests
for specific versions of Python, you specify the environment with `-e PXY` where `X` is the major version and `Y` is the
minor version.

```
tox -e py310
```

To target linting:

```
tox -e lint
```

To select spell checking and document building:

```
tox -e documents
```

## Code Coverage

When running the validation tests through Tox, it is setup to track code coverage via the Coverage
(@bitbucket:ned/coveragepy) module.  Coverage is run on each `pyxx` environment.  If you've made changes to the code,
you can clear the old coverage data:

```
coverage erase
```

Then run each unit test environment to generate coverage data. All the data from each run is merged together.  HTML is
output for each file in `.tox/pyXX/tmp`.  You can use these to see areas that are not covered/exercised yet with
testing.

You can checkout `tox.ini` to see how this is accomplished.

## Code Documentation

The Soup Sieve module is laid out in the following structure:

```
soupseive
├── __init__.py
├── __meta__.py
├── css_match.py
├── css_parser.py
├── css_types.py
└── util.py
```

File            | Description
--------------- | -----------
`__init__.py`   | Contains the API for the user.
`__meta__.py`   | Contains package meta data like version.
`css_match.py`  | Contains the logic for matching tags with a CSS selector.
`css_parser.py` | Contains the CSS selector parser.
`css_types.py`  | Contains the CSS types for the compiled CSS patterns.
`util.py`       | Contains miscellaneous helper functions, classes, and constants.

### Compiled CSS Selector Structure

When a CSS selector string is given to Soup Sieve, it is run through the `CSSParser` class.  `CSSParser` will return a
`SelectorList` class. This class is sent to the `SoupSieve` class as a parameter along with things like `namespace` and
`flags`. One of the most important things to understand when contributing is the structure of the `SelectorList` class.

A `SelectorList` represents a list of compound selectors.  So if you had the selector `#!css div > p`, you would get a
`SelectorList` object containing one `Selector` object. If you had `#!css div, p`, you would get a `SelectorList` with
two `Selector` objects as this is a selector list of two compound selectors.

A compound selector gets parsed into pieces. Each part of a specific compound selector is usually assigned to an
attribute in a single `Selector` object. The attributes of the `Selector` object may be as simple as a boolean or a
string, but they can also be a tuple of more `SelectorList` objects. In the case of `#!css *:not(p, div)`, `#!css *`
will be a `SelectorList` with one `Selector`. The `#!css :not(p, div)` selector list will be a tuple containing one
`SelectorList` of two `Selectors` (one for `p` and one for `div`) under the `selectors` attribute of the `#!css *`
`Selector`.

In short, `Selectors` are always contained within a `SelectorList`, and a compound selector is a single `Selector`
object that may chain other `SelectorLists` objects depending on the complexity of the compound selector. If you provide
a selector list, then you will get multiple `Selector` objects (one for each compound selector in the list) which in
turn may chain other `Selector` objects.

To view the selector list in in a compiled object for debugging purposes, one can access it via `SoupSieve.selectors`,
though it is recommended to pretty print them:

```pycon3
>>> import soupsieve as sv
>>> sv.compile('this > that.class[name=value]').selectors.pretty()
SelectorList(
    selectors=(
        Selector(
            tag=SelectorTag(
                name='that',
                prefix=None),
            ids=(),
            classes=(
                'class',
                ),
            attributes=(
                SelectorAttribute(
                    attribute='name',
                    prefix='',
                    pattern=re.compile(
                        '^value$'),
                    xml_type_pattern=None),
                ),
            nth=(),
            selectors=(),
            relation=SelectorList(
                selectors=(
                    Selector(
                        tag=SelectorTag(
                            name='this',
                            prefix=None),
                        ids=(),
                        classes=(),
                        attributes=(),
                        nth=(),
                        selectors=(),
                        relation=SelectorList(
                            selectors=(),
                            is_not=False,
                            is_html=False),
                        rel_type='>',
                        contains=(),
                        lang=(),
                        flags=0),
                    ),
                is_not=False,
                is_html=False),
            rel_type=None,
            contains=(),
            lang=(),
            flags=0),
        ),
    is_not=False,
    is_html=False)
```

### `SelectorList`

```py3
class SelectorList:
    """Selector list."""

    def __init__(self, selectors=tuple(), is_not=False):
        """Initialize."""
```

Attribute      | Description
-------------- | -----------
`selectors`    | A list of `Selector` objects.
`is_not`       | The selectors in the selector list are from a `:not()`.
`is_html`      | The selectors in the selector list are HTML specific.

### `Selector`

```py3
class Selector:
    """Selector."""

    def __init__(
        self, tag, ids, classes, attributes, nth, selectors, relation,
        rel_type, contains, lang, flags
    ):
        """Initialize."""
```

Flags               | Description
------------------- | -----------
`SEL_EMPTY`         | The current compound selector contained an `:empty` pseudo-class.
`SEL_ROOT`          | The current compound selector contains `:root`.
`SEL_DEFAULT`       | The compound selector has a `:default` pattern  and requires additional logic to determine if it is the first `submit` button in a form.
`SEL_INDETERMINATE` | The compound selector has a `:indeterminate` pattern and requires additional logic to ensure a `radio` element and all of the `radio` elements with the same `name` under a form are not set.

Attribute       | Description
--------------- | -----------
`tag`           | Contains a single [`SelectorTag`](#selectortag) object, or `None`.
`id`            | Contains a tuple of ids to match. Usually if multiple conflicting ids are present, it simply won't match a tag, but it allows multiple to handle the syntax `tag#1#2` even if it is invalid.
`classes`       | Contains a tuple of class names to match.
`attributes`    | Contains a tuple of attributes. Each attribute is represented as a [`SelectorAttribute`](#selectorattribute).
`nth`           | Contains a tuple containing `nth` selectors, each selector being represented as a [`SelectorNth`](#selectornth). `nth` selectors contain things like `:first-child`, `:only-child`, `#!css :nth-child()`, `#!css :nth-of-type()`, etc.
`selectors`     | Contains a tuple of `SelectorList` objects for each pseudo-class selector  part of the compound selector: `#!css :is()`, `#!css :not()`, `#!css :has()`, etc.
`relation`      | This will contain a `SelectorList` object with one `Selector` object, which could in turn chain an additional relation depending on the complexity of the compound selector.  For instance, `div > p + a` would be a `Selector` for `a` that contains a `relation` for `p` (another `SelectorList` object) which also contains a relation of `div`.  When matching, we would match that the tag is `a`, and then walk its relation chain verifying that they all match. In this case, the relation chain would be a direct, previous sibling of `p`, which has a direct parent of `div`. A `:has()` pseudo-class would walk this in the opposite order. `div:has(> p + a)` would verify `div`, and then check for a child of `p` with a sibling of `a`.
`rel_type`      | `rel_type` is attached to relational selectors. In the case of `#!css div > p + a`, the relational selectors of `div` and `p` would get a relational type of `>` and `+` respectively. `:has()` relational `rel_type` are preceded with `:` to signify a forward looking relation.
`contains`      | Contains a tuple of [`SelectorContains`](#selectorcontains) objects. Each object contains the list of text to match an element's content against.
`lang`          | Contains a tuple of [`SelectorLang`](#selectorlang) objects.
`flags`         | Selector flags that used to signal a type of selector is present.

### `SelectorNull`

```py3
class SelectorNull:
    """Null Selector."""

    def __init__(self):
        """Initialize."""
```

The null selector is like `Selector`, but it matches nothing.

### `SelectorTag`

```py3
class SelectorTag:
    """Selector tag."""

    def __init__(self, name, prefix):
        """Initialize."""
```

Attribute     | Description
------------- | -----------
`name`        | `name` contains the tag name to match.
`prefix`      | `prefix` contains the namespace prefix to match. `prefix` can also be `None`.


### `SelectorAttribute`

```py3
class SelectorAttribute:
    """Selector attribute rule."""

    def __init__(self, attribute, prefix, pattern, xml_type_pattern):
        """Initialize."""
```

Attribute           | Description
------------------- | -----------
`attribute`         | Contains the attribute name to match.
`prefix`            | Contains the attribute namespace prefix to match if any.
`pattern`           | Contains a `re` regular expression object that matches the desired attribute value.
`xml_type_pattern`  | As the default `type` pattern is case insensitive, when the attribute value is `type` and a case sensitivity has not been explicitly defined, a secondary case sensitive `type` pattern is compiled for use with XML documents when detected.

### `SelectorContains`

```py3
class SelectorContains:
    """Selector contains rule."""

    def __init__(self, text):
        """Initialize."""
```

Attribute           | Description
------------------- | -----------
`text`              | A tuple of acceptable text that that an element should match. An element only needs to match at least one.

### `SelectorNth`

```py3
class SelectorNth:
    """Selector nth type."""

    def __init__(self, a, n, b, of_type, last, selectors):
        """Initialize."""
```

Attribute     | Description
------------- | -----------
`a`           | The `a` value in the formula `an+b` specifying an index.
`n`           | `True` if the provided formula has included a literal `n` which signifies the formula is not a static index.
`b`           | The `b` value in the formula `an+b`.
`type`        | `True` if the `nth` pseudo-class is an `*-of-type` variant.
`last`        | `True` if the `nth` pseudo-class is a `*last*` variant.
`selectors`   | A `SelectorList` object representing the `of S` portion of `:nth-chld(an+b [of S]?)`.

### `SelectorLang`

```py3
class SelectorLang:
    """Selector language rules."""

    def __init__(self, languages):
        """Initialize."""
```

Attribute     | Description
------------- | -----------
`languages`   | A list of regular expression objects that match a language pattern.

# Development

## Project Layout

There are a number of files for build, test, and continuous integration in the root of the project, but in general, the project is broken up like so.

```
├── docs
│   └── src
│       ├── dictionary
│       └── markdown
├── soupsieve
└── requirements

```

Directory             | Description
--------------------- | -----------
`docs/src/dictionary` | This contains the spell check wordlist(s) for the project.
`docs/src/markdown`   | This contains the content for the documentation.
`soupsieve`           | This contains the source code for the project.
`requirements`        | This contains files with lists of dependencies that are required for the project, and required for continuous integration.

## Coding Standards

When writing code, the code should roughly conform to PEP8 and PEP257 suggestions.  The project utilizes the Flake8 linter (with some additional plugins) to ensure code conforms (give or take some of the rules).  When in doubt, follow the formatting hints of existing code when adding or modifying files. existing files.  Listed below are the modules used:

- @gitlab:pycqa/flake8
- @gitlab:pycqa/flake8-docstrings
- @gitlab:pycqa/pep8-naming
- @ebeweber/flake8-mutable
- @gforcada/flake8-builtins

Usually this can be automated with Tox (assuming it is installed): `tox -e lint`.

## Building and Editing Documents

Documents are in Markdown (with with some additional syntax provided by extensions) and are converted to HTML via Python Markdown. If you would like to build and preview the documentation, you must have these packages installed:

- @Python-Markdown/markdown: the Markdown parser.
- @mkdocs/mkdocs: the document site generator.
- @squidfunk/mkdocs-material: a material theme for MkDocs.
- @facelessuser/pymdown-extensions: this Python Markdown extension bundle.

In order to build and preview the documents, just run the command below from the root of the project and you should be able to view the documents at `localhost:8000` in your browser. After that, you should be able to update the documents and have your browser preview update live.

```
mkdocs serve
```

## Spell Checking Documents

Spell checking is performed via @facelessuser/pyspelling.

During validation we build the docs and spell check various files in the project. [Aspell][aspell] must be installed and in the path.  Currently this project uses one of the more recent versions of Aspell.  It is not expected that everyone will install and run Aspell locally, but it will be run in CI tests for pull requests.

In order to perform the spell check, it is expected you are setup to build the documents, and that you have Aspell installed in your system path (if needed you can use the `--binary` option to point to the location of your Aspell binary). It is also expected that you have the `en` dictionary installed as well. To initiate the spell check, run the following command from the root of the project.

You will need to make sure the documents are built first:

```
mkdocs build --clean
```

And then run the spell checker. Using `python -m` from the project root will load your checked out version of PySpelling instead of your system installed version:

```
pyspelling
```

It should print out the files with the misspelled words if any are found.  If you find it prints words that are not misspelled, you can add them in `docs/src/dictionary/en-custom.text`.

## Validation Tests

In order to preserve good code health, a test suite has been put together with pytest (@pytest-dev/pytest). There are currently two kinds of tests: syntax and targeted.  To run these tests, you can use the following command:

```
python run_tests.py
```

### Running Validation With Tox

Tox (@tox-dev/tox) is a great way to run the validation tests, spelling checks, and linting in virtual environments so as not to mess with your current working environment. Tox will use the specified Python version for the given environment and create a virtual environment and install all the needed requirements (minus Aspell).  You could also setup your own virtual environments with the Virtualenv module without Tox, and manually do the same.

First, you need to have Tox installed:

```
pip install tox
```

By running Tox, it will walk through all the environments and create them (assuming you have all the python versions on your machine) and run the related tests.  See `tox.ini` to learn more.

```
tox
```

If you don't have all the Python versions needed to test all the environments, those entries will fail.  You can ignore those.  Spelling will also fail if you don't have the correct version of Aspell.

As most people will not have all the Python versions on their machine, it makes more sense to target specific environments. To target a specific environment to test, you use the `-e` option to select the environment of interest.  To select lint:

```
tox -e lint
```

To select Python 3.7 unit tests (or other versions -- change accordingly):

```
tox -e py37
```

To select spelling and document building:

```
tox -e documents
```

## Code Coverage

When running the validation tests through Tox, it is setup to track code coverage via the Coverage (@bitbucket:ned/coveragepy) module.  Coverage is run on each `pyxx` environment.  If you've made changes to the code, you can clear the old coverage data:

```
coverage erase
```

Then run each unit test environment to and coverage will be calculated. All the data from each run is merged together.  HTML is output for each file in `.tox/pyXX/tmp`.  You can use these to see areas that are not covered/exercised yet with testing.

You can checkout `tox.ini` to see how this is accomplished.

--8<-- "links.txt"

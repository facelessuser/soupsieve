"""Tests for ASCII-only case folding with the attribute selector i flag."""

import bs4
import pytest
import soupsieve


@pytest.fixture(params=['html.parser', 'html5lib', 'lxml', 'xml'])
def parser(request):
    """Exercise HTML parsers and the XML parser when available."""
    if request.param == 'html5lib':
        pytest.importorskip('html5lib')
    elif request.param in ('lxml', 'xml'):
        pytest.importorskip('lxml')
    return request.param


@pytest.mark.parametrize(
    ('operator', 'ascii_value', 'unicode_value'),
    [
        ('=', 'S', '\u017f'),
        ('^=', 'Start', '\u017ftart'),
        ('$=', 'endS', 'end\u017f'),
        ('*=', 'aSb', 'a\u017fb'),
        ('~=', 'a S b', 'a \u017f b'),
        ('|=', 'S-end', '\u017f-end'),
    ],
)
def test_explicit_i_folds_ascii_only(parser, operator, ascii_value, unicode_value):
    """Match ASCII case but not Unicode lookalikes for each operator."""
    markup = f'<root><a id="ascii" data-x="{ascii_value}"></a><a id="unicode" data-x="{unicode_value}"></a></root>'
    soup = bs4.BeautifulSoup(markup, parser)
    assert [node['id'] for node in soupsieve.select(f'[data-x{operator}"s" i]', soup)] == ['ascii']


@pytest.mark.parametrize(
    ('selector_value', 'other_value'),
    [('s', '\u017f'), ('k', '\u212a'), ('i', 'İ'), ('i', '\u0131'), ('é', 'É')],
)
def test_explicit_i_preserves_unicode_case(parser, selector_value, other_value):
    """Match identical non-ASCII values without Unicode case folding."""
    markup = f'<root><a id="same" data-x="{selector_value}"></a><a id="different" data-x="{other_value}"></a></root>'
    soup = bs4.BeautifulSoup(markup, parser)
    assert [node['id'] for node in soupsieve.select(f'[data-x="{selector_value}" i]', soup)] == ['same']


def test_explicit_i_not_equal_extension(parser):
    """Apply ASCII-only matching to Soup Sieve's not-equal extension."""
    markup = '<root><a id="ascii" data-x="S"></a><a id="unicode" data-x="\u017f"></a></root>'
    soup = bs4.BeautifulSoup(markup, parser)
    assert [node['id'] for node in soupsieve.select('a[data-x!="s" i]', soup)] == ['unicode']


@pytest.mark.parametrize('operator', ['*=', '$=', '~='])
def test_explicit_i_handles_newlines(parser, operator):
    """Keep matching across and around newlines."""
    soup = bs4.BeautifulSoup('<root><a id="match" data-x="prefix&#10;S"></a></root>', parser)
    assert [node['id'] for node in soupsieve.select(f'[data-x{operator}"s" i]', soup)] == ['match']

"""Test that we don't fail the same test cases that Beautiful Soup fails for."""
from bs4 import BeautifulSoup
import unittest
import soupsieve as sv


class SelectorNthOfTypeBugTest(unittest.TestCase):
    """
    Original Beautiful soup test html document.

    http://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/bs4/tests/test_tree.py, line 1627.
    """

    HTML = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>The title</title>
<link rel="stylesheet" href="blah.css" type="text/css" id="l1">
</head>
<body>
<custom-dashed-tag class="dashed" id="dash1">Hello there.</custom-dashed-tag>
<div id="main" class="fancy">
<div id="inner">
<h1 id="header1">An H1</h1>
<p>Some text</p>
<p class="onep" id="p1">Some more text</p>
<h2 id="header2">An H2</h2>
<p class="class1 class2 class3" id="pmulti">Another</p>
<a href="http://bob.example.org/" rel="friend met" id="bob">Bob</a>
<h2 id="header3">Another H2</h2>
<a id="me" href="http://simonwillison.net/" rel="me">me</a>
<span class="s1">
<a href="#" id="s1a1">span1a1</a>
<a href="#" id="s1a2">span1a2 <span id="s1a2s1">test</span></a>
<span class="span2">
<a href="#" id="s2a1">span2a1</a>
</span>
<span class="span3"></span>
<custom-dashed-tag class="dashed" id="dash2"/>
<div data-tag="dashedvalue" id="data1"/>
</span>
</div>
<x id="xid">
<z id="zida"/>
<z id="zidab"/>
<z id="zidac"/>
</x>
<y id="yid">
<z id="zidb"/>
</y>
<p lang="en" id="lang-en">English</p>
<p lang="en-gb" id="lang-en-gb">English UK</p>
<p lang="en-us" id="lang-en-us">English US</p>
<p lang="fr" id="lang-fr">French</p>
</div>

<div id="footer">
</div>
"""

    def setUp(self):
        """Setup."""

        self.soup = BeautifulSoup(self.HTML, 'html.parser')

    def test_parent_nth_of_type_preconditions(self):
        """Test `nth` type preconditions."""

        els = sv.select('div > h1', self.soup, flags=sv.HTML)
        # check that there is a unique selection
        self.assertEqual(len(els), 1)
        self.assertEqual(els[0].string, 'An H1')

        # Show that the `h1`'s parent `div#inner` is the first child of type `div` of the grandparent `div#main`.
        # so that the selector `div:nth-of-type(1) > h1` should also give `h1`.
        h1 = els[0]
        div_inner = h1.parent
        div_main = div_inner.parent
        div_main_children = [child for child in div_main.children]
        self.assertEqual(div_main_children[0], '\n')
        self.assertEqual(div_main_children[1], div_inner)

    def test_parent_nth_of_type(self):
        """Test parent of `nth` of type."""

        els = sv.select('div:nth-of-type(1) > h1', self.soup, flags=sv.HTML)
        self.assertEqual(len(els), 1)
        self.assertEqual(els[0].string, 'An H1')

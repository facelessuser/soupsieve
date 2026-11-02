"""Test default selectors."""
from .. import util
import soupsieve as sv
from bs4 import BeautifulSoup

IFRAME_TEXT = BeautifulSoup('<iframe><div></div></iframe>', 'html.parser').iframe.text == '<div></div>'


class TestDefault(util.TestCase):
    """Test default selectors."""

    def test_default(self):
        """Test default."""

        markup = """
        <form>

        <input type="radio" name="season" id="spring">
        <label for="spring">Spring</label>

        <input type="radio" name="season" id="summer" checked>
        <label for="summer">Summer</label>

        <input type="radio" name="season" id="fall">
        <label for="fall">Fall</label>

        <input type="radio" name="season" id="winter">
        <label for="winter">Winter</label>

        <select id="pet-select">
            <option value="">--Please choose an option--</option>
            <option id="dog" value="dog">Dog</option>
            <option id="cat" value="cat">Cat</option>
            <option id="hamster" value="hamster" selected>Hamster</option>
            <option id="parrot" value="parrot">Parrot</option>
            <option id="spider" value="spider">Spider</option>
            <option id="goldfish" value="goldfish">Goldfish</option>
        </select>

        <input type="checkbox" name="enable" id="enable" checked>
        <label for="enable">Enable</label>

        <button type="button">
        not default
        </button>

        <button id="d1" type="submit">
        default1
        </button>

        <button id="d2" type="submit">
        default2
        </button>

        </form>

        <form>

        <div>
        <button id="d3" type="submit">
        default3
        </button>
        </div>

        <button id="d4" type="submit">
        default4
        </button>

        </form>

        <button id="d5" type="submit">
        default4
        </button>
        """

        self.assert_selector(
            markup,
            ":default",
            ['summer', 'd1', 'd3', 'hamster', 'enable'],
            flags=util.HTML
        )

    def test_default_submit_buttons(self):
        """
        Test submit buttons that are not `type="submit"`.

        A `button` with a missing or invalid `type` is a submit button unless it invokes a command or is a child of
        a `select`, and an `input` with `type="image"` is a submit button as well.
        """

        markup = """
        <form>
        <input type="button">
        <button type="RESET">reset</button>
        <button type="button">button</button>
        <button id="d1">default1</button>
        <button id="s1" type="submit">submit</button>
        </form>

        <form>
        <input id="d2" type="IMAGE" src="image.png">
        <button id="s2" type="submit">submit</button>
        </form>

        <form>
        <button commandfor="dialog">command1</button>
        <button command="show-modal">command2</button>
        <select><button>select</button><option>option</option></select>
        <button id="d3">default3</button>
        </form>

        <form>
        <button id="d4" type="submit" commandfor="dialog">default4</button>
        <button id="s4">button</button>
        </form>

        <form>
        <button id="d5" type="bogus">default5</button>
        </form>

        <form>
        <input type="text">
        <input type="checkbox">
        <button type="button">button</button>
        </form>
        """

        self.assert_selector(
            markup,
            ":default",
            ['d1', 'd2', 'd3', 'd4', 'd5'],
            flags=util.HTML
        )

    def test_iframe(self):
        """Test with `iframe`."""

        markup = """
        <html>
        <body>
        <form>
        <button id="d1" type="submit">default1</button>
        </form>

        <form>
        <iframe>
        <html>
        <body>
        <button id="d2" type="submit">default2</button>
        </body>
        </html>
        </iframe>
        <button id="d3" type="submit">default3</button>
        </form>

        <iframe>
        <html>
        <body>
        <form>
        <button id="d4" type="submit">default4</button>
        </form>
        </body>
        </html>
        </iframe>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            ":default",
            ['d1', 'd3'] if IFRAME_TEXT else ['d1', 'd3', 'd4'],
            flags=util.PYHTML
        )

    def test_nested_form(self):
        """
        Test nested form.

        This is technically invalid use of forms, but browsers will generally evaluate first in the nested forms.
        """

        markup = """
        <form>

        <form>
        <button id="d1" type="submit">
        button1
        </button>
        </form>

        <button id="d2" type="submit">
        button2
        </button>
        </form>
        """

        self.assert_selector(
            markup,
            ":default",
            ['d1'],
            flags=util.HTML
        )

    def test_default_cached(self):
        """
        Test that we use the cached "default".

        For the sake of coverage, we will do this impractical select
        to ensure we reuse the cached default.
        """

        markup = """
        <form>

        <form>
        <button id="d1" type="submit">
        button1
        </button>
        </form>

        <button id="d2" type="submit">
        button2
        </button>
        </form>
        """

        self.assert_selector(
            markup,
            ":default:default",
            ['d1'],
            flags=util.HTML
        )

    def test_nested_form_fail(self):
        """
        Test that the search for elements will bail after the first nested form.

        You shouldn't nest forms, but if you do, when a parent form encounters a nested form,
        we will bail evaluation like browsers do. We should see button 1 getting found for nested
        form, but button 2 will not be found for parent form.
        """

        markup = """
        <form>

        <form>
        <span>what</span>
        </form>

        <button id="d2" type="submit">
        button2
        </button>
        </form>
        """

        self.assert_selector(
            markup,
            ":default",
            [],
            flags=util.HTML
        )

    def test_default_cached_none(self):
        """Test that a form without a default button is cached and not searched again for every candidate."""

        markup = """
        <form>
        <select>
        <button id="b1">button1</button>
        <button id="b2">button2</button>
        <button id="b3">button3</button>
        </select>
        </form>

        <form>
        <select><button id="b4">button4</button></select>
        <button id="d1">default1</button>
        </form>
        """

        self.assert_selector(
            markup,
            ":default",
            ['d1'],
            flags=util.HTML
        )

    def test_default_radio_group(self):
        """Test that all radio buttons with `checked` are default, even those not left checked in their group."""

        markup = """
        <form>
        <input type="radio" name="a" id="1" checked>
        <input type="radio" name="a" id="2" checked>
        <input type="radio" name="a" id="3">
        </form>
        """

        self.assert_selector(
            markup,
            ":default",
            ['1', '2'],
            flags=util.HTML
        )

    def test_form_attribute_first_in_tree(self):
        """Test that the default button is the first in the tree, even if it is outside the form."""

        for control in ('<button form="f" id="1"></button>', '<input form="f" id="1" type="submit">',
                        '<input form="f" id="1" type="image">'):
            self.assert_selector(
                f"""
                <body>
                {control}
                <form id="f"><button id="2"></button></form>
                </body>
                """,
                ":default",
                ['1'],
                flags=util.HTML
            )

    def test_form_attribute_after_default(self):
        """Test that a submit button outside the form does not replace an earlier default button."""

        markup = """
        <body>
        <form id="f"><button id="1"></button></form>
        <button form="f" id="2"></button>
        </body>
        """

        self.assert_selector(
            markup,
            ":default",
            ['1'],
            flags=util.HTML
        )

    def test_form_attribute_only_submit_buttons(self):
        """Test that only submit buttons can be a default button with the `form` attribute."""

        markup = """
        <body>
        <button form="f" type="button" id="1"></button>
        <button form="f" type="reset" id="2"></button>
        <input form="f" type="text" id="3">
        <form id="f"><button id="4"></button></form>
        </body>
        """

        self.assert_selector(
            markup,
            ":default",
            ['4'],
            flags=util.HTML
        )

    def test_form_attribute_leaves_ancestor(self):
        """Test that a submit button that belongs to another form is not considered for its ancestor form."""

        markup = """
        <body>
        <form id="f">
        <button form="g" id="1"></button>
        <button id="2"></button>
        </form>
        <form id="g"><button id="3"></button></form>
        </body>
        """

        self.assert_selector(
            markup,
            ":default",
            ['1', '2'],
            flags=util.HTML
        )

    def test_form_attribute_no_form(self):
        """Test that a `form` attribute that doesn't refer to a form leaves a submit button without a form."""

        markup = """
        <body>
        <div id="d"></div>
        <form>
        <button form="{}" id="1"></button>
        <button id="2"></button>
        </form>
        <button form="{}" id="3"></button>
        </body>
        """

        for value in ('d', 'nope', ''):
            self.assert_selector(
                markup.format(value, value),
                ":default",
                ['2'],
                flags=util.HTML
            )

    def test_form_attribute_first_id(self):
        """Test that the `form` attribute only looks at the first element with an ID."""

        markup = """
        <body>
        <div id="f"></div>
        <form id="f"><button id="1"></button></form>
        <button form="f" id="2"></button>
        </body>
        """

        self.assert_selector(
            markup,
            ":default",
            ['1'],
            flags=util.HTML
        )

    def test_form_attribute_foreign_form(self):
        """Test that a `form` element that is not an HTML element is not a form."""

        markup = """
        <body>
        <svg><form id="f"></form></svg>
        <button form="f" id="1"></button>
        </body>
        """

        self.assert_selector(
            markup,
            ":default",
            [],
            flags=util.HTML5
        )

    def test_form_attribute_checked(self):
        """Test that the `form` attribute has no effect on elements that are default due to `checked`."""

        markup = """
        <body>
        <input form="nope" type="checkbox" id="1" checked>
        <input form="nope" type="radio" id="2" checked>
        </body>
        """

        self.assert_selector(
            markup,
            ":default",
            ['1', '2'],
            flags=util.HTML
        )

    def test_form_attribute_after_nested_form(self):
        """Test that the `form` attribute works after a nested form, which ends the search of the parent form."""

        markup = """
        <form id="f">
        <form><span>what</span></form>
        <button id="1"></button>
        <button form="f" id="2"></button>
        </form>
        """

        self.assert_selector(
            markup,
            ":default",
            ['2'],
            flags=util.PYHTML
        )

    def test_form_attribute_iframe(self):
        """Test that the `form` attribute does not see forms outside an `iframe`."""

        soup = self.soup('<form id="f"></form><iframe></iframe>', 'html.parser')
        soup.iframe.append(soup.new_tag('button', attrs={'form': 'f', 'id': '1'}))

        self.assertEqual(sv.select(':default', soup), [])

    def test_form_attribute_template(self):
        """Test that the `form` attribute is ignored in a `template`, whose contents are not connected."""

        markup = """
        <body>
        <template>
        <form id="f"></form>
        <button form="f" id="1"></button>
        <form><button form="nope" id="2"></button></form>
        </template>
        </body>
        """

        for parser in util.available_parsers('html.parser', 'lxml', 'html5lib'):
            soup = self.soup(markup, parser)
            self.assertEqual([el['id'] for el in sv.select(':default', soup.template)], ['2'])

    def test_nested_form_before(self):
        """Test that the contents of a nested form belong to the parent form, as a browser ignores nested forms."""

        markup = """
        <form>
        <button id="1"></button>
        <form><button id="2"></button></form>
        <button id="3"></button>
        </form>
        """

        # `lxml` turns this into sibling forms, which can't be told apart from real ones.
        for flags in (util.PYHTML, util.HTML5):
            self.assert_selector(
                markup,
                ":default",
                ['1'],
                flags=flags
            )

    def test_nested_form_many(self):
        """Test that the first end tag ends all nested forms, and that a form can follow it."""

        markup = """
        <form>
        <form><form><span>what</span></form><button id="1"></button></form>
        <form><button id="2"></button></form>
        <button id="3"></button>
        </form>
        """

        self.assert_selector(
            markup,
            ":default",
            ['2'],
            flags=util.PYHTML
        )

    def test_nested_form_attribute(self):
        """Test that the `form` attribute can't refer to a nested form, as it does not exist in a browser."""

        markup = """
        <form>
        <form id="f"><button id="1"></button></form>
        <button form="f" id="2"></button>
        </form>
        """

        self.assert_selector(
            markup,
            ":default",
            ['1'],
            flags=util.HTML
        )

    def test_nested_form_xhtml(self):
        """Test that nested forms are real forms in XHTML, as there is nothing to prevent them."""

        markup = self.wrap_xhtml("""
        <form>
        <form><input id="1" type="submit"/></form>
        <input id="2" type="submit"/>
        </form>
        """)

        self.assert_selector(
            markup,
            ":default",
            ['1', '2'],
            flags=util.XHTML
        )

    def test_nested_form_template(self):
        """Test that nested forms are real forms in a `template`, as the HTML specification allows them there."""

        markup = """
        <body>
        <template>
        <form>
        <form><button id="1"></button></form>
        <button id="2"></button>
        </form>
        </template>
        </body>
        """

        # `lxml` turns this into sibling forms, and `html5lib` drops the nested form.
        soup = self.soup(markup, 'html.parser')
        self.assertEqual(sorted(el['id'] for el in sv.select(':default', soup.template)), ['1', '2'])

    def test_default_option(self):
        """Test that options are default due to their `selected` attribute, not due to being selected."""

        markup = """
        <body>
        <select><option id="1" selected></option><option id="2" selected></option></select>
        <select><option id="3"></option><option id="4"></option></select>
        </body>
        """

        self.assert_selector(
            markup,
            ":default",
            ['1', '2'],
            flags=util.HTML
        )

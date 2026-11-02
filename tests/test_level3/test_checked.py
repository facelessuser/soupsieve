"""Test checked selectors."""
from .. import util
import soupsieve as sv


class TestChecked(util.TestCase):
    """Test checked selectors."""

    def test_checked(self):
        """Test checked."""

        markup = """
        <body>
        <div>
          <input type="radio" name="my-input" id="yes" checked>
          <label for="yes">Yes</label>

          <input type="radio" name="my-input" id="no">
          <label for="no">No</label>
        </div>

        <div>
          <input type="checkbox" name="my-checkbox" id="opt-in" checked>
          <label for="opt-in">Check me!</label>
        </div>

        <select name="my-select" id="fruit">
          <option id="1" value="opt1">Apples</option>
          <option id="2" value="opt2" selected>Grapes</option>
          <option id="3" value="opt3">Pears</option>
        </select>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['yes', 'opt-in', '2'],
            flags=util.HTML
        )

    def test_radio_group_last_checked(self):
        """Test that only the last radio button with `checked` in a group is checked."""

        markup = """
        <body>
        <div><input type="radio" name="a" id="1" checked></div>
        <p><span><input type="radio" name="a" id="2" checked></span></p>
        <input type="RADIO" name="a" id="3" checked disabled>
        <input type="radio" name="a" id="4">
        <input type="radio" name="b" id="5" checked>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['3', '5'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            markup,
            "input:not(:checked)",
            ['1', '2', '4'],
            flags=util.HTML
        )

    def test_radio_group_forms(self):
        """Test that radio buttons with the same name in different forms are in different groups."""

        markup = """
        <body>
        <input type="radio" name="a" id="1" checked>
        <form>
        <input type="radio" name="a" id="2" checked>
        <input type="radio" name="a" id="3" checked>
        </form>
        <form>
        <input type="radio" name="a" id="4" checked>
        </form>
        <input type="radio" name="a" id="5" checked>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['3', '4', '5'],
            flags=util.HTML
        )

    def test_radio_group_names(self):
        """Test that radio buttons only form a group if they have the same, non-empty name."""

        markup = """
        <body>
        <input type="radio" id="1" checked>
        <input type="radio" id="2" checked>
        <input type="radio" name="" id="3" checked>
        <input type="radio" name="" id="4" checked>
        <input type="radio" name="a" id="5" checked>
        <input type="radio" name="A" id="6" checked>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_radio_group_only_radios(self):
        """Test that other elements with the same name have no effect on a radio button."""

        markup = """
        <body>
        <input type="radio" name="a" id="1" checked>
        <input type="checkbox" name="a" id="2" checked>
        <input type="checkbox" name="a" id="3" checked>
        <input type="text" name="a" id="4" checked>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['1', '2', '3'],
            flags=util.HTML
        )

    def test_radio_group_form_attribute(self):
        """Test that the `form` attribute decides which form a radio button belongs to."""

        # Joins a form it is not in
        self.assert_selector(
            """
            <body>
            <form id="f"><input type="radio" name="a" id="1" checked></form>
            <input form="f" type="radio" name="a" id="2" checked>
            </body>
            """,
            ":checked",
            ['2'],
            flags=util.HTML
        )

        # The form can come later
        self.assert_selector(
            """
            <body>
            <input form="f" type="radio" name="a" id="1" checked>
            <form id="f"><input type="radio" name="a" id="2" checked></form>
            </body>
            """,
            ":checked",
            ['2'],
            flags=util.HTML
        )

        # Separates radio buttons that are not in a form, or that are in the same form
        self.assert_selector(
            """
            <body>
            <form id="f"></form>
            <form id="g"></form>
            <input form="f" type="radio" name="a" id="1" checked>
            <input form="g" type="radio" name="a" id="2" checked>
            <input type="radio" name="a" id="3" checked>
            <form id="h">
            <input type="radio" name="a" id="4" checked>
            <input form="f" type="radio" name="b" id="5" checked>
            <input type="radio" name="b" id="6" checked>
            </form>
            </body>
            """,
            ":checked",
            ['1', '2', '3', '4', '5', '6'],
            flags=util.HTML
        )

    def test_radio_group_form_attribute_no_form(self):
        """Test that a `form` attribute that doesn't refer to a form leaves a radio button without a form."""

        markup = """
        <body>
        <div id="d"></div>
        <form>
        <input type="radio" name="a" id="1" checked>
        <input form="{}" type="radio" name="a" id="2" checked>
        </form>
        <input type="radio" name="a" id="3" checked>
        </body>
        """

        for value in ('d', 'nope', ''):
            self.assert_selector(
                markup.format(value),
                ":checked",
                ['1', '3'],
                flags=util.HTML
            )

    def test_radio_group_form_attribute_first_id(self):
        """Test that the `form` attribute only looks at the first element with an ID."""

        markup = """
        <body>
        <div id="f"></div>
        <form id="f"><input type="radio" name="a" id="1" checked></form>
        <input form="f" type="radio" name="a" id="2" checked>
        <input type="radio" name="a" id="3" checked>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['1', '3'],
            flags=util.HTML
        )

    def test_radio_group_foreign_form(self):
        """Test that an element named `form` that is not an HTML element is not a form."""

        markup = """
        <body>
        <svg><form id="f"></form></svg>
        <input form="f" type="radio" name="a" id="1" checked>
        <input type="radio" name="a" id="2" checked>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['2'],
            flags=util.HTML5
        )

    def test_radio_group_foreign_object(self):
        """Test that radio buttons in an SVG `foreignObject` are in the same tree."""

        markup = """
        <body>
        <input type="radio" name="a" id="1" checked>
        <svg><foreignObject><input type="radio" name="a" id="2" checked></foreignObject></svg>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['2'],
            flags=util.HTML5
        )

    def test_radio_group_xhtml(self):
        """Test that elements outside the HTML namespace are not part of a group."""

        markup = """
        <?xml version="1.0" encoding="UTF-8"?>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <body>
        <input type="radio" name="a" id="1" checked="checked"/>
        <input type="radio" name="a" id="2" checked="checked"/>
        <input xmlns="urn:other" type="radio" name="a" id="3" checked="checked"/>
        </body>
        </html>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['2'],
            flags=util.XHTML
        )

    def test_radio_group_iframe(self):
        """Test that the contents of an `iframe` are not in the same tree as its parent document."""

        soup = self.soup('<input type="radio" name="a" id="1" checked><iframe></iframe>', 'html.parser')
        for value in ('2', '3'):
            soup.iframe.append(
                soup.new_tag('input', attrs={'type': 'radio', 'name': 'a', 'id': value, 'checked': ''})
            )

        self.assertEqual(
            sorted(el['id'] for el in sv.select(':checked', soup)),
            ['1', '3']
        )

    def test_radio_group_template(self):
        """Test that the contents of a `template` are all checked as they never become connected."""

        markup = """
        <body>
        <input type="radio" name="a" id="1" checked>
        <template>
        <input type="radio" name="a" id="2" checked>
        <input type="radio" name="a" id="3" checked>
        <template><input type="radio" name="a" id="5" checked></template>
        </template>
        <input type="radio" name="a" id="4" checked>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['4'],
            flags=util.HTML
        )

        for parser in util.available_parsers('html.parser', 'lxml', 'html5lib'):
            soup = self.soup(markup, parser)
            self.assertEqual(
                sorted(el['id'] for el in sv.select(':checked', soup.template)),
                ['2', '3']
            )

    def test_radio_group_nested_form(self):
        """Test that the contents of a nested form belong to the parent form, as a browser ignores nested forms."""

        markup = """
        <body>
        <form>
        <input type="radio" name="a" id="1" checked>
        <form><input type="radio" name="a" id="2" checked></form>
        </form>
        </body>
        """

        # `lxml` turns this into sibling forms, which can't be told apart from real ones.
        for flags in (util.PYHTML, util.HTML5):
            self.assert_selector(
                markup,
                ":checked",
                ['2'],
                flags=flags
            )

    def test_radio_group_after_nested_form(self):
        """Test that what follows a nested form is not in the parent form, as the nested form's end tag ended it."""

        markup = """
        <body>
        <form>
        <form><span>what</span></form>
        <input type="radio" name="a" id="1" checked>
        </form>
        <input type="radio" name="a" id="2" checked>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['2'],
            flags=util.HTML
        )

    def test_radio_group_nested_form_xhtml(self):
        """Test that nested forms are real forms in XHTML, as there is nothing to prevent them."""

        markup = self.wrap_xhtml("""
        <form>
        <input type="radio" name="a" id="1" checked="checked"/>
        <form><input type="radio" name="a" id="2" checked="checked"/></form>
        </form>
        """)

        self.assert_selector(
            markup,
            ":checked",
            ['1', '2'],
            flags=util.XHTML
        )

    def test_option_last_selected(self):
        """Test that only the last option with `selected` in a `select` is selected."""

        markup = """
        <body>
        <select>
        <option id="1" selected></option>
        <option id="2" selected></option>
        <option id="3"></option>
        </select>
        <select>
        <optgroup><option id="4" selected></option></optgroup>
        <optgroup><option id="5" selected></option></optgroup>
        </select>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['2', '5'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            markup,
            "option:not(:checked)",
            ['1', '3', '4'],
            flags=util.HTML
        )

    def test_option_disabled_selected(self):
        """Test that a `disabled` option can be selected, and takes part in being the last one."""

        markup = """
        <body>
        <select>
        <option id="1" selected disabled></option>
        <option id="2" selected></option>
        <option id="3" selected disabled></option>
        </select>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['3'],
            flags=util.HTML
        )

    def test_option_multiple(self):
        """Test that all options with `selected` are selected with `multiple`, which selects none by default."""

        markup = """
        <body>
        <select multiple>
        <option id="1" selected></option>
        <option id="2" selected></option>
        <option id="3"></option>
        </select>
        <select multiple size="1">
        <option id="4"></option>
        </select>
        <select MULTIPLE>
        <option id="5" SELECTED></option>
        <option id="6" SELECTED></option>
        </select>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['1', '2', '5', '6'],
            flags=util.HTML
        )

    def test_option_first_enabled(self):
        """Test that the first enabled option is selected if none have `selected`."""

        markup = """
        <body>
        <select><option id="1"></option><option id="2"></option></select>
        <select><option id="3" disabled></option><option id="4"></option></select>
        <select><optgroup disabled><option id="5"></option></optgroup><option id="6"></option></select>
        <select><optgroup><option id="7"></option></optgroup><option id="8"></option></select>
        <select disabled><option id="9"></option></select>
        <select><option id="10" hidden></option></select>
        <select><option id="11" disabled></option></select>
        <select></select>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['1', '4', '6', '7', '9', '10'],
            flags=util.HTML
        )

    def test_option_size(self):
        """Test that the first enabled option is only selected if the `select` shows a single option."""

        markup = """
        <body>
        <select size="{}"><option id="1"></option><option id="2"></option></select>
        </body>
        """

        for size in ('1', '0', '00', '01', '-1', '-0', '', 'abc', '1e1', '1x', '\u0662'):
            self.assert_selector(
                markup.format(size),
                ":checked",
                ['1'],
                flags=util.HTML
            )

        for size in ('2', '+2', ' 2', '2x', '2.5'):
            self.assert_selector(
                markup.format(size),
                ":checked",
                [],
                flags=util.HTML
            )

    def test_option_size_many_selected(self):
        """Test that only the last option with `selected` is selected, even if many options are shown."""

        markup = """
        <body>
        <select size="2"><option id="1" selected></option><option id="2" selected></option></select>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['2'],
            flags=util.HTML
        )

    def test_option_no_select(self):
        """Test that an option outside of the list of options of a `select` only uses its `selected` attribute."""

        markup = """
        <body>
        <option id="1" selected></option>
        <option id="2" selected></option>
        <option id="3"></option>
        <datalist>
        <option id="4" selected></option>
        <option id="5" selected></option>
        <option id="6"></option>
        </datalist>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['1', '2', '4', '5'],
            flags=util.HTML
        )

    def test_option_list(self):
        """Test what is and isn't part of the list of options of a `select`."""

        markup = """
        <body>
        <select>
        <div><option id="1" selected></option></div>
        <div><optgroup><option id="2" selected></option></optgroup></div>
        </select>
        <select>
        <datalist><option id="3" selected></option></datalist>
        <option id="4" selected></option>
        </select>
        <select>
        <datalist><option id="5"></option></datalist>
        <option id="6"></option>
        </select>
        </body>
        """

        # `html5lib` removes elements from `select` that the HTML specification now allows.
        self.assert_selector(
            markup,
            ":checked",
            ['2', '3', '4', '6'],
            flags=util.PYHTML
        )

    def test_option_unclosed(self):
        """Test that options that are not closed are handled, even by parsers that end up nesting them."""

        markup = """
        <body>
        <select><option id="1" selected>a<option id="2" selected>b<option id="3">c</select>
        <select><optgroup disabled><option id="4">a<optgroup><option id="5">b</select>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['2', '5'],
            flags=util.HTML
        )

    def test_option_nested_select(self):
        """Test that a `select` in a `select` ends it, as a browser would."""

        markup = """
        <body>
        <select>
        <option id="1" selected></option>
        <div><select><option id="2" selected></option></select></div>
        <option id="3" selected></option>
        </select>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['1', '2', '3'],
            flags=util.HTML
        )

    def test_option_foreign_select(self):
        """Test that an element named `select` that is not an HTML element is not a `select`."""

        markup = """
        <body>
        <svg><select><foreignObject><option id="1" selected></option><option id="2" selected></option>
        </foreignObject></select></svg>
        </body>
        """

        self.assert_selector(
            markup,
            ":checked",
            ['1', '2'],
            flags=util.HTML5
        )

    def test_option_iframe(self):
        """Test that an option in an `iframe` does not belong to a `select` outside of it."""

        soup = self.soup('<select><option id="1"></option><iframe></iframe></select>', 'html.parser')
        soup.iframe.append(soup.new_tag('option', attrs={'id': '2', 'selected': ''}))

        self.assertEqual([el['id'] for el in sv.select(':checked', soup)], ['1', '2'])

    def test_option_template(self):
        """Test that a `select` in a `template` selects options, as this does not require being connected."""

        markup = """
        <body>
        <template>
        <select><option id="1" selected></option><option id="2" selected></option></select>
        <select><option id="3"></option><option id="4"></option></select>
        </template>
        </body>
        """

        for parser in util.available_parsers('html.parser', 'lxml', 'html5lib'):
            soup = self.soup(markup, parser)
            self.assertEqual(sorted(el['id'] for el in sv.select(':checked', soup.template)), ['2', '3'])

    def test_option_xhtml(self):
        """Test options in XHTML, where elements are only nested if the document says so."""

        markup = self.wrap_xhtml("""
        <select>
        <option id="1" selected="selected"/>
        <option id="2" selected="selected"><option id="3" selected="selected"/></option>
        <optgroup><optgroup><option id="4" selected="selected"/></optgroup></optgroup>
        <hr/>
        <select><option id="5"/></select>
        </select>
        """)

        self.assert_selector(
            markup,
            ":checked",
            ['2', '3', '4', '5'],
            flags=util.XHTML
        )

"""Test default selectors."""
from .. import util
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

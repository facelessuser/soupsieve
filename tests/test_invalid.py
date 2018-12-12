"""Test invalid cases."""
import unittest
import soupsieve as sv


class TestInvalid(unittest.TestCase):
    """Test invalid."""

    def test_invalid_mode(self):
        """Test invalid mode."""

        with self.assertRaises(ValueError):
            sv.compile('p', None, 0)

    def test_invalid_combination(self):
        """
        Test invalid combination.

        Selectors cannot start with relational symbols unless in `:has()`.
        `:has()` cannot start with `,`.
        """

        with self.assertRaises(SyntaxError):
            sv.compile('> p')

        with self.assertRaises(SyntaxError):
            sv.compile(', p')

        with self.assertRaises(SyntaxError):
            sv.compile(':has(, p)')

        with self.assertRaises(SyntaxError):
            sv.compile('div >> p')

        with self.assertRaises(SyntaxError):
            sv.compile('div >')

    def test_invalid_pseudo_close(self):
        """Test invalid pseudo close."""

        with self.assertRaises(SyntaxError):
            sv.compile('div)')

        with self.assertRaises(SyntaxError):
            sv.compile(':is(div,)')

    def test_invalid_pseudo_open(self):
        """Test invalid pseudo close."""

        with self.assertRaises(SyntaxError):
            sv.compile(':is(div')

    def test_invalid_incomplete_has(self):
        """Test invalid `:has()`."""

        with self.assertRaises(SyntaxError):
            sv.compile(':has(>)')

        with self.assertRaises(SyntaxError):
            sv.compile(':has()')

    def test_invalid_tag(self):
        """
        Test invalid tag.

        Tag must come first.
        """

        with self.assertRaises(SyntaxError):
            sv.compile(':is(div)p')

    def test_invalid_syntax(self):
        """Test invalid syntax."""

        with self.assertRaises(SyntaxError):
            sv.compile('div?')

    def test_invalid_namespace(self):
        """Test invalid namespace."""

        with self.assertRaises(TypeError):
            sv.ct.Namespaces(((3, 3),))

        with self.assertRaises(TypeError):
            sv.ct.Namespaces({'a': {}})

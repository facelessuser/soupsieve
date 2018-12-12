"""
Test extra selectors.

Extra patterns that are not in the specification, but may be useful.

```
:contains(text)
```
"""
from . import util
import soupsieve as sv


class TestLevel1(util.TestCase):
    """Test level 1 selectors."""

    def test_contains(self):
        """Test tag."""

        markup = """
        <div id="1">
        Testing
        <span id="2"> that </span>
        contains works.
        </div>
        """

        self.assert_selector(
            markup,
            'body span:contains(that)',
            ['2'],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            'body span:contains(" that ")',
            ['2'],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            'body :contains(" that ")',
            ['1', '2'],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            'body :contains( "Testing" )',
            ['1'],
            flags=sv.HTML5
        )

        self.assert_selector(
            markup,
            'body :contains(bad)',
            [],
            flags=sv.HTML5
        )

"""Test at-rule cases."""
from __future__ import unicode_literals
from .. import util


class TestAtRule(util.TestCase):
    """Test at-rules."""

    def test_at_rule(self):
        """Test at-rule (not supported)."""

        self.assert_raises('@page :left', NotImplementedError)

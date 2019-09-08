"""
Test language tag/range canonicalization.

```
# grandfathered registrations
'zh-hakka' => "hak"

# canonical and extlang forms
'sgn-jsl' => "jsl" => "sgn-jsl"

# variants
'ja-Latn-hepburn-heploc' => "ja-Latn-hepburn-alalc97"

# etc.
```

"""
from __future__ import unicode_literals
import unittest


class TestLangCanonicalization(unittest.TestCase):
    """Test language canonicalization."""

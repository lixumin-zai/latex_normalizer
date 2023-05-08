import unittest

from ..mapping.token_mapping import normalize_sentence_char


class TestMapping(unittest.TestCase):
    def test_char_mapping__pi(self):
        self.assertEqual(
            normalize_sentence_char(r"3π + 5π = \frac{2}{π} / π"),
            r"3\pi + 5\pi = \frac{2}{\pi} / \pi"
        )




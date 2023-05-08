import unittest

from ..normalize import normalize_latex_expression, normalize_latex_in_sentence


class TestSameResult(unittest.TestCase):
    def test_latex__brace(self):
        self.assertEqual(
            normalize_latex_expression(r"x^{2}+\left(y-1\right)^{2}=4",
                                       keep_left_right_marker=False,
                                       normalize_token=True),
            normalize_latex_expression(r"x^2+(y-1)^{2}=4",
                                       keep_left_right_marker=False,
                                       normalize_token=True)
        )

    def test_latex__eq(self):
        self.assertEqual(
            normalize_latex_expression(r"f(x)\geq 0",
                                       keep_left_right_marker=False,
                                       normalize_token=True),
            normalize_latex_expression(r"f(\left x\right)\ge 0",
                                       keep_left_right_marker=False,
                                       normalize_token=True)
        )

        self.assertEqual(
            normalize_latex_expression(r"f(\left x\right)\gt 0",
                                       keep_left_right_marker=False,
                                       normalize_token=True),
            normalize_latex_expression(r"f(\left x\right)> 0",
                                       keep_left_right_marker=False,
                                       normalize_token=True)
        )

        self.assertEqual(
            normalize_latex_expression(r"x^{2}+\left(y-1\right)^{2}=4",
                                       keep_left_right_marker=False,
                                       normalize_token=True),
            normalize_latex_expression(r"x^2+(y-1)^{2}=4",
                                       keep_left_right_marker=False,
                                       normalize_token=True)
        )

    def test_latex__sup_sub_index(self):
        self.assertEqual(
            normalize_latex_expression(r"A^{n}_{m}",
                                       keep_left_right_marker=False,
                                       normalize_token=True),
            normalize_latex_expression(r"A_{m}^{n}",
                                       keep_left_right_marker=False,
                                       normalize_token=True)
        )

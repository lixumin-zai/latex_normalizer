import unittest

from xizi_latex_normalizer.utils.common_utils import (
    trans_chinese_unit_to_latex, split_to_latex_and_not
)


class TestCommon(unittest.TestCase):
    def test__split(self):
        self.assertEqual(
            split_to_latex_and_not(r"测试$abc$测试$def$"),
            ["测试", "abc", "测试", "def", ""]
        )

        self.assertEqual(
            split_to_latex_and_not(r"测试$abc$$def$"),
            ["测试", "abc", "", "def", ""]
        )

        self.assertEqual(
            split_to_latex_and_not(r"测试$a\$bc$测试$de\$f$"),
            ["测试", r"a\$bc", "测试", r"de\$f", ""]
        )

        self.assertEqual(
            split_to_latex_and_not(r"测\$试$a\$bc$测\$试$de\$f$"),
            [r"测\$试", r"a\$bc", r"测\$试", r"de\$f", ""]
        )

    def test__trans(self):
        self.assertEqual(
            trans_chinese_unit_to_latex("其中$64$米的长度"),
            "其中$64 \\rm m$的长度"
        )

        self.assertEqual(
            trans_chinese_unit_to_latex("其中$64$中米的长度"),
            "其中$64$中米的长度",
        )

        self.assertEqual(
            trans_chinese_unit_to_latex("其中\$\$米$64$米的长度"),
            r"其中\$\$米$64 \rm m$的长度"
        )

        self.assertEqual(
            trans_chinese_unit_to_latex("水温为$5$度"),
            r"水温为$5 ^{\circ}$"
        )

        self.assertEqual(
            trans_chinese_unit_to_latex("水温为$5$摄氏度"),
            r"水温为$5 ^{\circ}C$"
        )

        self.assertEqual(
            trans_chinese_unit_to_latex("房间面积为$5$平方米"),
            r"房间面积为$5 \rm m^2$"
        )

import unittest

from ..stream import LatexTokenStream


class TestTokenStream(unittest.TestCase):
    def test_token1(self):
        latex = r"\frac{1}2"
        stream = LatexTokenStream(latex)

        self.assertEqual(
            stream.get_all_tokens(),
            ['\\frac', '{', '1', '}', '2']
        )

    def test_token2(self):
        latex = r" \frac {1} 2"
        stream = LatexTokenStream(latex)

        self.assertEqual(
            stream.get_all_tokens(),
            ['\\frac', '{', '1', '}', '2']
        )

    def test_token3(self):
        latex = r"\frac {\frac{1 }{ 2 }} {2}"
        stream = LatexTokenStream(latex)

        self.assertEqual(
            stream.get_all_tokens(),
            ['\\frac', '{', '\\frac', '{', '1', '}', '{', '2', '}', '}', '{', '2', '}']
        )
        
    def test_token4(self):
        latex = r"1 \frac{1}{2}+5="
        stream = LatexTokenStream(latex)

        self.assertEqual(
            stream.get_all_tokens(),
            ['1', '\\frac', '{', '1', '}', '{', '2', '}', '+', '5', '=']
        )

    def test_token5(self):
        latex = r"\vec a-\vec b"
        stream = LatexTokenStream(latex)

        self.assertEqual(
            stream.get_all_tokens(),
            ['\\vec', 'a', '-', '\\vec', 'b']
        )

    def test_token6(self):
        latex = r"S _ O A B"
        stream = LatexTokenStream(latex)

        self.assertEqual(
            stream.get_all_tokens(),
            ['S', '_', 'OAB'],
        )

    def test_token7(self):
        latex = r"S _ O A B + S_ AC D"
        stream = LatexTokenStream(latex)

        self.assertEqual(
            stream.get_all_tokens(),
            ['S', '_', 'OAB', '+', 'S', '_', 'ACD'],
        )

    def test_token8(self):
        latex = r"S _ O A B + S_ AC D+ "
        stream = LatexTokenStream(latex)

        self.assertEqual(
            stream.get_all_tokens(),
            ['S', '_', 'OAB', '+', 'S', '_', 'ACD', '+'],
        )

    def test_token9(self):
        latex = r"3.2 + 2.5"
        stream = LatexTokenStream(latex)

        self.assertEqual(
            stream.get_all_tokens(),
            ['3.2', '+', '2.5'],
        )

    def test_token__expression(self):
        self.assertEqual(
            LatexTokenStream(r"3\alpha+4\beta", 
                             normalize_token=True).get_all_tokens(),
            ["3", "\\alpha", "+", "4", "\\beta"]
        )

    def test_token__lower_captical(self):
        ignore = True
        self.assertEqual(
            LatexTokenStream(r"C+Cad+\Cabc", 
                             ignore_similar_despite_capital=ignore).get_all_tokens(),
            ["c", "+", "Cad", "+", r"\Cabc"]
        )
        self.assertEqual(
            LatexTokenStream(r"X+Cad+\Cabc", 
                             ignore_similar_despite_capital=ignore).get_all_tokens(),
            ["x", "+", "Cad", "+", r"\Cabc"]
        )
        self.assertEqual(
            LatexTokenStream(r"Xxx+Cad+\Cabc", 
                            ignore_similar_despite_capital=ignore).get_all_tokens(),
            ["Xxx", "+", "Cad", "+", r"\Cabc"]
        )

    def test_token__left_right_marker(self):
        self.assertEqual(
            LatexTokenStream(r"\left(1, 2\right)", 
                             keep_left_right_marker=False).get_all_tokens(),
            ["(", "1", ",", "2", ")"]
        )

        self.assertEqual(
            LatexTokenStream(r"\left(\frac{\pi  }{4}+2k\pi ,\frac{\pi }{2}+2k\pi \right)", 
                             keep_left_right_marker=False).get_all_tokens(),
            ["(", "\\frac", "{", "\\pi", "}", "{", "4", "}", "+", "2k", "\\pi", ",", "\\frac", "{", "\pi", "}", "{", "2", "}", "+", "2k", "\\pi", ")"]
        )

        self.assertEqual(
            LatexTokenStream(r"\left(\frac{\pi  }{4}+2k\pi ,\frac{\pi }{2}+2k\pi \right)", 
                             keep_left_right_marker=True).get_all_tokens(),
            ["\\left", "(", "\\frac", "{", "\\pi", "}", "{", "4", "}", "+", "2k", "\\pi", ",", "\\frac", "{", "\pi", "}", "{", "2", "}", "+", "2k", "\\pi", "\\right", ")"]
        )

    def test_token__angle_marker(self):
        self.assertEqual(
            LatexTokenStream(r"\sin \angle A", 
                             strip_angle=True).get_all_tokens(),
            ["\\sin", "A"]
        )

        self.assertEqual(
            LatexTokenStream(r"(\angle A + \angle B)", 
                             strip_angle=True).get_all_tokens(),
            ["(", "A", "+", "B", ")"]
        )

    def test_token__log(self):
        self.assertEqual(
            LatexTokenStream(r"{\log_{\cot}}", 
                             strip_angle=True).get_all_tokens(),
            ["{", "\\log", "_", "{", "\\cot", "}", "}"]
        )

    def test_token__equation_group(self):
        self.assertEqual(
            LatexTokenStream(
                r"\left\{\begin{matrix}x^{2}+4y^{2}=36\\x+2y-8=0\end{matrix}"
                r"\right.").get_all_tokens(),
            ["\\left", "\\{", "\\begin", "{", "matrix", "}", "x", "^", "{", "2", 
             "}", "+", "4y", "^", "{", "2", "}", "=", "36", "\\\\", "x", "+", "2y", 
             "-", "8", "=", "0", "\\end", "{", "matrix", "}", "\\right", "."]
        )

    def test_token__equation_group(self):
        self.assertEqual(
            LatexTokenStream(
                r"\left\{\begin{matrix}x^{2}+4y^{2}=36\\x+2y-8=0\end{matrix}"
                r"\right.").get_all_tokens(),
            ["\\left", "\\{", "\\begin", "{", "matrix", "}", "x", "^", "{", "2", 
             "}", "+", "4y", "^", "{", "2", "}", "=", "36", "\\\\", "x", "+", "2y", 
             "-", "8", "=", "0", "\\end", "{", "matrix", "}", "\\right", "."]
        )

    def test_token_complete_token(self):
        self.assertEqual(
            LatexTokenStream(r"sinxcosx").get_all_tokens(),
            ["\sin", "x", "\cos", "x"]
        )

        self.assertEqual(
            LatexTokenStream(r"sin(xcosx)").get_all_tokens(),
            ["\sin", "(", "x", "\cos", "x", ")"]
        )

        self.assertEqual(
            LatexTokenStream(r"s in (x cosx)").get_all_tokens(),
            ["\sin", "(", "x", "\cos", "x", ")"]
        )

        self.assertEqual(
            LatexTokenStream(r"lg10").get_all_tokens(),
            ["\lg", "10"]
        )

        self.assertEqual(
            LatexTokenStream(r"ln10").get_all_tokens(),
            ["\ln", "10"]
        )

        self.assertEqual(
            LatexTokenStream(r"lg10\ln50").get_all_tokens(),
            ["\lg", "10", "\\ln", "50"]
        )

        self.assertEqual(
            LatexTokenStream(r"log10").get_all_tokens(),
            ["\log", "10"]
        )

        self.assertEqual(
            LatexTokenStream(r"sinxlgyln10").get_all_tokens(),
            ["\\sin", "x", "\\lg", "y", "\\ln", "10"]
        )

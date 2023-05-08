
import unittest

from ..components.list_component import (
    BeginEndComponent, BraceComponent, SquareBraceComponent, AbsComponent
)

from ..stream import LatexTokenStream


class TestBeginEnd(unittest.TestCase):
    def test_begin_end1(self):
        latex = r"\begin{array}{l}{\frac{x^{2}}{a^{2}}+\frac{y^{2}}{a^{2}-9}=1} \\ {y=k(x-3)}\end{array}"
        stream = LatexTokenStream(latex)
        
        #print(stream.get_all_tokens())

        comp = BeginEndComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\begin{array}{l} {\frac{x^{2}}{a^{2}} + \frac{y^{2}}{a^{2} - 9} = 1} \\ {y = k (x - 3)} \end{array}"
        )

    def test_begin_end2(self):
        latex = "\\begin{cases}{y=k(x-2)}\\\\{\\frac{x^2}{6}+\\frac{y^2}{2}=1}\\end{cases}"
        stream = LatexTokenStream(latex)
        
        comp = BeginEndComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\begin{cases} {y = k (x - 2)} \\ {\frac{x^{2}}{6} + \frac{y^{2}}{2} = 1} \end{cases}"
        )

    def test_begin_end__unstandard_format(self):
        latex = r"\begin{cases} {x=4}\\y=1\\ \end{cases}"
        stream = LatexTokenStream(latex)
        
        comp = BeginEndComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\begin{cases} {x = 4} \\ {y = 1} \end{cases}"
        )


class TestBrace(unittest.TestCase):
    def test_brace1(self):
        latex = r"{a^2}"
        stream = LatexTokenStream(latex)
        
        #print(stream.get_all_tokens())

        comp = BraceComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"a^{2}"
        )

    def test_brace2(self):
        latex = r"{y^2_{2}}"

        stream = LatexTokenStream(latex)
        
        comp = BraceComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"y_{2}^{2}"
        )

    def test_brace3(self):
        latex = r"{3 + y^2_{2}}"

        stream = LatexTokenStream(latex)
        
        comp = BraceComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"3 + y_{2}^{2}"
        )

    def test_brace4(self):
        latex = r"{3 + y^2_{2} + \frac14}"

        stream = LatexTokenStream(latex)
        
        comp = BraceComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"3 + y_{2}^{2} + \frac{1}{4}"
        )

    def test_brace5(self):
        latex = r"{3 + y^2_{y+2} + \frac14}"

        stream = LatexTokenStream(latex)
        
        comp = BraceComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"3 + y_{y + 2}^{2} + \frac{1}{4}"
        )

    def test_brace6(self):
        latex = r"{3 + y^{x+2}_2 + \frac14}"

        stream = LatexTokenStream(latex)
        
        comp = BraceComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"3 + y_{2}^{x + 2} + \frac{1}{4}"
        )

    def test_brace7(self):
        latex = r"{3 + y^{x+2}_{y+2} + \frac14}"

        stream = LatexTokenStream(latex)
        
        comp = BraceComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"3 + y_{y + 2}^{x + 2} + \frac{1}{4}"
        )

    def test_brace__brace_match(self):
        latex = r"[4, +\infty)"

        stream = LatexTokenStream(latex)
        
        comp = SquareBraceComponent.match(stream)

        self.assertEqual(
            comp.to_string(with_head=True),
            r"[4 , + \infty)"
        )


class TestAbs(unittest.TestCase):
    def test_abs__normal(self):
        self.assertEqual(
            AbsComponent.match(LatexTokenStream(r"\vert a \vert")).to_string(), 
            r"|a|"
        )

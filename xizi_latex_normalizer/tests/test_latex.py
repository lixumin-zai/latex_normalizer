import unittest

from ..normalize import normalize_latex_expression, normalize_latex_in_sentence
from ..exceptions.base_exception import NormalizerException

from ..stream import LatexTokenStream


class TestLatex(unittest.TestCase):
    def test_latex1(self):
        latex = r"x+\frac12+\vec a-\sqrt[2]5+\frac{\frac12}{\frac1{3}}"
        result = normalize_latex_expression(latex)

        self.assertEqual(
            result,
            r"x + \frac{1}{2} + \vec{a} - \sqrt[2]{5} + \frac{\frac{1}{2}}{\frac{1}{3}}"
        )

    def test_latex2(self):
        latex = r"\left\{\begin{array}{l}{\frac{x^{2}}{a^{2}}+\frac{y^{2}}{a^{2}-9}=1} \\ {y=k(x-3)}\end{array} \Rightarrow \frac{x^{2}}{a^{2}}+\frac{k^{2}(x-3)^{2}}{a^{2}-a}=1\right."
        result = normalize_latex_expression(latex)

        self.assertEqual(
            result,
            r"\left \{ \begin{array}{l} {\frac{x^{2}}{a^{2}} + \frac{y^{2}}{a^{2} - 9} = 1} \\ {y = k (x - 3)} \end{array} \Rightarrow \frac{x^{2}}{a^{2}} + \frac{k^{2} (x - 3)^{2}}{a^{2} - a} = 1 \right ."
        )

    def test_latex3(self):
        latex = r"3 + y^{x+2}_{y+2} + \frac14"
        result = normalize_latex_expression(latex)

        self.assertEqual(
            result,
            r"3 + y_{y + 2}^{x + 2} + \frac{1}{4}"
        )

    def test_latex__brace(self):
        latex = r"[3, 4]"
        result = normalize_latex_expression(latex)

        self.assertEqual(
            result,
            r"[3 , 4]"
        )
        
    def test_latex___with_token_nomalize(self):
        latex = r"x\geqslant y"
        result = normalize_latex_expression(latex, normalize_token=True)

        self.assertEqual(
            result,
            r"x \ge y"
        )

    def test_latex___with_token_nomalize_and_case_ignore(self):
        latex = r"X\geqslant Y"
        result = normalize_latex_expression(
            latex, 
            normalize_token=True,
            ignore_similar_despite_capital=True
        )

        self.assertEqual(
            result,
            r"x \ge y"
        )

    def test_latex__normalize_latex_in_sentence(self):

        self.assertEqual(
            normalize_latex_in_sentence(
                r"这是一次测试$x\geqslant y$, 或者也是$\frac3{4}$", 
                normalize_token=True
            ),
            r"这是一次测试$x \ge y$, 或者也是$\frac{3}{4}$"
        )

        self.assertEqual(
            normalize_latex_in_sentence(
                r"$>$", 
                normalize_token=True
            ),
            r"$\gt$"
        )
        
    def test_latex__normalize_latex_in_sentence_and_ignore(self):
        self.assertEqual(
            normalize_latex_in_sentence(
                r"X$X > C$Y", 
                normalize_token=True,
                ignore_similar_despite_capital=True
            ),
            r"X$x \gt c$Y"
        )

        self.assertEqual(
            normalize_latex_in_sentence(
                r"Z$x > C$Z", 
                normalize_token=True,
                ignore_similar_despite_capital=True
            ),
            r"Z$x \gt c$Z"
        )

    def test_latex__strip_angle_in_tri(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\sin{x}+\cos\angle y", 
                strip_angle_for_tri=True
            ),
            r"\sin(x) + \cos(y)"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\sin(\angle A + \angle B)", 
                strip_angle_for_tri=True
            ),
            r"\sin(A + B)"
        )

    def test_latex__global_char_mapping(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\sin 5π+\frac{\cos 2π}{5}", 
                normalize_token=True
            ),
            r"\sin(5\pi) + \frac{\cos(2\pi)}{5}"
        )

    def test_latex__with_rm(self):
        self.assertEqual(
            normalize_latex_expression(
                r"38\rm{kg}", keep_rm_sign=False
            ),
            r"38 kg"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\sin 4x\rm{kg}", keep_rm_sign=False
            ),
            r"\sin(4x) kg"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\sin 5\pi\rm{kg}", keep_rm_sign=False
            ),
            r"\sin(5\pi) kg"
        )

    def test_latex__with_or_without_sup_for_degree(self):
        self.assertEqual(
            normalize_latex_expression(
                r"60\degree",
                normalize_token=True,
            ),
            r"60^{\circ}"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"60^\degree",
                normalize_token=True,
            ),
            r"60^{\circ}"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"60^{\degree}",
                normalize_token=True,
            ),
            r"60^{\circ}"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"60^{\circ}",
                normalize_token=True,
            ),
            r"60^{\circ}"
        )

    def test_latex__equation_group(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\left\{\begin{matrix}x^{2}+4y^{2}=36\\x+2y-8=0\end{matrix}\right.",
            ),
            r"\left \{ \begin{matrix} {x^{2} + 4y^{2} = 36} \\ {x + 2y - 8 = 0} \end{matrix} \right ."
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\left\{\begin{matrix}\frac{x^{2}}{5}+y^{2}=1\\x=my+2\end{matrix}\right.",
            ),
            r"\left \{ \begin{matrix} {\frac{x^{2}}{5} + y^{2} = 1} \\ {x = my + 2} \end{matrix} \right ."
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\left\{\begin{matrix}y=x-c\\\frac{x^{2}}{a^2}+\frac{y^{2}}{b^2}=1\end{matrix}\right.",
            ),
            r"\left \{ \begin{matrix} {y = x - c} \\ {\frac{x^{2}}{a^{2}} + \frac{y^{2}}{b^{2}} = 1} \end{matrix} \right ."
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\left\{\begin{matrix}m=1\\n=\frac{1}{25}\end{matrix}\right.",
            ),
            r"\left \{ \begin{matrix} {m = 1} \\ {n = \frac{1}{25}} \end{matrix} \right ."
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\left\{\begin{matrix}\frac{9}{25}m+16n=1\\\frac{16}{25}m+9n=1\end{matrix}\right.",
            ),
            r"\left \{ \begin{matrix} {\frac{9}{25} m + 16n = 1} \\ {\frac{16}{25} m + 9n = 1} \end{matrix} \right ."
        )

    def test_latex__invalid_syntax_exception(self):
        with self.assertRaises(NormalizerException):
            normalize_latex_expression(
                r"(",
                ensure_valid_formula=True,
            )

        with self.assertRaises(NormalizerException):
            normalize_latex_expression(
                r"[",
                ensure_valid_formula=True,
            )

        with self.assertRaises(NormalizerException):
            normalize_latex_expression(
                r"\frac{1}",
                ensure_valid_formula=True,
            )

        self.assertEqual(
            normalize_latex_expression(
                r"\frac{1}",
                ensure_valid_formula=False,
            ),
            r"\frac { 1 }"
        )

        self.assertEqual(
            normalize_latex_expression(
                r" ( ",
                ensure_valid_formula=False,
            ),
            r"("
        )

        self.assertEqual(
            normalize_latex_expression(
                r") ( ",
                ensure_valid_formula=False,
            ),
            r") ("
        )

    def test_latex__strip_outmost_brace(self):
        self.assertEqual(
            normalize_latex_expression(
                r"{{abc}}",
                ensure_valid_formula=False,
            ),
            r"abc"
        )

    def test_sent__invalid_syntax_exception(self):
        with self.assertRaises(NormalizerException):
            normalize_latex_in_sentence(
                r"这是一次测试$x\geqslant y$, 或者也是$\frac3$", 
                normalize_token=True,
                ensure_valid_formula=True,
            )

        with self.assertRaises(NormalizerException):
            normalize_latex_in_sentence(
                r"这是一次测试$($, 或者也是$\frac3{4}$", 
                normalize_token=True,
                ensure_valid_formula=True,
            )

        self.assertEqual(
            normalize_latex_in_sentence(
                r"这是一次测试$x\geqslant y$, 或者也是$\frac3$", 
                normalize_token=True,
                ensure_valid_formula=False,
            ),
            r"这是一次测试$x \ge y$, 或者也是$\frac 3$"
        )

        self.assertEqual(
            normalize_latex_in_sentence(
                r"这是一次测试$ ) ($, 或者也是$\frac3$", 
                normalize_token=True,
                ensure_valid_formula=False,
            ),
            r"这是一次测试$) ($, 或者也是$\frac 3$"
        )

    def test_latex__not_strip_brace(self):
        self.assertEqual(
            normalize_latex_expression(
                r"a^{(2)}",
                ensure_valid_formula=False,
            ),
            r"a^{(2)}"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\frac{3}{(4)}",
                ensure_valid_formula=False,
            ),
            r"\frac{3}{(4)}"
        )

    def test_latex__begin_end_with_and(self):
        self.assertEqual(
            normalize_latex_expression(
                r"y= \begin{cases} x & (x \in (-1, 0])\\  x + x& (x> 0) \end{cases}",
            ),
            r"y = \begin{cases} x & (x \in (- 1 , 0]) \\ x + x & (x > 0) \end{cases}"
        )

    def test_latex__sin_and_sup(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\sin^2\alpha",
            ),
            r"\sin^{2}(\alpha)"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\cos^2\alpha",
            ),
            r"\cos^{2}(\alpha)"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\tan^2\alpha",
            ),
            r"\tan^{2}(\alpha)"
        )

    def test_latex__with_prime(self):
        self.assertEqual(
            normalize_latex_expression(
                r"g^{\prime} (x) \gt 0",
            ),
            r"g' (x) \gt 0"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"g^{\prime} (x) \lt 0",
            ),
            r"g' (x) \lt 0"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"F^{\prime \prime} (x) \gt 0",
            ),
            r"F'' (x) \gt 0"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"F^{\prime} (x) = e^{x} + \frac{k}{x + 1} - (k + 1)",
            ),
            r"F' (x) = e^{x} + \frac{k}{x + 1} - (k + 1)"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"F^{\prime \prime} (x) \gt 0",
            ),
            r"F'' (x) \gt 0"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"g^{\prime} (x) = \frac{x - 2}{x}",
            ),
            r"g' (x) = \frac{x - 2}{x}"
        )

    def test_latex__with_invalid_brace(self):
        self.assertEqual(
            normalize_latex_expression(
                r"{\log_{m}(2)} + {\log_{m}(5)} = 2",
            ),
            r"\log_{m}(2) + \log_{m}(5) = 2"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"{\log_{m}(10)} = 2",
            ),
            r"\log_{m}(10) = 2"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"f (x) = {(\frac{1}{2^{x}})}^{2} - \frac{1}{2^{x}} + 1",
            ),
            r"f (x) = (\frac{1}{2^{x}})^{2} - \frac{1}{2^{x}} + 1"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"f (x) = \begin{cases} {| 2x + 1 |} , & (x \lt 1) \\ {\ln(x - 1)} , & (x \gt 1) \end{cases}",
            ),
            r"f (x) = \begin{cases} | 2x + 1 | , & (x \lt 1) \\ \ln(x - 1) , & (x \gt 1) \end{cases}"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"\begin{cases} {x \lt \log_{a}(3) , (0 \lt a \lt 1)} \\ {x \gt \log_{a}(3) , (a \gt 1)} \end{cases}",
            ),
            r"\begin{cases} {x \lt \log_{a}(3) , (0 \lt a \lt 1)} \\ {x \gt \log_{a}(3) , (a \gt 1)} \end{cases}"
        )

    def test_latex__with_overset(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\overset{\to}{AC} = 3\overset{\to}{F_{2}C}",
            ),
            r"\overset{\to}{AC} = 3 \overset{\to}{F_{2} C}"
        )

    def test_latex__with_complete_token(self):
        self.assertEqual(
            normalize_latex_expression(
                r"sinx+cosb=1",
            ),
            r"\sin(x) + \cos(b) = 1"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"a sinx+bcosb=1",
            ),
            r"a \sin(x) + b \cos(b) = 1"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"sinxlgyln10",
            ),
            r"\sin(x) \lg(y) \ln(10)"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"arcsinx+arccosb=1",
            ),
            r"arcsinx + arccosb = 1"
        )

    def test_latex__with_complete_token(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\cos ln3",
            ),
            r"\cos(\ln(3))"
        )

    def test_latex__with_log_no_brace(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\log_23", brace_single_elem_for_log=False
            ),
            r"\log_{2}3"
        )

    def test_latex__with_abs(self): 
        self.assertEqual(
            normalize_latex_expression(
                r"\frac{\vert e \vert}{2}", 
            ),
            r"\frac{|e|}{2}"
        )
        
        self.assertEqual(
            normalize_latex_expression(
                r"\frac{\frac{\vert e \vert}{3}}{2}", 
            ),
            r"\frac{\frac{|e|}{3}}{2}"
        )

        self.assertEqual(
            normalize_latex_expression(
                r"a+\vert -a \vert", 
            ),
            r"a + |- a|"
        )

    def test_latex__normalize(self):
        self.assertEqual(
            normalize_latex_expression(
                r"(-3s+\frac{1}{2}t)⋅(-7st^{2})", normalize_token=True,
            ),
            r"(- 3s + \frac{1}{2} t) \cdot (- 7st^{2})",
        )
        self.assertEqual(
            normalize_latex_expression(
                r"(3x + 2y)^{2} - (x + 2y) (2y - x) – (12x^{2} y^{2} - 2x^{2} y) \div xy",
                normalize_token=True,
            ),
            r"(3x + 2y)^{2} - (x + 2y) (2y - x) - (12x^{2} y^{2} - 2x^{2} y) \div xy",
        )

    def test_latex__intefral(self):
        self.assertEqual(
            normalize_latex_expression(
                r" $\int_{0}^{\pi / 2} \sin ^{4} x \cos x d x$", normalize_token=True,
            ),
            r"$ \int_{0}^{\pi / 2} \sin^{4}(x) \cos(xdx) $",
        )

    def test_latex__tan(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\frac{d}{dx}tan^{-1} 3 x", normalize_token=True,
            ),
            r"\frac{d}{dx} \tan^{- 1}(3x)",
        )

    def test_latex__csc(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\frac{d}{d x}\left(\csc ^{5} 3 x\right)", normalize_token=True,
            ),
            r"\frac{d}{dx} \left (\csc^{5}(3x) \right)",
        )

    def test_latex__ln_20221031(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\ln(2x - 1)^{2} = 7", normalize_token=True,
            ),
            r"\ln((2x - 1)^{2}) = 7",
        )

    def test_latex__moninal_consecutive(self):
        self.assertEqual(
            normalize_latex_expression(
                r"\frac{d}{dx}(e^{\cos \pi x})", normalize_token=True,
            ),
            r"\frac{d}{dx} (e^{\cos(\pi x)})",
        )

import unittest

from ..components.unary_component import (
    SqrtComponent, ExpComponent, SubscriptComponent, Vector2Component, 
    VectorComponent, SineFunctionComponent, CosineFunctionComponent, 
    TangentFunctionComponent, LogrithmComponent, LgComponent, LnComponent,
    AngleComponent, MoninalComponent, RmComponent
)

from ..stream import LatexTokenStream


class TestSqrt(unittest.TestCase):
    def test_sqrt1(self):
        latex = r"\sqrt5"
        stream = LatexTokenStream(latex)

        comp = SqrtComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\sqrt{5}"
        )

    def test_sqrt2(self):
        latex = r"\sqrt[3]5"
        stream = LatexTokenStream(latex)

        comp = SqrtComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\sqrt[3]{5}"
        )

    def test_sqrt3(self):
        latex = r"\sqrt[3]\frac12"
        stream = LatexTokenStream(latex)

        comp = SqrtComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\sqrt[3]{\frac{1}{2}}"
        )

    def test_sqrt__expr(self):
        self.assertEqual(
            SqrtComponent.match(LatexTokenStream(r"\sqrt {2a}")).to_string(),
            r"\sqrt{2a}"
        )

        self.assertEqual(
            SqrtComponent.match(LatexTokenStream(r"\sqrt 2a}")).to_string(),
            r"\sqrt{2}"
        )


class TestExp(unittest.TestCase):
    def test_exp1(self):
        latex = r"^5"
        stream = LatexTokenStream(latex)

        comp = ExpComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"^{5}"
        )

    def test_exp2(self):
        latex = r"^\frac12"
        stream = LatexTokenStream(latex)

        comp = ExpComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"^{\frac{1}{2}}"
        )

    def test__with_prime(self):
        self.assertEqual(
            ExpComponent.match(LatexTokenStream(r"^\prime")).to_string(),
            r"'"
        )

        self.assertEqual(
            ExpComponent.match(LatexTokenStream(r"^{\prime}")).to_string(),
            r"'"
        )

        self.assertEqual(
            ExpComponent.match(LatexTokenStream(r"^{\prime\prime}")).to_string(),
            r"''"
        )


class TestSubscript(unittest.TestCase):
    def test_sub1(self):
        latex = r"_5"
        stream = LatexTokenStream(latex)

        comp = SubscriptComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"_{5}"
        )

    def test_sub2(self):
        latex = r"_\frac12"
        stream = LatexTokenStream(latex)

        comp = SubscriptComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"_{\frac{1}{2}}"
        )


class TestVector(unittest.TestCase):
    def test_vector1(self):
        latex = r"\vec a"
        stream = LatexTokenStream(latex)

        comp = VectorComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\vec{a}"
        )

    def test_vector2(self):
        latex = r"\textbf a"
        stream = LatexTokenStream(latex)

        comp = Vector2Component.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\textbf{a}"
        )


class TestTrigonometric(unittest.TestCase):
    def test_sine(self):
        self.assertEqual(
            SineFunctionComponent.match(LatexTokenStream(r"\sin x+1")).to_string(),
            r"\sin(x)"
        )

        self.assertEqual(
            SineFunctionComponent.match(LatexTokenStream(r"\sin{x+1}")).to_string(),
            r"\sin(x + 1)"
        )

        self.assertEqual(
            SineFunctionComponent.match(LatexTokenStream(r"\sin(x+1)")).to_string(),
            r"\sin(x + 1)"
        )

        self.assertEqual(
            SineFunctionComponent.match(LatexTokenStream(r"\sin 60^\circ")).to_string(),
            r"\sin(60^{\circ})"
        )

        self.assertEqual(
            SineFunctionComponent.match(LatexTokenStream(r"\sin 0.3")).to_string(),
            r"\sin(0.3)"
        )

        self.assertEqual(
            SineFunctionComponent.match(LatexTokenStream(r"\sin 3 \theta")).to_string(),
            r"\sin(3\theta)"
        )

        self.assertEqual(
            SineFunctionComponent.match(LatexTokenStream(r"\sin t dt")).to_string(),
            r"\sin(tdt)"
        )

        self.assertEqual(
            SineFunctionComponent.match(LatexTokenStream(r"\sin \frac{1}2 \theta")).to_string(),
            r"\sin(\frac{1}{2} \theta)"
        )

    def test_cos(self):
        self.assertEqual(
            CosineFunctionComponent.match(LatexTokenStream(r"\cos x+1")).to_string(),
            r"\cos(x)"
        )

        self.assertEqual(
            CosineFunctionComponent.match(LatexTokenStream(r"\cos{x+1}")).to_string(),
            r"\cos(x + 1)"
        )

        self.assertEqual(
            CosineFunctionComponent.match(LatexTokenStream(r"\cos(x+1)")).to_string(),
            r"\cos(x + 1)"
        )

        self.assertEqual(
            CosineFunctionComponent.match(LatexTokenStream(r"\cos 60^\circ")).to_string(),
            r"\cos(60^{\circ})"
        )

    def test_tangent(self):
        self.assertEqual(
            TangentFunctionComponent.match(LatexTokenStream(r"\tan x+1")).to_string(),
            r"\tan(x)"
        )

        self.assertEqual(
            TangentFunctionComponent.match(LatexTokenStream(r"\tan{x+1}")).to_string(),
            r"\tan(x + 1)"
        )

        self.assertEqual(
            TangentFunctionComponent.match(LatexTokenStream(r"\tan(x+1)")).to_string(),
            r"\tan(x + 1)"
        )

        self.assertEqual(
            TangentFunctionComponent.match(LatexTokenStream(r"\tan 60^\circ")).to_string(),
            r"\tan(60^{\circ})"
        )

        self.assertEqual(
            TangentFunctionComponent.match(LatexTokenStream(r"\tan((2x - \frac{\pi}{3}))")).to_string(),
            r"\tan(2x - \frac{\pi}{3})"
        )


class TestLogorithm(unittest.TestCase):
    def test_log(self):
        self.assertEqual(
            LogrithmComponent.match(LatexTokenStream(r"\log_23")).to_string(),
            r"\log_{2}(3)"
        )

        self.assertEqual(
            LogrithmComponent.match(LatexTokenStream(r"\log_2 0.3")).to_string(),
            r"\log_{2}(0.3)"
        )

        self.assertEqual(
            LogrithmComponent.match(LatexTokenStream(r"\log_2{3}")).to_string(),
            r"\log_{2}(3)"
        )

        self.assertEqual(
            LogrithmComponent.match(LatexTokenStream(r"\log(3)")).to_string(),
            r"\log(3)"
        )

        self.assertEqual(
            LogrithmComponent.match(LatexTokenStream(r"\log(3 \theta)")).to_string(),
            r"\log(3 \theta)"
        )

        self.assertEqual(
            LogrithmComponent.match(LatexTokenStream(r"\log3 \theta")).to_string(),
            r"\log(3\theta)"
        )

    def test_ln(self):
        self.assertEqual(
            LnComponent.match(LatexTokenStream(r"\ln 3")).to_string(),
            r"\ln(3)"
        )

        self.assertEqual(
            LnComponent.match(LatexTokenStream(r"\ln{3x+1}")).to_string(),
            r"\ln(3x + 1)"
        )

        self.assertEqual(
            LnComponent.match(LatexTokenStream(r"\ln3 \theta")).to_string(),
            r"\ln(3\theta)"
        )

        self.assertEqual(
            LnComponent.match(LatexTokenStream(r"\ln t dt")).to_string(),
            r"\ln(tdt)"
        )

    def test_lg(self):
        self.assertEqual(
            LgComponent.match(LatexTokenStream(r"\lg 3")).to_string(),
            r"\lg(3)"
        )

        self.assertEqual(
            LgComponent.match(LatexTokenStream(r"\lg{3x+1}")).to_string(),
            r"\lg(3x + 1)"
        )

    def test_lg_append_with_sup_or_sub(self):
        self.assertEqual(
            LgComponent.match(LatexTokenStream(r"\lg 3^{2}")).to_string(),
            r"\lg(3^{2})"
        )

        self.assertEqual(
            LogrithmComponent.match(LatexTokenStream(r"\log 3^2}")).to_string(),
            r"\log(3^{2})"
        )

        self.assertEqual(
            LnComponent.match(LatexTokenStream(r"\ln 3^2}")).to_string(),
            r"\ln(3^{2})"
        )

    def test_logarithm__with_sup(self):
        self.assertEqual(
            LgComponent.match(LatexTokenStream(r"\lg^2 x")).to_string(),
            r"\lg^{2}(x)"
        )

        self.assertEqual(
            LogrithmComponent.match(LatexTokenStream(r"\log^2 x")).to_string(),
            r"\log^{2}(x)"
        )

        self.assertEqual(
            LnComponent.match(LatexTokenStream(r"\ln^2 x")).to_string(),
            r"\ln^{2}(x)"
        )

        self.assertEqual(
            LogrithmComponent.match(LatexTokenStream(r"\log^2_3 x")).to_string(),
            r"\log_{3}^{2}(x)"
        )


class TestAngle(unittest.TestCase):
    def test_angle(self):
        self.assertEqual(
            AngleComponent.match(LatexTokenStream(r"\angle AB")).to_string(),
            r"\angle AB"
        )

        self.assertEqual(
            AngleComponent.match(LatexTokenStream(r"\angle A")).to_string(),
            r"\angle A"
        )

    def test_angle__without_marker(self):
        self.assertEqual(
            AngleComponent.match(LatexTokenStream(r"\angle AB")).to_string(with_angle_marker=False),
            r"AB"
        )

        self.assertEqual(
            AngleComponent.match(LatexTokenStream(r"\angle A")).to_string(with_angle_marker=False),
            r"A"
        )


class TestMoninal(unittest.TestCase):
    def test_moninal_(self):
        self.assertEqual(
            MoninalComponent.match(LatexTokenStream(r"-3x")).to_string(),
            r"-3x"
        )

    def test_moninal_(self):
        self.assertEqual(
            MoninalComponent.match(LatexTokenStream(r"3x")).to_string(),
            r"3x"
        )

        self.assertEqual(
            MoninalComponent.match(LatexTokenStream(r"3\pi")).to_string(),
            r"3\pi"
        )

        self.assertEqual(
            MoninalComponent.match(LatexTokenStream(r"3\beta")).to_string(),
            r"3\beta"
        )

        self.assertEqual(
            MoninalComponent.match(LatexTokenStream(r"3\alpha")).to_string(),
            r"3\alpha"
        )

        self.assertEqual(
            MoninalComponent.match(LatexTokenStream(r"3\sigma")).to_string(),
            r"3\sigma"
        )

        self.assertEqual(
            MoninalComponent.match(LatexTokenStream(r"3\theta")).to_string(),
            r"3\theta"
        )


class TestRmComponent(unittest.TestCase):
    def test_moninal_(self):
        RmComponent.set_status(keep_rm=False)
        self.assertEqual(
            RmComponent.match(LatexTokenStream(r"\rm{kg}")).to_string(),
            r"kg"
        )

        self.assertEqual(
            RmComponent.match(LatexTokenStream(r"\rm kg")).to_string(),
            r""
        )

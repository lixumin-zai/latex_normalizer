import unittest

from ..components.binary_component import (
    FracComponent, OversetComponent, UndersetComponent, ComplementComponent,
    DFracComponent,
)

from ..stream import LatexTokenStream


class TestFrac(unittest.TestCase):
    def test_frac1(self):
        latex = r"\frac{1}2"
        stream = LatexTokenStream(latex)

        comp = FracComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\frac{1}{2}"
        )

    def test_frac2(self):
        latex = r"\frac12"
        stream = LatexTokenStream(latex)

        comp = FracComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\frac{1}{2}"
        )

    def test_frac3(self):
        latex = r"\frac1{2}"
        stream = LatexTokenStream(latex)

        comp = FracComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\frac{1}{2}"
        )

    def test_frac4(self):
        latex = r"\frac{\frac{1}{2}}1"
        stream = LatexTokenStream(latex)

        comp = FracComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\frac{\frac{1}{2}}{1}"
        )

    def test_frac5(self):
        latex = r"\frac1{\frac{1}{2}}"
        stream = LatexTokenStream(latex)

        comp = FracComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\frac{1}{\frac{1}{2}}"
        )

    def test_dfrac(self):
        latex = r"\dfrac1{\frac{1}{2}}"
        stream = LatexTokenStream(latex)

        comp = DFracComponent.match(stream)

        self.assertEqual(
            comp.to_string(),
            r"\dfrac{1}{\frac{1}{2}}"
        )


class TestOverset(unittest.TestCase):
    def test__normal(self):
        self.assertEqual(
            OversetComponent.match(LatexTokenStream(r"\overset{\to}{AC}")).to_string(),
            r"\overset{\to}{AC}"
        )

        self.assertEqual(
            OversetComponent.match(LatexTokenStream(r"\overset{\to}A")).to_string(),
            r"\overset{\to}{A}"
        )

        self.assertEqual(
            OversetComponent.match(LatexTokenStream(r"\overset\to A")).to_string(),
            r"\overset{\to}{A}"
        )


class TestUnderset(unittest.TestCase):
    def test__normal(self):
        self.assertEqual(
            UndersetComponent.match(LatexTokenStream(r"\underset{\to}{AC}")).to_string(),
            r"\underset{\to}{AC}"
        )

        self.assertEqual(
            UndersetComponent.match(LatexTokenStream(r"\underset{\to}A")).to_string(),
            r"\underset{\to}{A}"
        )

        self.assertEqual(
            UndersetComponent.match(LatexTokenStream(r"\underset\to A")).to_string(),
            r"\underset{\to}{A}"
        )


class TestComplement(unittest.TestCase):
    def test__with_sub(self):
        self.assertEqual(
            ComplementComponent.match(LatexTokenStream(r"\complement_{C}{A}")).to_string(),
            r"\complement_{C}{A}"
        )

        self.assertEqual(
            ComplementComponent.match(LatexTokenStream(r"\complement_C{A}")).to_string(),
            r"\complement_{C}{A}"
        )

        self.assertEqual(
            ComplementComponent.match(LatexTokenStream(r"\complement_CA")).to_string(),
            r"\complement_{C}{A}"
        )

        self.assertEqual(
            ComplementComponent.match(LatexTokenStream(r"\complement_C{A}")).to_string(),
            r"\complement_{C}{A}"
        )

    def test__without_sub(self):
        self.assertEqual(
            ComplementComponent.match(LatexTokenStream(r"\complement A")).to_string(),
            r"\complement{A}"
        )

        self.assertEqual(
            ComplementComponent.match(LatexTokenStream(r"\complement{A}")).to_string(),
            r"\complement{A}"
        )

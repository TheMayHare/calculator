import unittest
from calculator_core import Parser, Evaluator, Calculator, Plus, Min, Mult, Div, Number


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.parser = Parser()
        self.evaluator = Evaluator()

    def test_parser(self):
        # Тест парсера с экспоненциальной записью
        self.assertEqual(repr(self.parser.parse("1.35e-7")), "Number(1.35e-07)")
        self.assertEqual(repr(self.parser.parse("2.5E+3")), "Number(2500.0)")
        self.assertEqual(repr(self.parser.parse("1+2.5e-2")), "Plus(Number(1.0), Number(0.025))")

        # Остальные тесты
        self.assertEqual(repr(self.parser.parse("1+2")), "Plus(Number(1.0), Number(2.0))")
        self.assertEqual(repr(self.parser.parse("3*4+5")), "Plus(Mult(Number(3.0), Number(4.0)), Number(5.0))")

    def test_evaluator(self):
        # Тест вычислителя с экспоненциальной записью
        self.assertAlmostEqual(self.evaluator.evaluate(Number(1.35e-7)), 1.35e-7)
        self.assertEqual(self.evaluator.evaluate(Plus(Number(1), Number(2.5e-2))), 1.025)

        # Остальные тесты
        self.assertEqual(self.evaluator.evaluate(Plus(Number(1), Number(2))), 3)
        self.assertEqual(self.evaluator.evaluate(Mult(Number(3), Number(4))), 12)

    def test_calculator(self):
        # Тест калькулятора с экспоненциальной записью
        self.assertEqual(self.calc.calculate("1.35e-7"), 1.35e-7)
        self.assertEqual(self.calc.calculate("2.5E+3"), 2500.0)
        self.assertEqual(self.calc.calculate("1+2.5e-2"), 1.025)
        self.assertEqual(self.calc.calculate("1e10*1e-10"), 1.0)

        # Остальные тесты
        self.assertEqual(self.calc.calculate("1+2"), 3)
        self.assertEqual(self.calc.calculate("3*4+5"), 17)
        self.assertEqual(self.calc.calculate("1/0"), "Деление на ноль")


if __name__ == "__main__":
    unittest.main()
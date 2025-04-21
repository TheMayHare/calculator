import unittest
from calculator_core import *


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.parser = Parser()
        self.evaluator = Evaluator()

    def test_parser(self):
        # Тест парсера с научной нотацией
        self.assertEqual(repr(self.parser.parse("1.25e+9")), "Number(1250000000.0)")
        self.assertEqual(repr(self.parser.parse("3.5E-3")), "Number(0.0035)")

        # Тест операции возведения в степень
        self.assertEqual(repr(self.parser.parse("2^3")), "Pow(Number(2.0), Number(3.0))")
        self.assertEqual(repr(self.parser.parse("2^(3^2)")), "Pow(Number(2.0), Pow(Number(3.0), Number(2.0)))")

        # Тест скобочных выражений
        self.assertEqual(repr(self.parser.parse("(1+2)*3")), "Mult(Plus(Number(1.0), Number(2.0)), Number(3.0))")
        self.assertEqual(repr(self.parser.parse("1+(2*3)")), "Plus(Number(1.0), Mult(Number(2.0), Number(3.0)))")

        # Тест приоритета операций
        self.assertEqual(repr(self.parser.parse("2+3*4^2")),
                         "Plus(Number(2.0), Mult(Number(3.0), Pow(Number(4.0), Number(2.0))))")

    def test_evaluator(self):
        # Тест вычисления с научной нотацией
        self.assertEqual(self.evaluator.evaluate(Number(1.25e+9)), 1.25e+9)
        self.assertEqual(self.evaluator.evaluate(Number(3.5E-3)), 0.0035)

        # Тест возведения в степень
        self.assertEqual(self.evaluator.evaluate(Pow(Number(2), Number(3))), 8)
        self.assertEqual(self.evaluator.evaluate(Pow(Number(3), Number(2))), 9)

        # Тест скобочных выражений
        self.assertEqual(self.evaluator.evaluate(self.parser.parse("(1+2)*3")), 9)
        self.assertEqual(self.evaluator.evaluate(self.parser.parse("1+(2*3)")), 7)

        # Тест приоритета операций
        self.assertEqual(self.evaluator.evaluate(self.parser.parse("2+3*4^2")), 50)
        self.assertEqual(self.evaluator.evaluate(self.parser.parse("2^3^2")), 64)

        def test_calculator(self):
            self.assertEqual(self.calc.calculate("1.25e+9"), 1.25e+9)
            self.assertEqual(self.calc.calculate("3.5E-3"), 0.0035)
            self.assertEqual(self.calc.calculate("2^3"), 8)
            self.assertEqual(self.calc.calculate("3^2"), 9)
            self.assertEqual(self.calc.calculate("(1+2)*3"), 9)
            self.assertEqual(self.calc.calculate("1+(2*3)"), 7)
            self.assertEqual(self.calc.calculate("2+3*4^2"), 50)
            self.assertEqual(self.calc.calculate("2^3^2"), 512)
            self.assertEqual(self.calc.calculate("1e10*1e-10"), 1.0)

            # Тест ошибок
            self.assertEqual(self.calc.calculate("2/0"), "Деление на ноль")
            self.assertEqual(self.calc.calculate("2^1000"), "Арифметическое переполнение")
            self.assertEqual(self.calc.calculate("2 ^^ 3"), "Неизвестный символ в позиции 2: '^'")

    if __name__ == "__main__":
        unittest.main()
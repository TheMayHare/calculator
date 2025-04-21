import unittest
import time
from calculator_core import *


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.evaluator_rad = Evaluator(angle_unit='radian')
        self.evaluator_deg = Evaluator(angle_unit='degree')

    def test_parser(self):
        # Тест функций
        self.assertEqual(repr(self.parser.parse("sqrt(4)")), "FuncCall('sqrt', Number(4.0))")
        self.assertEqual(repr(self.parser.parse("sin(pi/2)")),
                         "FuncCall('sin', Div(Number(3.141592653589793), Number(2.0)))")

        # Тест констант
        self.assertEqual(repr(self.parser.parse("pi")), "Number(3.141592653589793)")
        self.assertEqual(repr(self.parser.parse("e")), "Number(2.718281828459045)")

    def test_evaluator_radians(self):
        # Тригонометрия в радианах
        self.assertAlmostEqual(self.evaluator_rad.evaluate(self.parser.parse("sin(pi/2)")), 1.0)
        self.assertAlmostEqual(self.evaluator_rad.evaluate(self.parser.parse("cos(0)")), 1.0)
        self.assertAlmostEqual(self.evaluator_rad.evaluate(self.parser.parse("tg(pi/4)")), 1.0)

        # Другие функции
        self.assertAlmostEqual(self.evaluator_rad.evaluate(self.parser.parse("sqrt(4)")), 2.0)
        self.assertAlmostEqual(self.evaluator_rad.evaluate(self.parser.parse("ln(e)")), 1.0)
        self.assertAlmostEqual(self.evaluator_rad.evaluate(self.parser.parse("exp(0)")), 1.0)

    def test_evaluator_degrees(self):
        # Тригонометрия в градусах
        self.assertAlmostEqual(self.evaluator_deg.evaluate(self.parser.parse("sin(90)")), 1.0)
        self.assertAlmostEqual(self.evaluator_deg.evaluate(self.parser.parse("cos(0)")), 1.0)
        self.assertAlmostEqual(self.evaluator_deg.evaluate(self.parser.parse("tg(45)")), 1.0)

    def test_calculator_integration(self):
        # Интеграционные тесты
        calc_rad = Calculator(angle_unit='radian')
        calc_deg = Calculator(angle_unit='degree')

        self.assertAlmostEqual(calc_rad.calculate("sqrt(ln(exp(2)^2))"), 2.0)
        self.assertAlmostEqual(calc_deg.calculate("sin(90)"), 1.0)
        self.assertAlmostEqual(calc_rad.calculate("sin(pi/2)"), 1.0)
        self.assertAlmostEqual(calc_rad.calculate("exp(ln(2))"), 2.0)

    def test_performance(self):
        """Тест производительности (не должен превышать 200мс)"""
        calc = Calculator()

        # Длинное выражение
        start_time = time.time()
        result = calc.calculate("1" + "+1" * 500)  # 1+1+1+...+1 (501 раз)
        execution_time = (time.time() - start_time) * 1000

        self.assertEqual(result, 501)
        self.assertLess(execution_time, 200,
                        f"Время выполнения {execution_time:.2f}мс превысило 200мс")

        # Большие числа
        start_time = time.time()
        result = calc.calculate("1e300 * 1e-300")
        execution_time = (time.time() - start_time) * 1000

        self.assertEqual(result, 1.0)
        self.assertLess(execution_time, 200,
                        f"Время выполнения {execution_time:.2f}мс превысило 200мс")


if __name__ == "__main__":
    unittest.main()
import unittest
from calculator_core import calculate


class TestSafeCalculator(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(calculate("2+3"), 5)
        self.assertEqual(calculate("5-2"), 3)
        self.assertEqual(calculate("3*4"), 12)
        self.assertEqual(calculate("10/2"), 5)
        self.assertAlmostEqual(calculate("0.1+0.2"), 0.3, places=10)

    def test_operator_priority(self):
        self.assertEqual(calculate("2+3*5"), 17)
        self.assertEqual(calculate("2*3+5"), 11)
        self.assertEqual(calculate("10-4/2"), 8)

    def test_invalid_expressions(self):
        with self.assertRaises(ValueError):
            calculate("2/0")  # Деление на ноль

        with self.assertRaises(ValueError):
            calculate("2+")  # Неполное выражение

        with self.assertRaises(ValueError):
            calculate("abc")  # Нечисловые символы

        with self.assertRaises(ValueError):
            calculate("2++3")  # Двойной оператор

    def test_spaces_ignored(self):
        self.assertEqual(calculate("2 + 3"), 5)
        self.assertEqual(calculate("2+ 3"), 5)
        self.assertEqual(calculate("2 +3"), 5)

    def test_decimal_numbers(self):
        self.assertAlmostEqual(calculate("1.5*2"), 3.0)
        self.assertAlmostEqual(calculate("0.1+0.2"), 0.3, places=10)


if __name__ == "__main__":
    unittest.main()
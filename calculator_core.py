import re
import math
import time
import argparse
from typing import Union, List, Dict, Callable


class ParseError(Exception):
    pass


class CalculationError(Exception):
    pass


# Классы для AST
class Expr:
    """Базовый класс для выражений"""
    pass


class Number(Expr):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class Plus(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Plus({self.left}, {self.right})"


class Min(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Min({self.left}, {self.right})"


class Mult(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Mult({self.left}, {self.right})"


class Div(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Div({self.left}, {self.right})"


class Pow(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Pow({self.left}, {self.right})"


class FuncCall(Expr):
    def __init__(self, func_name: str, arg: Expr):
        self.func_name = func_name
        self.arg = arg

    def __repr__(self):
        return f"FuncCall('{self.func_name}', {self.arg})"


class Parser:
    """Парсер математических выражений с поддержкой функций и констант"""

    def __init__(self):
        self.operators = {
            '+': (1, lambda left, right: Plus(left, right)),
            '-': (1, lambda left, right: Min(left, right)),
            '*': (2, lambda left, right: Mult(left, right)),
            '/': (2, lambda left, right: Div(left, right)),
            '^': (3, lambda left, right: Pow(left, right))
        }
        self.functions = {
            'sqrt', 'sin', 'cos', 'tg', 'ctg', 'ln', 'exp'
        }
        self.constants = {
            'pi': math.pi,
            'e': math.e
        }
        self.tokens = []
        self.current = 0

    def parse(self, expression: str) -> Expr:
        """Основной метод парсинга"""
        self.tokens = self._tokenize(expression)
        self.current = 0
        return self._parse_expression()

    def _tokenize(self, expression: str) -> List[Union[str, float]]:
        """Разбивает выражение на токены"""
        expr = expression.replace(" ", "")
        tokens = []
        i = 0

        # Регулярное выражение для чисел и функций
        number_pattern = re.compile(r'(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?')
        func_pattern = re.compile(r'([a-zA-Z]+)\(')

        while i < len(expr):
            if expr[i] in {'+', '-', '*', '/', '^', '(', ')', ','}:
                # Обработка унарного минуса
                if expr[i] == '-' and (not tokens or tokens[-1] in {'+', '-', '*', '/', '^', '('}):
                    tokens.append('u-')
                else:
                    tokens.append(expr[i])
                i += 1
            else:
                # Проверяем, может быть это функция
                func_match = func_pattern.match(expr, i)
                if func_match:
                    func_name = func_match.group(1)
                    if func_name not in self.functions:
                        raise ParseError(f"Неизвестная функция: {func_name}")
                    tokens.append(func_name + '(')
                    i = func_match.end()
                    continue

                # Проверяем, может быть это константа
                if expr[i].isalpha():
                    const_name = ''
                    while i < len(expr) and expr[i].isalpha():
                        const_name += expr[i]
                        i += 1

                    if const_name in self.constants:
                        tokens.append(self.constants[const_name])
                    else:
                        raise ParseError(f"Неизвестная константа: {const_name}")
                    continue

                # Пытаемся извлечь число
                num_match = number_pattern.match(expr, i)
                if num_match:
                    num_str = num_match.group(0)
                    try:
                        num = float(num_str)
                    except ValueError:
                        raise ParseError(f"Неверное число: {num_str}")
                    tokens.append(num)
                    i = num_match.end()
                    continue

                raise ParseError(f"Неизвестный символ в позиции {i}: '{expr[i]}'")

        return tokens

    def _parse_expression(self) -> Expr:
        """Парсит выражение с учетом приоритета операций"""
        return self._parse_binary_op(0)

    def _parse_binary_op(self, precedence: int) -> Expr:
        """Рекурсивный парсинг бинарных операций"""
        left = self._parse_unary_op()

        while (self.current < len(self.tokens) and
               isinstance(self.tokens[self.current], str) and
               self.tokens[self.current] in self.operators and
               self.operators[self.tokens[self.current]][0] >= precedence):
            op = self.tokens[self.current]
            self.current += 1
            op_prec, op_ctor = self.operators[op]
            right = self._parse_binary_op(op_prec + 1)
            left = op_ctor(left, right)

        return left

    def _parse_unary_op(self) -> Expr:
        """Парсит унарные операции, функции и первичные выражения"""
        if self.current >= len(self.tokens):
            raise ParseError("Неожиданный конец выражения")

        token = self.tokens[self.current]

        if token == 'u-':
            self.current += 1
            return Min(Number(0), self._parse_unary_op())
        elif isinstance(token, str) and token.endswith('('):
            # Обработка вызова функции
            func_name = token[:-1]
            self.current += 1
            arg = self._parse_expression()
            if self.current >= len(self.tokens) or self.tokens[self.current] != ')':
                raise ParseError("Ожидалась закрывающая скобка для функции")
            self.current += 1
            return FuncCall(func_name, arg)
        elif token == '(':
            self.current += 1
            expr = self._parse_expression()
            if self.current >= len(self.tokens) or self.tokens[self.current] != ')':
                raise ParseError("Ожидалась закрывающая скобка")
            self.current += 1
            return expr
        elif isinstance(token, (int, float)):
            self.current += 1
            return Number(token)

        raise ParseError(f"Неожиданный токен: {token}")


class Evaluator:
    """Вычислитель AST с поддержкой функций и констант"""

    def __init__(self, angle_unit: str = 'radian'):
        self.angle_unit = angle_unit
        self.functions: Dict[str, Callable[[float], float]] = {
            'sqrt': math.sqrt,
            'sin': self._trig_wrapper(math.sin),
            'cos': self._trig_wrapper(math.cos),
            'tg': self._trig_wrapper(math.tan),
            'ctg': lambda x: 1 / self._trig_wrapper(math.tan)(x),
            'ln': math.log,
            'exp': math.exp
        }

    def _trig_wrapper(self, func: Callable[[float], float]) -> Callable[[float], float]:
        """Обертка для тригонометрических функций с учетом единиц измерения углов"""

        def wrapper(x: float) -> float:
            if self.angle_unit == 'degree':
                x = math.radians(x)
            return func(x)

        return wrapper

    def evaluate(self, node: Expr) -> float:
        """Вычисляет значение AST"""
        if isinstance(node, Number):
            return node.value

        if isinstance(node, Plus):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return left + right

        if isinstance(node, Min):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return left - right

        if isinstance(node, Mult):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return left * right

        if isinstance(node, Div):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if right == 0:
                raise CalculationError("Деление на ноль")
            return left / right

        if isinstance(node, Pow):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            try:
                result = left ** right
                if abs(result) > 1e300:
                    raise OverflowError
                return result
            except OverflowError:
                raise CalculationError("Арифметическое переполнение")

        if isinstance(node, FuncCall):
            func = self.functions.get(node.func_name)
            if not func:
                raise CalculationError(f"Неизвестная функция: {node.func_name}")
            arg = self.evaluate(node.arg)
            try:
                result = func(arg)
                if abs(result) > 1e300:
                    raise OverflowError
                return result
            except ValueError as e:
                raise CalculationError(str(e))
            except OverflowError:
                raise CalculationError("Арифметическое переполнение")

        raise CalculationError(f"Неизвестный тип узла: {type(node)}")


class Calculator:
    """Обертка для парсера и вычислителя с поддержкой CLI"""

    def __init__(self, angle_unit: str = 'radian'):
        self.parser = Parser()
        self.evaluator = Evaluator(angle_unit)

    def calculate(self, expression: str) -> Union[float, str]:
        """Основной метод калькулятора с замером времени"""
        start_time = time.time()

        try:
            ast = self.parser.parse(expression)
            result = self.evaluator.evaluate(ast)

            # Форматирование результата
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                elif abs(result) < 1e-4 or abs(result) >= 1e10:
                    result = float(f"{result:.8e}")

            execution_time = (time.time() - start_time) * 1000  # в миллисекундах
            if execution_time > 200:
                raise CalculationError(f"Время выполнения превысило 200мс: {execution_time:.2f}мс")

            return result
        except (ParseError, CalculationError) as e:
            return str(e)


def main():
    """Точка входа для CLI"""
    parser = argparse.ArgumentParser(description='Калькулятор математических выражений')
    parser.add_argument('expression', help='Математическое выражение для вычисления')
    parser.add_argument('--angle-unit', choices=['degree', 'radian'], default='radian',
                        help='Единицы измерения углов (по умолчанию: радианы)')

    args = parser.parse_args()

    calculator = Calculator(angle_unit=args.angle_unit)
    result = calculator.calculate(args.expression)
    print(f"Результат: {result}")


if __name__ == "__main__":
    main()
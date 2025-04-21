import re
import math
from typing import Union


class ParseError(Exception):
    pass


class CalculationError(Exception):
    pass


class Expr:
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


class Parser:

    def __init__(self):
        self.operators = {
            '+': (1, lambda left, right: Plus(left, right)),
            '-': (1, lambda left, right: Min(left, right)),
            '*': (2, lambda left, right: Mult(left, right)),
            '/': (2, lambda left, right: Div(left, right)),
            '^': (3, lambda left, right: Pow(left, right))  # Наивысший приоритет
        }
        self.tokens = []
        self.current = 0

    def parse(self, expression: str) -> Expr:
        self.tokens = self._tokenize(expression)
        self.current = 0
        return self._parse_expression()

    def _tokenize(self, expression: str) -> list:
        expr = expression.replace(" ", "")
        tokens = []
        i = 0

        # Регулярное выражение для чисел (включая научную нотацию)
        number_pattern = re.compile(r'(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?')

        while i < len(expr):
            if expr[i] in {'+', '-', '*', '/', '^'}:
                if expr[i] == '-' and (not tokens or tokens[-1] in {'+', '-', '*', '/', '^', '('}):
                    tokens.append('u-')
                else:
                    tokens.append(expr[i])
                i += 1
            elif expr[i] == '(':
                tokens.append(expr[i])
                i += 1
            elif expr[i] == ')':
                tokens.append(expr[i])
                i += 1
            else:
                match = number_pattern.match(expr, i)
                if not match:
                    raise ParseError(f"Неизвестный символ в позиции {i}: '{expr[i]}'")

                num_str = match.group(0)
                try:
                    num = float(num_str)
                except ValueError:
                    raise ParseError(f"Неверное число: {num_str}")

                tokens.append(num)
                i = match.end()

        return tokens

    def _parse_expression(self) -> Expr:
        return self._parse_binary_op(0)

    def _parse_binary_op(self, precedence: int) -> Expr:
        left = self._parse_unary_op()

        while (self.current < len(self.tokens) and
               (isinstance(self.tokens[self.current], str)) and
               (self.tokens[self.current] in self.operators) and
               (self.operators[self.tokens[self.current]][0] >= precedence)):
            op = self.tokens[self.current]
            self.current += 1
            op_prec, op_ctor = self.operators[op]
            right = self._parse_binary_op(op_prec + 1)
            left = op_ctor(left, right)

        return left

    def _parse_unary_op(self) -> Expr:
        if self.current >= len(self.tokens):
            raise ParseError("Неожиданный конец выражения")

        token = self.tokens[self.current]

        if token == 'u-':
            self.current += 1
            return Min(Number(0), self._parse_unary_op())
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

    def evaluate(self, node: Expr) -> float:
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

        raise CalculationError(f"Неизвестный тип узла: {type(node)}")


class Calculator:

    def __init__(self):
        self.parser = Parser()
        self.evaluator = Evaluator()

    def calculate(self, expression: str) -> Union[float, str]:
        try:
            ast = self.parser.parse(expression)
            result = self.evaluator.evaluate(ast)

            if isinstance(result, float):
                if result.is_integer():
                    return int(result)
                if abs(result) < 1e-4 or abs(result) >= 1e10:
                    return float(f"{result:.8e}")
            return result
        except (ParseError, CalculationError) as e:
            return str(e)


if __name__ == "__main__":
    calculator = Calculator()
    while True:
        expr = input("Введите выражение (или 'exit' для выхода): ")
        if expr.lower() == 'exit':
            break
        result = calculator.calculate(expr)
        print(f"Результат: {result}")
import sys
import re


def parse_number(expr, pos):
    start_pos = pos
    while pos < len(expr) and (expr[pos].isdigit() or expr[pos] == '.'):
        pos += 1
    if pos == start_pos:
        return None, pos
    num_str = expr[start_pos:pos]
    if '.' in num_str:
        return float(num_str), pos
    return int(num_str), pos


def apply_operator(a, op, b):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            raise ValueError("Деление на ноль")
        return a / b
    else:
        raise ValueError(f"Неизвестный оператор: {op}")


def calculate(expression):
    expr = expression.replace(" ", "")
    if not expr:
        raise ValueError("Пустое выражение")

    if not re.match(r'^[\d\.\+\-\*/]+$', expr):
        raise ValueError("Недопустимые символы в выражении")

    numbers = []
    operators = []
    pos = 0

    num, pos = parse_number(expr, pos)
    if num is None:
        raise ValueError("Ожидалось число в начале выражения")
    numbers.append(num)

    while pos < len(expr):
        if pos >= len(expr) or expr[pos] not in '+-*/':
            raise ValueError(f"Ожидался оператор на позиции {pos}")
        op = expr[pos]
        pos += 1

        num, pos = parse_number(expr, pos)
        if num is None:
            raise ValueError(f"Ожидалось число после оператора на позиции {pos}")

        if op in '*/':
            left = numbers.pop()
            result = apply_operator(left, op, num)
            numbers.append(result)
        else:
            operators.append(op)
            numbers.append(num)

    if not numbers:
        raise ValueError("Некорректное выражение")

    result = numbers[0]
    for i in range(len(operators)):
        result = apply_operator(result, operators[i], numbers[i + 1])

    return result


def main():
    if len(sys.argv) != 2:
        print("Использование: python safe_calc.py 'выражение'")
        print("Пример: python safe_calc.py '2+3*5'")
        sys.exit(1)

    try:
        result = calculate(sys.argv[1])
        print(result)
    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
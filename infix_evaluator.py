from numpy import exp as e, sin, cos, tan, log

import re


def _tokenize(expression):
    """ tokenize the input expression into numbers, and operators. """
    # replace unary minus as in -n with (0 - n)
    # uses a negative lookahead to match unary minus:
    # unary minus doesnot have an operand or ) preceeding the - sign
    # n in -n can be an integer like 2 or decimal like 2.0
    expression = re.sub(r'(?<![\d)])-(\d+\.?\d*)', r'(0-\1)', expression)

    tokens = re.findall(
        r'\d+\.\d+|\d+|[+\-*/^()]|sin|cos|tan|log|e', expression)
    return tokens


def _has_greater_precedence(op1, op2):
    """ true if op1 has greater or equal precedence than op2"""
    precedence = {
        "+": 0,
        "-": 0,
        "*": 1,
        "/": 1,
        "^": 2,
        "sin": 3,
        "cos": 3,
        "tan": 3,
        "log": 3,
        "e": 3,
        "(": 4,
    }
    op1_precedence = precedence[op1]
    op2_precedence = precedence[op2]
    return op1_precedence >= op2_precedence


def _permform_op(op, x, y):
    if op == "+":
        return x + y
    elif op == "-":
        return x - y
    elif op == "*":
        return x * y
    elif op == "/" and y != 0:
        return x / y
    elif op == "^":
        return x ** y
    elif op == "sin":
        return sin(y)
    elif op == "cos":
        return cos(y)
    elif op == "tan":
        return tan(y)
    elif op == "log" and y > 0:
        return log(y)
    elif op == "e":
        return e(y)
    return None


def evaulate_infix(expression):
    operand = list()
    operator = list()
    tokens = _tokenize(expression)
    for token in tokens:
        if operator:
            top_operator = operator[-1]
        if re.search(r"\d+\.\d+|\d+", token):  # decimals or multidigit numbers
            # match operands
            token = float(token)
            operand.append(token)
        elif token == "(":
            # match operators
            operator.append(token)
        elif re.search(r"[+\-*\^/]|sin|cos|tan|log|e", token):
            this_operator = token
            # TODO: separate this while block that is repeated three times into a helper function evaulate_infix_process()
            while operator and top_operator != "(" and _has_greater_precedence(top_operator, this_operator):
                top_operator = operator.pop()
                y = operand.pop()  # operand 2
                x = 0
                if not re.search(r"sin|cos|tan|log|e", top_operator):
                    x = operand.pop()  # operand 1
                result = _permform_op(top_operator, x, y)
                operand.append(result)
            operator.append(this_operator)
        elif token == ")":
            while (1):
                top_operator = operator.pop()
                if (top_operator == "("):
                    break
                y = operand.pop()  # operand 2
                x = 0
                if not re.search(r"sin|cos|tan|log|e", top_operator):
                    x = operand.pop()  # operand 1
                result = _permform_op(top_operator, x, y)
                operand.append(result)
    while (operator):
        top_operator = operator.pop()
        y = operand.pop()  # operand 2
        x = 0
        if not re.search(r"sin|cos|tan|log|e", top_operator):
            x = operand.pop()  # operand 1
        result = _permform_op(top_operator, x, y)
        operand.append(result)
    return operand[-1]


if __name__ == "__main__":
    print(_tokenize("e(10)"))

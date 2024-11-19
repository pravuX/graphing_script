from numpy import exp as e, sin, cos, tan, log

import re


def _tokenize(expression):
    """ Tokenize the input expression into numbers, and operators. """
    # Converts all unary minuses into u-
    expression = re.sub(r'^-', r'u-', expression)
    expression = re.sub(r'([+\*/^(])-', r'\1u-', expression)
    expression = re.sub(r'u--', r'u-u-', expression)
    tokens = re.findall(
        r'\d*\.?\d+|[+\-*/^()]|sin|cos|tan|log|e|u-', expression)
    return tokens


def _compare_precedence(op1, op2, comparison):
    """ Returns the truth value of the specified comparison between two given operators"""
    precedence = {
        "(": 0,
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "u-": 3,
        "^": 4,
        "sin": 5,
        "cos": 5,
        "tan": 5,
        "log": 5,
        "e": 5,
    }
    op1_precedence = precedence[op1]
    op2_precedence = precedence[op2]
    if comparison == "<=":
        return op1_precedence <= op2_precedence
    if comparison == ">=":
        return op1_precedence >= op2_precedence
    if comparison == "<":
        return op1_precedence < op2_precedence
    if comparison == ">":
        return op1_precedence > op2_precedence


def _associativity_of(operator):
    associativity = {
        "+": "L",
        "-": "L",
        "*": "L",
        "/": "L",
        "sin": "R",
        "cos": "R",
        "tan": "R",
        "log": "R",
        "e": "R",
        "u-": "R",
        "^": "R",
    }
    return associativity[operator]


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
    elif op == "u-":
        return -1 * y
    return None


def infix_to_postfix(expression):
    operators = list()
    postfix = list()
    tokens = _tokenize(expression)
    for token in tokens:
        if re.search(r"[+\-*\^/]|sin|cos|tan|log|e|u-", token):
            this_operator = token
            if operators:
                top_operator = operators[-1]
                while top_operator and (_associativity_of(this_operator) == "L" and _compare_precedence(this_operator, top_operator, "<=")) or (_associativity_of(this_operator) == "R" and _compare_precedence(this_operator, top_operator, "<")):
                    top_operator = operators.pop()
                    postfix.append(top_operator)
                    try:
                        top_operator = operators[-1]
                    except:
                        top_operator = None
            operators.append(this_operator)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            if operators:
                top_operator = operators.pop()
                while (top_operator != "("):
                    postfix.append(top_operator)
                    top_operator = operators.pop()
        else:
            postfix.append(token)

    while operators:
        postfix.append(operators.pop())
    return " ".join(postfix)


def evaulate_infix(expression):
    expression = infix_to_postfix(expression)
    return evaulate_postfix(expression)


def evaulate_postfix(expression):
    stack = list()
    tokens = _tokenize(expression)
    for token in tokens:
        if re.search(r"\d*\.?\d+", token):  # decimals or multidigit numbers
            token = float(token)
            stack.append(token)
        else:
            x = 0
            if re.search(r"sin|cos|tan|log|e|u-", token):
                y = stack.pop()
            elif re.search(r"[+\-*\^/]", token):
                y = stack.pop()
                x = stack.pop()
            result = _permform_op(token, x, y)
            stack.append(result)

    return stack[-1]

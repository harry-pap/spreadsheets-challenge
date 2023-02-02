import re

from parser.node import Node
from parser.numeric_operation import Addition, Subtraction, Multiplication, Division
from parser.raw_matcher import RawNumberMatcher
from parser.funtion import SquareFunction

class MainLoopContinue(Exception):
    pass


class ExpressionParser:
    def __init__(self, validate_parentheses, arithmetic_operators, functions, raw_matchers):
        self.validate_parentheses = validate_parentheses
        self.arithmetic_operators = arithmetic_operators
        self.functions = functions
        self.raw_matchers = raw_matchers

    def parse(self, expression):
        self.validate_parentheses(expression)

        root = None
        last_added_node = None
        scanned_subtree = None

        i = 0

        while i < len(expression):
            try:
                if expression[i] == "(":
                    if scanned_subtree is not None:
                        raise Exception("Scanned subexpression after value or expression without an operator in between")

                    closing_index = index_of_closing_parentheses(expression[i + 1:])
                    subexpression = expression[i + 1: i + 1 + closing_index]
                    scanned_subtree = self.parse(subexpression)
                    i += closing_index + 2
                    raise MainLoopContinue

                for function in self.functions:
                    if not expression[i:].startswith(function.symbol):
                        continue

                    function_end_index = i + len(function.symbol) + 1
                    closing_parentheses_index = index_of_closing_parentheses(expression[function_end_index:])
                    subexpression = expression[function_end_index: function_end_index + closing_parentheses_index]

                    subtree = self.parse(subexpression)

                    scanned_subtree = Node(
                        function,
                        subtree,
                        None
                    )
                    i = function_end_index + closing_parentheses_index + 1
                    raise MainLoopContinue

                for matcher in self.raw_matchers:
                    match = re.match(matcher.regex, expression[i:])
                    if match is not None:
                        if scanned_subtree is not None:
                            raise Exception("Scanned consecutive values without an operator")

                        scanned_subtree = Node(
                            matcher.value(expression[i:i+(match.end())]),
                            None,
                            None
                        )
                        i += match.end()
                        raise MainLoopContinue

                for operator in self.arithmetic_operators:
                    if operator.symbol != expression[i]:
                        continue

                    if scanned_subtree is None:
                        raise Exception("Operator scanned without an operand first")

                    if last_added_node is None:
                        last_added_node = Node(
                            operator,
                            scanned_subtree,
                            None
                        )
                        root = last_added_node
                    elif operator.weight > last_added_node.value.weight:
                        new_node = Node(
                            operator,
                            scanned_subtree,
                            None
                        )
                        last_added_node.right = new_node
                        last_added_node = new_node
                    elif operator.weight > root.value.weight:
                        last_added_node.right = scanned_subtree
                        last_added_node = Node(
                            operator,
                            last_added_node,
                            None
                        )
                        root.right = last_added_node
                    else:
                        last_added_node.right = scanned_subtree
                        root = Node(operator, root, None)
                        last_added_node = root

                    i += 1
                    scanned_subtree = None
                    raise MainLoopContinue
            except MainLoopContinue:
                pass

        if root is None:
            return scanned_subtree

        last_added_node.right = scanned_subtree
        return root


def default_expression_parser():
    return ExpressionParser(
        validate_parentheses_in_expression,
        [
            Addition(),
            Subtraction(),
            Multiplication(),
            Division(),
        ],
        [
            SquareFunction(),
        ],
        [
            RawNumberMatcher(),
        ]
    )


def index_of_closing_parentheses(expression):
    level = 1
    i = 0

    for current in expression:
        if current == '(':
            level += 1
        elif current == ')':
            level -= 1

        if level == 0:
            return i
        i += 1


def validate_parentheses_in_expression(expression):
    counter = 0

    for i in expression:
        if i == '(':
            counter += 1
        elif i == ')':
            counter -= 1

        if counter < 0:
            raise Exception("Illegal syntax, ')' found without a matching '('")

    if counter != 0:
        raise Exception("Illegal syntax, '(' found without a matching ')'")



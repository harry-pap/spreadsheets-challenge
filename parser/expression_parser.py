import re

from parser.node import Node
from parser.numeric_operation import Addition, Subtraction, Multiplication, Division
from parser.raw_matcher import RawNumberMatcher


class MainLoopContinue(Exception):
    pass


class ExpressionParser:
    def __init__(self, arithmetic_operators, raw_matchers):
        self.arithmetic_operators = arithmetic_operators
        self.raw_matchers = raw_matchers

    def parse(self, expression):
        root = None
        last_added_node = None
        scanned_subtree = None

        i = 0

        while i < len(expression):
            try:
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

        last_added_node.right = scanned_subtree
        return root


def default_expression_parser():
    return ExpressionParser(
        [
            Addition(),
            Subtraction(),
            Multiplication(),
            Division(),
        ],
        [
            RawNumberMatcher()
        ]
    )

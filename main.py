from parser.node import Node
from parser.expression_parser import ExpressionParser
from parser.numeric_operation import Addition, Subtraction, Multiplication, Division
from parser.raw_matcher import RawNumberMatcher
import parser.numeric_operation as num


def main():
    expression = "10+20*300+4000"

    parser = ExpressionParser(
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

    result = parser.parse(expression)
    print("Tree:\n{}".format(result))
    print("Result:{}".format(result.visit()))


def create_operetion_node():
    the_node = Node(
        num.Multiplication(),
        Node(num.Addition(),
             Node(1, None, None),
             Node(2, None, None)
             ),
        Node(3, None, None)
    )

    print("Foobar:\n{}".format(the_node))
    result = the_node.visit()
    print("Result: {}".format(result))


def print_sample_tree():
    the_node = Node(
        "abc",
        Node("cde",
             Node("def", None, None),
             Node("ghi", None, Node("klm", None, None))),
        None
    )
    print("Foobar:\n{}".format(the_node))


if __name__ == '__main__':
    main()

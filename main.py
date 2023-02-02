import parser.numeric_operation as num
from parser.expression_parser import default_expression_parser
from parser.node import Node


def main():
    expression = "sqr(sqr(2))+1*3"

    parser = default_expression_parser()

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

import parser.numeric_operation as num
import re
from parser.csvparser import CSVParser
from parser.node import Node
from parser.expression_parser import default_expression_parser
from parser.cell_processor import CellProcessor
from parser.value_referrence import SpecificCellMatcher
from parser.cell import Cell
from parser.cell_processor import CellStorage

def main():
    parser = CSVParser(CellProcessor(default_expression_parser()))
    parser.parse_file("/tmp/parser/test.csv", "/tmp/parser/output.csv")


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
    result = the_node.visit(Cell.from_string("A1"), CellStorage())
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
    expression = "A12+35"
    matcher = SpecificCellMatcher()
    result = re.match(matcher.regex, expression)
    cell_identifier = expression[0:0+(result.end())]

    print(result)

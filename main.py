import sys

from parser.cell_processor import CellProcessor
from parser.csvparser import CSVParser
from parser.expression_parser import default_expression_parser


def main():
    parser = CSVParser(CellProcessor(default_expression_parser()))
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    parser.parse_file(input_path, output_path)


if __name__ == '__main__':
    main()

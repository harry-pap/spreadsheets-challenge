import sys
import csv

from parser.cell import Cell
from parser.expression_parser import default_expression_parser
from parser.cell_processor import CellProcessor


class CSVParser:
    def __init__(self, cell_processor: CellProcessor):
        self.cell_processor = cell_processor

    def parse_file(self, path_to_input, path_to_output):
        with open(path_to_input, 'r') as fin:
            reader = csv.reader(fin, delimiter='|')

            with open(path_to_output, 'w') as fout:
                writer = csv.writer(fout, delimiter='|')
                self.__parse(reader, writer)

    def __parse(self, reader, writter):
        row_counter = 1
        column_size = 0

        for line in reader:
            row = []
            if column_size == 0:
                column_size = len(line)
            if column_size != len(line):
                print("Line {} has different size {} than expected {}".format(row_counter, len(line), column_size), file=sys.stderr)

            column_counter = 0
            for item in line:
                column_counter += 1
                if item == "":
                    row.append(None)
                    continue
                cell = Cell(column_counter, row_counter)
                try:
                    result = self.cell_processor.process(cell, item)
                    row.append(result)
                except Exception as e:
                    print("Failed to process cell {}, error: {}".format(cell, e.__str__()), file=sys.stderr)
                    row.append("###ERROR###")
            writter.writerow(row)
            row_counter += 1


if __name__ == '__main__':
    parser = CSVParser(CellProcessor(default_expression_parser()))
    parser.parse_file("/tmp/parser/test.csv", "/tmp/parser/output.csv")
    print("Done!")

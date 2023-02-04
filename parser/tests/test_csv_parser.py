import unittest

from parser.cell_processor import CellProcessor
from parser.csvparser import CSVParser
from parser.expression_parser import default_expression_parser
from pathlib import Path


class CSVParserTest(unittest.TestCase):
    input_file = "/tmp/csv_parser_test.csv"
    output_file = "/tmp/csv_parser_test_output.csv"

    def test_csv_parser_with_explicit_cell_references(self):
        parser_input = """!date|!transaction_id|!tokens|!token_prices|!total_cost
2022-02-20|=concat("t_", "foobar")|btc,eth,dai||=sum(spread(split("38341.88,2643.77,1.0003", ",")))
2022-02-21|=concat("t_", "boink")|btc,eth,dai||=10+sum(spread(split("304.38,2621.15,1.0001", ",")))
2022-02-22|=concat("t_", "boom")|btc,eth,dai|=30|=D4+E3"""
        expected_parser_output = """date|transaction_id|tokens|token_prices|total_cost
2022-02-20|t_foobar|btc,eth,dai||40986.6503
2022-02-21|t_boink|btc,eth,dai||2936.5301
2022-02-22|t_boom|btc,eth,dai|30|2966.5301
"""

        self.__verify_parser_output(parser_input, expected_parser_output)

    def test_csv_parser_with_relative_cell_references(self):
        parser_input = """!date|!transaction_id|data_1|data_2
2022-02-20|=concat("t_", "acb")|=315|=3*5
2022-02-21|=concat("t_", "def")|=C^v*D^|foobar"""
        expected_parser_output = """date|transaction_id|data_1|data_2
2022-02-20|t_acb|315|15
2022-02-21|t_def|4725|foobar
"""

        self.__verify_parser_output(parser_input, expected_parser_output)

    def test_csv_parser_with_more_relative_cell_references(self):
        parser_input = """!date|!transaction_id|data_1|data_2
2022-02-20|=concat("t_", "acb")|=315|=3*5
2022-02-21|=concat("t_", "def")|=C^v*D^|foobar
2022-02-22|||
2022-02-23||=C^v+1000
"""
        expected_parser_output = """date|transaction_id|data_1|data_2
2022-02-20|t_acb|315|15
2022-02-21|t_def|4725|foobar
2022-02-22|||
2022-02-23||5725
"""

        self.__verify_parser_output(parser_input, expected_parser_output)

    def __verify_parser_output(self, parser_input, expected_parser_output):
        with open(self.input_file, "w") as fout:
            fout.write(parser_input)
        parser = CSVParser(CellProcessor(default_expression_parser()))
        parser.parse_file(self.input_file, self.output_file)
        actual_output = Path(self.output_file).read_text()

        self.assertEqual(expected_parser_output, actual_output)


if __name__ == '__main__':
    unittest.main()

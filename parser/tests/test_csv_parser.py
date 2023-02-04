import unittest

from parser.cell_processor import CellProcessor
from parser.csvparser import CSVParser
from parser.expression_parser import default_expression_parser
from pathlib import Path


class CSVParserTest(unittest.TestCase):
    def test_csv_parser(self):
        parser_input = """!date|!transaction_id|!tokens|!token_prices|!total_cost
2022-02-20|=concat("t_", "foobar")|btc,eth,dai||=sum(spread(split("38341.88,2643.77,1.0003", ",")))
2022-02-21|=concat("t_", "boink")|bch,eth,dai||=10+sum(spread(split("304.38,2621.15,1.0001", ",")))"""
        expected_parser_output = """date|transaction_id|tokens|token_prices|total_cost
2022-02-20|t_foobar|btc,eth,dai||40986.6503
2022-02-21|t_boink|bch,eth,dai||2936.5301
"""

        input_file = "/tmp/csv_parser_test.csv"
        output_file = "/tmp/csv_parser_test_output.csv"
        with open(input_file, "w") as fout:
            fout.write(parser_input)

        parser = CSVParser(CellProcessor(default_expression_parser()))
        parser.parse_file(input_file, output_file)

        actual_output = Path(output_file).read_text()

        self.assertEqual(expected_parser_output, actual_output)


if __name__ == '__main__':
    unittest.main()

import unittest

from parser.cell import Cell
from parser.cell_processor import CellProcessor
from parser.expression_parser import default_expression_parser


class CellProcessorTest(unittest.TestCase):
    processor = CellProcessor(default_expression_parser())

    def test_processor_handles_function_as_expected(self):
        result = self.processor.process(Cell.from_string("A1"), "=1+3+3")

        self.assertEqual(7, result)

    def test_processor_handles_labels_as_expected(self):
        result = self.processor.process(Cell.from_string("A1"), "!foobar")

        self.assertEqual("foobar", result)

    def test_processor_handles_raw_values_as_expected(self):
        result = self.processor.process(Cell.from_string("A1"), "1234")

        self.assertEqual("1234", result)

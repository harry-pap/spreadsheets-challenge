import unittest

from parser.cell import Cell


class CellTest(unittest.TestCase):
    def test_from_string_returns_expected_cell(self):
        cell = Cell.from_string("C13")
        self.assertEqual(3, cell.column)
        self.assertEqual(13, cell.row)

    def test_fails_if_column_is_invalid(self):
        with self.assertRaises(Exception) as context:
            Cell.from_string("113")

        self.assertEqual("Column should be an uppercase letter between {A...Z}", str(context.exception))

    def test_fails_if_row_is_invalid(self):
        with self.assertRaises(Exception) as context:
            Cell.from_string("AB")

        self.assertEqual("Row should be an integer", str(context.exception))

    def test_eq_and_hash_work_as_expected(self):
        cells = {
            Cell.from_string("A3"): 10,
            Cell.from_string("Z22"): 22,
        }

        self.assertEqual(10, cells[Cell.from_string("A3")])
        self.assertEqual(22, cells[Cell.from_string("Z22")])

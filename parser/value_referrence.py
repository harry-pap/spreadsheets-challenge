from parser.cell import Cell
import re
from parser.cell_processor import CellStorage
from parser.node import Node


class CellMatcher:
    pass


class SpecificCellMatcher(CellMatcher):
    regex = "^[A-Z][0-9]+"

    def match(self, expression: str, current_cell: Cell, cell_storage: CellStorage):
        result = re.match(self.regex, expression)
        cell_identifier = expression[:(result.end())]
        cell = Cell.from_string(cell_identifier)

        node = cell_storage.cells[cell]

        return node.visit() if isinstance(node, Node) else node


class LastComputedInColumnMatcher(CellMatcher):
    regex = "^[A-Z]\^v"

    def match(self, expression: str, current_self: Cell, cell_storage: CellStorage):
        column_name = expression[0]
        column_id = Cell.int_identifier_from_column_name(column_name)

        node = cell_storage.last_added[column_id]

        return node.visit() if isinstance(node, Node) else node


class LastCellInColumnMatcher(CellMatcher):
    regex = "^[A-Z]\^"

    def match(self, expression: str, current_cell: Cell, cell_storage: CellStorage):
        column_name = expression[0]

        target_cell = Cell.from_string("{}{}".format(column_name, current_cell.row - 1))
        node = cell_storage.cells[target_cell]

        return node.visit() if isinstance(node, Node) else node

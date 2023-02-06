import re
import copy
from parser.cell import Cell
from parser.cell_processor import CellStorage
from parser.node import Node
from parser.cell_referrence import LastComputedCellInColumnReferencingNode, LastCellInColumnReferencingNode


class CellMatcher:
    pass


class SpecificCellMatcher(CellMatcher):
    regex = "^[A-Z][0-9]+"

    def match(self, expression: str, current_cell: Cell, cell_storage: CellStorage):
        result = re.match(self.regex, expression)
        cell_identifier = expression[:(result.end())]

        cell = cell_storage.cells[Cell.from_string(cell_identifier)]

        return cell if isinstance(cell, Node) else Node(
            cell,
            None,
            None
        )


class LastComputedInColumnMatcher(CellMatcher):
    regex = "^[A-Z]\^v"

    def match(self, expression: str, current_self: Cell, cell_storage: CellStorage):
        column_name = expression[0]
        column_id = Cell.int_identifier_from_column_name(column_name)

        return Node(
            LastComputedCellInColumnReferencingNode(column_id),
            None,
            None
        )


class LastCellInColumnMatcher(CellMatcher):
    regex = "^[A-Z]\^"

    def match(self, expression: str, current_cell: Cell, cell_storage: CellStorage):
        column_name = expression[0]

        return Node(
            LastCellInColumnReferencingNode(column_name),
            None,
            None
        )


class NamedCellMatcher(CellMatcher):
    regex = "^@[a-z_]+<[0-9]+>"

    def match(self, expression: str, current_cell: Cell, cell_storage: CellStorage):
        match = re.match(self.regex, expression)
        matching_expression = expression[:match.end()]

        label = matching_expression[:match.end()].split("@")[1].split("<")[0]
        identifier = int(matching_expression[:match.end()].split("<")[1].split(">")[0])

        initial_labeled_cell = cell_storage.named_cells[label]

        cell = cell_storage.cells[Cell(initial_labeled_cell.column, initial_labeled_cell.row + identifier)]

        return cell if isinstance(cell, Node) else Node(
            cell,
            None,
            None
        )


class SpecialCopyMatcher(CellMatcher):
    regex = "^\^\^"

    def match(self, expression: str, current_cell: Cell, cell_storage: CellStorage):
        target_cell = Cell(current_cell.column, current_cell.row - 1)
        node = cell_storage.cells[target_cell]

        new_node = copy.deepcopy(node)

        new_node.apply_special_copy()

        return new_node

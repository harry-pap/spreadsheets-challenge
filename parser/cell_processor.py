from parser.cell import Cell


class CellProcessor:
    def __init__(self, expression_parser):
        self.expression_parser = expression_parser
        self.cell_storage = CellStorage()

    def process(self, cell, expression):
        if expression.startswith("!"):
            name = expression[1:]
            self.cell_storage.cells[cell] = name
            self.cell_storage.named_cells[name] = cell
            return name
        elif expression.startswith("="):
            node = self.expression_parser.parse(expression[1:], cell, self.cell_storage)
            self.cell_storage.cells[cell] = node
            return node.visit(cell, self.cell_storage)
        else:
            self.cell_storage.cells[cell] = expression
            return expression


class CellStorage:
    def __init__(self):
        self.named_cells = {}
        self.cells = {}

    def last_added_before(self, cell: Cell):
        if cell.row < 2:
            raise Exception("Invalid row id provided")

        above_cell = Cell(cell.column, cell.row - 1)
        if above_cell in self.cells:
            return above_cell

        return self.last_added_before(above_cell)

class CellProcessor:
    def __init__(self, expression_parser):
        self.expression_parser = expression_parser
        self.cell_storage = CellStorage()

    def process(self, cell, expression):
        if expression.startswith("!"):
            name = expression[1:]
            self.cell_storage.cells[cell] = name
            self.cell_storage.named_cells[name] = cell
            self.cell_storage.last_added[cell.column] = name
            return name
        elif expression.startswith("="):
            node = self.expression_parser.parse(expression[1:], cell, self.cell_storage)
            self.cell_storage.cells[cell] = node
            result = node.visit()
            self.cell_storage.last_added[cell.column] = result
            return result
        else:
            self.cell_storage.cells[cell] = expression
            self.cell_storage.last_added[cell.column] = expression
            return expression


class CellStorage:
    def __init__(self):
        self.named_cells = {}
        self.last_added = {}
        self.cells = {}

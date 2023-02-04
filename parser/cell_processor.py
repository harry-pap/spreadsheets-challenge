class CellProcessor:
    def __init__(self, expression_parser):
        self.expression_parser = expression_parser
        self.named_cells = {}
        self.last_added = {}
        self.cells = {}

    def process(self, cell, expression):
        if expression.startswith("!"):
            name = expression[1:]
            self.cells[cell] = name
            self.named_cells[name] = cell
            self.last_added[cell.column] = name
            return name
        elif expression.startswith("="):
            node = self.expression_parser.parse(expression[1:])
            self.cells[cell] = node
            result = node.visit()
            self.last_added[cell.column] = result
            return result
        else:
            self.cells[cell] = expression
            self.last_added[cell.column] = expression
            return expression

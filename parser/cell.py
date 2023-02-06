class Cell:
    CHAR_BEFORE_A_CAPITAL = '@'
    INDEX_OF_A_CAPITAL = 65

    def __str__(self):
        return "{}{}".format(chr(ord(Cell.CHAR_BEFORE_A_CAPITAL) + self.column), self.row)

    def __repr__(self):
        return self.__str__()

    def __init__(self, column, row):
        if not isinstance(column, int) or column < 1 or column > 26:
            raise Exception("Invalid column identifier, should be a number between: {1,...,26}")
        if not isinstance(row, int) or row < 0:
            raise Exception("Invalid row identifier, should be an int greater than zero")

        self.column = column
        self.row = row

    def __eq__(self, another):
        return isinstance(another, Cell) and (self.column == another.column and self.row == another.row)

    def __hash__(self):
        return hash((self.column, self.row))

    @staticmethod
    def from_string(string):
        if not string[0].isalpha() or not string[0].isupper():
            raise Exception("Column should be an uppercase letter between {A...Z}")
        try:
            int(string[1:])
        except Exception as e:
            raise Exception("Row should be an integer")

        column = ord(string[0]) - Cell.INDEX_OF_A_CAPITAL + 1
        row = int(string[1:])

        return Cell(column, row)

    @staticmethod
    def int_identifier_from_column_name(string):
        if not string[0].isalpha() or not string[0].isupper():
            raise Exception("Column should be an uppercase letter between {A...Z}")

        return ord(string[0]) - Cell.INDEX_OF_A_CAPITAL + 1


if __name__ == '__main__':
    cell = Cell.from_string("C33")
    print(cell)

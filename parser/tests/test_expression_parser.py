import unittest
from parameterized import parameterized

from parser.expression_parser import default_expression_parser
from parser.expression_parser import validate_parentheses_in_expression
from parser.cell_processor import CellStorage
from parser.cell import Cell
from decimal import Decimal


class ExpressionParserTest(unittest.TestCase):
    @parameterized.expand([
        ["1*3", Decimal(3)],
        ["1+3", Decimal(4)],
        ["1+3*5", Decimal(16)],
        ["1-10+50-22-15+159-2100", Decimal(-1937)],
        ["1*3-15+7*12-129*31", Decimal(-3927)],
        ["15+251-256*3-5125+3*1052+17", Decimal(-2454)],
        ["1*15+30+3/15*12/3+1351", Decimal('1396.8')],
        ["2+50/12*128/150/12*24*40+256-360*222+2154*126/22/10*20*50*2*3*5", Decimal('36930258.80808080808080808079')],
        ["1+2*(1+5)-4", Decimal(9)],
        ["(1+2)*(1+5)-4*(1+9)-3", Decimal(-25)],
        ["(1+2*(1+3))*(1+5)-4*(1*(3+4-5))-3", Decimal(43)],
        ["(1+2)*(3+4*5*(6-4))-(9/3)", Decimal(126)],
        ["sqr(sqr(2))", Decimal(16)],
        ["sqr(sqr(sqr(2)))", Decimal(256)],
        ["sqr(sqr(2))+1*3", Decimal(19)],
        ["sqr(sqr(sqr(2)))+1*3", Decimal(259)],
        ["1+(sqr(sqr(2)))*(1+5)-4", Decimal(93)],
        ["uppercase(\"abc\")", "ABC"],
        ["uppercase(text(sqr(2)))", "4"],
        ["sum(1,2,3,4)", Decimal(10)],
        ["sum(1,2,sqr(sqr(2)),4)", Decimal(23)],
        ["sum(sum(1,sqr(2),3),2,sqr(sqr(2)),4)", Decimal(30)],
        ["bte(12,10)", True],
        ["bte(sqr(2),4)", True],
        ["bte(sqr(2),4.2)", False],
        ["concat(\"abc\",\"def\",text(123),uppercase(\"bar\"))", "abcdef123BAR"],
        ["3+sum(spread(split(\"123,456\",\",\")))", Decimal(582)],
        ["text(bte(12,10))", "True"],
    ])
    def test_standalone_expressions(self, expression, expected):
        parser = default_expression_parser()
        node = parser.parse(expression, Cell.from_string("A1"), CellStorage())
        actual = node.visit()
        self.assertEqual(expected, actual)

    def test_expressions_with_static_cross_references(self):
        expression = "30+A3*C5"
        cellstorage = CellStorage()
        cellstorage.cells[Cell.from_string("A3")] = Decimal(100)
        cellstorage.cells[Cell.from_string("C5")] = Decimal(300)
        parser = default_expression_parser()

        node = parser.parse(expression, Cell.from_string("A1"), cellstorage)

        actual = node.visit()
        expected = Decimal(30030)

        self.assertEqual(expected, actual)

    def test_expressions_with_relative_cross_references(self):
        expression = "15+B^*C^v"
        cellstorage = CellStorage()
        cellstorage.last_added[Cell.int_identifier_from_column_name("C")] = Decimal(1000)
        cellstorage.cells[Cell.from_string("B1")] = Decimal(3)
        parser = default_expression_parser()

        node = parser.parse(expression, Cell.from_string("B2"), cellstorage)

        actual = node.visit()
        expected = Decimal(3015)

        self.assertEqual(expected, actual)

    def test_expressions_with_label_reference(self):
        expression = "15+@foobar<2>*3"
        cellstorage = CellStorage()
        cellstorage.named_cells["foobar"] = Cell.from_string("B3")
        cellstorage.cells[Cell.from_string("B5")] = Decimal(75)
        parser = default_expression_parser()

        node = parser.parse(expression, Cell.from_string("F2"), cellstorage)

        actual = node.visit()
        expected = Decimal(240)

        self.assertEqual(expected, actual)

    @parameterized.expand([
        ["*3", 'Operator scanned without an operand first'],
        ["2(3)", "Scanned subexpression after value or expression without an operator in between"],
        ["\"abc\"+3", "Left operand of numeric operation is not a number but str"],
        ["3+\"abc\"", "Right operand of numeric operation is not a number but str"],
        ["sqr(\"abc\")", "SquareFunction requires number as input, instead got 'abc'"],
        ["sum(\"abc\")", "SumFunction requires list of numbers as input, instead got 'abc'"],
        ["sum(1,\"abc\")", "SumFunction requires list of numbers as input, instead got '[Decimal('1'), 'abc']'"],
        ["bte(2)", "BTE function requires 2 arguments to be provided as list, instead got '2'"],
        ["bte(1,2,3)", "BTE function requires exactly 2 arguments to be provided as list,"
                       " instead got '[Decimal('1'), Decimal('2'), Decimal('3')]'"],
        ["bte(1,\"abc\")", "BTE function requires numbers as arguments, instead got '[Decimal('1'), 'abc']'"],
        ["uppercase(32)", "uppercase requires text as input, instead got '32'"],
        ["split(35)", "split function requires list of text as input, instead got '35'"],
        ["split(\"foobar\", 22)", "split function requires text as arguments"],
        ["split(\"foo\", \"bar\",\",\")", "split function requires exactly 2 arguments of text type to be provided in a"
                                          " list, instead got '['foo', 'bar', ',']'"],
        ["spread(22)", "spread function requires list of text as input, instead got '22'"],
        ["concat(\"abc\")", "cancat function requires list of text as input, instead got 'abc'"],
        ["concat(\"abc\", 22)", "concat function requires sequence of text as argument,"
                                " instead got '['abc', Decimal('22')]'"],
    ])
    def test_raises_exception_for_invalid_input(self, expression, expected):
        parser = default_expression_parser()
        with self.assertRaises(Exception) as context:
            parser.parse(expression, Cell.from_string("A1"), CellStorage()).visit()

        self.assertEqual(expected, str(context.exception), "expression:{}".format(expression))


class ValidateParenthesesTest(unittest.TestCase):
    ILLEGAL_CLOSING = "Illegal syntax, ')' found without a matching '('"
    ILLEGAL_OPENING = "Illegal syntax, '(' found without a matching ')'"

    @parameterized.expand([
        ["(a", ILLEGAL_OPENING],
        ["(a+(b+c)", ILLEGAL_OPENING],
        ["(a+b+(c+d)))", ILLEGAL_CLOSING],
        ["(a+b))+(c+d)", ILLEGAL_CLOSING],
    ])
    def test_validate_parentheses_should_raise_for_invalid_input(self, expression, expected):
        with self.assertRaises(Exception) as context:
            validate_parentheses_in_expression(expression)

        self.assertEqual(expected, str(context.exception), "expression:{}".format(expression))

    @parameterized.expand([
        ["(a+b)"],
        ["(a)+(b+c)"],
        ["(a+b)+(c+d+(e+f))"],
    ])
    def test_validate_parentheses_should_not_raise_for_valid_input(self, expression):
        try:
            validate_parentheses_in_expression(expression)
        except Exception as e:
            self.fail("Exception not expected but raised for expression:{}, exception".format(expression, e))


if __name__ == '__main__':
    unittest.main()

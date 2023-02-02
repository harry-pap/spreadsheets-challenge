import unittest
from parameterized import parameterized

from parser.expression_parser import default_expression_parser
from parser.expression_parser import validate_parentheses_in_expression
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
    ])
    def test_numeric_operations(self, expression, expected):
        parser = default_expression_parser()
        actual = parser.parse(expression).visit()
        self.assertEqual(expected, actual)

    @parameterized.expand([
        ["*3", 'Operator scanned without an operand first'],
        ["2(3)", "Scanned subexpression after value or expression without an operator in between"],
        ["\"abc\"+3", "Left operand of numeric operation is not a number but str"],
        ["3+\"abc\"", "Right operand of numeric operation is not a number but str"],
    ])
    def test_raises_exception_for_invalid_input(self, expression, expected):
        parser = default_expression_parser()
        with self.assertRaises(Exception) as context:
            parser.parse(expression).visit()

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

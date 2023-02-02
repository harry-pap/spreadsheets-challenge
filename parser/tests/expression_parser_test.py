import unittest
from parameterized import parameterized
from parser.expression_parser import default_expression_parser


class ExpressionParserTest(unittest.TestCase):
    @parameterized.expand([
        ["1*3", 3],
        ["1+3", 4],
        ["1+3*5", 16],
        ["1-10+50-22-15+159-2100", -1937],
        ["1*3-15+7*12-129*31", -3927],
        ["15+251-256*3-5125+3*1052+17", -2454],
        ["1*15+30+3/15*12/3+1351", 1396.8],
        ["2+50/12*128/150/12*24*40+256-360*222+2154*126/22/10*20*50*2*3*5", 36930258.80808081]
    ])
    def test_numeric_operations(self, expression, expected):
        parser = default_expression_parser()
        self.assertEqual(expected, parser.parse(expression).visit())


    @parameterized.expand([
        ["*3", 'Operator scanned without an operand first'],
    ])
    def test_raises_exception_for_invalid_input(self, expression, expected):
        parser = default_expression_parser()
        with self.assertRaises(Exception) as context:
            parser.parse(expression)

        self.assertEqual(expected, str(context.exception))


if __name__ == '__main__':
    unittest.main()

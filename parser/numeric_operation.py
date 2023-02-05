from decimal import Decimal


class Operation:
    # TODO implement implicit casts from string to decimal when needed
    def verify(self, left, right):
        if not isinstance(left, Decimal):
            if isinstance(left, str):
                try:
                    left = Decimal(left)
                except Exception:
                    raise Exception("Left operand of numeric operation is not a number but {}"
                                    .format(type(left).__name__))
            else:
                raise Exception("Left operand of numeric operation is not a number but {}"
                                .format(type(left).__name__))

        if not isinstance(right, Decimal):
            if isinstance(right, str):
                try:
                    right = Decimal(right)
                except Exception:
                    raise Exception("Right operand of numeric operation is not a number but {}"
                                    .format(type(right).__name__))
            else:
                raise Exception("Right operand of numeric operation is not a number but {}"
                                .format(type(right).__name__))
        return left, right


class Addition(Operation):
    def __str__(self):
        return "Addition"

    def __call__(self, left, right):
        (left, right) = self.verify(left, right)
        return left + right

    symbol = "+"

    weight = 1


class Subtraction(Operation):
    def __str__(self):
        return "Subtraction"

    def __call__(self, left, right):
        (left, right) = self.verify(left, right)
        return left - right

    symbol = "-"

    weight = 1


class Multiplication(Operation):
    def __str__(self):
        return "Multiplication"

    def __call__(self, left, right):
        (left, right) = self.verify(left, right)
        return left * right

    symbol = "*"

    weight = 2


class Division(Operation):
    def __str__(self):
        return "Division"

    def __call__(self, left, right):
        (left, right) = self.verify(left, right)
        return left / right

    symbol = "/"

    weight = 2

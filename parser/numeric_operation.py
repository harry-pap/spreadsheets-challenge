class Operation:
    pass


class Addition(Operation):
    def __str__(self):
        return "Addition"

    def __call__(self, left, right):
        return left + right

    symbol = "+"

    weight = 1


class Subtraction(Operation):
    def __str__(self):
        return "Subtraction"

    def __call__(self, left, right):
        return left - right

    symbol = "-"

    weight = 1


class Multiplication(Operation):
    def __str__(self):
        return "Multiplication"

    def __call__(self, left, right):
        return left * right

    symbol = "*"

    weight = 2


class Division(Operation):
    def __str__(self):
        return "Division"

    def __call__(self, left, right):
        return left / right

    symbol = "/"

    weight = 2

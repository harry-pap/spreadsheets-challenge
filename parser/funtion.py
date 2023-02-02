from decimal import Decimal


class Function:
    pass


class SquareFunction(Function):
    def __str__(self):
        return "Square"

    def __call__(self, value):
        if not isinstance(value, Decimal):
            raise ("SquareFunction requires number as input, instead got '{}'".format(value))

        return value * value

    symbol = "sqr"


class UppercaseFunction(Function):
    def __str__(self):
        return "Uppercase"

    def __call__(self, value):
        if not isinstance(value, str):
            raise ("uppercase text as input, instead got '{}'".format(value))

        return value.upper()

    symbol = "uppercase"


class TextFunction(Function):
    def __str__(self):
        return "Text"

    def __call__(self, value):
        if isinstance(value, Decimal):
            return str(remove_exponent(value))

        return str(value)

    symbol = "text"


def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


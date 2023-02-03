from decimal import Decimal


class Function:
    pass


class SquareFunction(Function):
    def __str__(self):
        return "Square"

    def __call__(self, arg):
        if not isinstance(arg, Decimal):
            raise "SquareFunction requires number as input, instead got '{}'".format(arg)

        return arg * arg

    symbol = "sqr"


class SumFunction(Function):
    def __str__(self):
        return "Sum"

    def __call__(self, arg):
        if not isinstance(arg, list):
            raise "SumFunction requires list of numbers as input, instead got '{}'".format(arg)

        for item in arg:
            if not isinstance(item, Decimal):
                raise "SumFunction requires list of numbers as input, instead got '{}' as part of the argument list".format(arg)

        return sum(arg)

    symbol = "sum"


class BiggerThanOrEqualToFunction(Function):
    def __str__(self):
        return "BTE"

    def __call__(self, arg):
        if not isinstance(arg, list):
            raise "BTE function requires 2 arguments to be provided as list, instead got '{}'".format(arg)

        if len(arg) != 2:
            raise "BTE function requires exactly 2 arguments to be provided as list, instead got '{}'".format(arg)

        for item in arg:
            if not isinstance(item, Decimal):
                raise "BTE function requires numbers as arguments".format(arg)

        return arg[0] >= arg[1]

    symbol = "bte"


class UppercaseFunction(Function):
    def __str__(self):
        return "Uppercase"

    def __call__(self, arg):
        if not isinstance(arg, str):
            raise "uppercase requires text as input, instead got '{}'".format(arg)

        return arg.upper()

    symbol = "uppercase"


class SplitFunction(Function):
    def __str__(self):
        return "Split"

    def __call__(self, arg):
        if not isinstance(arg, list):
            raise "split function requires list of text as input, instead got '{}'".format(arg)

        if len(arg) != 2:
            raise "split function requires exactly 2 arguments of text type to be provided in a list, instead got '{}'".format(arg)

        for item in arg:
            if not isinstance(item, str):
                raise "split function requires text as arguments".format(arg)

        return [Decimal(it) for it in arg[0].split(arg[1])]

    symbol = "split"


class SpreadFunction(Function):
    """
    Added so that the example in transaction.csv would be valid, the approach was to use list for variable length
    types everywhere.
    """
    def __str__(self):
        return "Spread"

    def __call__(self, arg):
        if not isinstance(arg, list):
            raise "spread requires list of text as input, instead got '{}'".format(arg)

        return arg

    symbol = "spread"


class ConcatFunction(Function):
    def __str__(self):
        return "Concat"

    def __call__(self, arg):
        if not isinstance(arg, list):
            raise "cancat requires list of text as input, instead got '{}'".format(arg)

        for item in arg:
            if not isinstance(item, str):
                raise "Concat function requires sequence of text as argument".format(arg)

        return "".join(arg)

    symbol = "concat"


class TextFunction(Function):
    def __str__(self):
        return "Text"

    def __call__(self, arg):
        if isinstance(arg, Decimal):
            return str(remove_exponent(arg))

        return str(arg)

    symbol = "text"


def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

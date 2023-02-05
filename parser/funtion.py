from decimal import Decimal


class Function:
    pass


class SquareFunction(Function):
    def __str__(self):
        return "Square"

    def __call__(self, arg):
        if not isinstance(arg, Decimal):
            raise Exception("SquareFunction requires number as input, instead got '{}'".format(arg))

        return arg * arg

    symbol = "sqr"


class SumFunction(Function):
    def __str__(self):
        return "Sum"

    def __call__(self, arg):
        if not isinstance(arg, list):
            raise Exception("SumFunction requires list of numbers as input, instead got '{}'".format(arg))

        for item in arg:
            if not isinstance(item, Decimal):
                raise Exception("SumFunction requires list of numbers as input, instead got '{}'".format(arg))

        return sum(arg)

    symbol = "sum"


class BiggerThanOrEqualToFunction(Function):
    def __str__(self):
        return "BTE"

    def __call__(self, arg):
        if not isinstance(arg, list):
            raise Exception("BTE function requires 2 arguments to be provided as list, instead got '{}'".format(arg))

        if len(arg) != 2:
            raise Exception("BTE function requires exactly 2 arguments to be provided as list, instead got '{}'"
                            .format(arg))

        for index, item in enumerate(arg):
            if not isinstance(item, Decimal):
                if isinstance(item, str):
                    try:
                        arg[index] = Decimal(item)
                    except Exception:
                        raise Exception("BTE function requires numbers as arguments, instead got '{}'".format(arg))
                else:
                    raise Exception("BTE function requires numbers as arguments, instead got '{}'".format(arg))

        return arg[0] >= arg[1]

    symbol = "bte"


class UppercaseFunction(Function):
    def __str__(self):
        return "Uppercase"

    def __call__(self, arg):
        if not isinstance(arg, str):
            raise Exception("uppercase requires text as input, instead got '{}'".format(arg))

        return arg.upper()

    symbol = "uppercase"


class SplitFunction(Function):
    def __str__(self):
        return "Split"

    def __call__(self, arg):
        if not isinstance(arg, list):
            raise Exception("split function requires list of text as input, instead got '{}'".format(arg))

        if len(arg) != 2:
            raise Exception("split function requires exactly 2 arguments of text type to be provided in a list,"
                            " instead got '{}'".format(arg))

        for item in arg:
            if not isinstance(item, str):
                raise Exception("split function requires text as arguments".format(arg))

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
            raise Exception("spread function requires list of text as input, instead got '{}'".format(arg))

        return arg

    symbol = "spread"


class ConcatFunction(Function):
    def __str__(self):
        return "Concat"

    def __call__(self, arg):
        if not isinstance(arg, list):
            raise Exception("cancat function requires list of text as input, instead got '{}'".format(arg))

        for item in arg:
            if not isinstance(item, str):
                raise Exception("concat function requires sequence of text as argument, instead got '{}'".format(arg))

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


class IncrementFromFunction(Function):
    def __str__(self):
        return "IncrementFrom"

    def __call__(self, arg):
        if not isinstance(arg, Decimal):
            raise Exception("Argument to incFrom function should be a number")

        return arg

    symbol = "incFrom"


def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

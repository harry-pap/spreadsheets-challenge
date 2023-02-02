class Function:
    pass


class SquareFunction(Function):
    def __str__(self):
        return "Square"

    def __call__(self, value):
        if not isinstance(value, float):
            raise ("SquareFunction requires number as input, instead got '{}'".format(value))

        return value * value

    symbol = "sqr"


from parser.numeric_operation import Operation
from parser.funtion import Function
from decimal import Decimal


class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self, level=0):
        ret = "    " * level + "└──" + str(self.value) + "\n"
        for child in filter(None, [self.left, self.right]):
            ret += child.__str__(level + 1)
        return ret

    def visit(self, sum=Decimal(0)):
        from_left = None if self.left is None else self.left.visit(sum)
        from_right = None if self.right is None else self.right.visit(sum)

        if isinstance(self.value, Operation):
            return self.value(from_left, from_right)
        elif isinstance(self.value, Function):
            return self.value(from_left)
        else:
            return self.value

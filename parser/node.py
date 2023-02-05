from parser.numeric_operation import Operation
from parser.funtion import Function
from parser.funtion import IncrementFromFunction
from decimal import Decimal


class Link:
    pass


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
        elif isinstance(self.value, Link):
            list_from_left = self.__list_from_link(from_left)
            list_from_right = self.__list_from_link(from_right)

            return list(filter(None, list_from_left + list_from_right))
        else:
            return self.value

    def apply_special_copy(self):
        if isinstance(self.value, IncrementFromFunction):
            if not isinstance(self.left.value, Decimal):
                raise Exception("incFrom should have a static number as seed")
            self.left.value = self.left.value + 1
        if self.left is not None:
            self.left.apply_special_copy()
        if self.right is not None:
            self.right.apply_special_copy()

    @staticmethod
    def __list_from_link(result_from_subtree):
        if result_from_subtree is None:
            list_from_left = []
        elif isinstance(result_from_subtree, list):
            list_from_left = result_from_subtree
        else:
            list_from_left = [result_from_subtree]

        return list_from_left

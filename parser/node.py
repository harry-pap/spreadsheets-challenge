from decimal import Decimal
from io import StringIO

from parser.cell import Cell
from parser.cell_processor import CellStorage
from parser.cell_referrence import CellReferencingNode
from parser.funtion import Function
from parser.funtion import IncrementFromFunction
from parser.numeric_operation import Operation


class Link:
    pass


class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        with StringIO() as buffer:
            self.__print_tree(buffer, "", "")
            return buffer.getvalue()

    def __print_tree(self, buffer, prefix, children_prefix):
        buffer.write(prefix)
        buffer.write(str(self.value))
        buffer.write('\n')

        existing_children = list(filter(None, [self.left, self.right]))
        for index, value in enumerate(existing_children):
            if len(existing_children) > index + 1:
                value.__print_tree(buffer, "{}├── ".format(children_prefix), "{}│   ".format(children_prefix))
            else:
                value.__print_tree(buffer, "{}└── ".format(children_prefix), "{}    ".format(children_prefix))

    def visit(self, current_cell: Cell, cell_storage: CellStorage, sum=Decimal(0)):
        from_left = None if self.left is None else self.left.visit(current_cell, cell_storage, sum)
        from_right = None if self.right is None else self.right.visit(current_cell, cell_storage, sum)

        if isinstance(self.value, Operation):
            return self.value(from_left, from_right)
        elif isinstance(self.value, Function):
            return self.value(from_left)
        elif isinstance(self.value, CellReferencingNode):
            return self.value.instantiate(current_cell, cell_storage)
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

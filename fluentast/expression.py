from ast import expr, stmt, FunctionDef, AsyncFunctionDef, Lambda
from .utils import get_all_parents_types


def get_all_parents_function(self):
    return get_all_parents_types(self, (FunctionDef, AsyncFunctionDef, Lambda))


def contains(self, node):
    for e in get_all_parents_types(node, expr):
        if e is self:
            return True
    return False

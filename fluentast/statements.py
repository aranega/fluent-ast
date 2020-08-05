from ast import expr, stmt, FunctionDef, AsyncFunctionDef, Lambda
from .utils import get_all_parents_types


def get_all_parents_function(self):
    yield from get_all_parents_types(self, (FunctionDef, AsyncFunctionDef, Lambda))


def contains(self, node):
    return next(get_all_parents_types(node, stmt), None) is self

from ast import expr, stmt, FunctionDef, AsyncFunctionDef, Lambda, iter_child_nodes, Name
from .utils import get_all_parents_types


def all_parents_function(self):
    yield from get_all_parents_types(self, (FunctionDef, AsyncFunctionDef, Lambda))


def contains(self, node):
    return next(get_all_parents_types(node, stmt), None) is self


def all_variable_use(self):
    for child in iter_child_nodes(self):
        if isinstance(child, Name):
            yield child
        elif isinstance(child, expr):
            yield from child.all_variable_use()

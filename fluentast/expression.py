from ast import expr, stmt, FunctionDef, AsyncFunctionDef, Lambda, Module, ClassDef, Assign
from .utils import get_all_parents_types


def all_parents_function(self):
    yield from get_all_parents_types(self, (FunctionDef, AsyncFunctionDef, Lambda))


def contains(self, node):
    for e in get_all_parents_types(node, expr):
        if e is self:
            return True
    return False


def get_scopes(self):
    yield from get_all_parents_types(
        self, (FunctionDef, AsyncFunctionDef, Module, ClassDef)
    )


def is_in_assign(self):
    return isinstance(next(get_all_parents_types(self, Assign), None), Assign)


def get_top_statement(self):
    return next(get_all_parents_types(self, stmt), None)

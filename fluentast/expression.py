from ast import (
    expr,
    stmt,
    FunctionDef,
    AsyncFunctionDef,
    Lambda,
    Module,
    ClassDef,
    Assign,
    iter_child_nodes,
    Name
)
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


def top_statement(self):
    return next(get_all_parents_types(self, stmt), None)


def all_variable_use(self):
    for child in iter_child_nodes(self):
        if isinstance(child, Name):
            yield child
        elif isinstance(child, expr):
            yield from child.all_variable_use()

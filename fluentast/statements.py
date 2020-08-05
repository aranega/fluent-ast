from ast import (
    expr,
    stmt,
    FunctionDef,
    AsyncFunctionDef,
    Lambda,
    iter_child_nodes,
    Name,
)
from .utils import get_all_parents_types


def all_parents_function(self):
    """
    Yields all functions in which this statement is contained.
    The functions are yield from the closest one to the farest one.
    """
    yield from get_all_parents_types(self, (FunctionDef, AsyncFunctionDef, Lambda))


def contains(self, node):
    """
    Checks if a node is contained by this statement.
    """
    return next(get_all_parents_types(node, stmt), None) is self


def all_variable_use(self):
    """
    Yields a generator with all the variables used in this statement.
    The order of the yield variable is each direct variable, then variables from inner expressions.
    """
    for child in iter_child_nodes(self):
        if isinstance(child, Name):
            yield child
        elif isinstance(child, expr):
            yield from child.all_variable_use()

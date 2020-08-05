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
    Name,
)
from .utils import get_all_parents_types


def all_parents_function(self):
    """
    Yields all functions in which this expression is contained.
    The functions are yield from the closest one to the farest one.
    """
    yield from get_all_parents_types(self, (FunctionDef, AsyncFunctionDef, Lambda))


def contains(self, node):
    """
    Checks if a node is contained in the expression (a sub-element)
    """
    for e in get_all_parents_types(node, expr):
        if e is self:
            return True
    return False


def get_scopes(self):
    """
    Yields all scopes in which this expression will look up values for variables.
    The scopes are yield from the most close scope (e.g: containing function) to the least close scope (Module).
    """
    yield from get_all_parents_types(
        self, (FunctionDef, AsyncFunctionDef, Module, ClassDef)
    )


def is_in_assign(self):
    """
    Checks if the expression is part of an assignement
    """
    return isinstance(next(get_all_parents_types(self, Assign), None), Assign)


def top_statement(self):
    """
    Gets the top statement in which this expression appears, None otherwise.
    """
    return next(get_all_parents_types(self, stmt), None)


def all_variable_use(self):
    """
    Yields a generator with all the variables used in this expression.
    The order of the variable is given by the order of evaluation of the AST.
    """
    for child in iter_child_nodes(self):
        if isinstance(child, Name):
            yield child
        elif isinstance(child, expr):
            yield from child.all_variable_use()

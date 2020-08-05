from ast import Name, walk, Return
from .utils import get_all_parents_types


def all_variable_use(self):
    """
    Yields all the variables used in the function.
    The order of variables is given by "all_variable_use" in statements.
    Each statement is took regarding "execution order".
    """
    for statement in self.body:
        yield from statement.all_variable_use()


def unconditional_returns(self):
    """
    Yields all the unconditionnal returns of this function.
    """
    for statement in self.body:
        if isinstance(statement, Return):
            yield statement


def unconditional_return(self):
    """
    Returns the first unconditionnal return of this function.
    """
    return next(self.unconditional_returns(), None)

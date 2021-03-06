from ast import Name, iter_child_nodes, arg, Assign
from .utils import get_all_parents_types


def bound_parameter(self):
    """
    Returns the tuple (function, arg) to which this variable is bound.
    If the variable is not bound to any parameter, (None, None) is returned.
    """
    name = self.id
    for fun in self.all_parents_function():
        for a in (a for a in iter_child_nodes(fun.args) if isinstance(a, arg)):
            if name == a.arg:
                return (fun, a)
    return (None, None)


def first_assignment(self):
    """
    Returns the first assignment of this variable in the current bloc.
    """
    fun, e = self.bound_parameter()
    if e:
        return None  # FIXME

    top_stmt = self.top_statement()
    for statement in top_stmt.parent.body:
        if isinstance(statement, Assign) and self.id in tuple(t.id for t in statement.targets):
            return statement
        elif statement is top_stmt:
            break
    return None


def next_assign(self):
    """
    Returns the next assignemnt of this variable in the current bloc.
    """
    top_stmt = self.top_statement()
    i = top_stmt.parent.body.index(top_stmt)
    for s in top_stmt.parent.body[i + 1:]:
        if isinstance(s, Assign) and self.id in tuple(t.id for t in s.targets):
            return s
    return None

from ast import (
    expr,
    stmt,
    FunctionDef,
    AsyncFunctionDef,
    Lambda,
    iter_child_nodes,
    Name,
    Expr,
)
from .utils import get_all_parents_types, replace_node, BadPosition, BadASTNode, assign


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


def insert(self, statement, position="before", auto_assign=True, auto_assign_name=None):
    """
    Inserts a statement in a position relative to this statement.
    Possible positions are "before", "after", "instead".
    This methods returns the inserted statement.
    If the statement is actually an expression, the node is automatically wrapped to an Expr node.
    In this case, if the "auto_assign" option is passed (default: True), it inserts an assignement with an auto generated name.
    The assignement name can be controlled with the "auto_assign_name" parameter
    """
    if isinstance(statement, expr):
        if auto_assign:
            name = auto_assign_name if auto_assign_name else f"@{id(statement)}"
            statement = assign(name, statement)
        else:
            statement = Expr(value=statement)
    elif not isinstance(statement, stmt):
        raise BadASTNode(stmt, type(statement))
    container = self.parent.body
    i = container.index(self)
    if position == "before":
        container.insert(i, statement)
        statement.parent = self.parent
    elif position == "after":
        container.insert(i + 1, statement)
        statement.parent = self.parent
    elif position == "instead":
        replace_node(self, statement)
    else:
        raise BadPosition()
    return statement

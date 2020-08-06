from ast import (
    iter_fields,
    iter_child_nodes,
    walk,
    stmt,
    expr,
    Expr,
    Name,
    Assign,
    Store,
    Constant,
    Load,
)


def replace_node(old, new):
    """
    Replaces a node by another.
    If the new node is an expression while the old one is a statement, this function
    wraps the expression in an Expr node.
    """
    if isinstance(old, stmt) and isinstance(new, expr):
        new = Expr(value=new)
    for field, values in iter_fields(old.parent):
        try:
            values[values.index(old)] = new
            break
        except Exception:
            if old is values:
                setattr(old.parent, field, new)
                break
    new.parent = old.parent
    old.parent = None
    return new


def set_parents(root):
    """
    Sets the "parent" relationship to each node of an AST.
    """
    root.parent = None
    for node in walk(root):
        for child in iter_child_nodes(node):
            child.parent = node


def get_all_parents_types(variable, types):
    """
    Yields all the parent elements that are from dedicated types.
    """
    current = variable
    while current != None:
        if isinstance(current, types):
            yield current
        current = current.parent


class BadPosition(Exception):
    ...


class BadASTNode(TypeError):
    def __init__(self, expected, actual, *args, **kwargs):
        self.expected = expected
        self.actual = actual
        msg = f"Bad AST node insertion, waiting for {expected.__name__} node, but get {actual.__name__} node instead"
        super().__init__(msg, *args, **kwargs)


def assign(name, expr):
    # if name is None or name == "":
    #     name = f"@{type(expr).__name__}_{id(expr)}"
    return Assign(targets=[Name(id=name, ctx=Store())], value=expr)


def var_ref(name):
    return Name(id=name, ctx=Load())


def extract_all_subexpr(statement):
    for field, value in iter_fields(statement):
        if field in ("targets",):
            continue
        if isinstance(value, expr):
            extract_all_subexpr_expr(value)


def extract_all_subexpr_expr(expression, single_element_granularity=False):
    if not single_element_granularity and isinstance(expression, (Name, Constant)):
        return
    for subexpr in iter_child_nodes(expression):
        if isinstance(subexpr, expr):
            extract_all_subexpr_expr(subexpr)
    expression.extract(auto_insert=True)

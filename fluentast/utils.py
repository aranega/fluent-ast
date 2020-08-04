from ast import iter_fields, iter_child_nodes, walk, stmt, expr, Expr


def replace_node(old, new):
    if isinstance(old, stmt) and isinstance(new, expr):
        new = Expr(value=new)
    for field, values in iter_fields(old.parent):
        try:
            values[values.index(old)] = new
        except Exception:
            if old is values:
                setattr(old.parent, field, new)
    new.parent = old.parent
    old.parent = None
    return new


def set_parents(root):
    root.parent = None
    for node in walk(root):
        for child in iter_child_nodes(node):
            child.parent = node


def get_all_parents_types(variable, types):
    current = variable
    while current != None:
        if isinstance(current, types):
            yield current
        current = current.parent

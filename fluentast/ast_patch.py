from ast import stmt, expr, mod, AST, iter_child_nodes


def init_patch_parent(self, *args, **kwargs):
    AST.__init__(self, *args, **kwargs)
    for node in iter_child_nodes(self):
        node.parent = self
    self.parent = None


stmt.__init__ = init_patch_parent
expr.__init__ = init_patch_parent
mod.__init__ = init_patch_parent


from . import statements

stmt.all_parents_function = statements.all_parents_function
stmt.__contains__ = statements.contains


from . import expression

expr.all_parents_function = expression.all_parents_function
expr.__contains__ = expression.contains
expr.get_scopes = expression.get_scopes
expr.is_in_assign = expression.is_in_assign
expr.top_statement = expression.top_statement

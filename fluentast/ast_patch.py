from ast import stmt, expr, mod, AST, iter_child_nodes, FunctionDef, Name


"""
This patched version automatically set the "parent" relationship.
"""


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
stmt.all_variable_use = statements.all_variable_use
stmt.insert = statements.insert


from . import expression

expr.all_parents_function = expression.all_parents_function
expr.__contains__ = expression.contains
expr.get_scopes = expression.get_scopes
expr.is_in_assign = expression.is_in_assign
expr.top_statement = expression.top_statement
expr.all_variable_use = expression.all_variable_use
expr.extract = expression.extract


from . import functions

FunctionDef.all_variable_use = functions.all_variable_use


from . import name

Name.bound_parameter = name.bound_parameter

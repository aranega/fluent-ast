from fluentast import utils
import ast


def test__all_functions():
    funcs = """
def f1():
    def f2():
        def f3():
            ...

def f4():
    return 1
    """
    module = ast.parse(funcs)
    ellipsis = module.body[0].body[0].body[0].body[0]
    utils.set_parents(module)
    assert isinstance(ellipsis, ast.Expr)
    assert isinstance(ellipsis.value, ast.Ellipsis)
    all_funcs = tuple(f.name for f in ellipsis.all_parents_function())
    assert ("f3", "f2", "f1") == all_funcs
    assert "f4" not in all_funcs


def test__contains_expr():
    stmt = ast.Assign(value=ast.Constant(value=123))
    other = ast.Constant(value=123)
    assert stmt.value in stmt
    assert other not in stmt

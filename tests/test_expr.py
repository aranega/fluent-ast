from fluentast import utils
import ast


def test__get_all_functions():
    funcs = """
def f1():
    def f2():
        def f3():
            class A():
                def f4():
                    ...

def f5():
    return 1
    """
    module = ast.parse(funcs)
    ellipsis = module.body[0].body[0].body[0].body[0].body[0].body[0].value
    utils.set_parents(module)
    assert isinstance(ellipsis, ast.Ellipsis)
    all_funcs = tuple(f.name for f in ellipsis.get_all_parents_function())
    assert ("f4", "f3", "f2", "f1") == all_funcs
    assert "f5" not in all_funcs


def test__contains_expr():
    n = ast.BinOp(left=ast.Constant(), right=ast.Constant())
    other = ast.Constant()
    assert n.left in n
    assert n.right in n
    assert other not in n

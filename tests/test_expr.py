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
    all_funcs = tuple(f.name for f in ellipsis.all_parents_function())
    assert ("f4", "f3", "f2", "f1") == all_funcs
    assert "f5" not in all_funcs


def test__contains_expr():
    n = ast.BinOp(left=ast.Constant(), right=ast.Constant())
    other = ast.Constant()
    assert n.left in n
    assert n.right in n
    assert other not in n


def test__get_scopes():
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
    scopes = tuple(getattr(f, "name", "module") for f in ellipsis.get_scopes())
    assert ("f4", "A", "f3", "f2", "f1", "module") == scopes
    assert "f5" not in scopes


def test__is_in_assign():
    exprs = """
a = 1 + 2 + 3
3 + 4 + 5
b = 5 if True else 0
    """
    module = ast.parse(exprs)
    utils.set_parents(module)
    expr1 = module.body[0].value.left.left
    expr2 = module.body[1].value.left.left
    expr3 = module.body[2].value.test
    assert expr1.is_in_assign() is True
    assert expr2.is_in_assign() is False
    assert expr3.is_in_assign() is True


def test__top_statement():
    exprs = """
a = 1 + 2 + 3
3 + 4 + 5
b = 5 if True else 0
    """
    module = ast.parse(exprs)
    utils.set_parents(module)
    expr1 = module.body[0].value.left.left
    expr2 = module.body[1].value.left.left
    expr3 = module.body[2].value.test
    assert expr1.top_statement() is module.body[0]
    assert expr2.top_statement() is module.body[1]
    assert expr3.top_statement() is module.body[2]


def test__all_variable_use():
    exprs = """
a + b + 5 + c if a in d else f
"""
    module = ast.parse(exprs)
    utils.set_parents(module)
    expr = module.body[0].value
    variables = list(expr.all_variable_use())
    assert len(variables) == 6
    assert variables[0].id == "a"
    assert variables[1].id == "d"
    assert variables[2].id == "a"
    assert variables[3].id == "b"
    assert variables[4].id == "c"
    assert variables[5].id == "f"


def test__extract_controlled_name():
    func = """
def foo():
    return 1 + 2 + 1
assert foo() == 4
    """
    module = ast.parse(func)
    utils.set_parents(module)
    ret = module.body[0].body[0]
    ret_plus = module.body[0].body[0].value.left

    assignement, var = ret_plus.extract(assign_name="a")
    assert assignement.parent is None
    assert ret_plus.parent is assignement
    assert var.parent is ret.value

    ret.insert(assignement, position="before")

    ast.fix_missing_locations(module)
    obj = compile(module, filename="<ast>", mode="exec")
    eval(obj)


def test__extract_uncontrolled_name():
    func = """
def foo():
    return 1 + 2 + 1
assert foo() == 4
    """
    module = ast.parse(func)
    utils.set_parents(module)
    ret = module.body[0].body[0]
    ret_plus = module.body[0].body[0].value.left

    assignement, var = ret_plus.extract()
    assert assignement.parent is None
    assert ret_plus.parent is assignement
    assert var.parent is ret.value

    ret.insert(assignement, position="before")

    ast.fix_missing_locations(module)
    obj = compile(module, filename="<ast>", mode="exec")
    eval(obj)


def test__extract_autoinsert():
    func = """
def foo():
    return 1 + 2 + 1
assert foo() == 4
    """
    module = ast.parse(func)
    utils.set_parents(module)
    ret = module.body[0].body[0]
    ret_plus = module.body[0].body[0].value.left

    assignement, var = ret_plus.extract(auto_insert=True)
    assert assignement.parent is ret.parent
    assert ret_plus.parent is assignement
    assert var.parent is ret.value

    ast.fix_missing_locations(module)
    obj = compile(module, filename="<ast>", mode="exec")
    eval(obj)

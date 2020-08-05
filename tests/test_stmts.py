import pytest
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


def test__insert_before():
    func = """
def foo():
    return a
assert foo() == 4
    """
    module = ast.parse(func)
    utils.set_parents(module)
    ret = module.body[0].body[0]

    stmt = ast.parse("a = 4").body[0]
    result = ret.insert(stmt)
    assert stmt.parent is module.body[0]
    assert result is stmt
    assert result is module.body[0].body[0]

    ast.fix_missing_locations(module)
    obj = compile(module, filename="<ast>", mode="exec")
    eval(obj)


def test__insert_after():
    func = """
def foo():
    a = 1
    return a
assert foo() == 4
    """
    module = ast.parse(func)
    utils.set_parents(module)
    assign = module.body[0].body[0]

    stmt = ast.parse("a = 4").body[0]
    result = assign.insert(stmt, position="after")
    assert stmt.parent is module.body[0]
    assert result is stmt
    assert assign is module.body[0].body[0]
    assert result is module.body[0].body[1]

    ast.fix_missing_locations(module)
    obj = compile(module, filename="<ast>", mode="exec")
    eval(obj)


def test__insert_instead():
    func = """
def foo():
    a = 1
    return a
assert foo() == 4
    """
    module = ast.parse(func)
    utils.set_parents(module)
    assign = module.body[0].body[0]

    stmt = ast.parse("a = 4").body[0]
    result = assign.insert(stmt, position="instead")
    assert stmt.parent is module.body[0]
    assert result is stmt
    assert assign not in module.body[0]
    assert assign.parent is None
    assert result is module.body[0].body[0]

    ast.fix_missing_locations(module)
    obj = compile(module, filename="<ast>", mode="exec")
    eval(obj)


def test__insert_badposition():
    func = """
def foo():
    ...
    """
    module = ast.parse(func)
    utils.set_parents(module)
    ellipsis = module.body[0].body[0]

    stmt = ast.parse("a = 4").body[0]
    with pytest.raises(utils.BadPosition):
        result = ellipsis.insert(stmt, position="unknown")


def test__insert_badtype():
    func = """
def foo():
    ...
    """
    module = ast.parse(func)
    utils.set_parents(module)
    ellipsis = module.body[0].body[0]

    stmt = ast.parse("a = 4")
    with pytest.raises(utils.BadASTNode) as exception_info:
        result = ellipsis.insert(stmt, position="unknown")
    exception = exception_info.value
    assert exception.expected is ast.stmt
    assert exception.actual is ast.Module


def test__insert_expression_controledname():
    func = """
def foo():
    return a
assert foo() == 4
    """
    module = ast.parse(func)
    utils.set_parents(module)
    ret = module.body[0].body[0]

    expr = ast.parse("1 + 3").body[0].value
    result = ret.insert(expr, assign_name="a")
    assert isinstance(result, ast.Assign)
    assert result is module.body[0].body[0]
    assert result.value is expr
    assert expr.parent is result

    ast.fix_missing_locations(module)
    obj = compile(module, filename="<ast>", mode="exec")
    eval(obj)


def test__insert_expression_autogenname():
    func = """
def foo():
    return 3
    """
    module = ast.parse(func)
    utils.set_parents(module)
    ret = module.body[0].body[0]

    expr = ast.parse("1 + 3").body[0].value
    result = ret.insert(expr)
    assert isinstance(result, ast.Assign)
    assert result is module.body[0].body[0]
    assert result.value is expr
    assert expr.parent is result
    assert len(result.targets) == 1
    assert result.targets[0].id == f"@{id(expr)}"


def test__insert_expression_autoassign_off():
    func = """
def foo():
    return 3
    """
    module = ast.parse(func)
    utils.set_parents(module)
    ret = module.body[0].body[0]

    expr = ast.parse("1 + 3").body[0].value
    result = ret.insert(expr, auto_assign=False)
    assert isinstance(result, ast.Expr)
    assert result is module.body[0].body[0]
    assert result.value is expr
    assert expr.parent is result

from fluentast import utils
import ast


def test__all_variable_use():
    func = """
def foo():
    a = 4
    b = 5
    c = 6
    a = 7
    """
    module = ast.parse(func)
    utils.set_parents(module)
    foo = module.body[0]
    variables = list(foo.all_variable_use())
    assert "a" == variables[0].id
    assert "b" == variables[1].id
    assert "c" == variables[2].id
    assert "a" == variables[3].id
    assert len(variables) == 4


def test__unconditional_returns_return():
    func = """
def foo():
    if True:
        return 1
    else:
        return 2
    return 3
    return 4
    """
    module = ast.parse(func)
    utils.set_parents(module)
    foo = module.body[0]
    returns = list(foo.unconditional_returns())
    assert len(returns) == 2
    assert returns[0].value.value == 3
    assert returns[1].value.value == 4

    assert foo.unconditional_return().value.value == 3

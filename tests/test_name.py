from fluentast import utils
import ast


def test__bound_parameter():
    func = """
def foo(a):
    b = a + 5
    c = 4
    """
    module = ast.parse(func)
    utils.set_parents(module)
    foo = module.body[0]
    variables = list(foo.all_variable_use())
    assert variables[0].bound_parameter() == (None, None)
    arg_a = foo.args.args[0]
    assert variables[1].bound_parameter() == (foo, arg_a)
    assert variables[2].bound_parameter() == (None, None)


def test__bound_parameter_2():
    func = """
def foo(a, b=4, *args, **kwargs):
    b = a + 5
    c = 4
    args
    kwargs
    """
    module = ast.parse(func)
    utils.set_parents(module)
    foo = module.body[0]
    variables = list(foo.all_variable_use())
    arg_a = foo.args.args[0]
    arg_b = foo.args.args[1]
    args = foo.args.vararg
    kwargs = foo.args.kwarg
    assert variables[0].bound_parameter() == (foo, arg_b)
    assert variables[1].bound_parameter() == (foo, arg_a)
    assert variables[2].bound_parameter() == (None, None)
    assert variables[3].bound_parameter() == (foo, args)
    assert variables[4].bound_parameter() == (foo, kwargs)


def test__bound_parameter_3():
    func = """
a = 5
    """
    module = ast.parse(func)
    utils.set_parents(module)
    assert module.body[0].targets[0].bound_parameter() == (None, None)

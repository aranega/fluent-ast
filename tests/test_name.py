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


def test__first_assign():
    func = """
b = 4
a = 5
a = a + b
c
    """
    module = ast.parse(func)
    utils.set_parents(module)

    var_ref = module.body[-2].value.left
    assert var_ref.first_assignment() is module.body[1]

    var_ref = module.body[-2].value.right
    assert var_ref.first_assignment() is module.body[0]

    var_ref = module.body[-1].value
    assert var_ref.first_assignment() is None


def test__next_assign():
    func = """
a = 5
b = 4
a = a + b
    """
    module = ast.parse(func)
    utils.set_parents(module)

    var_ref = module.body[0].targets[0]
    assert var_ref.next_assign() is module.body[-1]

    var_ref = module.body[1].targets[0]
    assert var_ref.next_assign() is None

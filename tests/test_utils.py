import fluentast
from fluentast import utils
import ast
import inspect


def test__replace_expr_by_expr():
    node = ast.BinOp(left=ast.Constant(value=5), right=ast.Constant(value=3))
    new = ast.Constant(value="abc")
    old = node.left
    utils.replace_node(old, new)
    assert old.parent is None
    assert new.parent is node
    assert node.left is new


def test__replace_stmt_by_expr():
    node = ast.FunctionDef(body=[ast.Expr(value=ast.Constant(value=1))])
    old = node.body[0]
    new = ast.Constant(value=1234)
    new_node = utils.replace_node(old, new)
    assert old.parent is None
    assert isinstance(new_node, ast.Expr)
    assert node.body[0] is new_node
    assert new_node.value is new
    assert new.parent is new_node


def test__replace_stmt_by_stmt():
    node = ast.FunctionDef(body=[ast.Expr(value=ast.Constant(value=1))])
    old = node.body[0]
    new = ast.Constant(value=1234)
    new_node = utils.replace_node(old, new)
    assert old.parent is None
    assert isinstance(new_node, ast.Expr)
    assert node.body[0] is new_node
    assert new_node.value is new
    assert new.parent is new_node


def test__set_parents():
    module = ast.parse(inspect.getsource(utils))
    utils.set_parents(module)
    i = 0
    for node in ast.walk(module):
        assert hasattr(node, "parent")
        i += 1
    assert i > 2

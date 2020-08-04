import fluentast
import ast


def test__parent_stmt():
    n = ast.FunctionDef(body=[ast.Expr(value=ast.Constant(value=1))])
    assert n.body[0].parent is n
    assert n.body[0].value.parent is n.body[0]
    assert n.parent is None


def test__parent_mod():
    n = ast.FunctionDef(body=[ast.Expr(value=ast.Constant(value=1))])
    n_module = ast.Module(body=n)
    assert n.parent is n_module
    assert n_module.parent is None
    assert n.body[0].parent is n
    assert n.body[0].value.parent is n.body[0]


def test__parent_expr():
    n = ast.BinOp(left=ast.Constant(), right=ast.Constant())
    assert n.parent is None
    assert n.left.parent is n
    assert n.right.parent is n

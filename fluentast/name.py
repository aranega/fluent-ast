from ast import Name, iter_child_nodes, arg
from .utils import get_all_parents_types


def bound_parameter(self):
    name = self.id
    for fun in self.all_parents_function():
        for a in (a for a in iter_child_nodes(fun.args) if isinstance(a, arg)):
            if name == a.arg:
                return (fun, a)
    return (None, None)

from ast import Name, walk
from .utils import get_all_parents_types


def all_variable_use(self):
    for statement in self.body:
        yield from statement.all_variable_use()

from ast import Name, walk
from .utils import get_all_parents_types


def all_variable_use(self):
    for e in walk(self):
        if isinstance(e, Name):
            yield e

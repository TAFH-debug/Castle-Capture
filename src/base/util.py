from typing import Generic, TypeVar
import numpy

T = TypeVar("T")


class Sequence(Generic[T]):
    _cont: list[T]

    def __init__(self):
        self.cont = list()

    def add(self, var: T):
        self._cont.append(var)

    def pop(self, index=0):
        self._cont.pop(index)

    def foreach(self, func):
        for i in self._cont:
            func(i)

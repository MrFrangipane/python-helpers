from typing import Type, TypeVar

from pythonhelpers.singleton_metaclass import SingletonMetaclass


T = TypeVar('T')


class Injector(metaclass=SingletonMetaclass):

    def __init__(self, dependencies: dict = None):
        self._dependencies = {}
        if dependencies is not None:
            self._dependencies = dependencies

    def  set_dependencies(self, dependencies: dict):
        for abstract, implementation in dependencies.items():
            self._dependencies[abstract] = implementation

    def inject(self, abstract: Type[T]) -> T:
        if abstract not in self._dependencies:
            raise KeyError(f"Injector has no dependency registered for '{abstract.__name__}'")

        return self._dependencies[abstract]

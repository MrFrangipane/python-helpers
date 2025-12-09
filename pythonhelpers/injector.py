from typing import Type, TypeVar

from pythonhelpers.singleton_metaclass import SingletonMetaclass


T = TypeVar('T')


class Injector(metaclass=SingletonMetaclass):

    def __init__(self, dependencies: dict = None):
        self._dependencies = {}
        if dependencies is not None:
            self._dependencies = dependencies

    def set_dependencies(self, dependencies: dict):
        for abstract, implementation in dependencies.items():
            if not isinstance(implementation, abstract):
                raise TypeError(f"Expected '{implementation.__class__.__name__}' to be an instance of '{abstract.__name__}'")

            self._dependencies[abstract] = implementation

    def inject(self, abstract: Type[T]) -> T:
        if abstract not in self._dependencies:
            raise KeyError(f"Injector has no dependency registered for '{abstract.__name__}'")

        return self._dependencies[abstract]


# TODO write tests
# Works as tests and example
if __name__ == '__main__':
    from abc import ABC, abstractmethod


    class IDependency(ABC):
        @abstractmethod
        def some_method(self) -> None:
            pass

    class Dependency(IDependency):

        def some_method(self) -> None:
            print("Dependency method called")

    injector = Injector()
    injector.set_dependencies({
        IDependency: Dependency()
    })

    dependency = injector.inject(IDependency)
    dependency.some_method()

    class LooseClass:
        def some_method(self) -> None:
            print("Loose class method called")

    injector.set_dependencies({
        IDependency: LooseClass()
    })
    dependency = injector.inject(IDependency)
    dependency.some_method()

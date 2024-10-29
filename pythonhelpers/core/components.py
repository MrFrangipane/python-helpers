from dataclasses import dataclass

from pythonhelpers.core.configuration import Configuration
from pythonhelpers.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()

"""
Thread unsafe implementation of the observer pattern.

Example can be found in pyside6-helpers
"""
from dataclasses import dataclass, field
from typing import Callable

from pythonhelpers.singleton_metaclass import SingletonMetaclass


# TODO : study use case for Observer deletion


@dataclass
class LatestCall:
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)


@dataclass
class Observer:
    channel:  str
    callback: Callable


class Reactive(metaclass=SingletonMetaclass):

    def __init__(self, parent=None):
        self._observers: dict[str, list[Observer]] = dict()
        self._latest_calls: dict[str, LatestCall] = dict()

    def add_observer(self, observer: Observer):
        if observer.channel not in self._observers:
            self._observers[observer.channel] = list()

        self._observers[observer.channel].append(observer)

        latest_call = self._latest_calls.get(observer.channel, None)
        if latest_call is not None:
            observer.callback(*latest_call.args, **latest_call.kwargs)

    def remove_observer(self, observer: Observer):
        if observer.channel not in self._observers:
            return

        self._observers[observer.channel].remove(observer)
        if not self._observers[observer.channel]:
            del self._observers[observer.channel]

    def notify_observers(self, channel, *args, **kwargs):
        self._latest_calls[channel] = LatestCall(args, kwargs)

        if channel not in self._observers:
            return

        for observer in self._observers[channel]:
            observer.callback(*args, **kwargs)

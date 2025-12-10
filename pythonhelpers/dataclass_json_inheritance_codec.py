from typing import Generic, TypeVar, Any, Type

T = TypeVar("T")


class DataclassJsonInheritanceCodec(Generic[T]):

    @staticmethod
    def decode(data: dict[str, Any], cls: Type[T], **kwargs) -> T:
        result = []

        mapping = dict()
        for subclass in cls.__subclasses__():
            mapping[subclass.__name__] = subclass

        return mapping[data["__type__"]].from_dict(data)

    @staticmethod
    def encode(instance: T) -> dict[str, Any]:
        data: dict[str, Any] = instance.to_dict()
        data["__type__"] = instance.__class__.__name__

        return data

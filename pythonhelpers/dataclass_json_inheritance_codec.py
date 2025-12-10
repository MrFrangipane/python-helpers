from typing import Generic, TypeVar, Any, Type

T = TypeVar("T")


class DataclassJsonInheritanceCodec(Generic[T]):

    @staticmethod
    def _get_all_subclasses(cls: Type[T]) -> set[Type[T]]:
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in DataclassJsonInheritanceCodec._get_all_subclasses(c)]
        )

    @staticmethod
    def decode(data: dict[str, Any], cls: Type[T], **kwargs) -> T:
        mapping = dict()
        for subclass in DataclassJsonInheritanceCodec._get_all_subclasses(cls):
            mapping[subclass.__name__] = subclass

        return mapping[data["__type__"]].from_dict(data)

    @staticmethod
    def encode(instance: T) -> dict[str, Any]:
        data: dict[str, Any] = instance.to_dict()
        data["__type__"] = instance.__class__.__name__

        return data

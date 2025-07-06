from dataclasses import dataclass, fields, Field


class _DataclassAnnotateMetaclass(type):
    """
    Metaclass for validating dataclass inheritance annotations.

    Useful for DTOs that need to have the same fields as a parent domain's class

    This metaclass ensures that any dataclass inheriting from another dataclass
    properly re-annotates fields to avoid inheriting identical field annotations
    from the parent class. It validates the dataclass structure of the subclass
    and its parent, ensuring only one base class is allowed and that fields
    marking are correctly overridden in the subclass if they are present in
    the parent dataclass.
    """
    def __call__(cls, *args, **kwargs):
        try:
            fields_: dict[str, Field] = {field.name: field for field in fields(cls)}
        except TypeError:
            raise Exception(f"Class {cls} is not a dataclass") from None

        parent = cls.__bases__[0]
        try:
            parent_fields: dict[str, Field] = {field.name: field for field in fields(parent)}
        except TypeError:
            raise Exception(f"First base class {parent} is not a dataclass") from None

        for parent_field in parent_fields.values():
            if parent_field == fields_[parent_field.name]:
                raise Exception(f"Parent field {parent.__name__}.{parent_field.name} not annotated in {cls.__name__}")

        return super().__call__(*args, **kwargs)


class DataclassToFromBaseMixin:
    """
    Mixin for adding functionality to convert to and from a
    base representation.
    """
    @staticmethod
    def from_base(base):
        raise NotImplemented

    def to_base(self):
        raise NotImplemented


class DataclassAnnotateMixin(DataclassToFromBaseMixin, metaclass=_DataclassAnnotateMetaclass):
    """
    Mixin for validating dataclass inheritance annotations and adding
    functionality to convert to and from a base representation.

    Useful for DTOs that need to have the same fields as a parent domain's class

    Its metaclass ensures that any dataclass inheriting from another dataclass
    properly re-annotates fields to avoid inheriting identical field annotations
    from the parent class. It validates the dataclass structure of the subclass
    and its parent, ensuring only one base class is allowed and that fields
    marking are correctly overridden in the subclass if they are present in
    the parent dataclass.

    This class also provides static and instance methods for converting dataclass
    objects to a base representation and vice versa. The purpose is to enable
    seamless transformations of dataclasses, often involving serialization,
    deserialization, or compatibility with other formats.
    """


if __name__ == '__main__':
    @dataclass
    class TestBase:
        jean: int
        pierre: str

    @dataclass
    class TestSub(TestBase, DataclassAnnotateMixin):
        jean: int
        pierre: str
        huges: bool

    sub = TestSub(
        jean=123,
        pierre="456",
        huges=False,
    )

    print(sub)

# Python Helpers

Bits of code used in most Python based projects

## Dataclass JSON inheritance CoDec

 To ensure automatic de/serialiaztion of subclasses with dataclasses_json

Consider a `BaseSomeField` dataclass that has multiple subclasses

```python
from dataclasses import dataclass

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class BaseSomeField:
    a: int
    b: str


@dataclass_json
@dataclass
class SomeFieldSubC(BaseSomeField):
    c: float


@dataclass_json
@dataclass
class SomeFieldSubD(BaseSomeField):
    d: bool
```

Now you want to use it in a dataclass that has a field of type `list[BaseSomeField]`, where you plan to use a mix of `SomeFieldSubC` and `SomeFieldSubD` instances

```python
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config

from pythonhelpers.dataclass_json_inheritance_codec import DataclassJsonInheritanceCodec


_Codec = DataclassJsonInheritanceCodec[BaseLayerScope]


@dataclass_json
@dataclass
class Example:
    name: str
    some_field: BaseSomeField = field(metadata=config(
        decoder=lambda some_field_data: _Codec.decode(some_field_data, BaseSomeField),
        encoder=_Codec.encode
    ))
    a_list: list[BaseSomeField] = field(
        default_factory=list,
        metadata=config(
            decoder=lambda some_fields_data: [
                _Codec.decode(some_field_data, BaseSomeField) for some_field_data in some_fields_data
            ],
            encoder=lambda some_fields: [
                _Codec.encode(some_field) for some_field in some_fields
            ]
        )
    )
```

The resulting JSON has a `__type__` field that contains the fully qualified name of the sub-dataclass

````json
{
  "name": "example",
  "some_field": {
    "__type__": "SomeFieldSubC",
    "a": 1,
    "b": "abc",
    "c": 1.23
  },
  ...
}
````


### What IA says to improve


##### Overall Assessment
The concept **makes sense and is useful**, but the implementation could be more Pythonic. Here's my evaluation:

###### ✅ What Works Well
1. **Solves a real problem**: Polymorphic deserialization with `dataclasses_json` is genuinely challenging, and this addresses it
2. **Type-safe approach**: Using generics (`DataclassJsonInheritanceCodec[BaseLayerScope]`) is a good pattern
3. **Clear intent**: The `__type__` field approach is straightforward and traceable

###### ⚠️ Pythonic Concerns

**1. Boilerplate-heavy usage**
```python
# Current approach requires verbose lambda wrapping
_Codec = DataclassJsonInheritanceCodec[BaseSomeField]
metadata=config(
    decoder=lambda some_field_data: _Codec.decode(some_field_data, BaseSomeField),
    encoder=_Codec.encode
)
```

**More Pythonic alternative:**
```python
@dataclass_json
@dataclass
class Example:
    some_field: BaseSomeField = field(
        metadata=config(
            decoder=DataclassJsonInheritanceCodec.decoder_for(BaseSomeField),
            encoder=DataclassJsonInheritanceCodec.encoder_for(BaseSomeField)
        )
    )
```

**2. Parameter redundancy**
In `_Codec.decode(some_field_data, BaseSomeField)`, you're passing the base class when it's already known from the generic type. This could be implicit.

**3. List handling complexity**
The list comprehensions are verbose and error-prone. Consider:
```python
decoder=DataclassJsonInheritanceCodec.list_decoder_for(BaseSomeField)
```

###### 💡 Suggestions to Make It More Pythonic

1. **Add helper factory methods** that eliminate redundancy:
   ```python
   @classmethod
   def decoder_for(cls, base_type):
       return lambda data: cls.decode(data, base_type)
   ```

2. **Consider a decorator approach** for fields:
   ```python
   @polymorphic_field(BaseSomeField)
   some_field: BaseSomeField
   ```

3. **Auto-discovery of subclasses** to avoid manual type registration

4. **Use `__init_subclass__`** to automatically register subclasses

###### 🎯 Bottom Line
The solution is **pragmatic and useful**, but could reduce boilerplate significantly. It's already functional—any improvements would mainly be about reducing cognitive load and repetition in usage patterns.

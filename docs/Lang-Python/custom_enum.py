from types import SimpleNamespace
from enum import Enum


class MyItem(SimpleNamespace):
    def __init__(self, **kwargs):
        args = {
            "name": None,
            "id": None,
        }
        args.update(kwargs)
        super().__init__(**args)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id


class MyEnumClass(Enum):
    ONE_ENUM = MyItem(name="some_name", id=1234)
    ANOTHER_ENUM = MyItem(name="another_name", id=4321)

    def __str__(self):
        return self.value.name

    def __int__(self):
        return self.value.id


print(f"ONE_ENUM name: {MyEnumClass.ONE_ENUM}")
print(f"ANOTHER_ENUM id: {int(MyEnumClass.ANOTHER_ENUM)}")

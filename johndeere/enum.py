"""Module containig custom enumeration classes."""

from __future__ import annotations

from typing import Any
from typing import Callable

import aenum


__all__ = [
    # Class exports
    "ExtendableIntEnum",
    "ExtendableStrEnum",
]


class _ExtendableEnumMeta(aenum.EnumMeta):
    def __contains__(cls, item: Any) -> bool:
        try:
            cls(item)
        except ValueError:
            return False
        return True


@aenum.unique
class ExtendableEnum(aenum.Enum, metaclass=_ExtendableEnumMeta):
    @classmethod
    def values(cls, type_fn: Callable) -> list[Any]:
        """Returns all enum member values as one list."""
        return [type_fn(cls[name].value) for name in cls.names()]

    @classmethod
    def names(cls) -> list[str]:
        """Returns all enum member names as one list."""
        return [
            name
            for name in dir(cls)
            if not name.startswith("_") and name.isupper()
        ]

    @classmethod
    def extend(cls, other: ExtendableStrEnum):
        [aenum.extend_enum(cls, x.name, x.value) for x in other]


class ExtendableIntEnum(aenum.IntEnum, ExtendableEnum):
    """Extendable, custom, integer enumeration."""

    @classmethod
    def values(cls) -> list[int]:
        """Returns all enum member values as one list."""
        return super().values(int)


class ExtendableStrEnum(aenum.StrEnum, ExtendableEnum):
    """Extendable, custom, string enumeration."""

    @classmethod
    def values(cls) -> list[str]:
        """Returns all enum member values as one list."""
        return super().values(str)

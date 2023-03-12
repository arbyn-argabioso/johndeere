"""Module containing custom type hints."""

from __future__ import annotations

from typing import Any
from typing import Dict


__all__ = [
    # Variable exports
    "JSONLike",
]


# JSON-like responses/dictionaries
JSONLike = Dict[str, Any]

"""Module containing common objects between different mixins."""

from __future__ import annotations

from johndeere.enum import ExtendableStrEnum


class RecordStatuses(ExtendableStrEnum):
    ALL: str = "ALL"
    ACTIVE: str = "ACTIVE"
    ARCHIVED: str = "ARCHIVED"

"""Module containing the John Deere API wrapper client."""

from __future__ import annotations

import logging
import os

from yarl import URL

from johndeere.mixins.fields import FieldsMixin
from johndeere.mixins.org import OrganizationsMixin
from johndeere.mixins.private import PrivateMixin


__all__ = [
    # Class exports
    "Client",
]

DEFAULT_LOGGER = logging.getLogger("johndeere")


class Client(
    PrivateMixin,
    OrganizationsMixin,
    FieldsMixin,
):

    BASE_URL = URL("https://sandboxapi.deere.com/platform/")

    def __init__(self, *args, **kwargs):
        self._logger = kwargs.get("logger", DEFAULT_LOGGER)

        # Prioritize the use of the keyword argument token. Only use
        # the environment variable version if there are no keyword
        # argument provided.
        self._access_token = os.environ.get("JOHN_DEERE_AUTH_TOKEN")
        self._access_token = kwargs.get("access_token", self._access_token)

        if self._access_token is None:
            raise ValueError("Authentication error, access token is missing.")

        # Initialize all mixins
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"access_token={self.mask(self.access_token)!r})"
        )

    @staticmethod
    def mask(confidential_str: str) -> str:
        return ("*" * 6) + confidential_str[-4:]

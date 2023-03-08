"""Module containing class mixins for performing private requests."""

from __future__ import annotations

import requests


__all__ = [
    # Class exports
    "PrivateMixin",
]


class PrivateMixin:

    def __init__(self, *args, **kwargs):
        self.private = requests.Session()
        self.private.verify = False  # fix SSLError / HTTPSConnectionPool
        self.private.headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/vnd.deere.axiom.v3+json",
        }
